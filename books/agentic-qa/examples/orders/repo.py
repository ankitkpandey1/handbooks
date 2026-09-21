# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Order repository backed by sqlite3."""
import sqlite3


class OrderNotFound(Exception):
    pass


class OrderRepo:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def migrate(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subtotal TEXT NOT NULL,
                total TEXT NOT NULL,
                code TEXT,
                paid INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self.conn.commit()

    def create(self, order: dict) -> int:
        cur = self.conn.execute(
            "INSERT INTO orders (subtotal, total, code, paid) "
            "VALUES (?, ?, ?, 0)",
            (
                str(order["subtotal"]),
                str(order["total"]),
                order.get("code"),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def get(self, order_id: int) -> dict | None:
        row = self.conn.execute(
            "SELECT id, subtotal, total, code, paid FROM orders "
            "WHERE id = ?",
            (order_id,),
        ).fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "subtotal": row[1],
            "total": row[2],
            "code": row[3],
            "paid": bool(row[4]),
        }

    def mark_paid(self, order_id: int) -> None:
        row = self.conn.execute(
            "SELECT paid FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        if row is None:
            raise OrderNotFound(f"no such order: {order_id}")
        if row[0]:
            return  # idempotent: already paid, no-op
        self.conn.execute(
            "UPDATE orders SET paid = 1 WHERE id = ?", (order_id,)
        )
        self.conn.commit()
