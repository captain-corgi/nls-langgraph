import os
import sqlite3
from pathlib import Path


def seed() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    db_path = data_dir / "sample.db"

    if db_path.exists():
        os.remove(db_path)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            joined_at TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            status TEXT NOT NULL,
            ordered_at TEXT NOT NULL
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
        );

        -- Customers
        INSERT INTO customers VALUES (1, 'Alice Johnson', 'alice@example.com', 'New York', '2024-01-15');
        INSERT INTO customers VALUES (2, 'Bob Smith', 'bob@example.com', 'San Francisco', '2024-02-20');
        INSERT INTO customers VALUES (3, 'Charlie Brown', 'charlie@example.com', 'Chicago', '2024-03-10');
        INSERT INTO customers VALUES (4, 'Diana Prince', 'diana@example.com', 'Seattle', '2024-04-05');
        INSERT INTO customers VALUES (5, 'Eve Davis', 'eve@example.com', 'Austin', '2024-05-12');

        -- Products
        INSERT INTO products VALUES (1, 'Laptop Pro', 'Electronics', 1299.99, 50);
        INSERT INTO products VALUES (2, 'Wireless Mouse', 'Electronics', 29.99, 200);
        INSERT INTO products VALUES (3, 'Python Cookbook', 'Books', 49.99, 100);
        INSERT INTO products VALUES (4, 'Standing Desk', 'Furniture', 599.99, 30);
        INSERT INTO products VALUES (5, 'Coffee Mug', 'Kitchen', 14.99, 500);
        INSERT INTO products VALUES (6, 'Mechanical Keyboard', 'Electronics', 149.99, 75);

        -- Orders
        INSERT INTO orders VALUES (1, 1, 'completed', '2024-06-01');
        INSERT INTO orders VALUES (2, 1, 'completed', '2024-06-15');
        INSERT INTO orders VALUES (3, 2, 'shipped', '2024-07-01');
        INSERT INTO orders VALUES (4, 3, 'pending', '2024-07-10');
        INSERT INTO orders VALUES (5, 4, 'completed', '2024-07-20');
        INSERT INTO orders VALUES (6, 5, 'shipped', '2024-08-01');
        INSERT INTO orders VALUES (7, 2, 'pending', '2024-08-15');

        -- Order Items
        INSERT INTO order_items VALUES (1, 1, 1, 1, 1299.99);
        INSERT INTO order_items VALUES (2, 1, 2, 2, 29.99);
        INSERT INTO order_items VALUES (3, 2, 3, 1, 49.99);
        INSERT INTO order_items VALUES (4, 3, 4, 1, 599.99);
        INSERT INTO order_items VALUES (5, 3, 5, 3, 14.99);
        INSERT INTO order_items VALUES (6, 4, 6, 1, 149.99);
        INSERT INTO order_items VALUES (7, 5, 1, 1, 1299.99);
        INSERT INTO order_items VALUES (8, 5, 5, 2, 14.99);
        INSERT INTO order_items VALUES (9, 6, 2, 1, 29.99);
        INSERT INTO order_items VALUES (10, 7, 3, 2, 49.99);
    """)

    conn.commit()
    conn.close()
    print(f"[Seed] Database created at {db_path.resolve()}")
    print("[Seed] Tables: customers, products, orders, order_items")


if __name__ == "__main__":
    seed()
