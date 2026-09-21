# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
# Typical agent-written suite (composite, for illustration)
from unittest.mock import MagicMock, patch
from orders.repo import OrderRepo


def test_create_calls_insert():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.lastrowid = 1
    repo = OrderRepo(mock_conn)
    repo.create(
        {"subtotal": "10.00", "total": "9.00", "code": "SAVE10"}
    )
    args, _ = mock_conn.execute.call_args
    assert "INSERT" in args[0]


def test_migrate_calls_execute():
    mock_conn = MagicMock()
    repo = OrderRepo(mock_conn)
    repo.migrate()
    assert mock_conn.execute.called


def test_mark_paid_calls_update():
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        mock_connect.return_value = mock_conn
        import sqlite3
        conn = sqlite3.connect(":memory:")
        repo = OrderRepo(conn)
        repo.mark_paid(1)
        assert mock_conn.execute.called


def test_get_returns_something():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = (
        1, "10.00", "9.00", "SAVE10", 1,
    )
    repo = OrderRepo(mock_conn)
    result = repo.get(1)
    assert result is not None
