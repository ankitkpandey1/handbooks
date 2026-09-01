# E05 Result

**Claim level:** `REPRODUCIBLE_INTERNAL` for the mathematical computation; `DESIGNED` for any real intervention
**Verdict:** useful conditional regime map; no empirical recommendation

The one-shot Luna baseline correctly identified the controlling differences `R−T` and `S−P`, refused to treat intervals as probabilities, and recommended conditional/worst-case analysis. It was already strong.

The seeded computation added a 100,000-world regime map under explicitly uniform independent draws:

- defection dominates: 56.284%;
- cooperation dominates: 6.247%;
- coordination/basin dependence: 18.732%;
- coexistence/interior equilibrium: 18.737%.

These are fractions of an authored parameter distribution, not real-world probabilities. The map quantifies sensitivity and shows why a single mental scenario is inadequate; it does not validate the parameter ranges.

Numerical integration checked 500 deterministic worlds from five starting states. Six of 2,500 trajectories remained more than 0.03 from their asymptotic analytic target after the fixed horizon. Inspection shows small selection gradients near regime boundaries and therefore slow convergence. The run is retained as a mismatch, not tuned away.

## Operational learning

Simulation should report separately:

1. model regime and asymptotic equilibrium;
2. finite decision/observation horizon;
3. parameter-distribution provenance;
4. boundary sensitivity;
5. measurements that control regime selection.

For this model, measure `S−P` to learn whether rare cooperation can invade and `R−T` to learn whether prevalent cooperation resists rare defection. If those are not calibrated, more simulated draws do not justify action.
