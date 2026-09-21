# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
# Typical agent-written suite (composite, for illustration)
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import date
from orders.service import checkout


@patch("orders.service.send_receipt")
@patch("orders.service.OrderRepo")
@patch("orders.service.apply_discount")
def test_checkout_returns_order_id(
    mock_discount, mock_repo_cls, mock_send
):
    mock_discount.return_value = Decimal("90.00")
    mock_repo = MagicMock()
    mock_repo.create.return_value = 42
    mock_repo.get.return_value = {"id": 42, "total": "90.00"}
    mock_repo_cls.return_value = mock_repo
    mock_send.return_value = True

    order_id = checkout(mock_repo, Decimal("100.00"), "SAVE10",
                         date(2026, 1, 1), http=MagicMock())

    assert order_id == mock_repo.create.return_value


@patch("orders.service.send_receipt")
@patch("orders.service.apply_discount")
def test_checkout_calls_mark_paid(mock_discount, mock_send):
    mock_discount.return_value = Decimal("90.00")
    mock_repo = MagicMock()
    mock_repo.create.return_value = 1
    mock_send.return_value = True

    checkout(mock_repo, Decimal("100.00"), "SAVE10", date(2026, 1, 1),
              http=MagicMock())

    assert mock_repo.mark_paid.called


@patch("orders.service.send_receipt")
@patch("orders.service.apply_discount")
def test_checkout_sends_receipt(mock_discount, mock_send):
    mock_discount.return_value = Decimal("90.00")
    mock_repo = MagicMock()
    mock_repo.create.return_value = 1

    checkout(mock_repo, Decimal("100.00"), "SAVE10", date(2026, 1, 1),
              http=MagicMock())

    assert mock_send.called


def test_checkout_mock_called_only():
    mock_http = MagicMock()
    mock_repo = MagicMock()
    mock_repo.create.return_value = 7
    with patch("orders.service.send_receipt") as mock_send, \
         patch("orders.service.apply_discount") as mock_discount:
        mock_discount.return_value = Decimal("1.00")
        checkout(mock_repo, Decimal("1.00"), "SAVE10", date(2026, 1, 1),
                  http=mock_http)
        assert mock_send.called
