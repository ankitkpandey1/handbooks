# Requirements — AI Superpower Book

**Status:** New requirements baseline  
**Date:** 2026-08-31  
**Authority:** Current owner instructions  
**Provenance rule:** `inventory/` contains prior attempts and is read-only evidence. It is not current project state and must never be edited.

## 1. The problem

The book must answer:

> **How can one expert use the unprecedented amount of cognition now available through AI to accomplish valuable work that was previously infeasible for one human?**

A human has finite attention, memory, search capacity, simulation capacity, execution time, and lifetime. AI makes knowledge, reasoning attempts, generation, search, computation, tool use, and simulation available at a radically different scale. One person can now call on machinery informed by more material than any person could read, ask it to perform advanced reasoning, generate vast numbers of alternatives, write executable tools, and simulate huge populations of possible worlds or evolutionary games.

The existence of that resource is not the answer. The problem is **how to exploit it**.

The book must show how one expert turns abundant but imperfect machine cognition into reliable real-world leverage without creating proportional human review, correlated nonsense, false confidence, proxy optimization, or beautifully executed work on the wrong problem.

## 2. The book’s promise

After reading the book, an expert should be able to:

- recognize cognitive workloads whose feasible frontier can be radically expanded;
- transform a vague real problem into structures that machines can search, simulate, test, and execute;
- use AI for breadth and depth far beyond a single conversational answer;
- construct populations of hypotheses, designs, representations, strategies, experiments, and counterexamples;
- use tools, computation, evidence, experiments, and formal checks to eliminate wrong candidates;
- compress machine-scale work into decisions a human can judge with bounded attention;
- move from an observed instance to siblings, classes, mechanisms, prevention, and discovery of unknown classes when worthwhile;
- build persistent systems that learn from outcomes and become more capable over time;
- know when machine scale will not help, or will make the result worse.

The result must be a practical expansion of what one person can accomplish—not improved chatting, prompt advice, or familiarity with AI terminology.

## 3. Usage is the organizing principle

Every major section must begin with something the expert is trying to accomplish and end with an operational method.

Required reader-facing unit:

```text
objective
  -> previously binding human limitation
  -> machine cognition that can be scaled
  -> operating architecture or procedure
  -> selection and verification
  -> compressed human decision or bounded execution
  -> measured outcome and learning
```

The main text must provide procedures, decision rules, reusable frameworks, system designs, worked cases, failure boundaries, stopping rules, and implementation patterns.

It must not be organized as a tour of models, AI history, mathematics, papers, products, or techniques.

## 4. Deep grounding versus reader curriculum

The book must be grounded in deep technical understanding. The reader does not need to be taught all of that understanding.

The research and design foundation must include, where relevant:

- modern LLM architecture and computation, including tokenization, embeddings, attention, residual streams/connections, representations, inference, context behavior, sampling, post-training, tool use, and adaptation;
- the mathematics underlying those systems;
- empirical knowledge of capabilities, scaling behavior, correlated failures, calibration, context/path dependence, self-verification limits, and tool-mediated performance;
- state-of-the-art mathematics and frameworks for search, optimization, information acquisition, uncertainty, causality, robustness, sequential decisions, control, games, evolution, experimental design, verification, and stopping;
- software and systems methods for orchestration, parallelism, durable state, observability, evaluation, and safe execution.

This substrate exists to make the book’s recommendations correct. The main text should normally present the derived capability, limitation, operating rule, and verification boundary—not teach the substrate itself.

Explain an internal mechanism or mathematical derivation to the reader only when it is needed to:

1. use a method correctly;
2. choose between meaningfully different actions;
3. diagnose an important failure;
4. understand a hard limit or safety boundary.

Optional technical depth may live in notes or appendices. No architecture trivia, decorative mathematics, model catalogues, or benchmark tourism belongs in the main flow.

## 5. Burn the lake

The book must make systemic escalation automatic.

When given an issue, opportunity, or question, the expert and the AI should consider:

```text
reported instance
  -> sibling instances
  -> recurring class
  -> adjacent or parent classes
  -> generating mechanism
  -> prevention or automatic detection
  -> machinery for discovering unknown future classes
```

This is not a command to over-engineer everything. Escalation stops when expected avoided loss, reuse, or new capability no longer justifies construction cost, maintenance, complexity, delay, and false positives.

The same rule governs creation of the book: repeated defects require changing the governing concept, architecture, or process before editing more paragraphs. Do not preserve a failed structure by accumulating patches.

## 6. Human and machine roles

The design target is not full autonomy. It is maximum useful cognition around genuinely scarce human judgment.

Machine cognition should be used aggressively for scalable work such as search, generation, calculation, simulation, retrieval, transformation, monitoring, adversarial testing, and repeated execution.

Human judgment remains responsible where necessary for objectives, values, tacit context, accountability, frame selection, irreversible consequences, and decisions with weak external verification.

The system must continually try to reduce unnecessary human work through better evaluators, stronger representations, automation, and compression. Generated volume is not success. Accepted real-world value per unit of human attention is the governing outcome.

## 7. Reality must select

Fluent model output is proposal material, not authority.

Every important output must specify what can falsify it. Depending on the claim, this may include primary evidence, deterministic computation, tests, static analysis, formal proof, simulation against measured data, controlled experiments, causal intervention, adversarial evaluation, independent expert judgment, or observed downstream outcomes.

The book must distinguish:

- generation from evidence;
- repeated samples from independent evidence;
- plausible explanation from causal explanation;
- passing a proxy from satisfying the real objective;
- immediate acceptance from durable real-world success.

Where strong verification cannot be built, the system must reduce confidence, narrow authority, seek discriminating information, preserve alternatives, or abstain.

## 8. General scope

The framework is general across expert work. It must apply to research, scientific and mathematical investigation, strategy and decisions, design, writing and synthesis, learning, software engineering, and other high-value knowledge work.

Software engineering should be a deep stress test because it offers rich tools and executable feedback. It must not become the hidden definition of all expert work.

Examples from different domains must demonstrate that the same underlying principles transfer while evidence, harm, verification, and authority differ.

## 9. Required architecture of the book

The book is limited to six chapters. The chapter spine must follow expert action:

1. **Find the Leverage** — identify the infeasible workload, scarce human judgment, scalable machine cognition, and verification economics.
2. **Turn the Problem into a Machine** — establish the exact objective and compile fuzzy work into searchable, testable, executable structures; apply burn-the-lake escalation.
3. **Expand What Can Be Considered** — scale search, alternative representations, retrieval, tools, simulation, experimentation, adversarial generation, and engineered diversity.
4. **Make Reality Select** — manufacture verification and use evidence, computation, tests, formal systems, interventions, and outcomes to reject attractive nonsense.
5. **Convert Scale into Action** — allocate cognition, compress outputs, manage human review and authority, execute safely, monitor, and stop.
6. **Build a System That Improves Itself** — preserve state and outcomes, learn better routing and evaluation, convert escaped failures into prevention, discover unknown classes, and recursively improve the cognitive system.

For every chapter, answer:

- What does the expert do?
- What previously scarce cognition becomes scalable?
- What deep technical or mathematical grounding justifies the method?
- What failure modes constrain it?
- What selects or falsifies the output?
- What reaches the human, and how much attention does it require?
- What concrete capability becomes possible that was not possible before?

## 10. Evidence requirements

The book must be evidence-grounded, not authority-sounding.

- Prefer primary research, canonical mathematics, authoritative technical documentation, and strong independent evaluations.
- Separate observed evidence, mathematical derivation, engineering synthesis, and speculation.
- Preserve counterevidence, boundary conditions, and uncertainty.
- Do not infer that a complete workflow is validated merely because its components have evidence.
- Do not fabricate experiments, measurements, multipliers, or calibration.
- Treat vendor claims and benchmarks narrowly and identify their limitations.
- Evaluate workflows and outcomes, not model prestige.
- Compare against simple approaches and human/AI-minimal baselines where feasible.
- Measure correctness, downstream value, time, cost, review burden, robustness, failure cost, and learning—not generated volume.
- Keep volatile product facts outside the durable conceptual spine.

“Billion books,” “billions of simulations,” and extreme multipliers express the qualitative scale discontinuity unless a specific quantitative claim is independently supportable.

## 11. Required worked demonstrations

The book must include end-to-end cases, not isolated anecdotes. Each case should begin with an ordinary request and show how the system changes the feasible frontier.

At minimum, demonstrate:

- one case that expands from a reported instance to siblings, mechanism, and prevention;
- one research or scientific case using massive hypothesis/evidence/experiment search;
- one mathematical, strategic, or evolutionary simulation case using machine-generated computation rather than human mental simulation;
- one weak-verifier case where the correct result is bounded assistance, information acquisition, or abstention;
- one contrasting case where burn-the-lake escalation correctly stops early.

Each demonstration must report the human role, machine workload, verification method, compressed deliverable, cost/review burden, and outcome or honest validation status.

## 12. Self-review before action

Before changing project requirements, research direction, book architecture, or manuscript content, perform an adversarial self-review:

1. Am I answering how one expert uses scalable cognition, or merely describing AI/mathematics?
2. Am I treating an instance when the defect indicates a broader class or broken architecture?
3. Is deep technical knowledge grounding the recommendation without becoming unnecessary reader curriculum?
4. Does this increase feasible capability without scaling human attention proportionally?
5. What selects the result in reality?
6. What evidence or counterexample could show the proposed change is wrong?
7. Am I importing assumptions from a prior failed attempt instead of deriving the requirement from the current problem?

Record material corrections and their causes in current project state. Never modify historical inventory to make it agree with the new project.

## 13. Deliverables and acceptance

Required durable outputs:

- a canonical Markdown manuscript;
- a generated reading edition;
- source and claim records sufficient to audit important recommendations;
- explicit records for planned versus completed validation;
- a failure/correction log;
- reproducible build and publication checks.

The book succeeds only if an expert can use it to design a workflow for a new problem—not merely repeat its examples—and can explain:

1. what cognition to scale;
2. how to structure the problem;
3. how to search or simulate beyond human capacity;
4. how to make reality select;
5. how to keep human judgment bounded;
6. how the system learns and improves.

If the manuscript mainly teaches what models or mathematical fields are, it fails regardless of technical correctness.
