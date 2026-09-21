# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Checkout orchestration."""
from decimal import Decimal
from datetime import date

from orders.pricing import apply_discount
from orders.repo import OrderRepo
from orders.notify import send_receipt


def checkout(
    repo: OrderRepo,
    subtotal: Decimal,
    code: str | None,
    today: date,
    http,
) -> int:
    total = apply_discount(subtotal, code, today)
    order_id = repo.create(
        {"subtotal": subtotal, "total": total, "code": code}
    )
    repo.mark_paid(order_id)
    order = repo.get(order_id)
    send_receipt(order, http=http)
    return order_id
