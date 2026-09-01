[
  {
    "id": "swe01",
    "binding_constraint": "Authorization inconsistency creates immediate exploit risk and prevents repository-wide confidence.",
    "first_action": "Contain the endpoint, preserve evidence, reproduce the bypass, and patch through the safest established authorization boundary.",
    "machine_work": "Enumerate authorization helpers and call sites, test the affected endpoint and nearby variants, and run focused security regression checks.",
    "selector": "Escalate systemically only if the bypass reflects a reusable helper, review, test, or ownership failure beyond this endpoint.",
    "human_object": "Claim: the endpoint is contained and correctly authorized. Action: approve emergency patch and escalation threshold.",
    "stop_authority": "Incident owner may stop rollout or widen containment on failed authorization tests or evidence of broader exposure.",
    "durable_learning": "Record exploit path, violated authorization invariant, affected patterns, and the systemic decision."
  },
  {
    "id": "swe02",
    "binding_constraint": "Insufficient failure observability prevents distinguishing product, test, and infrastructure causes.",
    "first_action": "Instrument one reproducible test run with correlation, timing, environment, and retry-state capture.",
    "machine_work": "Cluster failures by signature, compare first and retry runs, and replay under controlled environment variants.",
    "selector": "Select the cause category with reproducible differential evidence, not the most frequent hypothesis.",
    "human_object": "Claim: the evidence supports product race, test race, or infrastructure noise. Action: choose one remediation experiment.",
    "stop_authority": "Engineer may stop investigation when evidence is non-discriminating after the two-day budget and escalate with uncertainty.",
    "durable_learning": "Store failure signatures, discriminating conditions, and the minimum instrumentation required for recurrence."
  },
  {
    "id": "swe03",
    "binding_constraint": "Live consumers require compatibility while the type transition is potentially irreversible.",
    "first_action": "Define old and new representations, ownership, invariants, rollback conditions, and a dual-read/write migration path.",
    "machine_work": "Inventory consumers, add compatibility adapters, shadow-compare representations, and measure conversion failures.",
    "selector": "Advance only when consumer coverage, mismatch rate, backfill validation, and rollback readiness meet explicit thresholds.",
    "human_object": "Claim: all live consumers remain behaviorally compatible. Action: approve each migration stage.",
    "stop_authority": "Migration owner may halt writes, backfill, or cutover on mismatch, consumer failure, or rollback degradation.",
    "durable_learning": "Retain consumer inventory, compatibility assumptions, mismatch classes, and final removal criteria."
  },
  {
    "id": "swe04",
    "binding_constraint": "Latency regression is confounded across six changes and full rollback is costly.",
    "first_action": "Freeze further changes and establish a request-level latency baseline with deploy-correlated traces.",
    "machine_work": "Decompose p99 by route, dependency, code path, and change cohort; use targeted flags or reverts for controlled comparison.",
    "selector": "Select the smallest change or interaction whose removal restores the latency budget without violating urgent-fix invariants.",
    "human_object": "Claim: a specific change or interaction explains the regression. Action: authorize targeted mitigation.",
    "stop_authority": "Incident commander may disable a cohort or revert a targeted change when latency or error thresholds breach.",
    "durable_learning": "Capture causal cohort, latency signature, mitigation result, and missing observability."
  },
  {
    "id": "swe05",
    "binding_constraint": "Security exposure conflicts with serialization compatibility across 18 services.",
    "first_action": "Assess exploitability and isolate vulnerable paths while building a compatibility test matrix for the patch.",
    "machine_work": "Diff wire behavior, generate cross-version fixtures, run canary upgrades, and monitor deserialization errors.",
    "selector": "Choose staged upgrade, compensating control, or emergency isolation based on exploitability and compatibility evidence.",
    "human_object": "Claim: the patch preserves required contracts or the residual exposure is controlled. Action: approve staged rollout.",
    "stop_authority": "Security and service owners may halt rollout on exploit evidence, contract breakage, or unsafe fallback behavior.",
    "durable_learning": "Record vulnerability path, serialization deltas, compatibility fixtures, and accepted residual risk."
  },
  {
    "id": "swe06",
    "binding_constraint": "Silent loss is detectable only after ownership, lineage, and reconciliation are established.",
    "first_action": "Quarantine affected outputs and reconstruct counts, checkpoints, retries, and drop points for the prior run.",
    "machine_work": "Add stage-level cardinality metrics, immutable record identifiers, dead-letter capture, and replay checks.",
    "selector": "Select the control point with measurable conservation of records and an accountable owner.",
    "human_object": "Claim: loss is bounded and the pipeline has a recoverable control. Action: approve replay and control rollout.",
    "stop_authority": "Pipeline owner may stop downstream publication on unexplained count divergence or replay mismatch.",
    "durable_learning": "Store lineage, loss taxonomy, reconciliation invariant, ownership map, and alert thresholds."
  },
  {
    "id": "swe07",
    "binding_constraint": "Existing callers need stability while ambiguity must become impossible or explicit.",
    "first_action": "Specify the ambiguous cases and introduce an additive, explicit method while preserving the old method’s contract.",
    "machine_work": "Mine call patterns, add compile-time or runtime diagnostics, build compatibility tests, and compare old/new outputs.",
    "selector": "Migrate callers only when intent is explicit and behavior is equivalent or deliberately reviewed.",
    "human_object": "Claim: the new method removes the defect-causing ambiguity without breaking callers. Action: approve deprecation and migration.",
    "stop_authority": "SDK owner may pause deprecation or release on compatibility failures or unresolved semantic differences.",
    "durable_learning": "Record ambiguity examples, clarified contract, migration patterns, and deprecation evidence."
  },
  {
    "id": "n01",
    "binding_constraint": "Selection quality is limited by mechanism uncertainty and overlapping evidence, not paper volume.",
    "first_action": "Define discriminating outcomes and compress the 30 mechanisms into mutually testable predictions.",
    "machine_work": "Deduplicate papers, extract conditions and effect directions, map evidence dependencies, and score experiments by information gain.",
    "selector": "Select three experiments that maximally separate mechanisms under available resources and falsifiable readouts.",
    "human_object": "Claim: these experiments discriminate among the leading mechanisms. Action: approve the three protocols.",
    "stop_authority": "Research lead may stop an experiment whose readout cannot distinguish mechanisms or whose assumptions fail.",
    "durable_learning": "Store prediction matrix, evidence provenance, rejected options, and outcome-to-mechanism updates."
  },
  {
    "id": "n02",
    "binding_constraint": "The graph-class statement may be invalid, so computation cannot substitute for definition validation.",
    "first_action": "Formalize the conjecture and audit the claimed graph class before generating further examples.",
    "machine_work": "Check definitions, boundary cases, counterexamples, and computational generation against the formal class.",
    "selector": "Proceed only after the graph class and conjecture are syntactically and semantically well-defined.",
    "human_object": "Claim: the conjecture applies to the stated class. Action: authorize proof search or counterexample search.",
    "stop_authority": "Mathematical owner may stop computation when examples fall outside the class or definitions remain ambiguous.",
    "durable_learning": "Record corrected definitions, valid examples, boundary failures, and computational assumptions."
  },
  {
    "id": "n03",
    "binding_constraint": "Only two reversible tests are affordable while competitor response can confound long-run inference.",
    "first_action": "Define the free-tier hypothesis, guardrails, exposure cohort, and success and harm metrics.",
    "machine_work": "Simulate funnel and support effects, randomize two bounded tests, and monitor conversion, retention, cost, and competitor signals.",
    "selector": "Select the test whose result changes the decision and whose downside remains reversible.",
    "human_object": "Claim: a free tier improves strategic value within guardrails. Action: approve one test and a continuation rule.",
    "stop_authority": "Business owner may stop on margin damage, abuse, support overload, or competitor-triggered risk.",
    "durable_learning": "Store test design, segment effects, reversibility conditions, and decision update."
  },
  {
    "id": "n04",
    "binding_constraint": "Unknown validation, data, retention, appeal, and legal conditions make definitive notice claims unsafe.",
    "first_action": "Create a claims-and-unknowns register and obtain accountable legal, privacy, and hiring-owner decisions.",
    "machine_work": "Template conditional notice language, map data flows and retention states, and test candidate explanations and appeal routes.",
    "selector": "Select only language and process controls supported by verified policy and system facts.",
    "human_object": "Claim: the notice accurately describes governed use and candidate rights. Action: approve publication.",
    "stop_authority": "Legal or privacy authority may block release when validation, data use, retention, appeal, or compliance is unresolved.",
    "durable_learning": "Retain the claims register, evidence owners, approved wording, and unresolved-risk log."
  },
  {
    "id": "n05",
    "binding_constraint": "One instructor cannot manually individualize reliable practice and assessment for 90 learners.",
    "first_action": "Define proficiency bands, target technical tasks, assessment invariants, and feedback capacity.",
    "machine_work": "Generate leveled practice, automate first-pass diagnostics, and aggregate rubric-scored evidence for instructor review.",
    "selector": "Assign practice paths by demonstrated error patterns and advance only on rubric evidence.",
    "human_object": "Claim: learner performance improved on target technical-English tasks. Action: approve progression or remediation.",
    "stop_authority": "Instructor may stop automated progression when assessment validity, accessibility, or learner feedback quality fails.",
    "durable_learning": "Store anonymized error patterns, rubric reliability, intervention effects, and learner-level next actions."
  },
  {
    "id": "n06",
    "binding_constraint": "Urgent samples must remain protected despite variable arrivals and unknown downtime capacity.",
    "first_action": "Map priority classes, process dependencies, downtime modes, and current decision rights without assuming capacity.",
    "machine_work": "Build a queue policy and discrete-event stress model using parameter ranges, then test downtime and arrival scenarios.",
    "selector": "Select the policy minimizing urgent delay while remaining feasible across observed scenario ranges.",
    "human_object": "Claim: the policy protects urgent turnaround under stated scenarios. Action: approve a bounded pilot.",
    "stop_authority": "Lab operations authority may suspend the policy on urgent-delay breach, safety issue, or unmodeled downtime.",
    "durable_learning": "Record arrival and downtime observations, policy performance, exceptions, and updated scenario bounds."
  },
  {
    "id": "n07",
    "binding_constraint": "Wayfinding must be accessible across languages and visual abilities, with selection based on tested use.",
    "first_action": "Define navigation tasks, accessibility requirements, language coverage, and failure consequences.",
    "machine_work": "Generate system variants, check contrast and tactile/visual specifications, and analyze route-test results by user group.",
    "selector": "Select the variant with the fewest severe navigation failures across all required groups.",
    "human_object": "Claim: visitors can complete critical routes independently and safely. Action: approve pilot or revision.",
    "stop_authority": "Hospital accessibility owner may stop deployment on severe route failures or unmet accessibility requirements.",
    "durable_learning": "Store task-level failures, subgroup findings, chosen conventions, and maintenance ownership."
  },
  {
    "id": "n08",
    "binding_constraint": "Board usefulness must coexist with minority evidence preservation and identity protection.",
    "first_action": "Define decision questions, evidence taxonomy, confidentiality rules, and minority-evidence handling.",
    "machine_work": "Cluster transcripts, detect outliers and contradictions, redact identifiers, and link claims to representative evidence.",
    "selector": "Select recommendations whose strength reflects prevalence, severity, and decision relevance rather than frequency alone.",
    "human_object": "Claim: the synthesis supports this decision while preserving material dissent and anonymity. Action: approve board framing.",
    "stop_authority": "Research owner may block publication on re-identification risk, unsupported claims, or erased material dissent.",
    "durable_learning": "Retain de-identified evidence map, dissent register, provenance, and board decision outcomes."
  },
  {
    "id": "n09",
    "binding_constraint": "Field mapping is invalid if dataset duplication, leakage, and contradictory evidence are not separated.",
    "first_action": "Establish provenance keys, benchmark lineage, evaluation boundaries, and contradiction criteria.",
    "machine_work": "Deduplicate datasets and papers, trace benchmark reuse, test leakage paths, and build a dated evidence graph.",
    "selector": "Select conclusions supported by independent, leakage-screened evidence with contradictions explicitly retained.",
    "human_object": "Claim: the map distinguishes genuine progress from reuse or leakage. Action: approve priority gaps and follow-ups.",
    "stop_authority": "Research lead may stop a conclusion when provenance or leakage status is unresolved.",
    "durable_learning": "Store lineage graph, leakage tests, contradiction log, and time-stamped confidence changes."
  },
  {
    "id": "n10",
    "binding_constraint": "Authored payoff ranges are uncertainty sets, not empirical probability distributions.",
    "first_action": "Separate model assumptions, payoff ranges, probability beliefs, and robustness questions.",
    "machine_work": "Run sensitivity and worst-case simulations across payoff combinations and update rules without assigning unsupported probabilities.",
    "selector": "Select cooperation claims that survive the specified uncertainty set and parameter perturbations.",
    "human_object": "Claim: cooperation is robust, fragile, or unidentified under the modeled ranges. Action: approve scenario interpretation.",
    "stop_authority": "Simulation owner may stop inference when conclusions depend on unmodeled priors or unstable implementation choices.",
    "durable_learning": "Record payoff provenance, uncertainty-set boundaries, sensitivity results, and robustness limits."
  },
  {
    "id": "n11",
    "binding_constraint": "Urgent allocation must proceed before routes and rainfall forecasts stabilize.",
    "first_action": "Define priority populations, minimum service levels, staging points, and trigger-based contingency modes.",
    "machine_work": "Generate route-independent allocation plans, scenario-test supply and access disruptions, and maintain a live constraint ledger.",
    "selector": "Select the plan with adequate minimum coverage across plausible scenarios and reversible dispatch commitments.",
    "human_object": "Claim: priority needs can be met under the stated scenario. Action: authorize staged allocation and triggers.",
    "stop_authority": "Incident authority may redirect or pause dispatch on safety, access, contamination, or forecast-trigger breach.",
    "durable_learning": "Store demand observations, route failures, trigger performance, and allocation equity outcomes."
  },
  {
    "id": "n12",
    "binding_constraint": "One expert-month must resolve portfolio value under correlated evidence and unequal reversibility.",
    "first_action": "Define decision value, evidence dependence, reversibility, minimum learning milestones, and stopping rules.",
    "machine_work": "Build a dependency-adjusted portfolio model and compare allocations by expected information gain and downside exposure.",
    "selector": "Select the allocation that maximizes decision-relevant learning subject to irreversible-risk limits.",
    "human_object": "Claim: each bet has a justified resource level and exit condition. Action: approve the portfolio allocation.",
    "stop_authority": "Portfolio owner may stop or reallocate a bet when milestones fail or irreversible exposure rises.",
    "durable_learning": "Record dependency graph, milestone evidence, stop decisions, and portfolio reallocation effects."
  },
  {
    "id": "n13",
    "binding_constraint": "The issue is isolated, low-value, and lacks recurrence evidence; broad process changes are unjustified.",
    "first_action": "Correct the typo and verify the rendered sentence in its immediate context.",
    "machine_work": "Run a narrow text and rendering check limited to the edited sentence.",
    "selector": "Select no broader intervention unless recurrence or a related defect is observed.",
    "human_object": "Claim: the typo is corrected without semantic change. Action: accept the local edit.",
    "stop_authority": "Sentence owner may stop after local verification or reject any unnecessary scope expansion.",
    "durable_learning": "Record the correction only; no durable process change without recurrence evidence."
  }
]