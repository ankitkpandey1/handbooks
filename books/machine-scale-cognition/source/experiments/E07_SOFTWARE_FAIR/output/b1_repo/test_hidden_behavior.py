# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import pytest
from tier import Tier
from quote import quote
from refund import refund
from export import export
from support import support
from renewal import renewal

FLOWS = (quote, refund, export, support, renewal)

@pytest.mark.parametrize("flow", FLOWS)
@pytest.mark.parametrize("raw,want", [(" free ", Tier.FREE), ("PRO", Tier.PRO), (" Enterprise ", Tier.ENTERPRISE)])
def test_common_normalization(flow, raw, want):
    assert flow(raw) is want

@pytest.mark.parametrize("flow", FLOWS)
def test_unknown_rejected(flow):
    with pytest.raises(ValueError):
        flow("platinum")

def test_documented_enterprise_aliases():
    assert export("ent") is Tier.ENTERPRISE
    assert renewal("enterprise_plan") is Tier.ENTERPRISE
