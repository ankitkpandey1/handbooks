# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import math
import random
import sys

SEED = 20260831
N = 100_000
STARTS = (0.01, 0.1, 0.5, 0.9, 0.99)
DT = 0.05
STEPS = 4000
VERIFY_WORLDS = 500
rng = random.Random(SEED)

def regime(R, S, T, P):
    at_zero = S - P
    at_one = R - T
    if at_zero > 0 and at_one > 0: return "cooperation_dominates"
    if at_zero < 0 and at_one < 0: return "defection_dominates"
    if at_zero < 0 and at_one > 0: return "coordination"
    if at_zero > 0 and at_one < 0: return "coexistence"
    return "boundary"

def integrate(R, S, T, P, x):
    for _ in range(STEPS):
        delta = x * (R - T) + (1 - x) * (S - P)
        x = min(1.0, max(0.0, x + DT * x * (1 - x) * delta))
    return x

counts = {}
survival = {str(x): 0 for x in STARTS}
mismatches = 0
thresholds = []
examples = []
verify = []
for i in range(N):
    R = rng.uniform(2.5, 3.5)
    S = rng.uniform(-0.5, 1.5)
    T = rng.uniform(2.5, 4.5)
    P = rng.uniform(0.5, 1.5)
    kind = regime(R, S, T, P)
    if i < VERIFY_WORLDS:
        verify.append((R, S, T, P, kind))
    counts[kind] = counts.get(kind, 0) + 1
    denom = R - S - T + P
    xstar = (P - S) / denom if abs(denom) > 1e-12 else None
    if kind == "coordination" and xstar is not None:
        thresholds.append(xstar)
    for start in STARTS:
        if kind == "cooperation_dominates": expected = 1.0
        elif kind == "defection_dominates": expected = 0.0
        elif kind == "coexistence": expected = xstar
        elif kind == "coordination": expected = 1.0 if start > xstar else 0.0
        else: expected = start
        survival[str(start)] += expected >= 0.5

for R, S, T, P, kind in verify:
    denom = R - S - T + P
    xstar = (P - S) / denom if abs(denom) > 1e-12 else None
    for start in STARTS:
        end = integrate(R, S, T, P, start)
        if kind == "cooperation_dominates": expected = 1.0
        elif kind == "defection_dominates": expected = 0.0
        elif kind == "coexistence": expected = xstar
        elif kind == "coordination": expected = 1.0 if start > xstar else 0.0
        else: expected = start
        if abs(end - expected) > 0.03:
            mismatches += 1
            if len(examples) < 10:
                examples.append({"payoffs":[R,S,T,P],"kind":kind,"start":start,"end":end,"expected":expected})

out = {
    "seed": SEED,
    "worlds": N,
    "numerically_verified_worlds": VERIFY_WORLDS,
    "sampling_statement": "Uniform independent draws over stipulated intervals; not a real-world probability distribution.",
    "regime_counts": counts,
    "regime_fractions": {k:v/N for k,v in counts.items()},
    "fraction_ending_at_or_above_half_cooperation": {k:v/N for k,v in survival.items()},
    "coordination_threshold_summary": {
        "count": len(thresholds),
        "min": min(thresholds),
        "median": sorted(thresholds)[len(thresholds)//2],
        "max": max(thresholds),
    },
    "analytic_numeric_mismatches_over_003": mismatches,
    "mismatch_examples": examples,
    "decision_relevant_differences": ["S-P controls whether rare cooperation can invade", "R-T controls whether near-universal cooperation resists rare defection"],
}
json.dump(out, sys.stdout, indent=2)
sys.exit(0 if mismatches == 0 else 1)
