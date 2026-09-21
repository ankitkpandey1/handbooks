# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
# Typical agent-written suite (composite, for illustration)
from decimal import Decimal
from datetime import date
from orders.pricing import apply_discount


def test_save10_happy_path():
    result = apply_discount(
        Decimal("100.00"), "SAVE10", date(2026, 1, 1)
    )
    assert result == Decimal("90.00")


def test_freeship_happy_path():
    result = apply_discount(
        Decimal("20.00"), "FREESHIP", date(2026, 1, 1)
    )
    assert result == Decimal("15.00")


def test_no_code_happy_path():
    result = apply_discount(Decimal("50.00"), None, date(2026, 1, 1))
    assert result == Decimal("50.00")
