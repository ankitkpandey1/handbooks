# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from tier import Tier

def renewal(raw_tier: str) -> Tier:
    value = Tier.normalize(raw_tier).replace("_", "-")
    if value == "enterprise-plan":
        value = "enterprise"
    return Tier(value)
