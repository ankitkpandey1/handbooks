# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import responses
from orders.notify import send_receipt, NotifyFailed, RECEIPT_URL
import pytest


@responses.activate
def test_send_receipt_true_on_2xx():
    responses.add(
        responses.POST, RECEIPT_URL, json={"ok": True}, status=200
    )
    assert send_receipt({"id": 1, "total": "9.00"}) is True


@responses.activate
def test_send_receipt_raises_on_500():
    responses.add(responses.POST, RECEIPT_URL, json={"err": True},
                   status=500)
    with pytest.raises(NotifyFailed):
        send_receipt({"id": 1, "total": "9.00"})
