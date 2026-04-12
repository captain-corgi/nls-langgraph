# Kiến trúc hệ thống NL→SQL Chatbot

Tài liệu này mô tả kiến trúc ứng dụng **FastAPI + LangGraph** trong thư mục `nl_sql_chatbot/`, theo hướng **Clean Architecture** (interface → application → domain; infrastructure triển khai các port của domain).

---

## Tổng quan các thành phần

```mermaid
flowchart TB
    subgraph clients["Clients"]
        HTTP["HTTP clients\n(Swagger, curl, app)"]
        CLI["CLI\ninterface/cli/chat_cli.py"]
    end

    subgraph interface["Interface (delivery)"]
        API["FastAPI\ninterface/api/"]
        Routes["Routes: /chat/*\ninterface/api/routes/chat.py"]
        DI["dependencies.py\nget_db_repo, get_chat_repo, get_agent"]
    end

    subgraph application["Application (orchestration)"]
        SqlAgent["SqlAgent\nsql_agent.py"]
        Graph["LangGraph StateGraph\ngraph_builder.py"]
        Tools["SQL tools ×4\nsql_tools.py"]
        Prompts["System prompt\nsql_prompts.py"]
    end

    subgraph infrastructure["Infrastructure"]
        LLM["ChatOpenAI\ncreate_llm()"]
        DBAdp["SqlDatabaseAdapter\nSQLAlchemy + LangChain SQLDatabase"]
        Mem["InMemoryChatHistory"]
        Settings["get_settings()\n.env / pydantic-settings"]
        LS["LangSmith\nconfigure_langsmith()"]
    end

    subgraph domain["Domain (pure)"]
        Ports["SqlDatabasePort\nChatHistoryPort"]
        Entities["ChatMessage, QueryResult"]
    end

    subgraph external["External"]
        OpenAI["OpenAI API"]
        SQLite[("SQLite\nsample.db")]
    end

    HTTP --> API
    CLI --> SqlAgent
    API --> Routes
    Routes --> DI
    DI --> SqlAgent
    DI --> DBAdp

    SqlAgent --> Graph
    SqlAgent --> Mem
    Graph --> Tools
    Graph --> LLM
    Graph --> Prompts
    Tools --> DBAdp
    Tools --> LLM

    DBAdp --> Ports
    Mem --> Ports
    Mem --> Entities

    LLM --> OpenAI
    DBAdp --> SQLite
    Settings -.-> LLM
    Settings -.-> DBAdp
    LS -.-> LLM

    style domain fill:#fee2e2,stroke:#dc2626
    style application fill:#dcfce7,stroke:#16a34a
    style infrastructure fill:#fef9c3,stroke:#ca8a04
    style interface fill:#dbeafe,stroke:#2563eb
```

---

## Luồng LangGraph (agent ↔ tools)

`build_graph()` tạo đồ thị hai nút: LLM có tool gắn kèm và `ToolNode` thực thi các lệnh gọi công cụ. Vòng lặp kết thúc khi model trả lời dạng văn bản (không còn `tool_calls`).

```mermaid
flowchart LR
    START([START]) --> AGENT["agent node\nSystemMessage + history\nllm.bind_tools"]
    AGENT -->|tool_calls| TOOLS["tools node\nToolNode"]
    TOOLS --> AGENT
    AGENT -->|plain text| END([END])
```

---

## Luồng xử lý một yêu cầu chat (API)

```mermaid
sequenceDiagram
    participant C as Client
    participant R as POST /chat/
    participant A as SqlAgent
    participant H as ChatHistoryPort
    participant G as LangGraph
    participant L as LLM
    participant T as SQL tools
    participant D as SqlDatabaseAdapter

    C->>R: session_id, message
    R->>A: chat(...)
    A->>H: save_message (user)
    A->>H: get_history
    A->>G: invoke(messages, session_id)

    loop Until final answer
        G->>L: invoke with tools
        alt tool_calls
            G->>T: run tools
            T->>D: schema / query
            D-->>T: rows / metadata
            T-->>G: tool messages
        end
    end

    G-->>A: final AIMessage
    A->>H: save_message (assistant)
    A-->>R: answer
    R-->>C: ChatResponse
```

---

## Quy tắc phụ thuộc (Clean Architecture)

- **Domain**: không phụ thuộc framework; chỉ định **entities** và **ports** (interface ABC).
- **Application**: điều phối LangGraph và tools; dùng port để nói chuyện với DB và lịch sử chat.
- **Infrastructure**: triển khai port (`SqlDatabaseAdapter`, `InMemoryChatHistory`), cấu hình LLM, settings.
- **Interface**: HTTP (FastAPI) hoặc CLI; chỉ **wire** qua dependency injection tới `SqlAgent` và adapter.

Chi tiết triển khai file theo từng lớp xem `README.md` (mục directory structure) và mã nguồn trong `nl_sql_chatbot/`.
