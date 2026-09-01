# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from tier import Tier
from quote import quote

def test_reported_quote_whitespace():
    assert quote(" Pro ") is Tier.PRO

def test_quote_canonical():
    assert quote("free") is Tier.FREE
