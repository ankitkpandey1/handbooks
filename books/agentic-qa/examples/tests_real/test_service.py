# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import sqlite3
from decimal import Decimal
from datetime import date
import json
import responses
from orders.repo import OrderRepo
from orders.notify import RECEIPT_URL
from orders.service import checkout


@responses.activate
def test_checkout_end_to_end(tmp_path):
    responses.add(
        responses.POST, RECEIPT_URL, json={"ok": True}, status=200
    )

    conn = sqlite3.connect(tmp_path / "orders.db")
    repo = OrderRepo(conn)
    repo.migrate()

    import requests
    order_id = checkout(repo, Decimal("100.00"), "SAVE10",
                         date(2026, 1, 1), http=requests)

    row = repo.get(order_id)
    assert row["paid"] is True
    assert row["total"] == "90.00"

    sent_body = json.loads(responses.calls[0].request.body)
    assert sent_body["total"] == "90.00"
