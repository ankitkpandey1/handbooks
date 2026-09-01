---
author: Ankit Kumar Pandey <itsankitkp@gmail.com>
bibliography: references.bib
citeproc: true
classoption:
- paper=a4
- fontsize=11pt
- titlepage=true
colorlinks: true
date: 2026-09-01
documentclass: scrartcl
geometry: margin=0.82in
header-includes:
-
keywords:
- expert AI use
- language models
- decision theory
- verification
- test-time search
- AI safety
lang: en-GB
linkcolor: NavyBlue
mainfont: Noto Serif
monofont: DejaVu Sans Mono
numbersections: true
reference-section-title: References
rights: Copyright © 2026 Ankit Kumar Pandey. Licensed under CC-BY-4.0; code under Apache-2.0.
sansfont: Noto Sans
subject: Evidence-bounded use of language models for expert work
subtitle: A field guide to expanding checked search without expanding false confidence
title: One Expert, Machine-Scale Cognition
toc: true
toc-depth: 2
toccolor: NavyBlue
urlcolor: NavyBlue
version: Edition 1.0.0
---





# Publication information

**Tier B · Edition 1.0.0.** This is an evidence-bounded field guide for experts using language models to expand checked search, computation and comparison. It does not claim measured productivity gains, independently validated scientific conclusions, or safe autonomous action.

Copyright © 2026 Ankit Kumar Pandey. Prose and documentation are licensed under CC-BY-4.0. Code, scripts, executable experiment harnesses and code listings are licensed under Apache-2.0, following the repository licensing policy.

## Scope and evidence labels

Labels apply to the paragraph, box or result record in which they occur. A citation alone identifies a source; the label states what kind of support the text claims.

- **\[measured\]** — produced by a retained internal run with the stated artifacts. It is local evidence, not independent or outcome validation.

- **\[assessed\]** — judged by the author from a recorded run without blinded or independent raters.

- **\[documented\]** — supported by the cited primary paper or project documentation.

- **\[inferred\]** — a reasoned operational consequence of measurements, documented mechanisms or mathematics; not observed directly.

- **\[designed\]** — a specified procedure or case that has not produced a field outcome.

- **\[opinion\]** — a disclosed judgement about usefulness, presentation or priorities.

Unlabelled imperatives are instructions, not empirical performance claims. Treat any other unlabelled factual assertion as unverified and open a claim challenge.

## Code authenticity labels

- **\[executed\]** — the exact command or listing was run in the retained experiment.
- **\[adapted\]** — derived from executed code and edited for presentation.
- **\[illustrative\]** — not run; it demonstrates structure only.

## How to use this edition

Read the opening and Chapter 1 first. Then apply the field card to one real problem. The main text gives the operational explanation; optional Mathematical detail boxes preserve the formal statement and its assumptions. Appendix A records all ten experiment slots, including failed, null and adverse runs.

# What one expert can do now

Suppose you have a hard problem and one week to solve it. The usual limit is not intelligence. It is the amount of work one person can inspect, compare, calculate, test, and remember.

AI changes that limit. It can search a large collection, write small tools, run calculations, generate alternatives, and repeat a test thousands of times. It can do these jobs in parallel and keep a record of each result. One expert can therefore examine a much larger part of a problem than before.

But more output is not the same as better work. An AI can repeat the same wrong assumption many times. It can write a confident explanation without checking the evidence. It can optimise a score that does not match the real goal. If you ask for one hundred reports, you may simply create one hundred reports to review.

This guide explains how to get the benefit without inheriting that review burden.

The central rule is simple:

> **Field card: The operating card**
>
> **1. Result.** What must change in the real world? What harm must you avoid?
>
> **2. Current limit.** What work can one person not do well enough: organise, search, compare, check, review, act, or learn?
>
> **3. Check.** Before producing many answers, decide what evidence or test can reject a bad one.
>
> **4. Machine job.** Give the model the large, repeatable part: search, calculation, simulation, generation, testing, or monitoring.
>
> **5. Human decision.** Reduce the result to the smallest item a responsible person can judge. Aim for one or two pages. Track accepted value per hour of responsible review.
>
> **6. Limits on action.** Decide what the system may do, what needs approval, and when it must stop.
>
> **7. Learning.** Save the evidence, failures, decisions, and outcomes that will improve the next similar job.

The order matters. Start with the real result, not the document someone requested. Define the check before asking the machine to produce more. Decide what the human must see before the machine begins. If you cannot explain how a bad answer will be rejected, do not scale the work yet.

Here is a software example. A report says that one web endpoint bypasses an authorisation check. The small response is to patch that endpoint. The larger question is whether other endpoints use the same unsafe pattern. AI can search the repository, list related routes, generate exploit tests, and compare repair designs. Tests and static checks reject bad repairs. The human reviews a short table of affected routes and chooses whether to make a local fix or change the shared mechanism.

The same method works outside software. A scientist may need to examine 164 papers and choose three experiments. AI can collect and organise the papers, but it cannot make a paper true. Each scientific claim must still point to supporting evidence and a possible test. The scientist should receive a short list of competing mechanisms and experiments, not 164 summaries.

A strategist may want to know whether cooperation will survive under uncertain incentives. AI can calculate outcomes across 100,000 sets of assumed payoffs. That calculation can reveal which assumptions control the answer. It cannot reveal how common those payoffs are in the real world. The useful result is a map of conditions and a recommendation about what to measure next, not a made-up probability.

These examples show the division of labour used throughout the book. The machine does work that becomes cheap when repeated. The person keeps responsibility for the goal, important assumptions, weakly tested claims, and irreversible actions. Better tests and better representations can move some work from the human side to the machine side over time.

\[documented\] Modern language models explain why this discipline is necessary. They generate each next token from the preceding context. More samples from the same context may share the same missing fact or framing error (Hariri et al. 2026; Zhu et al. 2025). A likely continuation is not the same as a verified claim. Faster attention and cache methods reduce the cost of producing and comparing candidates, but they do not turn fluency into evidence (Vaswani et al. 2017; Dao et al. 2022).

> **Mechanism: What a model call actually supplies**
>
> A Transformer maps input tokens to vectors, then repeatedly updates those vectors through attention and feed-forward blocks connected by a residual stream. Attention moves information between token positions; feed-forward blocks transform the representation at each position; the residual path carries and combines these updates. The final state parameterizes a conditional distribution over the next token.
>
> This architecture is powerful because one context can activate many learned patterns and tools can connect those patterns to external computation. It also creates a specific limitation: another sample from nearly the same context is another draw from a related conditional process, not an independent measurement of the world. Shared context, retrieved evidence, model weights, and judge prompts create correlated errors.
>
> FlashAttention and newer kernels reduce memory traffic and make longer contexts or larger batches cheaper. Blackwell-specific FlashAttention-4 shows why these economics change with hardware generations (Dao et al. 2022; Zadouri et al. 2026). They change the feasible amount of search. They do not change the logical status of the result. A thousand cheap continuations remain proposals until a source, test, proof, measurement, or outcome selects among them.
>
> **Basis.** Transformer and attention-kernel architecture papers support the computation description and changing search cost (Vaswani et al. 2017; Dao et al. 2022; Zadouri et al. 2026). They do not support a claim that the complete operating method improves productivity.

> **Decision rule: The architecture-to-operation translation**
>
> Use residual computation and token sampling to generate, transform, and compare candidates. Use context isolation or different evidence paths when correlated errors matter. Use tools when the missing object is a calculation or observation. Use external selectors because token probability estimates which continuation fits the context; it does not establish which claim is true.

You do not need to study model architecture to use the guide. The technical lesson is enough: use the model to propose and transform work; use evidence, computation, tests, experiments, and observed outcomes to decide what survives.

The guide has six chapters. Chapter 1 helps you find work that is worth scaling. Chapter 2 turns a vague request into objects a machine can search and test. Chapter 3 shows how to explore more possibilities without producing copies of the same idea. Chapter 4 builds checks that reject attractive nonsense. Chapter 5 turns a large body of machine work into a small decision and a safe action. Chapter 6 stores outcomes and failures so the system improves.

The evidence boundary is also simple. This guide includes reproducible local work: a 164-record literature corpus, a 100,000-world game calculation, and executable software fixtures. It also includes failed and inconclusive experiments. These support parts of the method. They do not prove that the whole system improves expert productivity in the real world. That claim needs later human and field studies. The defensible promise is narrower: the method helps an expert expand checked search while exposing review debt, weak evidence, and reasons to stop.

## How to read the evidence labels

| Label                 | Meaning                                                                                                           |
|-----------------------|-------------------------------------------------------------------------------------------------------------------|
| Reproducible internal | Code, fixtures, stored output, and a repeatable scorer support the stated result. It is still a local experiment. |
| Assessed internal     | A recorded run was judged by the author without independent or blinded raters.                                    |
| Component grounded    | External research supports a mechanism or component, not the complete workflow.                                   |
| Designed              | The procedure is specified but has not produced the claimed real-world outcome.                                   |
| Outcome validated     | A downstream field outcome was measured. No claim in this edition has this label.                                 |

These labels are deliberately unequal. A reproducible fixture does not establish productivity, safety in production, or scientific truth. A designed case is an implementation pattern, not a result.

## How this guide was made

Ten experiment slots were fixed. Failed harness runs, null results, and adverse results kept their numbers. Each recorded experiment has a preregistration, inputs, outputs where a run occurred, a scorer or stated assessment method, and a result boundary under [`experiments/`](experiments/). Appendix A gives the full readable record and reproduction paths. The raw files, not the summary prose, are authoritative.

Use the operating card on a real problem as you read. By the end, you should be able to say what work to scale, what will check it, what you must personally judge, and when the system must stop.

*Define the check before increasing the volume.*

# Find the Useful Work

AI is useful when it removes a real limit on valuable work. It is not useful merely because it produces something quickly. This chapter helps you decide what to scale, what to keep human, and when to leave the task alone.

## Turn a request into a proposition reality can answer

A request often names a document rather than a result. “Write a market report” names an output. It does not say what decision the report should improve. “Fix this endpoint” names a local change. It does not say whether similar failures must also be prevented.

Before using AI, write two sentences:

- The result we need is \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.
- We must avoid \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.

These sentences are not a writing exercise. They construct the objective against which search will be selected. A model can optimise only the signal it receives: instructions in context, feedback from tools, and scores returned by a judge. If the instruction names an activity—“understand,” “improve,” or “research”—many incompatible outcomes satisfy it. The model can produce a fluent artifact while the real state of the world remains unchanged.

Make the first sentence observable by naming four things: the object that changes, the direction of change, the observation that reveals it, and the time or scope boundary. “Understand the literature” contains none of them. “By Friday, choose three experiments whose predicted observations differ under the two leading mechanisms” contains all four. “Improve the migration” is equally incomplete. “Move all 43 consumers to the new field, observe no inconsistent read in the compatibility test, and retain a rollback that restores the old version within ten minutes” can be rejected by evidence.

The second sentence turns a general warning into a boundary. You are not saying, “avoid harm if convenient.” You are saying, “an answer that crosses this boundary is unacceptable, however well it performs on the visible goal.” A fast migration that corrupts old clients loses even if it finishes early. A polished notice with an unsupported promise loses even if readers prefer it.

This matters because AI tends to improve what it can see and score. Speed, completeness, test count, and writing quality are visible. A rare compatibility failure or future legal harm may be harder to observe. Unless the prompt and checker treat that harm as a rejection condition, the system can win the visible contest while losing the real one.

> **Mathematical detail: value subject to a safety boundary**
>
> Let $a$ mean a proposed action, $U(a)$ the value produced by that action, and $H$ the harm we named. The evidence available now is $D$. We choose the most valuable action only from actions whose estimated chance of causing the harm stays below the tolerated limit $\epsilon$:

$$
\max\{U(a): P(H\mid a,D) \leq \epsilon\}.
$$

> The formula does not tell us the correct harm limit or provide reliable probabilities. People must choose the limit, and evidence must support the estimate. Its purpose is narrower: high value never compensates for violating a declared safety boundary.

This is relevant to Transformer machinery because next-token training supplies no privileged representation of your actual utility function. The model infers a locally plausible objective from the context. Longer reasoning can pursue that inferred objective more effectively; it cannot repair a goal that was never specified. The two sentences place the real-world criterion and its principal constraint inside the search problem.

AI may propose candidate formulations when stakeholders are speaking vaguely. Treat those formulations as probes: for each one, ask what observation would make it false and who bears the loss if it is wrong. The accountable human chooses because this choice supplies values that cannot be recovered from token probabilities. The output is one result sentence and one harm sentence, each tied to an observable rejection condition.

Stop if nobody can say what change will count as success. The reason is not caution for its own sake. Candidate quality is unidentifiable when no observation orders the candidates; extra generation then increases review load without increasing decision information.

## Find the binding constraint by intervention

Now ask why the result is difficult. A label such as “coverage problem” is not yet a diagnosis. A diagnosis predicts what will happen when one resource changes. If doubling retrieved papers would not change the decision, retrieval is not the binding constraint. If perfect tests would still leave two designs incomparable because the desired behaviour is disputed, testing is not the binding constraint.

Use the following as a checklist of possible constraints, not as a taxonomy of problem types:

- **Organisation.** The facts, claims, constraints, and actions are mixed together.
- **Coverage.** Relevant items exist outside the set examined, and encountering them could change the decision.
- **Discrimination.** The candidates make different claims, but the present observations give them nearly the same score.
- **Review.** A discriminating check exists, but applying it manually costs more attention than the decision warrants.
- **Safe action.** The answer is known, but execution needs permissions, monitoring, or rollback.
- **Learning.** Past results are not recorded in a form that improves the next similar task.

Find the binding constraint with a small counterfactual test. Ask: “If this resource became ten times cheaper tomorrow, would the final decision improve?” Then test the most plausible answer on a small sample.

| Suspected limit | Diagnostic intervention                                                                         | Evidence that it is binding                                                           |
|-----------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Coverage        | Add a different retrieval route to a frozen sample.                                             | It finds decision-relevant items missed by the existing route, not merely more items. |
| Discrimination  | Construct an observation for which the leading candidates predict different results.            | The observation changes their order or eliminates one.                                |
| Review          | Apply the existing check automatically to a sample, then audit false accepts and false rejects. | Human effort falls while the important error rate stays inside the stated bound.      |
| Organisation    | Convert a sample into a graph, constraint table, state machine or claim record.                 | A contradiction or dependency becomes mechanically detectable.                        |
| Safe action     | Run a reversible canary with a trip condition.                                                  | Feedback arrives before exposure becomes unacceptable.                                |
| Learning        | Retrieve prior decision records for a new case.                                                 | They change routing, a prior, a check or a stop rule.                                 |

This explains why tests sometimes solve a discrimination problem. They do so only when competing candidates predict different test outcomes. A test that every candidate passes adds no information. A side-by-side table helps only when its columns expose differences that affect the decision. Disproving examples help only when one candidate allows them and another does not. The intervention is not “write tests.” It is “find an observation on which the remaining explanations disagree.” This may be a unit test, scientific experiment, customer interview, proof obligation, or red-team example.

> **Mathematical detail: when an observation separates explanations**
>
> Suppose $h_1$ and $h_2$ are two possible explanations and $e$ is a test result. The result separates them when one explanation predicts it more strongly than the other:

**Likelihood ratio:** the probability of the result under explanation 1, divided by its probability under explanation 2, is not one.

> A ratio near one means both explanations expected roughly the same result, so the test teaches little. A ratio far above or below one can change which explanation deserves support. In practice, exact probabilities are often unavailable. The usable question is still plain: “Would the two explanations expect meaningfully different observations?”

Coverage has a different mechanism. Retrieval helps only if the unexamined region contains evidence with enough value of information to alter the action. Count novel mechanisms, contradicted claims, uncovered code paths, or changed decisions—not documents returned. If a second search route produces the same evidence dependencies as the first, the item count rose but independent evidence coverage did not.

Review is different again. When a good rejection rule already exists, compilation, static analysis, schemas, calculators, and test harnesses can apply it cheaply. When the rule is weak, automating it merely accepts mistakes faster. Measure the check on known good and deliberately damaged examples before trusting the saved review time.

For an unfamiliar problem, derive the machine job rather than selecting one from a menu:

- Name the decision that is presently blocked.
- List the observations that could change it.
- Identify why those observations are absent: not found, not generated, not distinguishable, too costly to check, or too risky to obtain.
- Run the smallest intervention that changes one cause while holding the others roughly fixed.
- Scale that intervention only if the decision improves or uncertainty relevant to it decreases.

> **Decision rule: Example: diagnosing a migration rather than naming it**
>
> Suppose two migration designs both pass the current unit tests. Calling this a “comparison problem” explains nothing. Inspect their disagreement: one predicts old and new clients can coexist; the other predicts an inconsistent read during the transition. A compatibility test that runs both client versions against the same staged database now has different expected outcomes. If both still pass, generate more migrations only if another material disagreement remains. If no such disagreement exists, the rational next move is a canary that observes production traffic, not more prose or more candidate code.

One local experiment in this project compared several elaborate operating systems across 20 tasks. No design won everywhere. Once every design had to state the result, the current limit, the check, the human decision, and the stop condition, most produced competent plans. The practical lesson is that a clear work contract matters more than a grand name for the workflow. This was an assessed planning experiment, not a productivity trial.

Write the current limit as a causal statement: “The decision is blocked because we lack \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_; if we obtain it, we expect \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ to change; we will test that prediction by \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.” If you cannot complete all three fields, you do not yet know what to scale.

## Decide how bad work will be rejected

The cost of producing an answer has fallen. The cost of deciding whether it is safe may not have fallen. That difference decides whether scaling helps.

List the strongest check available for the important claim:

- a deterministic calculation;
- a test or static analysis;
- a proof;
- a primary source linked to the exact claim;
- an experiment that gives different results under competing explanations;
- a reversible trial with monitoring;
- an observed outcome after enough time has passed.

Then estimate three quantities. How often will the check catch a bad result? What would a missed error cost? How much human attention does each candidate require?

The practical comparison is simple: additional checked work must be worth more than everything needed to produce, inspect, delay, and safely act on it. If ten more candidates require two days of expert reading and share the same weak check, they may reduce total value. One new experiment that separates the candidates may be worth more than all ten.

> **Mathematical detail: the escalation inequality**
>
> The compact form is

**Escalate when:** `benefit from more checked work > compute + delay + review + risk`

> Use ranges rather than invented precision. The inequality is a reminder to count costs that cheap generation hides, especially expert review and exposure to a missed error.

> **Mechanism: Why this is a decision-theory problem**
>
> The intuitive rule is to compare actions by both the value of their possible outcomes and how plausible those outcomes are. A spectacular outcome with almost no chance of occurring should not automatically beat a reliable, useful one. Likewise, a small chance of catastrophic harm may control the choice even when the average outcome looks attractive.
>
> Formally, let an action $a$ have possible consequences $x$, uncertain under current evidence $D$. Decision theory chooses the action with the highest probability-weighted value:

$$
a^*=\arg\max_a \sum_x P(x\mid a,D)U(x).
$$

> AI can cheaply enlarge the set of actions, hypotheses, or calculations. That helps only if a new candidate changes the maximizing action or reduces the chance of choosing badly. Output volume has no term in the equation.
>
> New evidence has value when it can change the decision. Its expected value of information is the expected utility after observing it minus the utility of acting now. Buy the evidence only when that gain exceeds search, delay, review, and failure exposure. Under severe uncertainty, use ranges or worst-case regret instead of inventing precise probabilities.
>
> **Basis.** The equation is the standard expected-utility decision rule; the value-of-information statement follows by comparing the best expected action before and after a possible observation. This is a mathematical rationale, not evidence that users estimate probabilities accurately. Use intervals when calibration is unavailable.

> **Decision rule: Impact of ignoring the rule**
>
> Without this comparison, cheap generation creates an asymmetric cost transfer: the machine creates candidates in seconds and the expert inherits hours of review. With a weak selector, the best-looking candidate may simply be the one that most effectively exploits the proxy score. The project becomes slower and more confident at the same time.

When the check is strong and cheap, scale aggressively. Software tests can reject thousands of bad changes. A formula can check a large simulation. A database constraint can reject invalid records automatically.

When the check is weak, spend the next unit of effort on better information. Find the missing source. Build a small test. Ask for a measurement. Narrow the claim. If none is possible and the harm is serious, stop.

## Choose scale, a better check, a smaller claim, or no work

You now have four choices.

**Scale the work** when a repeatable check can judge it and the final human decision stays small. Examples include searching related code paths, testing many parameter values, or retrieving papers into a structured table.

**Build a better check** when the machine could produce many candidates but you cannot tell which are good. Write a hidden test, obtain a reference measurement, or define a contradiction check before increasing volume.

**Narrow the claim** when only part of the problem can be checked. Recommend one verified sentence instead of a complete public notice. Migrate one consumer before the whole system. Report a conditional result instead of a probability.

**Stop** when the requested work is already small, the broader class has no evidence of recurrence, or further checking costs more than the likely loss. Correcting an isolated spelling error does not require a taxonomy, a multi-agent debate, or a monitoring system.

The chapter’s final output is a one-page work brief:

> **Field card: One-page work brief**
>
> **Result:** the observable change and the harm to avoid.
>
> **Current limit:** the work one person cannot perform well enough.
>
> **Check:** the artifact or observation that can reject a bad result.
>
> **Machine job:** the repeatable work to perform at scale.
>
> **Human decision:** the one- or two-page item that needs accountable judgment.
>
> **Choice:** scale, improve the check, narrow, or stop.

Do not proceed until each line is concrete. If the brief says only “use AI to research and analyse,” the project is not ready.

## Chapter 1 evidence and further reading

> **Field card: What the experiments tested**
>
> **Question.** Does one elaborate workflow architecture reliably produce better plans, or does the task contract matter more?
>
> **Setup.** E02 generated 21 plans: seven architectures applied to three tasks. The author scored specificity, selection, scalable work, bounded review, authority, and learning. E10 broadened the comparison to 20 frozen tasks, including seven software tasks. Every condition had to return the same seven operational fields.
>
> **Result.** E02 favored the richer hybrid, but its description was longer and the same model generated and judged every plan. In E10, all seven conditions completed all 20 task records. Different approaches fit different tasks; no architecture won across domains. The shared work contract caused much of the useful convergence.
>
> **Finding and limit.** Diagnose the constraint and define the check before choosing workflow machinery. These are **\[assessed\] Assessed internal** planning probes. They measured plan structure, not task success, expert time, or real productivity.

\[documented\] For the economics behind this chapter, read the verification result of Setlur and colleagues alongside the long-horizon failure analysis of Wang and colleagues (Setlur et al. 2025; X. J. Wang et al. 2026). The useful inference is limited: extra inference is valuable only when feedback and checks discriminate among outputs.

# Turn the Problem into a Machine

A vague request is hard to search, test, or automate because prose can hide which statements are observations, guesses, decisions, and consequences. The remedy is not prettier documentation. It is a representation whose elements admit different operations: sources support facts, experiments update assumptions, constraints reject actions, and monitoring measures outcomes.

## Separate what is known from what must be decided

Start with six lists because each list has a different update rule:

- **Facts:** observations you can point to.
- **Assumptions:** statements you are using but have not established.
- **Unknowns:** missing information that could change the decision.
- **Claims:** statements that may enter the final answer.
- **Actions:** changes someone could make.
- **Outcomes:** what happened after an action, including delay and side effects.

Do not let the model merge these categories. “The interface caused the failure” is a causal claim, not a fact: it requires an intervention or a test against competing explanations. “The paper supports mechanism A” is not established until the relevant passage and boundary are recorded. Treating both as ordinary text erases the difference between observing $X$, inferring $X\rightarrow Y$, and choosing action $a$.

Give every important claim four fields:

| Field      | Question                                                          |
|------------|-------------------------------------------------------------------|
| Evidence   | What exact source, test, or calculation supports it?              |
| Dependence | Does this rely on the same source or assumption as another claim? |
| Rejection  | What result would show that it is wrong?                          |
| Scope      | Where does it apply, and where does it not apply?                 |

AI can help create and populate these lists. It can extract claims from papers, locate code paths, or identify assumptions in a plan. But it must attach a source location or mark the item as unverified. A blank field is useful information. A guessed field is not.

The human output is a short table, not a transcript. A decision needs sufficient information for the choice, not a replay of every generated token. Stop when every decision-changing claim has a source or is marked unknown. If removing a row can reverse the action, restore it; if no possible value of a row changes the action, it is not decision-critical.

## Choose a form that can be checked

Different problems become easier in different forms because a representation determines which errors become mechanically visible. A long explanation permits almost any relation to remain implicit; an explicit structure exposes particular violations.

Use a **graph** when relationships matter. A graph can show which services call a shared authorisation helper, which papers support the same claim, or which decisions depend on one assumption.

Use a **state machine** when order matters. A migration can be described as old, dual-read, dual-write, cutover, and rollback states. Each transition can have a test and an owner.

Use a **constraint table** when a candidate must satisfy several rules. A design may need to meet cost, safety, latency, and compatibility limits. The table makes failure visible.

Use a **causal diagram** when the question asks what will happen after an intervention. It separates a factor that merely travels with the outcome from a factor that changes it.

Use a **game or simulator** when several actors adapt to one another or when a process changes over time. Write the actors, choices, payoffs, update rule, and time horizon before running it.

Use an **executable test or proof obligation** when correctness can be stated precisely. In software, write the failure as a test. In mathematics, state the conditions and the proposition. In data work, state the invariant that every valid record must satisfy.

Choose the form by naming the relation whose violation would change the decision. Use a graph for reachability or dependence; a state machine for legal order; a constraint table for simultaneous feasibility; a causal diagram for intervention claims; a game for mutually adapting choices; and a simulator for dynamics that resist useful closed form. If you cannot name the operation you will run on the representation, it is decoration.

Modern models build rich internal representations through attention and residual computation, but those representations are optimised to continue the task, not to provide a calibrated truth test. Changing the external form gives the system a new way to check itself. The reader does not need the matrix details to use this rule: if more reasoning repeats the same uncertainty, change the form of the problem.

> **Mechanism: Why external representation changes the operation**
>
> Inside a Transformer, attention and feed-forward components repeatedly write updates into a residual representation. That representation can encode relations, algorithms, and retrieved facts, but the normal interface exposes generated tokens rather than a certified graph, state transition, causal model, or invariant. Asking the same context for more prose keeps the task inside the same underspecified interface.
>
> An external representation changes what can reject an answer. A graph permits reachability and dependency checks. A state machine permits transition coverage. A constraint table permits row-wise elimination. A simulator permits sensitivity analysis. A proof obligation permits formal rejection. The value comes from the new operation, not from the mathematical name.
>
> **Basis.** Transformer architecture grounds the description of attention and residual updates (Vaswani et al. 2017). It does not prove that a particular external representation is correct. The relevant evidence is whether the representation catches seeded faults, predicts observations, or reduces a real decision.

## Move from the reported case to the cause

A reported problem may be one visible member of a larger class. Check the larger class before deciding the size of the repair.

Observing one failure raises at least two hypotheses: an idiosyncratic event $H_L$, or one instance of a shared mechanism $H_S$. A sibling search has value only when its sampling rule produces observations that are more likely under one hypothesis. Five routes sharing the same omitted authorisation helper support $H_S$; five generated verbal analogies do not. The search changes repair scope because a shared cause makes prevention reusable.

Follow the evidence outward. Start with the reported case. Search for genuinely similar cases. If they recur, test whether they share a cause. Only then design prevention around that cause and a detector for future cases. Each step can stop the expansion: no siblings supports a local repair; siblings without a shared cause call for separate repairs; a shared cause can justify one reusable control.

For an authorisation bypass, search for routes that call the same helper, accept the same malformed input, or omit the same check. If several routes share the cause, compare a local patch with a change to the shared mechanism. Add a test that fails when any route escapes.

For a scientific anomaly, search for related measurements, instruments, materials, and competing mechanisms. If the same pattern appears under several conditions, design an experiment that separates the causes rather than writing another explanation.

For a strategy failure, search for other decisions driven by the same incentive or information delay. Prevention may be a new control, an earlier signal, or a reversible decision stage.

Call this a systemic search: do not keep removing individual hazards when a shared source can be removed. The decision is economic, not heroic.

Escalate only while the shared repair is likely to prevent enough loss, often enough, to repay its construction, delay, upkeep, and false alarms. Use rough ranges if exact numbers are unavailable. A shared repair may be justified when the failure is costly, the mechanism appears often, and the new check will be reused. A one-line local fix is better when the event is isolated and the general machinery would create more risk than it removes.

> **Mathematical detail: when systemic prevention pays**
>
> The comparison can be written as

**Build shared prevention when:** `loss avoided + future reuse > build cost + maintenance + delay + false alarms`

> This is not a demand for exact forecasts. Estimate low and high ranges. If the repair loses even under favorable assumptions, stop. If it wins only under uncertain recurrence, first measure recurrence rather than building the full control.

The machine can search siblings and propose causes. Evidence decides whether the class is real. Before searching, state the shared feature, the universe searched, and the finding that would leave the local explanation preferred. Do not let the number of generated siblings substitute for observed recurrence.

## Design the human review before scaling

Before the machine starts, decide what the person will receive. This is a capacity constraint, not a formatting preference. When generation creates material faster than responsible reviewers can inspect it, unread work accumulates throughout the run. Predefining the decision object forces generation to preserve provenance and disagreement within a bounded review cost.

For each surviving claim, keep only:

- the claim in one sentence;
- the strongest supporting evidence;
- the most important contrary evidence;
- the test that could reject it;
- the action it supports;
- the uncertainty that still matters.

For each proposed action, add the owner, permission level, rollback, and monitor. A machine may run searches and tests automatically. It should not publish a consequential notice, change production data, or make an irreversible commitment merely because its report is well structured.

Set a size limit from available review time, not typography. Two pages is a useful default, not a law. Test the compressed object: can the reviewer identify the preferred action, decisive evidence, and reversal condition? If not, compression destroyed decision information. If this requires reading every attachment, the main object is not sufficient.

The chapter is complete when the problem has a checkable form, the possible wider class has been examined, and the final human review is already designed.

> **Field card: Chapter 2 checklist**
>
> Separate facts, assumptions, unknowns, claims, actions, and outcomes.
>
> Choose a graph, state machine, constraint table, causal diagram, simulator, test, or proof because it improves checking.
>
> Search from the reported case toward similar cases and a shared cause.
>
> Escalate only while avoided loss and reuse justify cost, delay, maintenance, and false alarms.
>
> Define the two-page human decision and the limits on action before scaling.

## Chapter 2 evidence and further reading

> **Field card: What the experiments tested**
>
> **Question.** When does a reported software defect justify a systemic repair rather than a local patch?
>
> **Setup.** E07 gave two conditions the same frozen repository and tool access. The baseline received an ordinary whitespace bug. The systemic condition also had to inspect sibling flows and centralize prevention when justified. Both completed their work before the same hidden tests were added. A second case specified a 43-consumer field migration and its rollback plan, but did not execute it.
>
> **Result.** Both E07 repairs passed 23 tests. The local repair left 11 normalisation operations spread across the fixture; the systemic repair left three around a shared mechanism. The behavioural tests could not distinguish them because the existing siblings already handled the tested inputs.
>
> **Finding and limit.** Systemic search exposed a structural difference, but the structure has not been linked to fewer future defects. E07 is **\[measured\] Reproducible internal**; the migration remains **\[designed\] Designed**. A live maintenance outcome could reverse the practical preference.

\[documented\] The model-architecture background is useful mainly because it explains why internal fluency is not an external truth test. The original Transformer and FlashAttention papers describe attention and efficient exact attention; they do not validate this workflow (Vaswani et al. 2017; Dao et al. 2022).

## Case: one authorisation bypass may reveal a wider defect

### Ordinary request — one authorisation bypass may reveal a wider defect

A security report says that one endpoint accepts a request without the required authorisation check. The immediate job appears simple: add the missing check and ship a patch.

The result that matters is larger: no route should permit the same bypass, and a future route should fail a visible check if it repeats the mistake. The harm to avoid is also clear. A broad repair must not change valid access or create a single fragile component.

### Constraint and selector — one authorisation bypass may reveal a wider defect

One engineer cannot reliably inspect every related route, helper, and call path in a large repository. Test that diagnosis before launching a broad scan. Search a sample through the shared helper, route registry, and input shape. The search is useful only if it finds concrete call paths that the endpoint-local inspection missed. The remaining designs need comparison only if they predict different behaviour on an exploit, mutation, or maintenance check.

Before searching, define the checks. An exploit request must succeed before the repair and fail afterward. Every related route found by the search must call an approved authorisation helper. A mutation that removes the helper must make a test fail. These checks decide whether a candidate repair survives.

### Strong minimal baseline — one authorisation bypass may reveal a wider defect

The smallest reasonable response is to reproduce the reported exploit, patch the endpoint, and run the existing tests. This may be the correct answer when the route is unique.

A controlled project fixture showed why passing tests is not enough to claim prevention. Both a local repair and a centralised repair passed all 23 behaviour tests. Static analysis counted 11 scattered normalisation operations in one version and three in the centralised version. No existing test proved that fewer operations would prevent future defects. The baseline therefore remained strong, and the larger claim remained unvalidated.

### Machine-scale system — one authorisation bypass may reveal a wider defect

The following five jobs follow from that diagnosis. Route search expands the observed universe. The table makes missing enforcement mechanically visible. Exploit variants create observations on which unsafe and safe paths differ. Repair alternatives expose the location of the cause. Tests reject alternatives that fail those observations.

First, list routes that use the same handler, helper, input shape, or permission rule. Second, build a table showing the route, required permission, current check, and test coverage. Third, generate exploit variants that change method, parameter position, encoding, and call path. Fourth, compare a local patch with a shared-mechanism repair. Fifth, run tests and static checks on both.

Do not ask several agents to debate the patch. Make branches differ through code paths, exploit inputs, or repair locations. Store the command and result for every checked route.

Run the work in a disposable branch with read-only access to production data. Give search and test jobs a fixed time and cost limit. A useful first pass may inspect hundreds of files, but only routes supported by a concrete call path enter the review table. Generated exploits remain test fixtures; they never run against a live service without separate authorisation.

Escalate to the shared repair only if several routes use the same unsafe mechanism and the expected avoided loss exceeds migration and maintenance cost. Otherwise keep the local patch.

### Compressed human object — one authorisation bypass may reveal a wider defect

The reviewer receives two pages. Page one is a route table: path, shared mechanism, exploit result before and after, and remaining gap. Page two compares the repairs: files changed, tests passed, mutation result, rollback, and new single-point-of-failure risk.

The reviewer decides whether the evidence supports a local repair or a repository rule. They do not read every search result or generated patch.

Review burden is measured directly: number of table rows, minutes spent on exceptions, and number of claims requiring manual code inspection. If compression still leaves dozens of unclear rows, improve the static check or split the repository by owner before asking for approval.

### What was actually checked — one authorisation bypass may reveal a wider defect

The local fixture is **\[measured\] Reproducible internal**. Both conditions passed 23 tests, and the structural count of normalisation operations was 11 versus three. The commands and scorer are stored under [`experiments/E07_SOFTWARE_FAIR/score.py`](experiments/E07_SOFTWARE_FAIR/score.py).

The proposed search across about 200 services is **\[designed\] Designed**. It has not been run on a live repository. The project therefore supports the checking method and the warning about weak tests, not a claim that centralisation prevents production failures.

### What remains unknown — one authorisation bypass may reveal a wider defect

The fixture does not measure maintenance cost, future defect rate, hidden routes, or production recovery. Centralization could simplify enforcement or create a larger failure point. Those outcomes require a real repository, delayed observation, and comparison with the local repair.

The stop rule is practical: if the route table finds no shared mechanism, ship the tested local fix and record why broader machinery was not justified.

## Case: change a live field without breaking 43 consumers

### Ordinary request — change a live field without breaking 43 consumers

A team wants to change the type of a field used by 40 internal services and three external consumers. The request says, “Write the migration plan.” A plan is not the real result. The real result is that old, new, and partially migrated clients continue to read and write consistent values, and that the team can reverse the change within a stated time.

### Constraint and selector — change a live field without breaking 43 consumers

The hard part is not writing SQL. It is finding every dependency and controlling the order of change. This diagnosis is testable: a repository-and-owner sweep should discover consumers absent from the initial plan, and mixed-version tests should expose histories that phase descriptions alone miss. If neither occurs on a representative sample, a large automated inventory may not repay its review cost.

Define the rejection rules first. The migration cannot begin if a consumer is missing from the dependency table, an external format is unknown, a mixed-version test fails, reconciliation produces unequal values, or rollback has not completed within the allowed time in rehearsal.

### Strong minimal baseline — change a live field without breaking 43 consumers

A good baseline plan adds the new field, writes both forms, moves readers, checks data, stops old writes, and removes the old field later. It includes backups and rollback.

This baseline is not weak. It may be enough for a small, well-known system. Its risk in this case is hidden coverage. A plan can list correct phases while missing a frozen parser, an export job, or an external client that interprets the old representation differently.

### Machine-scale system — change a live field without breaking 43 consumers

Use AI and repository tools to build a dependency table because migration safety is a graph property: every consumer reachable from the changed field must cross a compatible transition. Search schema files, queries, serializers, APIs, exports, tests, and deployment configuration. Give every consumer an owner and a status: old-only, dual-capable, new-only, or unknown. An unknown node blocks the transition because its behaviour cannot yet be placed in the state machine.

Generate compatibility tests from pairs of old and new values. Run them against old-only, new-only, and mixed histories. Create reconciliation queries that compare the two stored forms. Produce forward and reverse scripts, but do not allow either to run against production automatically.

Stage the action. First deploy code that can read both forms. Then begin dual writes. Reconcile stored values. Move consumers in small groups. Stop old writes only after the table shows complete coverage. Remove the old field after the rollback window closes.

At every stage, record the signal that allows progress and the signal that forces rollback. The machine may run tests and prepare scripts. A named human approves each production transition.

Keep execution separate from planning. Generated commands first run on a snapshot or staging copy. Capture row counts, checksums, query latency, storage growth, and recovery time. Compare them with limits chosen before rehearsal. A script that produces the right data but exceeds the recovery window is not ready.

### Compressed human object — change a live field without breaking 43 consumers

The reviewer receives a two-page control sheet. The first page summarizes 43 consumers by owner, compatibility state, test result, and rollback coverage. Exceptions appear at the top. The full row-level table remains attached.

The second page shows the stages, entry test, exit test, monitor, maximum time, and rollback command. Four numbers must be visible: consumers discovered, consumers passing mixed-version tests, unreconciled records, and rehearsed recovery time.

Estimate review cost before launch. Owners review only their exception rows. The migration lead reviews the stage gates and aggregate counts. Security or compliance reviewers see only fields affected by their rules. This prevents 43 consumers from becoming 43 full-plan reviews.

### What was actually checked — change a live field without breaking 43 consumers

The 43-consumer system is **\[designed\] Designed**. It comes from the fixed architecture task suite, not a live migration. Seven planning approaches completed all 20 suite tasks, including this scenario, but plan completeness was assessed from the written fields. No production database or client was changed.

The evidence supports the need to state dependencies, tests, rollback, authority, and learning. It does not establish that the proposed order is safe for an unknown system.

### What remains unknown — change a live field without breaking 43 consumers

Unknowns include actual traffic, storage load from dual writes, external upgrade timing, silent truncation, and recovery under failure. These must be measured in the target system.

If fewer than 43 consumers can be identified, do not hide the gap in a risk paragraph. Stop the full migration. Narrow the action to a compatibility layer or one known consumer while acquiring the missing ownership and format information.

# Expand What Can Be Considered

Once you know how bad work will be rejected, you can ask the machine to consider more than one person could. The central question is not how much inference to buy, but which uncertainty the extra computation can reduce. A longer answer, many complete answers, a branching search, and an external calculation alter different parts of search.

## Choose the right kind of extra work

Use a **longer step-by-step attempt** when later steps depend on earlier ones and each step can receive useful feedback. This works well when a failed test points to a line of code or a calculation exposes the first wrong step. It works poorly when the opening assumption is wrong, because the rest of the answer inherits it.

Use **many complete candidates** when several valid solutions may exist and a final test can compare them. Generate several designs, proofs, queries, or patches; run the same check on each; keep the survivors. This helps only when the check is strong enough to reject polished failures.

\[documented\] Use a **branching search** when an early choice changes everything that follows. Force distinct assumptions or approaches near the root, then develop each branch. Modern cache and attention methods make this cheaper, but shared text still creates shared mistakes (Hariri et al. 2026; Dao et al. 2022).

Use **external tools** when the answer requires information or computation that prose cannot supply. Search a database, run code, call a solver, execute a simulator, or inspect a repository. Tool output becomes evidence only when its inputs, method, and limits are recorded.

Diagnose the route with a perturbation. Change an early assumption: if the action changes, branch there. Hold assumptions fixed and change the sample: if viable endpoints vary, use parallel candidates. Replay a chain with tool feedback: if errors become locally identifiable, use a deeper trajectory. Replace a claimed quantity with a measured one: if that resolves the choice, call the tool. Internal reasoning cannot observe external state absent from its context.

Record the choice in one line: type of work, amount, and check. For example: “Four independent literature searches; deduplicate by DOI; reject claims without abstract support.”

> **Mechanism: Token distributions are search distributions**
>
> At generation step $t$, the model supplies $p(x_t\mid x_{<t},c)$, a distribution over the next token given the preceding tokens and context $c$. A temperature or top-p rule reshapes which continuations are sampled. It does not supply a calibrated distribution over semantic truth, project success, or real-world outcomes.
>
> A complete answer is a path through many conditional draws. Early framing choices alter the distribution of everything downstream. This is why a longer trace and several full samples solve different search problems. It is also why five samples can agree for the wrong reason: they may share the same early assumption and evidence.
>
> Search should therefore create variation at a decision-relevant branch, then use an external score. If the score is imperfect, increasing best-of-$N$ can overfit the score: observed proxy quality rises while true quality eventually falls. More test-time compute is an allocation variable, not a monotonic capability switch (Khalaf et al. 2025; Hariri et al. 2026).
>
> **Basis.** The next-token factorization follows from autoregressive sequence modelling (Vaswani et al. 2017). Khalaf and colleagues provide empirical and theoretical evidence for true reward rising and then declining under inference-time proxy optimisation. Hariri and colleagues report that test-time strategies depend on task, model, and budget. These results justify local routing and stopping, not one universal sampler.

> **Decision rule: Choose the topology from the uncertainty**
>
> Use one deeper trajectory for a locally checkable chain. Use parallel complete candidates for multiple valid endpoints with a strong final test. Branch near an uncertain root assumption. Call a tool when the missing state is external. Change the evidence path when samples are correlated. Stop when another branch cannot change the surviving action.

## Create differences that matter

Five agents given the same prompt and documents are not five independent witnesses. Their outputs depend on shared weights, context, retrieval, and often the same judge. Majority vote reduces error only to the extent that errors are not perfectly correlated. Useful diversity therefore changes what a branch can know or how it can fail.

Vary at least one of these:

- the evidence source or search query;
- the representation, such as a graph versus a state machine;
- the causal assumption or model of the world;
- the tool, solver, or test method;
- the starting data or parameter range.

In research, use search queries built around different mechanisms, not different adjectives. In design, ask one branch to minimise cost and another to minimise irreversible risk, then test both against the same constraints. In software, vary the suspected shared helper, call path, or input mutation. In strategy, vary assumptions that could reverse the preferred action.

\[documented\] Tag each result as sharing or not sharing its source, representation, and check with the others. Two claims based on the same three papers count as one evidence path, even if two agents wrote them. This simple record prevents false confidence from repeated samples (Zhu et al. 2025).

Estimate marginal diversity from artifacts, not personas: unique sources, causal assumptions, executable counterexamples, or failures caught by only one route. Stop when these counts flatten and the decision is unchanged. Change the evidence path or improve the check instead.

## Treat prompts as configuration, not magic

A prompt changes the conditional distribution from which the system produces actions and tokens. It can expose a tool, impose decomposition, supply evidence, or constrain output. It cannot insert a missing measurement or make a weak verifier discriminate. Treat prompting as configuration because its causal effect must be separated from changes in tools, context, model, and scorer.

Use a direct instruction for a short task with a clear external score. Break the task into parts when the parts have separate evidence and checks. Allow a longer internal attempt when steps depend on one another, but require the final answer to point to external evidence rather than asking the reader to trust a reasoning trace.

\[documented\] One small project experiment compared direct instructions, explicit decomposition, and chain-of-thought instructions on eight tool-available tasks. Every condition scored eight of eight and produced the same outputs. Token use differed, but accuracy did not. This is a narrow null result: it shows that prompt wording did not matter on that saturated batch. It does not show that prompts never matter. Other studies report strong sensitivity in particular tasks and models (Sadanandan and Behzadan 2026).

Run prompt experiments only when wording is a plausible source of error. Freeze the tasks and scoring first. Compare against a simple instruction. If a tool or better check explains the gain, credit the tool or check.

Stop tuning the prompt when several variants produce the same ranking under the external check. Spend the next effort on new evidence, a better representation, or a stronger test.

## Buy another batch only when it can change the decision

Do not choose “100 candidates” because the number sounds large. The relevant curve is accepted decision value as a function of additional checked search. Early samples may discover new modes; later samples often repeat them while review cost keeps rising. Estimate the marginal change, not the impressive total.

Ask four questions:

- How likely is the next batch to contain a meaningfully different candidate?
- How likely is the check to recognise that candidate?
- What is the value of changing the decision?
- What will computation, delay, review, and a missed error cost?

Continue only when the expected improvement is larger than the total cost. Rough estimates are enough to expose bad choices.

For retrieval, the next batch might be one new query family rather than another hundred results from the same query. For simulation, it might be a narrow sweep around the boundary where the answer changes. For software, it might be mutations designed to defeat the current test. For writing, it might be one source check rather than ten rewrites.

\[documented\] Weak automated judges create a special danger. Searching harder against the same faulty score can find outputs that exploit the score instead of satisfying the real goal (Setlur et al. 2025). Limit the search, add an independent check, or keep several options rather than declaring a winner.

\[documented\] Long tasks also need checkpoints. Agent performance often falls as actions become more numerous and dependent (X. J. Wang et al. 2026). Split the work at points where external state can be checked and recovery remains cheap.

The human receives a short search note: what was varied, how many paths ran, what check ranked them, what changed the decision, and why the search stopped.

## Chapter 3 evidence and further reading

> **Field card: What the experiments tested**
>
> **Question.** Does better prompt wording expand useful search, and does a large evidence workflow add value beyond a competent live-search answer?
>
> **Setup.** E03 ran direct, decomposed, and chain-of-thought instructions on the same eight exact-answer tasks with the same answer schema. E04 compared a live-search baseline with a second condition that received a frozen corpus built through four scientific query families.
>
> **Result.** Every E03 condition scored eight of eight and returned exactly identical final answers. The batch was saturated and could not compare prompting methods. E04 retrieved 164 unique DOI records, including 130 abstracts, and compressed them to 12 priority papers. The baseline cited four valid papers; the corpus condition cited 25 corpus papers and made evidence dependence easier to inspect.
>
> **Finding and limit.** Prompt labels were not the operative mechanism in the saturated batch. The larger research workflow improved recorded coverage and traceability, but no materials expert measured scientific correctness or decision value. E03 and the retrieval counts are **\[measured\] Reproducible internal**; scientific interpretation is **\[assessed\] Assessed internal**.

\[documented\] Hariri and colleagues distinguish useful test-time search regimes; Zhu and colleagues examine correlated agent errors; Sadanandan and Behzadan report prompt sensitivity in a specific medical setting (Hariri et al. 2026; Zhu et al. 2025; Sadanandan and Behzadan 2026). None supports a universal prompting recipe.

> **Field card: Chapter 3 checklist**
>
> Choose longer reasoning, complete candidates, branching search, or external tools according to where uncertainty lies.
>
> Create diversity by changing sources, representations, assumptions, tools, or data—not personas alone.
>
> Use prompts to configure work and tools. Test prompt variants only against frozen tasks and external scoring.
>
> Buy the next batch only when it can change the accepted decision after review and failure costs.

## Case: turn 164 papers into three useful experiments

### Ordinary request — turn 164 papers into three useful experiments

A materials scientist asks why conductivity falls in a solid electrolyte and what to test next. A normal response is a literature summary. The useful result is different: a short list of competing mechanisms and three experiments whose outcomes would separate them.

The human should not have to read every retrieved paper or trust an AI-written synthesis. The machine must expand coverage while keeping each important claim tied to evidence.

### Constraint and selector — turn 164 papers into three useful experiments

The suspected first limit is evidence coverage because relevant work uses different terms for interfacial resistance, dendrites, space charge, mechanics, and measurement methods. Test it by adding mechanism-specific query families and counting new decision-relevant mechanisms, conflicts, and methods rather than papers. The next limit is discrimination only if several mechanisms remain compatible with the observed loss. A useful experiment must then produce different predicted observations across those mechanisms.

Reject a scientific claim if it lacks a source in the frozen corpus, the available abstract does not support it, or its stated scope is broader than the source. Reject an experiment if competing mechanisms predict the same observation. These rules are imperfect, but they are stronger than fluent summary alone.

### Strong minimal baseline — turn 164 papers into three useful experiments

A one-shot baseline already performed well. It cited four valid papers, proposed three experiments, and noted that several measurements were needed. This matters: a large retrieval system must beat a competent short answer in coverage, auditability, or discrimination. Producing a longer review is not enough.

### Machine-scale system — turn 164 papers into three useful experiments

Run searches around different mechanism families because lexical variants of one query create correlated coverage. Distinct causal vocabulary gives each route a chance to reach a different evidence neighborhood. Collect results through a documented scholarly API. Merge duplicate DOI records. Record the query family, title, year, abstract availability, and source link for every item so overlap and dependence remain visible.

The project search produced 164 unique DOI records. Of these, 130 had abstracts and 29 appeared in more than one query family. Those counts describe the frozen corpus; they do not measure recall against the whole field.

Next, build a mechanism table. Each row contains the proposed mechanism, causal path, predicted observation, supporting DOI set, conflicting evidence, important confounder, and a result that would count against it. Title-only records may guide further search but cannot support a claim.

Finally, map competing rows to experiments. Prefer an experiment when its possible outcomes differ across mechanisms. For example, combine impedance measurements with blocking controls, imaging, magnetic resonance, or interphase chemistry only when the result will change which explanation survives.

Budget the run in stages. Stop the first retrieval pass after each query family returns mostly duplicates or off-topic records. Spend machine time on deduplication and source links before synthesis. Spend scientist time only on disputed mechanism rows and experiment feasibility. Record search calls, corpus size, and review minutes so a later run can judge whether another query family was worth its cost.

### Compressed human object — turn 164 papers into three useful experiments

The scientist receives two pages. Page one contains no more than six mechanism rows. Page two contains three experiment cards. Each card states the measurement, controls, predicted result under each mechanism, decision after each result, cost, and required equipment.

A separate 12-paper reading list contains the sources most likely to change the decision. The 164-record table remains available for audit and later searches; it is not the reading assignment.

Each experiment card also names the equipment, approximate duration, sample count assumption, and result that would cause the experiment to be repeated. These are planning fields, not measured costs. A laboratory owner must replace them with local values before action.

### What was actually checked — turn 164 papers into three useful experiments

Retrieval is **\[measured\] Reproducible internal**. The stored corpus contains 164 unique records, 130 abstracts, and 29 multi-query records. All 25 citations in the larger synthesis were found in that corpus, and all four baseline citations were found through Crossref. The commands and outputs are under [`experiments/E04_RESEARCH_SEARCH/`](experiments/E04_RESEARCH_SEARCH/).

The interpretation is **\[assessed\] Assessed internal**. No materials scientist graded the mechanism table or experiment choices. DOI existence proves neither the scientific claim nor the usefulness of an experiment. One generated report also incorrectly said that overlap could not be recomputed, even though membership data existed. That error remains part of the evidence.

### What remains unknown — turn 164 papers into three useful experiments

The corpus may miss relevant terminology, databases, older work, or negative results. Abstracts may omit boundary conditions. The proposed experiments may be impractical or non-discriminating in the actual laboratory.

Stop adding papers when the next search family is unlikely to change the mechanism table. If no proposed experiment distinguishes the remaining explanations, acquire a new measurement method or narrow the scientific question.

# Make Reality Select

AI should propose work. Something causally connected to the claimed property should decide what survives. A compiler is connected to syntax, a test run to covered behaviour, a source passage to attribution, and an intervention to a causal prediction. Model agreement is connected mainly to the model distribution. This chapter shows how to choose the external connection before generating many candidates.

## Write the rejection rule first

For every important output, complete this sentence:

Reject this result if \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.

A code change is rejected if required tests fail or a forbidden path remains. A literature claim is rejected if no primary source supports it. A simulation conclusion is rejected if it changes under plausible assumptions that were hidden from the summary. A migration plan is rejected if rollback has not been rehearsed.

The rule must name an artifact or observation that can be checked. “Reject if it seems weak” is not enough. “Reject if any claim lacks a source passage” is usable.

Write the rule before the machine sees the candidates. Candidate inspection changes the judge: people rationalize attractive answers, and search can exploit visible criteria. If exploration makes the rule indefensible, record the change and evaluate it on fresh cases rather than pretending it was fixed in advance.

The machine may help create tests, find counterexamples, and organise evidence. It should not be the only judge of its own unsupported prose. If no practical rejection rule exists, narrow the claim or obtain new information before scaling.

## Use the strongest check the problem allows

The strength of a check determines which errors can survive at scale. A format checker sees malformed JSON but not a fabricated fact. A test sees behaviour covered by its cases but not an unrepresented requirement. A source check sees whether a passage supports a claim but not whether the source is scientifically correct. An intervention observes causal response in one setting; a delayed field outcome can reveal harms that every earlier check missed.

Scale gives a weak checker more chances to make a consequential mistake. Imagine a checker that wrongly accepts one bad candidate in every hundred. Checking one candidate creates one opportunity for that miss. Checking one hundred creates many opportunities; it does not make the checker more careful. Under a simplified independence assumption, there is roughly a 63-percent chance that at least one bad candidate slips through. Real candidates share errors, so the precise number changes. The operational conclusion does not: repair the checker before multiplying candidates.

> **Mathematical detail: how false acceptance compounds**
>
> Let $q$ be the chance that the checker accepts a bad candidate, and let $N$ be the number checked. If those events were independent, the chance that at least one bad candidate passes would be

$$
1-(1-q)^N.
$$

> For $q=0.01$ and $N=100$, this is about 0.63. Independence is a simplifying assumption, not a fact about model outputs. Correlation can change the number, while repeated exposure to a known weak checker remains dangerous.

Checks have different strength. Use the highest practical level:

- **Format and constraints.** Is the output complete, valid, and within stated limits?
- **Calculation.** Does deterministic code reproduce the number?
- **Tests or proof.** Does the candidate satisfy executable behaviour or formal conditions?
- **Primary evidence.** Does the exact source support the exact claim within scope?
- **Intervention.** Does changing the suspected cause change the result as predicted?
- **Observed outcome.** Did the action work in the real setting over the required time?

Passing a lower level does not imply passing a higher one. Correct JSON can contain a false claim. Passing current tests does not prove that a repair prevents future defects. A simulation can be numerically exact while its assumptions are unrealistic. A plan can look complete without surviving execution.

> **Mechanism: Why the ladder is ordered**
>
> Each level rejects a broader class of failure because it connects the output to a less self-referential object. Syntax constrains form. Calculation constrains arithmetic. Tests and proofs constrain behaviour under stated conditions. Primary evidence constrains factual claims. Intervention constrains causal claims. Observed outcomes constrain whether the action worked in its actual environment.
>
> The levels do not replace one another. A field trial with corrupted measurement is weak. A proof of the wrong specification is exact and useless. The practical rule is to pair levels: validate the instrument or checker at a lower level, then use the strongest feasible level for the claim being made.
>
> **Basis.** The false-accept equation above is the complement rule for at least one accepted failure under an explicit independence simplification. Verification research supports allocating more inference only when the verifier discriminates useful work (Setlur et al. 2025). Neither source estimates the error rate of a reader’s actual checker; mutation testing must do that locally.

> **Decision rule: What changes in practice**
>
> Before scaling, name the failure class that matters and the lowest check that can detect it. Record the strongest level reached and the level still required. If the remaining gap can hide a high-cost failure, narrow the action, add an independent check, or stop. Do not collapse format checking, test passage, and outcome validation into the single word *tested*.

Record both the level reached and the level still needed. This prevents “tested” from quietly becoming “successful.”

\[documented\] Sometimes checking is much cheaper than producing the answer. A solver can verify many candidate solutions; a compiler can reject many invalid programs; a citation lookup can reject unsupported references. This asymmetry makes large search useful (Zeng et al. 2025). When checking is as hard as generation, keep the candidate set small and human authority narrow.

## Measure what the check misses

A check is useful only if you know its blind spots. Normal examples show whether good work passes; they do not show whether the checker detects the failures you fear. Deliberate faults supply a known denominator: of the seeded failures, how many were rejected, and which classes escaped?

Remove a required authorisation call and confirm that the software test fails. Delete a source link and confirm that the evidence check rejects the claim. Move a game payoff across a regime boundary and confirm that the classification changes. Insert an unsupported sentence into a notice and confirm that publication is blocked.

These are mutation tests. Seed faults at the boundary of the claimed guarantee, not only easy syntax errors. A citation checker needs a real paper that fails to support the sentence, not only a missing URL. A migration checker needs stale-client behaviour, not only a malformed row. If the system accepts them, its claimed scope is false; improve the check or narrow the claim before generating more work.

Also record coverage. A search that found 164 papers does not know how many relevant papers it missed. A test suite that covers all known routes may still miss a route created through reflection or external configuration. State the known universe, the part checked, and the paths that share the same source or judge.

\[documented\] Do not count repeated judgments from the same model and context as independent evidence. A shared judge can repeat one blind spot across every candidate (Zhu et al. 2025; Setlur et al. 2025).

The human receives a small checking report: failures inserted, failures caught, important coverage gaps, and the largest remaining risk.

## Build consequential writing from checked claims

Public notices, medical guidance, legal language, and executive recommendations can cause harm even when the prose sounds cautious. Ordinary generation creates sentences first and invites evidence afterward, encouraging post-hoc rationalization. Claim-first construction makes evidence and scope upstream dependencies of prose.

For each sentence:

- identify the factual claim;
- link it to an approved source or rule;
- record the limits of that support;
- reject or bracket the sentence if support is missing;
- generate prose only from the surviving claims.

Do not rescue an unsupported claim by adding “may,” “generally,” or “we believe.” Softer grammar does not create evidence.

\[documented\] Research on self-correction is mixed. Results depend on the model, task, prompt, and decoding setup (Tsui 2025; Ateia and Kruschwitz 2025; Liu et al. 2024). For consequential writing, feedback should point to a missing source, a violated rule, or a failed prediction. Generic requests to “be more careful” are too weak.

## Narrow the answer or refuse when checking stays weak

Abstention is useful when uncertainty relevant to harm remains high and no affordable observation can reduce it. It preserves the distinction between “not established” and “false.” Forced completion erases that distinction and converts missing evidence into invented specificity.

When the available check is weak and the cost of error is high, return one of four things:

- a smaller claim that can be supported;
- a request for the missing information;
- several reversible options without a forced winner;
- a clear refusal to publish or act.

State what would allow the work to continue. “Cannot determine” is less useful than “cannot determine until the external serialisation format and rollback time are measured.”

## Chapter 4 evidence and further reading

> **Field card: What the experiments tested**
>
> **Question.** What does computation add when an analytic check exists, and can structured caution prevent unsupported consequential writing?
>
> **Setup.** E05 classified 100,000 authored payoff worlds with closed-form sign conditions, then numerically integrated 500 deterministic worlds from five starting states. E08 compared a minimal baseline and the structured method on a sparse-fact applicant notice and on one isolated typo.
>
> **Result.** The analytic rule classified every sampled game, making most brute-force integration unnecessary. Six of 2,500 finite-horizon trajectories remained more than 0.03 from their analytic targets near slow boundaries. In E08, both notice responses invented facts. Both typo responses made the single correction and stopped.
>
> **Finding and limit.** Derive before simulating; use numerical work for boundaries and finite horizons. Cautious wording does not repair missing evidence. E05 is **\[measured\] Reproducible internal**; E08 is **\[assessed\] Assessed internal**. Neither experiment measured a real intervention or publication outcome.

\[documented\] Setlur and colleagues study verifier-based inference allocation. Zeng and colleagues study asymmetric verification, while work on self-correction and feedback shows why feedback quality matters (Setlur et al. 2025; Zeng et al. 2025; Tsui 2025; Ateia and Kruschwitz 2025; Liu et al. 2024). These sources ground components; they do not validate the complete field card.

## Case: calculate a hundred thousand games without inventing odds

### Ordinary request — calculate a hundred thousand games without inventing odds

A strategist asks whether cooperation will survive when rewards and penalties are uncertain. One person can reason through a few examples. A machine can calculate many more. The danger is reporting the fraction of simulated examples as if it were the probability of the real world.

The useful result is a map: which payoff relationships lead to cooperation, defection, coexistence, or dependence on the starting population? The map should also say which payoff must be measured first.

### Constraint and selector — calculate a hundred thousand games without inventing odds

The limit is not calculation alone. It is model definition. A simulation will faithfully repeat whatever distribution, update rule, population size, and time horizon the author supplies.

Write the governing comparison before sampling. In the two-strategy game used here, whether a rare cooperator can invade depends on the difference $S-P$. Whether cooperation resists invasion depends on $R-T$. An analytic classification based on those signs checks the simulation. If the rules and rejecting conditions cannot be written first, do not run a large sweep.

### Strong minimal baseline — calculate a hundred thousand games without inventing odds

The one-shot baseline was strong. It identified $S-P$ and $R-T$, refused to treat payoff intervals as probabilities, recommended conditional and worst-case analysis, and noted that population size, update rule, initial share, and time horizon matter.

The machine-scale run therefore had a narrow job: calculate the conditional map, check numerical behaviour against the analytic result, and expose slow convergence. It was not asked to replace the baseline’s judgment.

### Machine-scale system — calculate a hundred thousand games without inventing odds

The project drew 100,000 payoff sets from an explicitly authored uniform and independent distribution. It classified each set into four regimes from the two governing differences. It then selected 500 worlds and simulated five starting shares in each, producing 2,500 trajectories.

For every world, store the payoffs, analytic regime, starting share, finite-horizon result, and distance from the analytic target. Keep disagreements rather than averaging them away. Six trajectories remained more than 0.03 from the analytic target at the chosen horizon. They occurred near boundaries where change was slow.

Fix the random seed and save the code, assumptions, and output before reading the regime fractions. Rerun a small sample through an independent numerical method. Test exact boundary cases separately because random sampling rarely lands on them. These steps make the calculation reproducible and reduce the chance that a convenient result survives through unnoticed implementation error.

Use the map to choose information. If the decision changes when $S-P$ crosses zero, measure the payoff to a cooperator surrounded by defectors. If it changes when $R-T$ crosses zero, measure resistance to invasion. Do not spend more computation on the same assumed ranges when a real measurement is the limit.

### Compressed human object — calculate a hundred thousand games without inventing odds

The strategist receives one page. It shows the two controlling differences, the four conditional regimes, the assumed distribution, and the finite-horizon warning. It lists the six mismatches and explains why they were retained.

The four simulated fractions may appear only with the label “fraction under the authored draw.” They must not be described as real-world odds. The page ends with the next measurement and the decision it could change.

Machine cost is the simulation run and verification sample. Human review is limited to the model assumptions, boundary behaviour, retained mismatches, and proposed measurement. Reviewing thousands of trajectories would defeat the purpose of the calculation.

### What was actually checked — calculate a hundred thousand games without inventing odds

The computation is **\[measured\] Reproducible internal**. The stored output records 100,000 worlds, 500 numerically checked worlds, five starts per world, and six finite-horizon mismatches above 0.03. The code and output are under [`experiments/E05_EVOLUTIONARY_SIM/`](experiments/E05_EVOLUTIONARY_SIM/).

The game form is **\[documented\] Component grounded**. The intervention is **\[designed\] Designed**. No real population, payoff, or behavioural outcome was measured.

### What remains unknown — calculate a hundred thousand games without inventing odds

The uniform independent draw is not an empirical model. Real payoffs may be correlated, strategic actors may learn, and finite populations may behave differently. The update rule and horizon can change the result.

Stop at the conditional map until measured payoffs arrive. More simulated worlds would add decimal places, not evidence.

## Case: when the right answer is less work

### Ordinary request — when the right answer is less work

This case compares two small writing tasks.

The first asks for a public notice based on a short set of facts. Publishing an unsupported promise could affect applicants. The second asks for one spelling correction in a private sentence. The first has a weak factual check and meaningful harm. The second has a clear check and negligible wider scope.

### Constraint and selector — when the right answer is less work

For the notice, the limit is missing evidence. The supplied facts do not support every sentence a polished notice might normally contain. Reject any sentence whose factual content cannot be traced to the supplied record. If necessary information is absent, leave a visible bracket or ask for it.

For the spelling correction, the check is direct: the misspelled word is corrected, meaning is unchanged, and no other text moves. Search for a wider class only if the document shows repeated errors or a broken generation process.

### Strong minimal baseline — when the right answer is less work

The minimal notice response should preserve only supported statements and clearly mark gaps. The minimal editing response should return one corrected sentence and stop.

These baselines are deliberately strong. A larger system must not add process merely to demonstrate sophistication.

### Machine-scale system — when the right answer is less work

For the notice, first split the source into individual facts. Give each an identifier. Draft sentences only from those records. For each sentence, list the supporting identifiers. Reject a sentence if it adds a deadline, right, process, promise, or interpretation that the records do not contain.

If several notices recur, AI can maintain the fact table, compare versions, and flag unsupported additions. It still cannot authorise a consequential claim without an approved source.

Use two passes to break the causal path from plausible continuation to published claim. The first pass extracts source facts without drafting. A person or deterministic rule approves the fact table. The second pass may produce sentences only from approved rows. A final comparison checks that every factual phrase has a row. This costs more than direct drafting, so reserve it for repeated or consequential notices.

For the spelling task, do not create a fact table, agent team, taxonomy, or monitoring process. Apply the edit, compare before and after, and return the sentence. The wider search stops because there is no evidence of siblings, recurrence, or meaningful avoided loss.

### Compressed human object — when the right answer is less work

The notice reviewer receives the proposed text followed by a small table: sentence, source fact, unresolved gap, and approval status. Unsupported material remains bracketed. The reviewer sees no brainstorming transcript.

The spelling reviewer receives one sentence. The difference should be visible without explanation.

The contrast makes review cost explicit. The notice may justify a claim table and accountable approval. The spelling correction justifies a before-and-after comparison. Applying the notice process to the typo would increase cost without reducing meaningful risk.

### What was actually checked — when the right answer is less work

The project ran one paired assessment with a simple baseline and the field-card method. On the notice task, both responses invented unsupported content. They added ideas such as submitted materials, application materials, decision criteria, or applicant rights that were not in the prompt. Cautious tone did not solve the evidence gap.

On the spelling task, both responses made the single correction and stopped. Neither invented a wider project. These findings are **\[assessed\] Assessed internal** because a researcher judged the prose in one run. The prompts and results are under [`experiments/E08_WEAK_STOP/`](experiments/E08_WEAK_STOP/).

The result is adverse and useful. The operating card did not outperform the baseline. It showed that instructions alone cannot make unsupported facts safe, while both methods handled an obvious stop condition.

### What remains unknown — when the right answer is less work

One run cannot estimate fabrication rates or compare models. A stronger claim-level generation system might perform better, but it was not tested here. No legal or public outcome was observed.

The practical rule survives: when evidence is missing, scale evidence handling or return a visible bracket. When the task is one verified edit, make the edit and stop immediately.

# Convert Scale into Action

A large search is useful only when it leads to a decision that a person can understand and an action that can be controlled. This chapter turns machine-scale work into a small review package, a staged commitment, and a monitored result.

## Reduce the work to a decision

Do not give the decision-maker every generated answer. Attention is the final scarce channel: irrelevant detail increases search time and can bury the disagreement that changes the choice. For each surviving option, provide:

- the proposed action;
- the evidence for it and the strongest objection;
- the assumption most likely to change the choice;
- the expected benefit and important harm;
- the next check, rollback, and owner.

Put competing options side by side. Keep the main package to two pages. Link the full search, calculations, and rejected candidates as supporting material. Compression is successful when the reader can reconstruct why one option survives and what would reverse it without rereading the whole run. This is a sufficiency test: preserve the variables on which action is conditional, not every intermediate token.

If an omitted disagreement could reverse the choice, restore it. If a detail cannot change the choice or its safety, leave it in the audit record.

## Learn before making an irreversible commitment

When uncertainty is important, keep several options alive and buy information cheaply. Committing destroys option value when reversal is costly. A reversible probe preserves the ability to choose after observing new evidence.

List the irreversible parts of each option. Then design the smallest reversible step that could change the decision: a prototype, pilot, shadow deployment, limited experiment, or contract with an exit clause. State what result will cause you to continue, change course, or stop.

Prefer the test with the greatest expected decision value, not the most data. It needs different expected results under actions or hypotheses still in contention, and those results must be capable of changing the choice. A rollback rehearsal can dominate another design document because measured recovery time changes acceptable exposure. One blocking-control experiment can dominate fifty papers because it separates mechanisms the papers leave compatible.

Stop experimenting when the likely value of new information is lower than its delay, cost, and exposure to failure.

## Control the action after it starts

Planning ends when the system touches the world. From that point, use feedback.

Define the target, the measurements, the allowed change, the observation interval, and the shutdown condition. For a migration, monitor inconsistent reads, error rate, and rollback time. For a policy, monitor the outcome and the harm guard. For a scientific process, compare observations with the predicted ranges.

Do not use a proxy merely because it is easy to collect. A rising click rate may not mean that users understood the notice. A passing deployment check may not mean that old clients remain safe.

The machine can watch measurements and propose corrections. A person retains approval for changes whose consequences are hard to reverse or whose checks are weak.

> **Mechanism: Why plans become control systems**
>
> Once an action changes the world, the next state depends on the current state, the action, outside disturbance, and feedback. A simple model is

$$
s_{t+1}=f(s_t,a_t,w_t),   y_t=h(s_t)+v_t,
$$

> where $s_t$ is the hidden state, $a_t$ the action, $w_t$ a disturbance, and $y_t$ a noisy measurement. A plan that ignores this loop assumes the world will follow the initial forecast without reacting.
>
> Nonlinear systems make that assumption dangerous. Near thresholds, a small parameter or timing change can move the system into another basin of behaviour. Strategic actors also adapt: a policy changes incentives, which changes behaviour, which changes the policy’s effect. Monitoring is therefore part of the action, not an administrative task after it.
>
> **Basis.** The state and observation equations are the standard form of a partially observed feedback system. The nonlinear and strategic warnings are conditional: use them when feedback, thresholds, or adapting actors exist. E05 supplies an internal example where payoff signs and starting state select different evolutionary regimes; it does not validate a real policy.

> **Decision rule: Impact of ignoring feedback**
>
> Open-loop execution continues after its assumptions fail. A migration expands while divergence grows; a review queue accumulates faster than experts can serve it; a reward changes user behaviour and invalidates the original model. Stage commitments, observe leading and harm indicators, and define the state transition that triggers pause or rollback.

## Set permissions and review limits

Create three action levels because authority should scale with ease of recovery, check strength, and harm rather than model confidence:

- **Automatic:** reversible work with a strong check and a tested recovery path.
- **Approval required:** consequential work with good evidence but meaningful cost or harm.
- **Prohibited:** irreversible or high-harm work without an adequate check.

Set limits on volume, cost, time, and retries. A system that fails the same check twice should not keep rewriting indefinitely. It should return the failed artifact and ask for a new source, representation, or decision.

Measure accepted value per hour of responsible human attention. Generated tokens, agent count, and task count are operating costs, not success measures.

## Treat tool access as a security boundary

Text from a repository, web page, ticket, document, or tool response is untrusted input. A tool-using model consumes instructions and data through the same token interface; malicious data can therefore be interpreted as control text. This machinery-level fact makes prompt injection a security boundary, not a prose-quality defect. Do not let retrieved text change permissions, reveal credentials, disable a check, or redefine the goal.

Run machine work with the least privilege it needs. Separate read access from write access. Keep secrets out of prompts and logs. Use a sandbox for unfamiliar code, restrict network destinations, pin important dependencies, and require an explicit human approval before publication, data deletion, production changes, money movement, or messages to people.

The check and recovery path must use a different control boundary from the action when possible. An agent that can edit a test, change its own approval rule, and deploy the result does not have a strong check. Preserve an append-only action log containing the requested operation, evidence, approving identity, tool calls, result, and rollback status.

Automatic work is appropriate only when both the task and its inputs fit the allowed boundary. If untrusted content asks for wider authority or the requested action cannot be isolated, stop and escalate to a person.

## Manage a review queue without hiding risk

Large runs often fail at the final queue. Hundreds of items wait for one expert, urgent work mixes with harmless work, and the reviewer begins to approve by appearance.

Split the queue by consequence and check quality. This changes service time: routine items with measured automatic rejection need little expert attention, while novel items reserve slow review. Put strong-check, easy-rollback items in a fast lane; novel or weakly checked claims in a deliberate lane; and block high-harm items lacking required evidence. Never route by model confidence alone because token probability is not a calibrated estimate of downstream harm or factual correctness.

For each lane, define the maximum queue size and waiting time. When the limit is reached, stop generation. A full review queue is evidence that review, not production, is the current limit.

Sample accepted and rejected items. False acceptance shows that the check is too weak. Frequent false rejection shows that the check wastes good work. Adjust the check before adding more reviewers or agents.

Keep an exception log. An exception should state the failed rule, the evidence used to override it, the responsible person, and the expiry date. Repeated exceptions often reveal a bad rule or an unrepresented class of work.

Queueing theory explains why adding generation can make delivery collapse. Let candidates arrive for review at rate $\lambda$ and let responsible reviewers complete work at rate $\mu$. When $\lambda$ approaches $\mu$, waiting time rises sharply; when $\lambda\geq\mu$, the queue is unstable. More agents increase $\lambda$. They do not increase $\mu$ unless checking and compression remove reviewer work. This is why a queue limit is a correctness control as well as a scheduling rule.

This queueing argument applies only when work arrives repeatedly and reviewers are the constrained service. It does not justify bureaucracy for a one-off task. Measure arrival rate, completion rate, rework, and false acceptance before adding lanes.

## A practical action plan

Before launch, complete this table in ordinary language:

| Item       | Required answer                              |
|------------|----------------------------------------------|
| Decision   | What choice is being made now?               |
| Evidence   | What checked facts support it?               |
| First step | What is the smallest reversible action?      |
| Success    | What measurement permits continuation?       |
| Failure    | What measurement triggers pause or rollback? |
| Authority  | Who approves, acts, and receives an alert?   |
| Recovery   | How is the previous safe state restored?     |
| Learning   | What prediction and outcome will be saved?   |

Walk through a migration. The decision is whether to begin dual writes. Evidence includes complete consumer ownership and passing compatibility tests. The first step is a small internal cohort. Success means equal old and new values with acceptable latency. Failure means divergence or excess load. The migration lead approves the transition; automation performs the reversible command; monitoring can pause further cohorts. Recovery disables dual writes and restores the last reconciled state.

Walk through a research programme. The decision is which experiment to run first. Evidence is the mechanism table and predicted observations. The first step is a low-cost blocking control. Success and failure are not “good” and “bad” experimental outcomes; both should eliminate or weaken different explanations. The scientist approves the experiment, and the result updates the evidence table.

If the table cannot name failure, authority, or recovery, the action is not ready. Return to Chapter 4 for a better check or narrow the first step.

> **Field card: Chapter 5 checklist**
>
> Present options in a two-page decision package.
>
> Use small reversible tests before large commitments.
>
> After action starts, monitor the real target and the harm guard.
>
> Set automatic, approval-required, and prohibited action levels.
>
> Isolate untrusted inputs and grant the least tool authority required.
>
> Stop when another test or retry is unlikely to change the decision.

## Chapter 5 evidence and further reading

> **Field card: What the experiment tested**
>
> **Question.** Can a common output contract force different planning approaches to produce bounded, reviewable action plans?
>
> **Setup.** E10 applied seven approaches to 20 frozen tasks. Every record had to name the constraint, first action, machine-scale work, predeclared selector, bounded human object, stop or authority rule, and durable learning. A deterministic scorer checked presence and schema; the author assessed operational differences.
>
> **Result.** All seven conditions produced complete records for all 20 tasks. Control-oriented plans emphasized measurements and thresholds; options-oriented plans emphasized reversible tests; evidence-oriented plans emphasized provenance. The common schema caused strong convergence and the hybrid did not consistently beat the general lifecycle.
>
> **Finding and limit.** A stable action contract may matter more than a branded workflow. This chapter is still **\[designed\] Designed**: no condition executed a live organizational decision, measured review time, or observed delayed harm. Test authority lanes and accepted value per review-hour locally before automating them.

\[documented\] For long-horizon execution limits, see Wang and colleagues; for feedback-driven correction, see Liu and colleagues (X. J. Wang et al. 2026; Liu et al. 2024). Use those papers to design checks, not to infer that autonomous action is safe.

# Build a System That Improves Itself

A folder full of old answers is not learning. Learning requires a policy change caused by outcome evidence: a different search route, prior, checker, authority level, or stopping threshold on the next comparable job. Storage without such an update is archiving.

## Save decisions, not transcripts

After each job, keep a one-page record whose fields make a later causal comparison possible:

- the result sought and the representation used;
- the evidence and checks that mattered;
- the candidates rejected and why;
- the action taken and its rollback;
- the predicted result and the observed result;
- the failure, delay, and review cost;
- what should change next time.

Store links and hashes for supporting artifacts. Do not preserve long generated discussions unless they can change a future decision. A transcript records what was said; a decision record preserves treatment, prediction, selector, and outcome. Only the latter lets a later reviewer ask whether the method changed the result under comparable conditions.

## Turn escaped failures into prevention

When a failure reaches a reviewer, customer, experiment, or production system, do more than patch the visible case.

First reproduce the failure. Then find similar cases and the shared cause. Add a test that fails on the old behaviour. Put the preventive rule in one owned location when possible. Add monitoring for the next near miss. Finally, record the false alarms and maintenance cost created by the new control.

Do not turn every mistake into a global rule. Use the same economic test as Chapter 2: prevention is worthwhile when expected loss avoided and future reuse exceed build, maintenance, delay, and false alarms.

The durable result is the new test, control, owner, and monitor—not a polished postmortem.

## Improve routing from local evidence

Use past jobs to answer three questions. Which kind of extra work found the winning candidate? Which check caught the important failures? Which tasks required human approval?

Compare methods only within similar task classes. Twenty planning tasks cannot establish the best workflow for all expert work. A method that helps repository search may add useless ceremony to a spelling correction. A literature method may fail when evidence cannot be observed.

Track practical measures: time to the first useful check, review time, false acceptance, recovery time, and observed value. Use these measures to change the next allocation. Do not learn from generated volume alone.

Widen machine authority only after checks show better coverage and fewer escapes. Tighten it when failures rise or the environment changes.

## Detect new kinds of failure carefully

Known tests catch failures inside their encoded classes. Their residual errors are therefore selected: what escapes is disproportionately likely to lie outside the current representation. Unknown-class search examines that residual instead of pretending ordinary coverage certifies completeness.

Use AI to propose groups of unexplained failures, unusual overrides, evidence conflicts, and monitor alerts. Clustering supplies hypotheses, not natural kinds: embedding proximity may reflect wording rather than cause. Ask for the smallest shared feature, then seek counterexamples and an intervention. A cluster becomes operationally useful only when its members share a cause, a discriminator, or the same preventive action.

Do not create a rule for every statistical cluster. Some groups are accidents of wording or data collection. Require an owner, a reproducible example, a useful check, and an estimate of false alarms before adding detection to normal work.

Unknown-class search is justified when escaped failures are costly and the same discovery method can run repeatedly. It is not justified for a one-time low-risk task.

## Run small improvement experiments

Change one part of the system at a time when possible so an observed difference can be attributed to that change rather than to a stronger model, larger context, better tools, or friendlier tasks. Compare a new search strategy, check, summary format, or review lane against the current simple method on frozen tasks. Keep tools, evidence access, and scoring fair; if they cannot be equal, report a package comparison rather than a component result.

Choose measures before the comparison. Useful measures include accepted correctness, time to a decision-changing fact, expert review minutes, false acceptance, recovery time, and downstream outcome. Generated volume is not a benefit by itself.

Retain null and adverse results. In this project, three prompt styles tied on a small batch. A larger workflow did not beat a strong baseline on every case. Both methods invented facts in a weak-evidence notice. These results prevent the system from learning that more machinery is always better.

> **Mechanism: Learning requires a changing posterior—not a larger archive**
>
> A record improves future decisions only when new outcomes alter a belief, routing rule, or control threshold. In Bayesian terms, the system should update competing hypotheses through

$$
P(H_i\mid D)\propto P(D\mid H_i)P(H_i).
$$

> An outcome that all hypotheses predicted has little discriminating value. A result that one hypothesis considered unlikely can change the ranking. This is why records need the prediction made before action, not only the explanation written afterward.
>
> Repeated work also faces distribution shift. A rule learned from one model, repository, market, or reviewer may fail after the environment changes. Track outcome distributions and review escapes over time. A change-point is a reason to revalidate the routing rule, not automatically to retrain or add more memory.
>
> **Basis.** Bayes’ rule supplies the stated update exactly under the chosen hypothesis model. It does not make the hypotheses complete or the likelihoods correct. The operational requirement is therefore to store prior predictions and seek observations that differ across hypotheses. Change-point detection is relevant only for repeated measurements over time.

Do not generalize from one domain. Software offers fast tests that law, strategy, and science may not. A routing rule learned from code changes should remain local until it survives work with different evidence and harm.

Review the improvement policy on a fixed schedule. Retire checks that create persistent false alarms, update evidence sources that have changed, and narrow automation when the environment no longer matches the original tests.

The human receives a short change proposal: old rule, new rule, comparison tasks, measured difference, largest new risk, and rollback. The proposal becomes policy only after approval.

## Run the complete loop

For every new problem:

- name the real result and harm to avoid;
- find the work one person cannot perform well enough;
- define how a bad result will be rejected;
- choose a checkable representation;
- scale the right search, computation, generation, test, or monitoring work;
- reduce the survivors to a small human decision;
- act within permissions and rollback limits;
- compare the observed result with the prediction;
- save the decision record and improve the next run.

Stop the loop whenever the next pass costs more than the likely improvement. The isolated typo remains one edit. The weakly supported notice remains bracketed. The authored game remains a conditional map until measured payoffs arrive.

The project has not yet shown that this loop improves real expert productivity. That requires human trials on unseen work and measured downstream outcomes. The guide provides an implementable method and local evidence for its parts, not a universal performance guarantee.

> **Field card: Final operating card**
>
> What real result matters? What harm must not occur?
>
> What work is beyond one person’s practical capacity?
>
> What evidence or test can reject a bad result?
>
> What large, repeatable job should the machine perform?
>
> What is the smallest responsible human decision?
>
> What may happen automatically, and what requires approval?
>
> What outcome will be measured, and what will change next time?

## Chapter 6 evidence and further reading

> **Field card: What the experiment record changed**
>
> **Question.** Did retaining failed, null, and adverse runs change the method, or merely add disclosure?
>
> **Setup.** The project fixed ten experiment slots. E01 stopped because research had not preceded experimentation. E06 failed because the harness passed empty prompts. E03 saturated. E08 found unsupported claims in both conditions. E02, E09, and E10 did not produce a universal workflow winner.
>
> **Result.** The failed runs kept their numbers. Their artifacts remain in the repository. Together they forced three design changes: use one operating contract instead of one universal architecture, treat strong baselines as real competitors, and narrow the promise from demonstrated productivity to disciplined checked expansion.
>
> **Finding and limit.** A durable record can prevent selective memory and flattering conclusions. This is **\[assessed\] Assessed internal**; the project did not compare teams with and without such a record over time, so it has not measured compounding improvement.

\[documented\] Appendix A uses the same decision-record principle this chapter recommends: question, frozen rule, conditions, scorer, full result, deviations, errors, reproduction path, and unknowns. TrialMind provides a related example of structured evidence workflows, while the agent-diversity literature helps explain why stored disagreement needs dependency information (Z. Wang et al. 2024; Zhu et al. 2025).

# Experiment Record

This appendix makes every experiment slot visible. It is not a second argument for the method. It records what was asked, what was frozen, what happened, and what remains unknown. The repository paths are part of the record: prompts and summary tables alone are not enough to reproduce a result.

All runs were performed on August 31, 2026. Model-assisted conditions used the Codex CLI with the locally available `gpt-5.6-luna` configuration. The repository does not preserve a provider release manifest, temperature, or sampling controls, so those details are unknown and the model results should not be treated as stable benchmarks. Token counts are reported only where the raw event stream contains them. Dollar cost and human review time were not recorded. No experiment measured long-term expert productivity.

The evidence labels are defined in the front matter. “Frozen before execution” means the local preregistration says so; it is not a third-party timestamp or independent registry. Raw event streams are in each experiment’s `output/` directory. Commands below assume the repository root.

## E01: aborted architecture search

**Question and rule.** Could six proposed architectures produce distinct executable plans on three tasks? A zero on external selection or bounded review would disqualify an architecture. One combined call was planned to prevent selective reruns.

**What happened.** The run was stopped after thread creation and before model output because the hypotheses had not first been derived from research. This is an **\[assessed\] Assessed internal** process failure, not an architecture result. The run has no scorer output, ceiling check, or checker mutation test. The aborted transport events remain at [`experiments/E01_ARCHITECTURE/output/events.jsonl`](experiments/E01_ARCHITECTURE/output/events.jsonl).

**Unknowns.** E01 says nothing about which architecture works. It consumed its experiment number because removing it would hide a failed sequence. Read [`experiments/E01_ARCHITECTURE/preregistration.md`](experiments/E01_ARCHITECTURE/preregistration.md), `prompt.md`, and `tasks.md`.

## E02: research-derived architecture probe

**Question and rule.** Would a selector-first hybrid produce more task-specific first actions and stronger selector-before-scale behaviour than a general lifecycle? Twenty-one plans were generated: seven architectures across three tasks. Plans were to be scored from zero to four on six fields, with generic copied operations penalized.

**Result.** All 21 plans were produced. The hybrid ranked first under the author’s assessment, with task-local advantages for an evidence compiler and real-options approach. The result is **\[assessed\] Assessed internal**. The hybrid had a longer description; one model generated and judged the plans; tasks were authored during architecture development; no task was executed. These confounds prevent selection of a winner.

**Reproduction and unknowns.** The raw event stream is [`experiments/E02_ARCHITECTURE/output/events.jsonl`](experiments/E02_ARCHITECTURE/output/events.jsonl); the recorded judgment is `assessment.md`. No independent scorer, blind rater, mutation test, runtime, or cost record exists. The experiment only motivated later conditional routing.

## E03: prompt-routing ceiling effect

**Question and rule.** Direct instruction, explicit decomposition, and chain-of-thought instruction were compared on the same eight exact-answer tasks. Exact match and valid JSON were primary; token counts were secondary. Two answer-key errors were corrected before model calls.

**Result.** All three conditions scored eight of eight and their final outputs were exactly identical. Direct, decomposition, and chain-of-thought runs recorded 465, 592, and 386 output tokens respectively, with 333, 354, and 202 reasoning tokens. Run:

**\[executed\] Retained reproduction command**

``` bash
python experiments/E03_PROMPT_ROUTING/score.py
```

This is **\[measured\] Reproducible internal** for the frozen batch. It is a ceiling effect, not evidence that prompting methods are equivalent. Every condition used or attempted external computation, which further confounds the prompt labels. No floor batch, repeated sampling, checker mutation, runtime, dollar cost, or human-time record exists. Full inputs, answers, raw events, and outputs are in [`experiments/E03_PROMPT_ROUTING/`](experiments/E03_PROMPT_ROUTING/).

## E04: scientific retrieval and synthesis

**Question and rule.** A one-shot live-search baseline was compared with a workflow that received a frozen corpus retrieved through four query families. The task was to explain conductivity loss in solid-electrolyte battery systems and propose three discriminating experiments. Claims without source support, provenance, or distinguishing predictions would fail.

**Result.** Retrieval produced 164 unique DOI-bearing records; 130 contained abstracts and 29 appeared through more than one query family. The baseline cited four Crossref-resolvable papers and proposed three experiments in 1,259 words. The corpus condition cited 25 corpus papers, supplied three experiment cards, and compressed review to 12 papers in 2,151 words. One generated report wrongly said overlap could not be recomputed. Two Crossref checks were rate-limited, while their DOI records remained in the frozen OpenAlex corpus.

**Reproduction.** Run:

**\[executed\] Retained reproduction commands**

``` bash
python experiments/E04_RESEARCH_SEARCH/retrieve.py
python experiments/E04_RESEARCH_SEARCH/score.py
python experiments/E04_RESEARCH_SEARCH/verify_dois.py
```

The retrieval and provenance counts are **\[measured\] Reproducible internal**; scientific interpretation is **\[assessed\] Assessed internal**. The DOI parser and verifier were corrected after output and before interpretation; both changes are disclosed in `preregistration.md`. No materials expert, blinded comparison, recall gold standard, experiment execution, review-time measurement, or outcome measure exists. The measured gain is coverage and traceability, not established scientific value.

## E05: evolutionary-game regime map

**Question and rule.** The experiment asked whether cooperation survives across stipulated payoff ranges in a two-strategy replicator model. An analytic sign test classified regimes. A seeded independent uniform draw supplied 100,000 authored worlds; 500 deterministic worlds were numerically integrated from five starting states. Treating sampled fractions as empirical probabilities was a declared failure.

**Result.** The baseline already identified the controlling differences, $R-T$ and $S-P$, and refused invented probabilities. The sweep returned 56.284 percent defection dominance, 6.247 percent cooperation dominance, 18.732 percent coordination, and 18.737 percent coexistence under the authored draw. Six of 2,500 finite-horizon trajectories remained more than 0.03 from their analytic targets near slow boundaries.

**Reproduction and interpretation.** Run:

**\[executed\] Retained reproduction command**

``` bash
python experiments/E05_EVOLUTIONARY_SIM/simulate.py
```

The computation is **\[measured\] Reproducible internal**. The analytic classifier made a full brute-force simulation unnecessary; the useful numerical work was the boundary and finite-horizon check. The payoff distribution was not calibrated to reality, no intervention occurred, and no checker mutations were run. The code, baseline, and JSON output are in [`experiments/E05_EVOLUTIONARY_SIM/`](experiments/E05_EVOLUTIONARY_SIM/).

## E06: failed software harness

**Question and rule.** A local repair and systemic repair were to receive equal repository and tool access on a frozen tier-normalisation fixture. Hidden tests would be added only after both calls. No replacement fixture could be chosen after seeing results.

**What happened.** Relative prompt paths resolved from the wrong directory. Both calls received empty instructions and returned “How can I help?” No treatment occurred. This is a **\[measured\] Reproducible internal** harness failure, not a software comparison. The fixture, hidden test, prompts, and scorer were retained unchanged for E07.

**Unknowns.** The failed run supports no accuracy, token, or productivity conclusion. Read [`experiments/E06_SOFTWARE_FAIR/preregistration.md`](experiments/E06_SOFTWARE_FAIR/preregistration.md). The missing successful output is intentional, not a numbering gap.

## E07: corrected fair-access software comparison

**Question and rule.** E07 reran the frozen E06 design with absolute prompt paths. A baseline received the ordinary whitespace bug. The systemic condition also had to inspect siblings, infer the class, centralize prevention when justified, test, and stop. Both had equal repository and tool access. The hidden test was copied into both repositories only after their turns ended.

**Result.** Both conditions passed 23 tests. The baseline inspected siblings but changed only `quote.py`; the systemic condition centralised normalisation and changed five flows. Static scoring counted 11 independent normalisation operations in the baseline repository and three in the systemic repository. Run:

**\[executed\] Retained reproduction command**

``` bash
python experiments/E07_SOFTWARE_FAIR/score.py
```

Fixture behaviour and the static count are **\[measured\] Reproducible internal**. The behavioural suite did not distinguish the repairs because existing sibling flows already handled the tested inputs. The structural count is not a validated proxy for future defects, maintenance time, or product outcomes. There was no mutation test of future normalisation changes, blinded review, cost record, or live repository outcome.

## E08: weak evidence and correct early stopping

**Question and rule.** A baseline and structured condition each handled two tasks. The first requested a public notice from sparse facts about an automated hiring score; unsupported safeguards or rights were failures. The second requested correction of one typo; added process or automation was a failure. Human assessment had to quote the outputs.

**Result.** Both notice responses invented facts. The baseline implied submitted materials and a contact channel; the structured response asserted application-material use and review, correction, or accommodation rights. Both typo responses returned exactly the corrected sentence and stopped. This is **\[assessed\] Assessed internal**: one model run per condition and one unblinded researcher assessment.

**Reproduction and unknowns.** Prompts, raw events, outputs, and quoted assessment are under [`experiments/E08_WEAK_STOP/`](experiments/E08_WEAK_STOP/). No automated scorer, independent legal review, applicant-comprehension study, checker mutation, runtime, cost, or field outcome exists. The experiment rejects the claim that cautious process language alone grounds consequential prose.

## E09: reproducibly selected transfer task

**Question and rule.** A held-out task was selected from a frozen candidate list by taking the first 16 hexadecimal digits of the SHA-256 digest of `docs/02_REQUIREMENTS.md` modulo the candidate count. The selected index was two: a theorem-planning task. A baseline and structured condition were assessed for first action, scalable work, selector, bounded review, authority, and unsupported claims.

**Result.** Both conditions refused to invent a missing graph invariant. The baseline gave a strong one-week workflow. The structured condition placed formalization and a reproducible instance table before search and compressed the deliverable to four objects. This is **\[assessed\] Assessed internal**; no theorem was proved and no new mathematical capability was demonstrated.

**Reproduction.** Run:

**\[executed\] Retained reproduction command**

``` bash
python experiments/E09_HELDOUT/select.py
```

The candidate list, digest, selected index, prompts, events, and outputs are under [`experiments/E09_HELDOUT/`](experiments/E09_HELDOUT/). No independent rater, execution, repeated draw, time, or cost comparison exists.

## E10: cross-domain architecture suite

**Question and rule.** Seven architectures were applied to 20 frozen tasks: seven software tasks and 13 tasks from other domains. Every answer had to state the binding constraint, first action, scalable work, selector, bounded human object, stop or authority boundary, and durable learning. The preregistration forbade declaring a winner from model self-score or ignoring earlier null and adverse findings.

**Result.** Every condition returned 20 schema-complete records. Different operators fit different tasks, but the mandatory output contract caused substantial convergence. The hybrid did not consistently beat the general lifecycle. The result rejected a universal architecture and supported one invariant spine with conditional evidence, bottleneck, options, control, and adversarial-search operators.

**Reproduction and unknowns.** Run:

**\[executed\] Retained reproduction command**

``` bash
python experiments/E10_ARCHITECTURE_SUITE/score.py
```

Schema completeness is **\[measured\] Reproducible internal**; operational distinctions are **\[assessed\] Assessed internal**. The suite measured plan fields, not task success, reviewer burden, safety, or productivity. The richer hybrid description remained a treatment confound. Tasks, architecture definitions, prompt builder, raw events, outputs, and scorer are under [`experiments/E10_ARCHITECTURE_SUITE/`](experiments/E10_ARCHITECTURE_SUITE/).

## What this record supports

The record supports three modest conclusions. First, strong baselines often perform well, so additional machinery needs its own burden of proof. Second, external checks and structured provenance reveal failures that fluent prose hides, but a weak checker remains weak at machine scale. Third, null, adverse, and failed runs change design when they remain visible.

The record does not establish that the complete method increases expert productivity, improves real-world outcomes, or transfers unchanged across domains. A suitable next study would freeze representative tasks, compare against a competent minimal baseline, measure accepted decision value per hour of expert review, validate the checker with seeded faults, and observe downstream outcomes long enough for delayed failure to appear.

# Edition history

- **1.0.0 (2026-09-01)** — first handbook edition. Includes the complete E01–E10 experiment record, context-first mathematics, evidence labels and bundled experiment artifacts. No outcome-validated productivity claim.

# References

<div id="refs" class="references csl-bib-body hanging-indent" entry-spacing="0">

<div id="ref-ateia2025feedback" class="csl-entry">

Ateia, Samy, and Udo Kruschwitz. 2025. ‘Can Language Models Critique Themselves? Investigating Self-Feedback for Retrieval Augmented Generation at BioASQ 2025’. <https://arxiv.org/abs/2508.05366>.

</div>

<div id="ref-flashattention2022" class="csl-entry">

Dao, Tri, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Re. 2022. ‘FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness’. <https://arxiv.org/abs/2205.14135>.

</div>

<div id="ref-hariri2026tts" class="csl-entry">

Hariri, Mohsen, Weicong Chen, Nahal Shahini, Vikash Singh, Kai Ye, Amirhossein Samandar, Debargha Ganguly, et al. 2026. ‘Test-Time Scaling in Reasoning LLMs: Inference Regimes, Evaluation, and Reproducibility’. <https://arxiv.org/abs/2608.04001>.

</div>

<div id="ref-khalaf2025reward" class="csl-entry">

Khalaf, Hadi, Claudio Mayrink Verdun, Alex Oesterling, Himabindu Lakkaraju, and Flavio du Pin Calmon. 2025. ‘Inference-Time Reward Hacking in Large Language Models’. <https://arxiv.org/abs/2506.19248>.

</div>

<div id="ref-liu2024feedback" class="csl-entry">

Liu, Dancheng, Amir Nassereldine, Ziming Yang, Chenhui Xu, Yuting Hu, Jiajie Li, Utkarsh Kumar, Changjae Lee, and Jinjun Xiong. 2024. ‘Large Language Models Have Intrinsic Self-Correction Ability’. <https://arxiv.org/abs/2406.15673>.

</div>

<div id="ref-sadanandan2026cot" class="csl-entry">

Sadanandan, Binesh, and Vahid Behzadan. 2026. ‘When Chain-of-Thought Backfires: Evaluating Prompt Sensitivity in Medical Language Models’. <https://arxiv.org/abs/2603.25960>.

</div>

<div id="ref-setlur2025verification" class="csl-entry">

Setlur, Amrith, Nived Rajaraman, Sergey Levine, and Aviral Kumar. 2025. ‘Scaling Test-Time Compute Without Verification or RL Is Suboptimal’. <https://arxiv.org/abs/2502.12118>.

</div>

<div id="ref-tsui2025selfcorrection" class="csl-entry">

Tsui, Ken. 2025. ‘Self-Correction Bench: Uncovering and Addressing the Self-Correction Blind Spot in Large Language Models’. <https://arxiv.org/abs/2507.02778>.

</div>

<div id="ref-vaswani2017attention" class="csl-entry">

Vaswani, Ashish, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. ‘Attention Is All You Need’. <https://arxiv.org/abs/1706.03762>.

</div>

<div id="ref-horizon2026" class="csl-entry">

Wang, Xinyu Jessica, Haoyue Bai, Yiyou Sun, Haorui Wang, Shuibai Zhang, Wenjie Hu, Mya Schroder, Bilge Mutlu, Dawn Song, and Robert D. Nowak. 2026. ‘The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break’. <https://arxiv.org/abs/2604.11978>.

</div>

<div id="ref-trialmind2024" class="csl-entry">

Wang, Zifeng, Lang Cao, Benjamin Danek, Qiao Jin, Zhiyong Lu, and Jimeng Sun. 2024. ‘Accelerating Clinical Evidence Synthesis with Large Language Models’. <https://arxiv.org/abs/2406.17755>.

</div>

<div id="ref-flashattention4_2026" class="csl-entry">

Zadouri, Ted, Markus Hoehnerbach, Jay Shah, Timmy Liu, Vijay Thakkar, and Tri Dao. 2026. ‘FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling’. <https://arxiv.org/abs/2603.05451>.

</div>

<div id="ref-zeng2025falsifier" class="csl-entry">

Zeng, Weihao, Keqing He, Chuqiao Kuang, Xiaoguang Li, and Junxian He. 2025. ‘Pushing Test-Time Scaling Limits of Deep Search with Asymmetric Verification’. <https://arxiv.org/abs/2510.06135>.

</div>

<div id="ref-zhu2025agents" class="csl-entry">

Zhu, King, Hanhao Li, Siwei Wu, Tianshun Xing, Dehua Ma, Xiangru Tang, Minghao Liu, et al. 2025. ‘Scaling Test-Time Compute for LLM Agents’. <https://arxiv.org/abs/2506.12928>.

</div>

</div>
