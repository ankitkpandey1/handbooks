# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Discount pricing rules for orders."""
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

SHIPPING = Decimal("5.00")
EXPIRY = date(2026, 12, 31)
CENT = Decimal("0.01")


class InvalidCode(Exception):
    pass


def _cents(amount: Decimal) -> Decimal:
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def apply_discount(
    subtotal: Decimal, code: str | None, today: date
) -> Decimal:
    if code is None:
        return _cents(subtotal)

    if code not in ("SAVE10", "FREESHIP"):
        raise InvalidCode(f"unknown code: {code!r}")

    if today > EXPIRY:
        raise InvalidCode(f"code expired: {code!r}")

    if code == "SAVE10":
        return _cents(subtotal * Decimal("0.90"))

    if code == "FREESHIP":
        result = subtotal - SHIPPING
        return _cents(result) if result > 0 else Decimal("0.00")

    raise InvalidCode(f"unknown code: {code!r}")
