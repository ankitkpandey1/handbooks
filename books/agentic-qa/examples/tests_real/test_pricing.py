# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from decimal import Decimal
from datetime import date
import pytest
from orders.pricing import apply_discount, InvalidCode, EXPIRY


def test_save10_is_exactly_ten_percent_off():
    assert apply_discount(Decimal("100.00"), "SAVE10",
                           date(2026, 1, 1)) == Decimal("90.00")


def test_freeship_subtracts_shipping():
    assert apply_discount(Decimal("20.00"), "FREESHIP",
                           date(2026, 1, 1)) == Decimal("15.00")


def test_freeship_never_goes_negative():
    assert apply_discount(Decimal("3.00"), "FREESHIP",
                           date(2026, 1, 1)) == Decimal("0.00")


def test_code_valid_on_expiry_day():
    assert apply_discount(Decimal("10.00"), "SAVE10", EXPIRY) == \
        Decimal("9.00")


def test_code_invalid_day_after_expiry():
    day_after = date(2027, 1, 1)
    with pytest.raises(InvalidCode):
        apply_discount(Decimal("10.00"), "SAVE10", day_after)


def test_unknown_code_raises():
    with pytest.raises(InvalidCode):
        apply_discount(Decimal("10.00"), "BOGUS", date(2026, 1, 1))
