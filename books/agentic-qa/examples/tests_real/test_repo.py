# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import sqlite3
import pytest
from orders.repo import OrderRepo, OrderNotFound


def make_repo(tmp_path):
    conn = sqlite3.connect(tmp_path / "orders.db")
    repo = OrderRepo(conn)
    repo.migrate()
    return repo


def test_create_then_get_round_trip(tmp_path):
    repo = make_repo(tmp_path)
    order_id = repo.create(
        {"subtotal": "10.00", "total": "9.00", "code": "SAVE10"}
    )
    row = repo.get(order_id)
    assert row["total"] == "9.00"
    assert row["paid"] is False


def test_mark_paid_unknown_id_raises(tmp_path):
    repo = make_repo(tmp_path)
    with pytest.raises(OrderNotFound):
        repo.mark_paid(999)


def test_mark_paid_twice_is_idempotent(tmp_path):
    repo = make_repo(tmp_path)
    order_id = repo.create(
        {"subtotal": "10.00", "total": "9.00", "code": "SAVE10"}
    )
    repo.mark_paid(order_id)
    repo.mark_paid(order_id)  # must not raise
    assert repo.get(order_id)["paid"] is True
