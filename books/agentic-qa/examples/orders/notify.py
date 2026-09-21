# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Receipt notification over HTTP."""
import requests

RECEIPT_URL = "https://mail.example.com/send"


class NotifyFailed(Exception):
    pass


def send_receipt(order: dict, http=requests) -> bool:
    resp = http.post(RECEIPT_URL, json=order)
    if 200 <= resp.status_code < 300:
        return True
    raise NotifyFailed(f"receipt send failed: {resp.status_code}")
