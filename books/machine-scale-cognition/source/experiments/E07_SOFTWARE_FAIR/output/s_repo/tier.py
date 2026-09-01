# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
from enum import Enum

class Tier(Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

    @classmethod
    def normalize(cls, raw_tier: str) -> str:
        """Normalize the common user-facing tier representation."""
        return raw_tier.strip().casefold()

    @classmethod
    def from_raw(cls, raw_tier: str) -> "Tier":
        return cls(cls.normalize(raw_tier))
