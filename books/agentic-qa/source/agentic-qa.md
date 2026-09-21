---
title: "Agentic QA"
subtitle: "Shipping fast and in volume without shipping what a token predictor writes"
author: "Ankit Kumar Pandey <itsankitkp@gmail.com>"
rights: "Copyright © 2026 Ankit Kumar Pandey. Licensed under CC-BY-4.0; code under Apache-2.0."
version: "Edition 1.0.0"
date: "2026-09-21"
lang: en-GB
subject: "Using language-model agents to test software without trusting their own verdicts"
keywords:
  - agentic QA
  - software testing
  - language models
  - mocking
  - mutation testing
  - verification
bibliography: references.bib
citeproc: true
reference-section-title: References
link-citations: true
documentclass: scrartcl
classoption:
  - paper=a4
  - fontsize=10pt
  - titlepage=true
geometry: margin=0.75in
toc: false
numbersections: true
colorlinks: true
linkcolor: NavyBlue
toccolor: NavyBlue
urlcolor: NavyBlue
mainfont: "Noto Serif"
sansfont: "Noto Sans"
monofont: "DejaVu Sans Mono"
header-includes:
  - |
    \usepackage{microtype}
    \usepackage{xurl}
    \usepackage{booktabs}
    \usepackage{longtable}
    \usepackage{xcolor}
    \definecolor{NavyBlue}{RGB}{18,52,86}
---

# Publication information

**Tier B · Edition 1.0.0.** A short working guide for engineers who ship with coding agents and want fewer of the agents' bugs to reach production. It derives its rules from how the models are trained and sampled, and from the arithmetic of what a passing test is worth. It is a manuscript plus metadata, structurally linted and built by CI. It does not carry the manifests, reproducibility package or verifier suite of a Tier A handbook, and it claims no measured productivity gain.

Copyright © 2026 Ankit Kumar Pandey. Prose is licensed under CC-BY-4.0; code listings under Apache-2.0.

## Scope and evidence labels

Every factual claim carries one of these labels, kept out of the running text: they sit in the **Basis.** line that closes each box, in tables, and in the Boundaries section.

- **[measured]** — observed in a campaign or run described well enough to repeat.
- **[documented]** — stated by a primary source: a paper, vendor documentation, or a project's own records. Cited.
- **[reported]** — stated by a secondary source or an industry report. Cited, and weaker.
- **[inferred]** — reasoning from the above. Not observed directly.
- **[designed]** — a construct built here: a rule, a table, a procedure.
- **[opinion]** — a judgement call. Argued, not asserted.

## Code authenticity labels

- **[executed]** — this exact listing was run.
- **[adapted]** — derived from material that was run or filed, edited for the page.
- **[illustrative]** — never run. Shows shape, not behaviour.

# The Crux

Take a team whose agent adds a caching layer to a billing service. It writes the change, then forty tests, all green, and the change ships. Three days later invoices are wrong for every account whose price was cached at the moment the config changed. The post-mortem finds that thirty-one of the forty tests assert against a mock of the exact module that changed — a mock the agent wrote, in the same session, told to return whatever the test needed. The suite watched itself agree.

That pattern is not invented. Coding agents add mocks to their tests in 36% of commits, against 26% for human commits, and touch test files in 23% of commits against 13% for humans (Hora and Robbes 2026).

Three mechanisms explain why, and each says something about what a green test from an agent is worth.

An agent's output is a sample from a next-token distribution: each token continues the prompt plausibly, not checked against the system it describes. Nothing forces the code and its test to agree with a database row, an HTTP response, or a log line; both are simply the likeliest continuation of the same context. For QA: a green result proves the continuation was fluent, not that its claim is true.

Preference training rewards length. Raters shown two similar answers favour the longer one, and a policy trained against that signal learns to emit more: more code, more tests, more mocks that make new tests pass at once. For QA: suite size and test count show what the reward function paid for, not thoroughness.

There is no execution inside the model, and no independent judge either. The model that writes the code and the model that grades it share the same weights, context, and blind spots. Judges built this way favour their own generations, match a stated view over a correct one, and rarely improve on a second look. For QA: an agent's self-review is one sample voting for itself twice.

> **Mechanism: why more tokens are not more evidence**
>
> $$ \hat{y} = \arg\max_y \; \big[\, R_{\mathrm{quality}}(y) + \beta \cdot \mathrm{len}(y) \,\big] $$
>
> A policy optimised against a reward with positive length term $\beta$ learns to pad, since padding raises the score even when quality is flat. Padding is also the expensive direction: output tokens price at roughly five times input tokens, a cached read costs a tenth of a fresh one, so a generated token costs about fifty times what re-reading an already cached context costs. Producing another candidate is the expensive direction; checking one against context you already hold is the cheap one.
>
> Operating rule: spend the marginal token checking a candidate against something real, not producing another one.
>
> **Basis.** \[documented\] Length-reward correlation is measured across RLHF and DPO settings (Singhal et al. 2024; Park et al. 2024). \[documented\] Token and cache-read pricing come from Anthropic's current pricing page (Anthropic 2026). \[documented\] Next-token training's limits on planning, self-preference in model judges, sycophancy, and the failure of unaided self-correction are each measured in the cited studies (Bachmann and Nagarajan 2024; Panickssery, Bowman, and Feng 2024; Sharma et al. 2024; Huang et al. 2024). \[designed\] The reward form shows the effect's direction, not a fitted model.

# How to Approach the Problem

Start by writing the requirement as an oracle before a test exists. State the observable state that must hold if the change works, and name where it lives: a table row, an HTTP response body, a rendered element's attribute, a log line. If you cannot say where the evidence would appear, you have a hope, not a requirement.

Next, find the truth boundary: the nearest point where the claim can be checked against something the agent did not write. Rank the options — production outcome, then a real dependency in a container or fake with its own contract tests, then in-process real code, then a DOM read or screenshot, then the agent's own assertion, which proves only that it believes what it wrote. Push every claim down that ladder as budget allows, and mock only the boundary you cannot run.

> **Mathematical detail: what a green test is worth**
>
> $$ LR = \frac{P(\mathrm{pass} \mid \mathrm{correct})}{P(\mathrm{pass} \mid \mathrm{broken})} = \frac{1 - f}{q} $$
>
> A green result is worth its likelihood ratio: how much more often the test passes when the code is right than when it is broken. The numerator is one minus the flake rate $f$; the denominator is the false-pass rate $q$, the share of real faults the test lets through. A test that asserts against a mock of the changed module passes whether or not the module works, so both probabilities sit near one and the ratio sits near 1: a pass tells you nothing you did not already believe. A test at the real boundary with $f = 0.05$ and $q = 0.05$ has LR 19. Starting from three-to-one odds that an agent's change is correct, one such pass moves you to fifty-seven to one, about 98%; the mock test leaves you at 75%.
>
> Operating rule: estimate $q$ by planting faults before trusting a suite, and give no weight to a pass from a test whose ratio is unknown.
>
> **Basis.** \[designed\] Standard likelihood-ratio arithmetic; the figures are worked examples, not measurements. \[documented\] Mutation score tracks real-fault detection independently of coverage, which is why planted faults are the right way to estimate the false-pass rate (Just et al. 2014; Inozemtseva and Holmes 2014). The mock-asserting case matches the unit-qa skill's false-pass catalogue, which lists a test that only reads back an injected value as its own distinct trap.

> **Mathematical detail: false accepts compound**
>
> $$ P(\mathrm{all}\ N\ \mathrm{changes\ good}) = (1-q)^N $$
>
> Over a day where agents ship $N$ changes, each with false-pass rate $q$, the chance every one was actually good falls fast. At $q = 0.05$ and $N = 30$, a plausible day's batch, that chance is about 21%: four days in five, something bad got through. Holding the batch 90% clean needs $q \approx 0.0035$, roughly fifteen times more discriminating than the 5% baseline.
>
> Operating rule: treat $q$ as a number to drive down; verification spend has to scale with $N$ faster than intuition suggests — the budget line is verification, not generation.
>
> **Basis.** \[designed\] Independence between changes is assumed; correlated failures make a batch worse, not better. \[reported\] The 2024 DORA report finds AI adoption correlated with a 7.2% fall in delivery stability and attributes it to larger batches (DORA and Google Cloud 2024).

Finally, decide which factor is short. Green, yet the bug ships from an untested path — coverage is short. Green on the right surface, yet the tests cannot fail — rejection power is short. Sound tests, yet bugs ship because a human must read every result and volume has outrun the hours — throughput is short.

| Symptom you see | What is short | Start with |
|---|---|---|
| Green suite, bug ships in a path no test exercised | Coverage | Requirement-first unit QA at the real boundary; Browser campaigns with triangulated evidence |
| Green suite, mutation kills near zero, no test has ever failed | Rejection power | Mutation-guided test generation; Property, metamorphic and differential oracles |
| Findings pile up faster than one reviewer's morning | Throughput | Split the generator from the verifier; Close the loop from production |

# Ways to Solve It

## Requirement-first unit QA at the real boundary

Use this when an owner can state what "correct" means before code exists.

Write one catalogue row per claim: the observable, where it lives, the oracle that decides it, and the known trap that would fake a pass. Check against real fixtures and a real database; mock only what you cannot run in-process. Apply the truth rule: a toast proves nothing, so require a real HTTP status, persistence after reload, and re-verification via every UI path. Score each candidate against the false-pass catalogue before filing. When the agent's tests are suspect, delete and regenerate from the requirement.

Cost: the catalogue row must exist before generation starts, and someone who owns the behaviour has to write it. Over-generation hides here if you let it: Meta's test-improvement pipeline found that only 75% of its generated tests built and 57% passed reliably, before any engineer looked at them. Characteristic failure: a claim with no catalogue row has no sanctioned oracle and ships on the agent's say-so.

> **Basis.** \[documented\] unit-qa's requirement catalogue, false-pass table, and truth rule; mock drift documented by Spadini (Spadini et al. 2017); build/pass figures are Meta's TestGen-LLM numbers (Alshahwan et al. 2024).

## Split the generator from the verifier

Use this when self-report alone cannot be trusted — money, authorisation, deletion.

Spawn a second agent; give it only the diff and the requirement, never the generator's transcript. Require evidence, not a verdict — a test failing before the change and passing after, or a mutant it can show the change kills. Work down an adversarial pass list ranked by blast radius. Treat a verifier FAIL as a hypothesis pending a second check, like a PASS.

Cost: doubles the verification budget, and buys nothing if the verifier inherits the generator's framing. Characteristic failure: the verifier reads the generator's explanation of the change and agrees with it.

> **Mechanism: why a second agent is not a second witness**
>
> Treat each verdict as a vote with variance $\sigma^2$ and correlation $\rho$. The independent-vote count for $n$ correlated votes is
>
> $$ n_{\mathrm{eff}} = \frac{n}{1 + (n-1)\rho} $$
>
> A verifier reading the generator's transcript shares nearly everything it believed — $\rho \approx 0.8$ — so two agents are worth $2/1.8 \approx 1.1$ witnesses, barely one. Cut $\rho$ to 0.2 by giving it only the diff and requirement, and the pair is worth $2/1.2 \approx 1.7$: most of a second opinion. Rule: the verifier's context must exclude the generator's transcript.
>
> **Basis.** \[inferred\] Standard effective-sample-size correction. Self-evaluating models favour their own generations by how well they recognise them, and self-correction without an external signal rarely improves the first answer (Panickssery, Bowman, and Feng 2024; Huang et al. 2024).

## Browser campaigns with triangulated evidence

Use this for UI regressions across many features, with no owner to write per-surface requirements by hand.

Build a feature ledger first: one row per feature or drag surface, with entry point, selectors, and status. Dispatch one feature per subagent from a fixed brief. Capture screenshot, DOM, network, and console for every claim, using a headless lane for scale and a real browser lane for pointer gestures. Build the comparison matrix by machine, and flag every row where DOM and network disagree — network and stored state outrank pixels.

Cost: two lanes to maintain, plus overhead retrieving evidence from a sandboxed session. Characteristic failure: a headless actionability model reports "does nothing" against elements that are actually hover-animated — caught only by a real-browser cross-check.

**[adapted]** from the Prague campaign's finding ledger, ISSUE-023.

```yaml
id: ISSUE-023
class: silent-success-on-failed-write
object: dataset 2530 / view 4397
state: ref_error (unrecoverable)
truth_check: HTTP status on POST pipeline/tasks
evidence: 4xx returned; UI showed no error
status: preserved, Trash (never emptied)
```

> **Basis.** \[documented\] Prague's dual-lane driver-vs-Chrome campaign and its machine-built disagreement matrix; structured browser automation as a truth boundary follows Playwright's accessibility-tree tooling (Microsoft 2026).

## Mutation-guided test generation

Use this once coverage stops being trustworthy: 90% coverage can mean tests that assert nothing.

Do not ask the agent to hit a coverage target; ask it to kill a targeted set of mutants representing uncaught faults. Generate the mutants first, run the suite, and keep only survivors as the target. Score by kill rate, not coverage. At scale, mutate only changed lines and suppress unexercised-code mutants, or the analysis gets too expensive.

Cost: mutant execution multiplies the run by the mutant count — a diff-based approach at code-review time, not a full-repository batch job, made this practical at Google's scale. Meta's pipeline had engineers accept 73% of its generated tests, 36% privacy-relevant. Characteristic failure: the equivalent mutant, indistinguishable from the original — Meta's detector needed pre-processing to move from 0.79 precision / 0.47 recall to 0.95 / 0.96.

> **Basis.** \[documented\] Diff-based mutation testing at code-review scale (Petrović and Ivanković 2018); Meta's ACH pipeline and its equivalent-mutant detector (Foster et al. 2025); mutation score's correlation with real, developer-fixed faults (Just et al. 2014).

## Property, metamorphic and differential oracles

Use this when a hand-written expected value is the weak link — nobody can state the correct output, or errors creep in exactly there.

Have the agent propose a property that must hold for every input — an invariant, an idempotence rule, a permutation relation — then let a framework generate the inputs. Where none is stated, run the same input against a reference implementation, an earlier release, or an alternate code path, and flag any divergence. Reject a property that is trivially true regardless of behaviour.

Cost: a correct property or reference implementation still needs domain understanding; a wrong property certifies bugs as correct. Characteristic failure: a property that describes the code's current behaviour rather than the required behaviour, so it cannot catch the bug it was written for.

> **Basis.** \[documented\] Property-based generation (Claessen and Hughes 2000), metamorphic relations as an oracle with no cheap ground truth (Chen et al. 2018), and differential testing against an independent implementation (McKeeman 1998).

## Close the loop from production

Use this once a bug has already escaped to production — the one signal no pre-release testing supplied.

Turn every escaped bug into a permanent regression-ledger entry, re-checked every run. Track change failure rate and recovery time alongside deployment frequency. Gate releases behind a canary population, and treat a canary failure as a blocker. Feed the failure back into the requirement catalogue as a new oracle.

Cost: this only pays for a bug already shipped, not a new failure class. Characteristic failure: treating velocity as the win — a 25% rise in AI adoption is tied to a 1.5% fall in delivery throughput and a 7.2% fall in stability, driven by larger changesets.

> **Basis.** \[reported\] Change failure rate and deployment frequency as the DORA metrics; AI-driven batch-size growth correlated with falling throughput and stability (DORA and Google Cloud 2024).

# One Campaign, End to End

On 19 and 20 September 2026, an unattended agentic visual QA campaign ran against a live staging deployment, tracking 117 rows in a feature ledger — 88 features and 29 drag-and-drop surfaces — each dispatched to one Sonnet subagent from a fixed brief, and verified against the same truth rule as the requirement-first method: a toast is not evidence, so a real HTTP status, a post-reload persistence check, and re-verification via every UI path were required before a claim was accepted. Two lanes ran in parallel — headless for scale, real-browser for genuine pointer gestures — because the headless lane's click model had already produced a confirmed false finding against working elements.

Every row was verdicted. The closing report is the record used below; a later summary note gives slightly different totals for the same closed campaign, and that conflict is noted rather than resolved.

| Rows | Issues by severity | Health | Refuted agent claims |
|---|---|---|---|
| 117 (88 F + 29 D) | 75 (8 / 16 / 18 / 33) | 46/100 | 6 |

The headline failure class was silent success on a failed write: a pipeline mutation could latch into an unrecoverable error state, and any failed status on the task-submission endpoint produced an eternal "processing" display instead of a visible error. Six agent FAIL claims were refuted on cross-check before filing, and one "regression-fixed" claim was itself later found to be an agent error and withdrawn. The deployed backend build did not change throughout, so findings reflect one fixed target, not drift. The method changed as a result: a FAIL claim from either lane now requires a second, independent check against a screenshot, the front-end source, or the database before filing.

# Boundaries

The numbers above are \[measured\] from one closed campaign, one product, one fixed backend build; the two records of that campaign's own totals disagree, and the primary artefact, not the memory summary, is the one used here. The method rules — the truth rule, one subagent per feature, network over pixels — are \[documented\] from the skills that define them, not validated against a control condition. The generator/verifier correlation argument is \[inferred\] from a standard statistical correction, not measured on this project's own agents.

No claim here is a productivity claim. Controlled measurement has found developers slower, not faster, with AI on real tasks, and survey data ties AI adoption to falling delivery throughput and stability (Becker et al. 2025; DORA and Google Cloud 2024).

# Edition history

- **1.0.0** (2026-09-21) — first edition.

# References

Alshahwan, Nadia, Jubin Chheda, Anastasia Finegenova, et al. 2024. "Automated Unit Test Improvement Using Large Language Models at Meta." In *ACM International Conference on the Foundations of Software Engineering (FSE), Industry Track*. <https://arxiv.org/abs/2402.09171>.

Anthropic. 2026. "Pricing --- Claude Platform Docs." <https://platform.claude.com/docs/en/about-claude/pricing>.

Bachmann, Gregor, and Vaishnavh Nagarajan. 2024. "The Pitfalls of Next-Token Prediction." In *International Conference on Machine Learning (ICML)*, 2296--2318. <https://arxiv.org/abs/2403.06963>.

Becker, Joel, Nate Rush, Elizabeth Barnes, and David Rein. 2025. "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity." *arXiv Preprint arXiv:2507.09089*. <https://arxiv.org/abs/2507.09089>.

Chen, Tsong Yueh, Fei-Ching Kuo, Huai Liu, Pak-Lok Poon, Dave Towey, T. H. Tse, and Zhi Quan Zhou. 2018. "Metamorphic Testing: A Review of Challenges and Opportunities." *ACM Computing Surveys* 51 (1): 4.

Claessen, Koen, and John Hughes. 2000. "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs." In *ACM SIGPLAN International Conference on Functional Programming (ICFP)*.

DORA, and Google Cloud. 2024. "Accelerate State of DevOps Report 2024." <https://dora.dev/research/2024/dora-report/>.

Foster, Christopher et al. 2025. "Mutation-Guided LLM-Based Test Generation at Meta." In *ACM International Conference on the Foundations of Software Engineering (FSE), Industry Track*. <https://arxiv.org/abs/2501.12862>.

Hora, Andre, and Romain Robbes. 2026. "Are Coding Agents Generating Over-Mocked Tests? An Empirical Study." IEEE/ACM International Conference on Mining Software Repositories (MSR). <https://arxiv.org/abs/2602.00409>.

Huang, Jie, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2024. "Large Language Models Cannot Self-Correct Reasoning Yet." In *International Conference on Learning Representations (ICLR)*. <https://arxiv.org/abs/2310.01798>.

Inozemtseva, Laura, and Reid Holmes. 2014. "Coverage Is Not Strongly Correlated with Test Suite Effectiveness." In *International Conference on Software Engineering (ICSE)*, 435--45.

Just, René, Darioush Jalali, Laura Inozemtseva, Michael D. Ernst, Reid Holmes, and Gordon Fraser. 2014. "Are Mutants a Valid Substitute for Real Faults in Software Testing?" In *ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE)*.

McKeeman, William M. 1998. "Differential Testing for Software." *Digital Technical Journal* 10 (1).

Microsoft. 2026. "Playwright MCP Documentation." <https://playwright.dev/docs/getting-started-mcp>.

Panickssery, Arjun, Samuel R. Bowman, and Shi Feng. 2024. "LLM Evaluators Recognize and Favor Their Own Generations." In *Advances in Neural Information Processing Systems (NeurIPS)*. <https://arxiv.org/abs/2404.13076>.

Park, Ryan, Rafael Rafailov, Stefano Ermon, and Chelsea Finn. 2024. "Disentangling Length from Quality in Direct Preference Optimization." In *Findings of the Association for Computational Linguistics (ACL)*. <https://arxiv.org/abs/2403.19159>.

Petrović, Goran, and Marko Ivanković. 2018. "State of Mutation Testing at Google." In *International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP)*.

Sharma, Mrinank, Meg Tong, Tomasz Korbak, et al. 2024. "Towards Understanding Sycophancy in Language Models." *International Conference on Learning Representations (ICLR)*. <https://arxiv.org/abs/2310.13548>.

Singhal, Prasann, Tanya Goyal, Jiacheng Xu, and Greg Durrett. 2024. "A Long Way to Go: Investigating Length Correlations in RLHF." In *Conference on Language Modeling (COLM)*. <https://arxiv.org/abs/2310.03716>.

Spadini, Davide, Maurı́cio Aniche, Magiel Bruntink, and Alberto Bacchelli. 2017. "To Mock or Not to Mock? An Empirical Study on Mocking Practices." In *IEEE/ACM International Conference on Mining Software Repositories (MSR)*. <https://doi.org/10.1109/MSR.2017.61>.
