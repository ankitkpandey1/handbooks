# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from tier import Tier

def export(raw_tier: str) -> Tier:
    aliases = {"ent": "enterprise", "enterprise-plan": "enterprise"}
    value = Tier.normalize(raw_tier)
    return Tier(aliases.get(value, value))
