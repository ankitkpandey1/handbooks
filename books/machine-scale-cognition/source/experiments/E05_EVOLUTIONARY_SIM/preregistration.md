# E05 Preregistration — Verified Evolutionary Regime Map

**Frozen before execution:** 2026-08-31
**Budget position:** experiment 5 of 10
**Purpose:** test H6 using a mathematically specified world with analytic verification

## Ordinary request

An expert community is considering a reward intervention intended to preserve cooperation. In a symmetric two-strategy game, cooperation/cooperation pays R, cooperator versus defector pays S, defector versus cooperator pays T, and defection/defection pays P. After the intervention, plausible—not empirically calibrated—ranges are R∈[2.5,3.5], S∈[-0.5,1.5], T∈[2.5,4.5], P∈[0.5,1.5]. Across these possible games and starting populations, does cooperation reliably survive, and what measurement is most decision-relevant?

## Conditions

- B1: one Luna answer from the ordinary request.
- S: seeded 100,000-world payoff draw; analytic regime classification; numerical replicator integration from five initial cooperation levels; analytic/numeric cross-check; sensitivity summary.
- S implementation: classify all 100,000 worlds analytically; numerically integrate a deterministic 500-world verification sample from five initial states. A pre-run self-review rejected integrating every trajectory because it added roughly two billion Python updates without additional decision value.

## Model

For cooperation fraction x:

`dx/dt = x(1-x)[x(R-T) + (1-x)(S-P)]`.

Signs at x=0 and x=1 classify dominance, coexistence, and coordination regimes. This equation is the external verifier for numerical trajectories.

## Hypothesis

The simulation will not yield a universal intervention recommendation. It will map how often each qualitative regime occurs under the stipulated sampling distribution, expose basin dependence in coordination games, and identify payoff differences S−P and R−T as the measurements controlling invasion and resistance to defection.

## Failure

Fail if numerical and analytic classifications disagree materially, if reported percentages are interpreted as real-world probabilities, or if the model recommends action without calibration.
