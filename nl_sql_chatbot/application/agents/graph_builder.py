from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from application.agents.state import AgentState
from application.prompts.sql_prompts import SYSTEM_PROMPT_TEMPLATE
from infrastructure.settings import get_settings


def build_graph(
    llm: BaseChatModel, tools: list[BaseTool], table_info: str
) -> CompiledStateGraph:
    settings = get_settings()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        table_info=table_info, max_rows=settings.max_query_results
    )
    llm_with_tools = llm.bind_tools(tools)

    def agent_node(state: AgentState) -> dict:
        system_message = SystemMessage(content=system_prompt)
        messages = [system_message] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()
