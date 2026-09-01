# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from tier import Tier

def renewal(raw_tier: str) -> Tier:
    value = raw_tier.strip().lower().replace("_", "-")
    if value == "enterprise-plan":
        value = "enterprise"
    return Tier(value)
