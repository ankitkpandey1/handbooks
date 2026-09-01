# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from tier import Tier

def quote(raw_tier: str) -> Tier:
    return Tier.from_raw(raw_tier)
