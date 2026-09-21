---
title: "Agentic QA"
subtitle: "How to ship fast with coding agents without shipping their bugs"
author: "Ankit Kumar Pandey <itsankitkp@gmail.com>"
rights: "Copyright © 2026 Ankit Kumar Pandey. Licensed under CC-BY-4.0; code under Apache-2.0."
version: "Edition 2.0.0"
date: "2026-09-21"
lang: en-GB
subject: "Practical QA for software written and tested by coding agents"
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
toc: true
toc-depth: 1
numbersections: false
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

**Tier B · Edition 2.0.0.** A practical handbook for engineers who ship with coding agents and want fewer of the agents' bugs to reach production. Every chapter gives you something to run, copy or paste: a test to compare against, a shell script, a block of rules for the agent, a CI gate, a checklist. The code examples were executed and their output is shown as it ran. This is a manuscript plus metadata, structurally linted and built by CI. It does not carry the manifests, reproducibility package or verifier suite of a Tier A handbook, and it claims no measured productivity gain.

Edition 2 replaces Edition 1, which put derivations and notation where a working engineer needed code and commands. The argument is the same; the book is now written to be used.

Copyright © 2026 Ankit Kumar Pandey. Prose is licensed under CC-BY-4.0; code listings under Apache-2.0.

## Scope and evidence labels

Every factual claim carries one of these labels, kept out of the running text. They appear in the short italic *Evidence* line that ends each chapter, in tables, and in the Boundaries section.

- **[measured]** — observed in a campaign or run described well enough to repeat.
- **[documented]** — stated by a primary source: a paper, vendor documentation, or a project's own records. Cited.
- **[reported]** — stated by a secondary source or an industry report. Cited, and weaker.
- **[inferred]** — reasoning from the above. Not observed directly.
- **[designed]** — a construct built here: a rule, a table, a procedure.
- **[opinion]** — a judgement call. Argued, not asserted.

## Code authenticity labels

- **[executed]** — this exact listing was run in the example repository that ships with the book under `examples/`, and the output shown is the output it produced. Versions are pinned there.
- **[adapted]** — derived from material that was run or filed, edited for the page.
- **[illustrative]** — never run. Shows shape, not behaviour.

# 1. What goes wrong

You ask the agent to add discount codes to checkout. Twenty minutes later there is a pull request: four source files, twelve new tests, all green, a tidy description. You skim the tests. They look like tests. You merge.

A week later a customer with a free-shipping code on a small order is charged a negative amount, and the refund path was never built because nothing negative was supposed to reach it. You open the test file properly this time. Nine of the twelve tests patch the pricing function, the order repository, or the mailer, and then assert that the function returned whatever the patch was told to return. Two assert that a mock was called. One tests the happy path with the exact number the code happened to produce. Not one of them would have gone red if the discount logic had been deleted.

This is not a bad agent or a bad prompt. It is the normal output of a coding agent asked to "add tests", and it is common enough to measure. Across 1.2 million commits in 2,168 repositories in 2025, commits by coding agents added mocks to tests in 36% of cases against 26% for humans, and touched test files in 23% of commits against 13% (Hora and Robbes 2026). Inside Meta's own test-generation pipeline, only 75% of generated tests even built, and 57% passed reliably, before an engineer looked at them (Alshahwan et al. 2024).

## What a test is for

A test is a bet that a specific piece of code can be broken in a specific way, and a check that would notice. If there is no way to break the code that turns the test red, the test is not a bet. It is a green light wired to the on switch.

Agent-written suites fail this in a particular way. The agent does not know what would break, because it has not run anything and has no idea what you were worried about. So it writes tests that describe the code it just wrote, using fakes it also just wrote, and the two agree with each other by construction. The suite is a mirror.

Here is one of the tests from the example repository this book uses throughout. It ships with the book under `examples/`: a small order service with pricing, a sqlite-backed repository and a receipt mailer, plus two test suites. One suite was written to match what agents typically produce; the other is the one the book recommends. Every listing was run there, and the README shows how to run it yourself.

**[executed]** from the example repository, `tests_agent/test_service.py`, two of its four tests shown; the other two assert only that a mock was called.

```python
# Typical agent-written suite (composite, for illustration)
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import date
from orders.service import checkout


@patch("orders.service.send_receipt")
@patch("orders.service.OrderRepo")
@patch("orders.service.apply_discount")
def test_checkout_returns_order_id(
    mock_discount, mock_repo_cls, mock_send
):
    mock_discount.return_value = Decimal("90.00")
    mock_repo = MagicMock()
    mock_repo.create.return_value = 42
    mock_repo.get.return_value = {"id": 42, "total": "90.00"}
    mock_repo_cls.return_value = mock_repo
    mock_send.return_value = True

    order_id = checkout(mock_repo, Decimal("100.00"), "SAVE10",
                         date(2026, 1, 1), http=MagicMock())

    assert order_id == mock_repo.create.return_value


def test_checkout_mock_called_only():
    mock_http = MagicMock()
    mock_repo = MagicMock()
    mock_repo.create.return_value = 7
    with patch("orders.service.send_receipt") as mock_send, \
         patch("orders.service.apply_discount") as mock_discount:
        mock_discount.return_value = Decimal("1.00")
        checkout(mock_repo, Decimal("1.00"), "SAVE10",
                 date(2026, 1, 1), http=mock_http)
        assert mock_send.called
```

Read what it proves. The function under test is `checkout`. Every collaborator it has is patched. The value asserted is the value the patch was told to return two lines earlier. The pricing logic, the database write, and the receipt could all be deleted and this test would stay green. In the example repository that is what happened. Three bugs were planted one at a time. The agent-style suite caught one of them by accident, because one test hard-codes the correct discount total, and passed everything with the other two in place. The suite written against the real code went red on all three.

| Bug planted | Agent-style suite | Real suite |
|---|---|---|
| SAVE10 gives 1% off instead of 10% | 1 failed, 10 passed | 3 failed, 9 passed |
| Paying an order twice now raises | 11 passed | 1 failed, 11 passed |
| Free shipping can make the total negative | 11 passed | 1 failed, 11 passed |

## The rule this book is built on

Do not accept a test you have not seen fail. Everything that follows is a way of making that cheap: breaking code on purpose, mutation testing, putting real databases under tests, telling the agent what to do and what not to, using a second agent to check the first, and gating the pipeline so that a green suite has to mean something. None of it needs a new tool you do not already have.

## What is in here

Chapter 2 explains, in a page, why agents write tests like this. Chapters 3 to 5 are the daily practice: proving a suite can fail, mocking only what you must, and working with the agent so that it produces fewer, better tests. Chapters 6 to 8 scale it: a second agent as reviewer, testing a UI with agents, and CI gates. Chapter 9 is one real campaign with its numbers. Chapter 10 is the checklists. If you read one chapter, read 3.

Two sources recur. The unit-qa skill is an internal tool that drives a coding agent through requirement-first QA of a web product: a requirement catalogue, a rule for what counts as proof, and a catalogue of the ways a test can pass without proving anything. The Prague campaign is an agent-run visual QA campaign on that product's staging environment, told in full in Chapter 9. Neither is a product you can install; both are practice you can copy.

*Evidence.* The opening story is a composite, not a measured event; the pattern it describes is [documented] in the over-mocking study and the Meta pipeline figures cited. The listing and the bug table are [executed] from the example repository under `examples/`. The rule is [designed].

# 2. Why the agent writes tests like this

Four habits produce a green suite that proves nothing, and none of them come from the model being lazy or careless. Each one is a sensible response to how the model was built and how it is used, which is exactly why telling it to "write better tests" does not fix any of them.

## It is trained to be approved, and longer looks better

The training that shapes a coding agent rewards output that looks thorough and helpful, and a reward model that learns from human preference data picks up length as a stand-in for quality without anyone asking it to. A model shaped this way over-generates: more tests, more assertions, more setup, because that pattern scored well long before it ever touched your repository. Two separate studies trace the same effect from different angles — reward gains in RLHF are driven mostly by length rather than the qualities length is supposed to signal, and once you correct evaluation for length, the picture behind a leaderboard changes (Singhal et al. 2024; Dubois et al. 2024). Nobody wrote a rule that says "generate twelve tests instead of four"; the twelve tests are just what a model shaped this way produces by default, for a checkout feature or anything else.

What this means for you: a pull request with forty new tests is not evidence of thoroughness. It is evidence of what got rewarded in training.

## It cannot run anything while it writes

The agent produces a test file the way it produces everything else: one token at a time, predicting what a plausible continuation looks like, with no way to pause and execute the code it is describing. It cannot watch the test go red, because nothing has run yet, and it has no memory of a real failure to draw on while it types the assertion. Research on self-correction backs this up directly — without an external check to run against, a model's own sense that its output is correct is unreliable, and re-reading what it just wrote does not fix that, sometimes it makes the output worse (Huang et al. 2024).

What this means for you: watching the agent type is not review. At that point in the process it cannot know whether the test would fail.

## It grades its own homework

Ask the same session whether its own tests are any good, and it will tend to say yes, because LLM evaluators measurably favour their own generations, even in cases where a human rater scores the alternative as equally good. The effect gets stronger, not weaker, in models that are better at recognising their own writing style (Panickssery, Bowman, and Feng 2024). Asking it to double check itself is not a second opinion; it is the same judgement asked twice, from inside the same habits that produced the first answer.

What this means for you: never ask the agent that wrote a suite to also approve it. You already know what the answer will be.

## Mocks are the fastest way to green

The fastest route from a red pull request to a green one is to stop depending on anything unpredictable. Patch the database, patch the HTTP client, patch the very module you are meant to be testing, then assert against the value you just told the patch to return. This is not a quirk of one bad prompt; it is common enough across real coding-agent commits to have been measured directly, at a scale well beyond any one team's repository (Hora and Robbes 2026). Every mock removes one more way the test could fail, and a suite built to remove every way it could fail will, unsurprisingly, never fail.

What this means for you: a suite that went green without ever failing first was probably built this way. Ask what would have to break before any of its tests noticed.

*Evidence.* The training and self-evaluation claims in this chapter are [documented] in peer-reviewed studies of preference optimisation and self-correction, not measured on any example in this book. The over-mocking claim is [documented] at commit-history scale by a separate empirical study. The four habits themselves are [inferred] from those studies applied to what a coding agent's test suite typically looks like.

# 3. Prove the suite can fail

## Break it on purpose

The bug table in Chapter 1 covers three planted bugs and what each suite caught. Trusting a green suite without ever having broken the code on purpose is exactly the habit that let the free-shipping bug through in the first place. Here is one of the three in full, so you can see exactly what planting a bug means in practice, not just the outcome in a summary row, and what the two suites actually did when it landed.

**[executed]** the exact change made to `orders/pricing.py` for the free-shipping bug:

```diff
-    return _cents(result) if result > 0 else Decimal("0.00")
+    return _cents(result)
```

One line, in the FREESHIP branch of `apply_discount`. Drop the floor at zero, and a shipping deduction bigger than the subtotal pushes the total negative — the same shape of bug that opens Chapter 1.

**[executed]** both suites run against the planted bug:

```text
$ python -m pytest -q tests_agent
...........                                                     [100%]
11 passed in 0.25s

$ python -m pytest -q tests_real
....F.......                                                    [100%]
1 failed, 11 passed in 0.24s
FAILED tests_real/test_pricing.py::test_freeship_never_goes_negative -
  AssertionError: assert Decimal('-2.00') == Decimal('0.00')
```

The agent suite's one FREESHIP test always uses a subtotal comfortably above the shipping charge, so it never reaches the boundary where the deduction could flip negative. Eleven passed, nothing to see. The suite built against real behaviour has a test aimed at exactly that boundary, and it turns red with the actual negative number in the failure line, not a patch's opinion of what should have happened.

**[executed]** `scripts/prove_it_fails.sh`, full:

```bash
#!/usr/bin/env bash
# Usage: prove_it_fails.sh <test_file> <source_file>
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
TEST_FILE="$1"; SRC_FILE="$2"
cp "$SRC_FILE" "$SRC_FILE.orig"
trap 'mv "$SRC_FILE.orig" "$SRC_FILE"' EXIT
echo "== baseline run =="
python -m pytest -q "$TEST_FILE" \
    || { echo "baseline failing, abort"; exit 2; }

if grep -q '>=' "$SRC_FILE"; then
    sed -i '0,/>=/{s/>=/>/}' "$SRC_FILE"; echo "mutated: '>=' -> '>'"
elif grep -q ' - ' "$SRC_FILE"; then
    sed -i '0,/ - /{s/ - / + /}' "$SRC_FILE"; echo "mutated: '-' -> '+'"
else
    echo "no mutable operator found"; exit 2
fi

echo "== mutant run =="
if python -m pytest -q "$TEST_FILE"; then
    echo "RESULT: suite did NOT notice the mutant (still green)"
else
    echo "RESULT: suite noticed the mutant (went red)"
fi
```

**[executed]** run against both suites' pricing tests:

```text
$ bash scripts/prove_it_fails.sh tests_agent/test_pricing.py \
    orders/pricing.py
== baseline run ==
...                                                              [100%]
3 passed in 0.01s
mutated: '-' -> '+'
== mutant run ==
.F.                                                              [100%]
FAILED tests_agent/test_pricing.py::test_freeship_happy_path -
  AssertionError: assert Decimal('25.00') == Decimal('15.00')
1 failed, 2 passed in 0.02s
RESULT: suite noticed the mutant (went red)

$ bash scripts/prove_it_fails.sh tests_real/test_pricing.py \
    orders/pricing.py
== baseline run ==
......                                                           [100%]
6 passed in 0.02s
mutated: '-' -> '+'
== mutant run ==
.FF...                                                           [100%]
FAILED tests_real/test_pricing.py::test_freeship_subtracts_shipping
FAILED tests_real/test_pricing.py::test_freeship_never_goes_negative
2 failed, 4 passed in 0.03s
RESULT: suite noticed the mutant (went red)
```

Both suites went red here, and that is worth sitting with. The agent suite, which missed two of the three planted bugs entirely, still caught this one, because a plain swap of a minus for a plus happens to land on the single FREESHIP line it exercises at all. A hand-picked mutation like this is a weak check on a suite — it tells you the suite can fail on this exact line, and nothing about the hundreds of lines you did not mutate by hand. Run it once, get two green ticks, and you have learned almost nothing about whether the suite would catch a bug anywhere else in the file. The three planted bugs above are the stronger check, because they were chosen to look like real defects, not to be easy to trip over. Between the two, prefer the planted bug: it tells you something about a specific behaviour you decided mattered, not just about one line an editor happened to pick.

## Mutation testing in ten minutes

**[executed]** the `mutmut` configuration used against `pricing.py` and `repo.py`:

```ini
[mutmut]
source_paths=
	orders/pricing.py
	orders/repo.py
also_copy=
	tests_agent
	tests_real
	orders/__init__.py
	orders/notify.py
	orders/service.py
	pytest.ini
pytest_add_cli_args_test_selection=tests_agent
```

The test-selection key was swapped to `tests_real` for the second run below.

**[executed]** commands and summaries:

```text
$ mutmut run          # test selection = tests_agent
101/101  killed 38  survived 63  (timeout 0, suspicious 0)

$ mutmut run          # test selection = tests_real
101/101  killed 68  survived 33  (timeout 0, suspicious 0)
```

Same 101 mutants generated across the two files, run against each suite in turn. The tool prints its counts as emoji; they are spelled out here. The agent suite killed 38 and let 63 survive: a 37.6% kill rate. The suite built against real behaviour killed 68 and let 33 survive: 67.3%.

Three of the agent suite's surviving mutants, with the reason each got past it:

1. `apply_discount`: `if today > EXPIRY:` changed to `if today >= EXPIRY:` and survived — the agent suite never tests the expiry boundary, so the change is invisible to it.
2. `OrderRepo.mark_paid`: the `order_id` parameter dropped from the `SELECT ... WHERE id = ?` query, and survived — the test for this line runs against a mocked connection that accepts any arguments, so the broken query is never actually evaluated.
3. `OrderRepo.create`: the INSERT string corrupted with stray characters at each end, and survived — the test only checks that the word INSERT appears somewhere in the query, and that substring is still there in the corrupted version.

Read the kill rate as a starting point for triage, not a grade. Each surviving mutant above failed for a different reason — a missing boundary case, an assertion that never reaches the real code path, an assertion too loose to notice corruption — and the fix for each one is different. A percentage alone does not tell you which.

Running mutation analysis over an entire codebase is slow, and mostly tells you about lines nobody touched this week. Google's own tooling mutates only the lines in a diff, scored at review time, for exactly that reason (Petrović and Ivanković 2018). Meta's ACH goes further and targets mutants for one concern at a time rather than exhausting every line (Foster et al. 2025). Set your own threshold the same way: measure the kill rate on the lines a pull request actually changes, and treat a drop against your own baseline as the signal, not a number copied out of a book.

## The thirty-second test review

Mutation testing takes ten minutes and a full CI run. Most tests in a pull request do not need either — they fail this list before you have finished reading them.

1. Does it import the real module, or does it import `unittest.mock`?
2. What does the assert compare against — a value the real code computed, or a value the test just set on a mock?
3. Could you delete the function under test and have this test still pass?
4. If it patches something, is that a boundary you do not own, or the very thing you are meant to be checking?
5. Does it exercise a boundary case, or only the first number the happy path happened to produce?
6. Has anyone actually seen this test fail?

*Evidence.* The bug diff, both pytest runs, the `prove_it_fails.sh` script and its output, the `setup.cfg`, the `mutmut` commands and summaries, and the three surviving mutants are all [executed] from the example repository. The threshold rule is [designed], following diff-based practice [reported] at Google and Meta.

# 4. Mocking: what to fake and what never to

A mock is a promise: this collaborator will behave exactly like
this, so you can test everything else on its own. Keep the promise
narrow and the test still means something. Widen it to cover the
code you actually care about, and the test stops proving anything.

## The three things worth faking

Three kinds of collaborator are worth faking, and only three.
Network you do not own — a payment gateway, a mail provider, a
third-party API — because it is slow, flaky, and outside your
control; intercept it at the HTTP boundary with `responses` in
Python or `respx` in async code, never by patching the function
that calls it. Clock and randomness, because a test that depends
on today's actual date or a live random seed cannot be repeated;
freeze the clock with `freezegun`, or better, pass the current time
in as an argument and seed randomness the same way. Anything paid
or slow enough to make a suite unusable — an SMS send, a GPU call,
a large upload — for the same reason as the network case: fake the
boundary, not the logic sitting behind it.

## What you must never fake

Four things earn a hard no. The module under test — fake it and the
test checks nothing at all. Your own repository or database layer —
fake it and the test never touches a real query, a real schema, or
a real constraint. The filesystem, for anything small enough to
write to a temp directory. And the framework you are running on —
if you cannot trust pytest or Django to behave like pytest or
Django, replacing it with a mock will not help you.

**[executed]** from the example repository, `tests_agent/test_repo.py`,
the `sqlite3.connect` mock (two of its three tests shown;
`test_migrate_calls_execute` has the same "assert `.called`" shape).

```python
def test_create_calls_insert():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.lastrowid = 1
    repo = OrderRepo(mock_conn)
    repo.create(
        {"subtotal": "10.00", "total": "9.00", "code": "SAVE10"}
    )
    args, _ = mock_conn.execute.call_args
    assert "INSERT" in args[0]


def test_mark_paid_calls_update():
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (0,)
        mock_connect.return_value = mock_conn
        import sqlite3
        conn = sqlite3.connect(":memory:")
        repo = OrderRepo(conn)
        repo.mark_paid(1)
        assert mock_conn.execute.called
```

Read `test_mark_paid_calls_update` closely. It patches
`sqlite3.connect` itself, so any code that opens a connection gets
the same `MagicMock` back. It pins `fetchone.return_value` to
`(0,)` — "this order exists and is unpaid" — as a constant decided
by the test author, not by any database. It calls `mark_paid(1)`
and checks one thing: that `execute` was called at all, not with
what SQL, not with what id. A change that drops the id parameter
from the `SELECT` — so the query would look up the wrong row, or no
row, against a real database — still passes, because the mock
answers `fetchone()` the same way no matter what was asked of it.
`test_create_calls_insert` fails the same way from the other side:
a fresh mock connection, never routed through anything resembling
the real driver, checked only for a substring of the SQL string.

## The real thing is cheaper than you think

A real sqlite file in `tmp_path`, a `testcontainers` Postgres, or a
real HTTP server on localhost each cost a few lines of setup and a
fraction of a second per test. In return you get a suite that runs
the actual query, the actual schema, the actual constraint.

**[executed]** from the example repository, `tests_real/test_repo.py`
(full).

```python
import sqlite3
import pytest
from orders.repo import OrderRepo, OrderNotFound


def make_repo(tmp_path):
    conn = sqlite3.connect(tmp_path / "orders.db")
    repo = OrderRepo(conn)
    repo.migrate()
    return repo


def test_create_then_get_round_trip(tmp_path):
    repo = make_repo(tmp_path)
    order_id = repo.create(
        {"subtotal": "10.00", "total": "9.00", "code": "SAVE10"}
    )
    row = repo.get(order_id)
    assert row["total"] == "9.00"
    assert row["paid"] is False


def test_mark_paid_unknown_id_raises(tmp_path):
    repo = make_repo(tmp_path)
    with pytest.raises(OrderNotFound):
        repo.mark_paid(999)


def test_mark_paid_twice_is_idempotent(tmp_path):
    repo = make_repo(tmp_path)
    order_id = repo.create(
        {"subtotal": "10.00", "total": "9.00", "code": "SAVE10"}
    )
    repo.mark_paid(order_id)
    repo.mark_paid(order_id)  # must not raise
    assert repo.get(order_id)["paid"] is True
```

`make_repo` opens a real file under `tmp_path` and runs the actual
`migrate()` against it; no connection is faked anywhere in the
file. Every assertion checks what the database holds after the
call, not what a mock was told to say.

**[executed]** from the example repository, `tests_real/test_service.py`
(full).

```python
import sqlite3
from decimal import Decimal
from datetime import date
import json
import responses
from orders.repo import OrderRepo
from orders.notify import RECEIPT_URL
from orders.service import checkout


@responses.activate
def test_checkout_end_to_end(tmp_path):
    responses.add(
        responses.POST, RECEIPT_URL, json={"ok": True}, status=200
    )

    conn = sqlite3.connect(tmp_path / "orders.db")
    repo = OrderRepo(conn)
    repo.migrate()

    import requests
    order_id = checkout(repo, Decimal("100.00"), "SAVE10",
                         date(2026, 1, 1), http=requests)

    row = repo.get(order_id)
    assert row["paid"] is True
    assert row["total"] == "90.00"

    sent_body = json.loads(responses.calls[0].request.body)
    assert sent_body["total"] == "90.00"
```

The only fake in this test is `responses` intercepting the outbound
POST to the receipt service — the one real network boundary the
system has. The sqlite file, the pricing maths, and the wiring
between repository and notifier all run for real, and mutation
testing against `pricing.py` and `repo.py` shows what that buys:
38 of 101 mutants killed (63 survived) by the agent-style suite,
against 68 of 101 (33 survived) by this one.

## The smell list

Most of this is visible without running anything, just by reading
the test file for these shapes (Spadini et al. 2017; Google Testing Blog 2013).

| Smell | What it looks like | What to do |
|---|---|---|
| Mock returns the value the test asserts | `mock.return_value = X` then `assert r == X` | Assert against a real computed result |
| Asserts `.called` and nothing else | `assert mock_send.called` | Assert the arguments, then the resulting state |
| Patches the function under test | `@patch` on the very function the test names | Never patch the thing the test exists to prove |
| Mocks `sqlite3.connect` | `patch("sqlite3.connect")` | Use a `tmp_path` sqlite file instead |
| `jest.mock` of the module under test | `jest.mock("../pricing")` in a pricing test | Test the real module; mock only its true boundary |
| Three or more collaborators faked in one test | a stack of `@patch` decorators on one function | Split the test, or stop faking the cheap ones |

**[illustrative]** the same smell in TypeScript, not run.

```typescript
jest.mock("../pricing");
import { applyDiscount } from "../pricing";

const mocked = applyDiscount as jest.Mock;
mocked.mockReturnValue(90);

test("checkout applies the discount", () => {
  expect(mocked()).toBe(90); // asserts the mock, not pricing.ts
});
```

*Evidence.* The `tests_agent/test_repo.py` listing and its
line-by-line reading are [executed] from the example repository.
The `tests_real` listings and the 38/101 versus 68/101 mutation
figures are [executed] from the same repository's mutation run in
chapter 3. The three-things-worth-faking list and the smell table
are [designed], informed by (Spadini et al. 2017) and
(Google Testing Blog 2013). The TypeScript snippet is [illustrative].

# 5. Working with the agent

An agent that writes both the code and the test is grading its own
homework. You cannot fix that by asking harder; you fix it by
handing over less for it to guess at, and demanding evidence for
what it hands back. That starts before it writes a single test.

## Write the requirement first

An agent asked to "add discount codes" invents its own definition
of correct, then writes tests that agree with whatever it invented.
Give it the definition first, in observable terms, and its test has
something outside itself to answer to.

**[illustrative]** adapted from the real behaviour in
`orders/pricing.py` and `orders/repo.py`, not itself run.

```text
Requirement: checkout discount codes
Observable: apply_discount(subtotal, code, today) -> Decimal
Lives in: orders/pricing.py, called from orders/service.py

- SAVE10 takes exactly 10% off the subtotal
- FREESHIP subtracts 5.00, never below 0.00
- a code used after 2026-12-31 raises InvalidCode
- an unknown code raises InvalidCode
- mark_paid on an already-paid order is a no-op
- mark_paid on an unknown order id raises OrderNotFound
```

Nine lines, and every line is something you can point at
when the agent's own tests disagree with it. If it cannot write
this itself from the ticket, do not let it write the test either —
write the requirement together first, then hand it over.

## Make it show you red before green

Ask for the failing test before any fix, and ask to see it fail.
Then you know it fails for the reason you expect, not an unrelated
import error, and you have proof that this check can fail at all. Refuse any test that was written and merged
without ever being shown red; you have no way of knowing what, if
anything, it would have caught.

**[executed]** from the example repository, `tests_real`, with bug
(a) planted — SAVE10 giving 1% off instead of 10% — the same run
shown in chapter 3's break-it-on-purpose section.

```console
$ python -m pytest -q tests_real
..F..F.....F                                                    [100%]
3 failed, 9 passed in 0.24s
FAILED tests_real/test_pricing.py::
  test_save10_is_exactly_ten_percent_off
FAILED tests_real/test_pricing.py::test_code_valid_on_expiry_day
FAILED tests_real/test_service.py::test_checkout_end_to_end
```

That is what "red before green" should look like pasted into a
pull request: a command, a failure, the exact assertion that broke.
Not a screenshot of a green run and a claim about what used to fail.

## Fewer tests, on purpose

Twelve tests for a four-line pricing rule is not thoroughness, it
is padding: more surface for the next refactor to trip over, more
time spent reading, and most of them answer to nothing you asked
for. When a pull request arrives with a large suite you did not
request, delete it and regenerate from the requirement block rather
than pruning by eye — pruning keeps whatever happens to survive a
skim, regeneration keeps only what the requirement demands. Cap the
count at one test per requirement line, plus one for the happy path
the first line already implies, and make the agent justify anything
over that in the description.

## Rules to paste into CLAUDE.md

**[illustrative]** ready to paste into a repository's `CLAUDE.md`,
not itself run.

```markdown
## Testing rules for agents working in this repo

1. Never mock a module this repo owns; use the sqlite fixture in
   `conftest.py` for anything that touches the database.
2. Never mock the function or class the test is named after.
3. Every new test must be shown failing once, on the code before
   your change, before it is shown passing.
4. Do not add a test that only asserts a mock was called.
5. Do not patch `sqlite3.connect`, `requests`, or any HTTP client
   directly; fake `responses` at the outbound call only.
6. One test per line of the requirement block. No more without
   asking first.
7. State the requirement in the pull request description before
   writing the test.
8. If a test would still pass with the function's body replaced by
   `pass`, delete it and write one that would not.
9. Run mutation testing on changed lines before asking for review;
   report the kill rate in the description.
10. Quote the exact failing assertion from the red run in the pull
    request, not a description of it.
```

## What to demand in the PR

A green suite is not the deliverable; the pull request description
is where you check that it meant something. Ask for four things
every time, and reject a submission that offers a green tick in
place of any one of them. Anthropic's own guidance for agentic
coding says the same: give the agent a way to verify its work, and
keep the writing and the checking apart (Anthropic 2025).

**[illustrative]** paste into the pull request template.

```markdown
## Test evidence

**Requirement**: <copy the relevant lines from the requirement
block>

**Red -> green**: <paste the failing pytest run, then the passing
one>

**Mutation result on changed lines**: <killed>/<survived>, e.g. 9/11

**Mock density on changed test files**: <mock_density.sh output,
or "none">
```

*Evidence.* The requirement block, the CLAUDE.md rules, and the
pull request template are [designed], built to match the real
behaviour in `orders/pricing.py` and `orders/repo.py`. The red run
is [executed], from the example repository's bug (a) run described
in chapter 3. The case for keeping the writer and the checker apart
is [documented] in Anthropic's own agentic-coding guidance.

# 6. A second agent as the reviewer

The agent that wrote the code cannot review it. Ask it to check its
own diff and it reads back what it meant to write, not what the diff
says. It remembers the requirement in the shape it already turned
into code, so every branch it never thought of the first time round
stays invisible the second time too. Agreement with yourself is not
review. It is the same inference, run twice, by the same model, over
the same code (Panickssery, Bowman, and Feng 2024).

So the reviewer has to be a different session, with none of the
first agent's memory to lean on. Open a fresh session. Give it two
things only: the diff, and the requirement it is meant to satisfy.
Do not hand it the first agent's transcript, its explanation of what
it did, or its own tests. Those are exactly the material the first
agent's confidence was built from, and a reviewer that reads them
will end up agreeing with the account it was just given rather than
checking the diff against the requirement.

A prompt you can paste into that fresh session, alongside the diff
and the requirement and nothing else. **[illustrative]**, built to
the shape of the unit-qa skill's review passes.

```text
You are reviewing a pull request. You did not write it and
you have not seen any discussion of it.

Attached: the diff, and the requirement it claims to
satisfy. Nothing else. Do not ask for the author's
explanation, test output, or transcript.

Do this:
1. List what would have to be true for the requirement to
   hold. One line per condition.
2. Check the diff against that list, not against how
   plausible the code looks.
3. For each condition you cannot confirm by reading, write a
   test that fails against the code before this diff and
   passes against the code after it. Run both.
4. If you cannot write such a test, find a mutant of the
   diff that the existing suite fails to catch, and show it.
5. Report FAIL only with the failing-then-passing test or
   the surviving mutant attached. An unsupported claim is
   not a finding.

Hand back: PASS or FAIL per condition, with the evidence for
every FAIL attached.
```

What the reviewer hands back has to be evidence, not opinion. "This
looks wrong" is not a finding. A test that is red against the parent
commit and green against the diff is a finding. A mutant the
existing suite lets through is a finding. If the second agent cannot
produce either one, it has not reviewed anything, whatever prose it
writes underneath.

Give it somewhere to spend its attention first, rather than let it
wander the whole diff evenly. The unit-qa skill ranks its own attack
classes by blast radius, and a reviewer working through a diff
should do the same, working down this list before it runs out of
time rather than up it:

- money and billing paths
- auth and tenancy boundaries
- deletion and retention behaviour
- export payloads
- scheduled or background writes

Then treat whatever the reviewer files as a hypothesis, not a
verdict, until someone or something else has cross-checked it. A
confident FAIL from a second agent is still one model's inference,
and it can be wrong in the same way a first agent's PASS can be
wrong. In the Prague campaign, six of the reviewing agents' own FAIL
claims were refuted on cross-check against shots, source or the
database, before a single one of them reached the findings ledger.
That check is not optional overhead bolted on afterwards; it is what
turns a second opinion into review.

*Evidence.* The refuted-FAIL count and the attack-class ranking are
[reported] in the unit-qa and Prague campaign material; the reviewer
prompt is [illustrative], built to the same shape as the practice it
describes.

# 7. Testing the UI with agents

Testing a user interface with agents fails the same way agent-written
unit tests fail, unless you put a structure around it first. The
Prague campaign's discipline scales to a whole product because it
never gives one agent more than one feature, and it never accepts a
claim on one kind of proof alone.

Before any agent touches a browser, write the feature list. One row
per feature: an id, the entry point it starts from, the exact
control it acts on, whether it mutates data, the feature flag it
sits behind, its current status, and where its findings live. A drag
surface gets its own row too, on the same terms as any other
feature. On the Prague campaign that list ran to 117 rows — 88
features and 29 drag surfaces — tracked in one file, so nobody has
to remember what still needs checking. **[adapted]** from the
Prague feature map's row schema; the values are made up.

```yaml
id: F-042
entry_point: /dashboards/:id, "Add Widget" button
control: widget-picker-confirm
mutates_data: true
feature_flag: dashboards_v3
status: not_run
runbook: briefs/dashboards-v3.md
last_run: null
findings: null
```

Dispatch one agent per row, never more than one, from the same brief
every time. A fixed brief keeps an agent from wandering off the
feature it was sent to check, and it means two different agents
produce comparable evidence for the same row instead of two
different kinds of story.

**[adapted]** from the Prague campaign's brief template, cut to
the lines that matter.

```text
Feature: F-042 - dashboards_v3 widget picker
Entry point: /dashboards/:id, "Add Widget" button
Do: confirm a widget can be added and that it persists

Rules:
- Any object you create is prefixed qa-<UTC timestamp>-.
- Clean up what you create, and show the cleanup worked.
- A toast is not evidence. See the truth rule below.
- Evidence per claim: a screenshot, the network request
  and its status, and the stored state after a reload.

Report: PASS, FAIL or UNVERIFIED, with evidence attached.
```

The unit-qa skill and the Prague campaign state the same rule
under the same name. **[adapted]** from both sources' wording.

```text
THE TRUTH RULE

A toast, a spinner, or any other on-screen success message
is not evidence.

Before you accept a claim:
- get the real HTTP status the write returned
- reload the page and check the state persisted
- re-check the same effect via every path in the UI that
  can trigger it, not just the one you used first
```

Every claim needs all three forms of evidence attached, not
whichever one was easiest to grab: a screenshot for what a user
would see, the network request for what actually passed between
browser and server, and a read of the stored state after a reload
for what actually survived. Reach for the screenshot last, not
first. It is the most expensive check to take and the easiest to
misread, so it belongs to recording a finding you already have,
not to discovering one.

Run the bulk of the rows headless, through a driver, for speed.
Reserve a real browser for anything that needs an actual pointer:
drag, hover, anything a headless engine has to fake rather than
perform. The Prague campaign found the difference the hard way — its
headless lane reported hover-animated elements as unclickable, and
that false finding was only caught by cross-checking the same
elements in a real Chrome tab before filing. Tooling built on the
Model Context Protocol now lets an agent drive that real browser
directly, reading the page's accessibility tree instead of guessing
from pixels (Microsoft 2026).

When a claim survives, file it with enough detail that someone else
can repeat it without you in the room. Prague's ISSUE-023 is the
model: a pipeline write that silently latched into a broken state,
kept alive on purpose as evidence rather than cleaned up.
**[adapted]** from the Prague findings ledger, ISSUE-023.

```text
ISSUE-023 - pipeline write latches into ref_error state

What we did: ran a normal pipeline task against dataset
2530.
What we saw: the UI reported success; no error surfaced.
What actually happened: the task's view (view 4397) latched
into the ref_error state with no recovery path - a silent
failure behind what looked like a successful write.

Repro: re-run the same task type against dataset 2530; view
4397 remains preserved in the latched state as evidence and
must not be removed from Trash.

Evidence: a screenshot of the "success" state, the network
log showing the underlying error, and the stored ref_error
state read back after a reload.
```

Keep a standing regression ledger too, checked every run rather than
rediscovered each time. Prague holds five such rows, R-01 through
R-05, and a run is not finished until all five have been re-checked,
not just the feature the agent was sent to test. Your own ledger
might carry a line like this. **[illustrative]**.

```text
R-01  free-shipping code on a tax-exempt order - re-check
      every run since 2026-08-14, last confirmed fixed.
```

*Evidence.* The feature-list schema, the two-lane browser split and
ISSUE-023 are [adapted] from the Prague campaign digest; the truth
rule is [adapted] from wording shared by the unit-qa and Prague
sources; the brief keeps the real verdict vocabulary from unit-qa.
The regression-ledger line is [illustrative]. The accessibility-tree
browser tooling is [documented] in the Playwright MCP release.

# 8. Gates in CI and after you ship

## The pipeline

A green pytest run in CI proves nothing more than one on a laptop, unless the same checks run on every pull request automatically. Everything in Chapters 2 and 3 is a discipline you can skip when you are busy, which on a real team means it gets skipped most weeks, by whoever is under the most pressure that day. A gate that runs itself does not care how busy anyone is.

That means the pipeline has to do three separate jobs, not one. It has to run the suite, which catches nothing new but stops an obviously broken change. It has to flag the shape of the tests themselves — the mock-to-assert ratio from `mock_density.sh` costs almost nothing to run and catches the pattern from Chapter 1 before anyone reads a single test by hand. And it has to run mutation analysis on the lines a pull request actually changed, with a threshold set from your own baseline, not copied from this book.

**[illustrative]** a job that runs the suite, checks mock density on changed test files, runs mutation on changed source files against a threshold, and quarantines flaky tests instead of retrying them silently:

```yaml
name: qa-gates
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}
      - run: pip install -r requirements.txt
      - run: python -m pytest -q --ignore=tests_flaky

      - name: mock density, changed test files only
        run: |
          F=$(git diff --name-only origin/main... -- 'tests*/*.py')
          [ -z "$F" ] || bash scripts/mock_density.sh $F

      - name: mutation, changed source files only
        run: |
          S=$(git diff --name-only origin/main... -- 'orders/*.py')
          [ -z "$S" ] || python scripts/mutate_changed.py $S \
            --min-kill-rate "$MIN_KILL_RATE"

  flaky_quarantine:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest -q tests_flaky
```

The mutation step calls a script you write yourself: a dozen lines that run `mutmut` on the listed files, read the killed and survived counts off the summary line shown in Chapter 3, and exit non-zero below the threshold.

A flaky test in the main job blocks a merge for a reason nobody can act on. Moving it to its own job, marked to continue on error, keeps it visible on every run without letting it block anyone or silently retrying itself into a false green. Auto-retry on failure is worse than either option: it makes a flaky test look identical to a stable one in the run history, and the only signal that something needs fixing — a first attempt going red — is exactly what gets thrown away.

**[executed]** `scripts/mock_density.sh`, full:

```bash
#!/usr/bin/env bash
# Mock/patch count vs assert count per file; exit 1 above THRESHOLD.
set -euo pipefail
THRESHOLD="${THRESHOLD:-0.5}"
FILES=("$@")
if [ "${#FILES[@]}" -eq 0 ]; then
    FILES=($(git diff --name-only -- '*.py' 2>/dev/null || true))
fi
STATUS=0
PAT='\b(mock|patch|MagicMock|jest\.mock)\b'
for f in "${FILES[@]}"; do
    [ -f "$f" ] || continue
    mocks=$( (grep -Eo "$PAT" "$f" || true) | wc -l)
    asserts=$( (grep -Eo '\bassert\b' "$f" || true) | wc -l)
    read -r ratio over <<< "$(awk -v m="$mocks" -v a="$asserts" \
        -v t="$THRESHOLD" 'BEGIN{
        if(a==0){r=(m>0)?"inf":"0.00";o=(m>0)?1:0}
        else{r=sprintf("%.2f",m/a);o=(m/a>t)?1:0}
        print r, o}')"
    printf '%-30s mocks=%-3s asserts=%-3s ratio=%s\n' \
        "$f" "$mocks" "$asserts" "$ratio"
    [ "$over" -eq 1 ] && STATUS=1
done
exit $STATUS
```

**[executed]** run against both suites:

```text
$ bash scripts/mock_density.sh tests_agent/test_pricing.py \
    tests_agent/test_repo.py tests_agent/test_service.py
tests_agent/test_pricing.py    mocks=0   asserts=3   ratio=0.00
tests_agent/test_repo.py       mocks=8   asserts=4   ratio=2.00
tests_agent/test_service.py    mocks=20  asserts=4   ratio=5.00
exit=1

$ bash scripts/mock_density.sh tests_real/test_pricing.py \
    tests_real/test_repo.py tests_real/test_notify.py \
    tests_real/test_service.py
tests_real/test_pricing.py     mocks=0   asserts=4   ratio=0.00
tests_real/test_repo.py        mocks=0   asserts=3   ratio=0.00
tests_real/test_notify.py      mocks=0   asserts=1   ratio=0.00
tests_real/test_service.py     mocks=0   asserts=3   ratio=0.00
exit=0
```

A flat zero across every real-suite file against a ratio running up to five-to-one on the agent suite, from a twenty-four line grep script, before either suite is even run for mutation. That gap is cheap to catch early, and cheap enough to run on every pull request without anyone noticing the extra time. Nobody had to read a diff or wait for a mutation run to see it — the script does not know what a mock is beyond a regular expression, and it still separated the two suites correctly on every file.

## After you ship

A bug that reaches production and gets fixed without a new test is a bug that can come back the same way. Before the fix merges, write the test that would have caught it, run it against the code as it stood before the fix, and confirm it fails there — the same red-then-green discipline as any other test, discovered a week later than anyone wanted. Put that test in the same pull request as the fix, not a follow-up ticket someone will deprioritise the moment the incident is closed. A fix without a regression test is a promise that the bug will not come back, made by the same process that let it through the first time.

What the pipeline tracks after that should not be how many tests exist. A rising test count is easy for an agent to produce on demand and tells you nothing about whether any of those tests would have caught the last incident — it is the same length-rewards-approval pattern from Chapter 2, applied to a dashboard instead of a pull request. Track change failure rate, the share of changes that cause an incident, and time to restore, because those are the numbers a customer feels, and neither can be inflated by writing more tests that do not check anything.

A large annual survey of software teams found a 25% increase in AI adoption associated with a 7.2% drop in delivery stability, and traced most of that cost to AI making it easy to ship larger batches of change at once, not to the quality of the generated code by itself (DORA and Google Cloud 2024). That points at a second lever alongside test quality: an agent that can produce a twelve-file change as easily as a two-file one will, left alone, default to the larger one, and a larger change is harder for any suite, human or agent-written, to check completely. Keeping changes small is a gate in its own right, upstream of any test at all.

Canaries close the loop on both. Ship the change to a slice of real traffic first, watch the same change-failure and time-to-restore numbers on that slice specifically, and only roll it further once they hold. A canary does not replace the suite or the mutation gate — it is what catches the failure mode neither of those can, the one that only shows up under real traffic, real data and real load, which is also exactly the boundary a mocked test can never reach.

*Evidence.* The CI job is [designed] for this book and was not run as shown. `mock_density.sh` and its output on both suites are [executed] from the example repository. The stability figure is [reported] from a large annual industry survey, not measured on the example repository.

# 9. One campaign, end to end

Over a little more than a day in September 2026, one agentic campaign
worked through every screen and drag surface of a live product, one
row at a time, and filed what it found in the open. It never touched
the backend: the deployed build stayed at one fixed commit for the
campaign's whole run, so every number below reflects that one build,
not drift underneath it.

The scope was 117 rows — 88 features and 29 drag-and-drop surfaces —
each dispatched to its own agent and checked against the truth rule
from the last chapter. Every row got a verdict.

| Severity | Count |
| --- | --- |
| Critical | 8 |
| High | 16 |
| Medium | 18 |
| Low | 33 |

Seventy-five issues in total, against a health score of 46 out of
100.

Nothing about the process was blind trust in the agents running it.
Six of the campaign's own FAIL claims were refuted on cross-check
before they were filed — the review discipline working as built. One
claim that did get filed, a "regression fixed" verdict, turned out
later to be agent error and had to be walked back after the fact:
even a campaign built entirely around cross-checking still let one
wrong claim into its own working state before catching it.

What the campaign changed was not the product; the backend build
never moved. It changed the method. Everything the campaign did by
hand — the dispatch discipline, the truth rule, the two-lane browser
split — was written back into the QA skill it started from, so the
next campaign runs it as a command instead of a habit one agent
happens to remember. That parity work was tracked row for row too:
twenty-two acceptance checks, one per mechanism the campaign had
used by hand, all reported complete and awaiting review as this
edition went to print.

*Evidence.* The scope, severity counts, health score and fixed
build commit are [reported] in the campaign's own closing report;
the refuted and walked-back claims are [reported] in campaign notes
kept alongside it; what the campaign changed in the method is
[inferred] from the follow-on work that turned its steps into
commands.

# 10. Checklists

Print these. They are the book in the form you will actually use.

## Before you accept an agent's pull request

1. The requirement is written down, and it is not the diff description. If you cannot point at it, write it now and ask the agent to re-derive the tests from it.
2. Every new test was shown red once. The PR carries the red run and the green run. No red run, no merge.
3. No test imports a mock of a module that lives in this repository. The only fakes are for network you do not own, the clock, randomness, and things that cost money or minutes.
4. No test asserts a value it planted in a mock two lines earlier, and none asserts only that something was called.
5. The mock-density check passed on the changed test files.
6. Mutation on the changed source lines is above the threshold you set, or the surviving mutants are listed with a reason each.
7. The test count is proportionate to the requirement. If there are twelve tests for three sentences of requirement, delete them and regenerate with a cap.
8. Something outside this session checked the change: a second agent with only the diff and the requirement, or a person, or a canary.

## Reviewing one test in thirty seconds

1. Does it import the real module under test, or a patched one?
2. What does the assertion compare against: a value from the real system, or a value the test itself supplied?
3. Delete the function body in your head. Does the test still pass?
4. Which planted bug would turn it red? If you cannot name one, it is not a test.
5. Does it touch the real store, or a mock of the store?
6. Is the edge case here, or only the happy path?

## When to fake something

| Fake it | Do not fake it |
|---|---|
| A third-party API you do not run | Your own modules and services |
| The clock, randomness, IDs | The database: use sqlite in a temp dir or a container |
| Anything paid, rate-limited or slow | The filesystem for small files: use a temp dir |
| An outage you need to simulate | The function under test, ever |

## Before an agent-run UI campaign

1. The feature list exists, one row per feature and per drag surface, with entry point and selector.
2. Every agent gets one row and the same fixed brief.
3. The brief carries the truth rule: a toast is not evidence; get the HTTP status, reload and check persistence, re-check via every path that triggers the same action.
4. Every claim files a screenshot, the network request, and the stored state after reload.
5. Drag, hover and pointer gestures go to a real browser, not the headless lane.
6. A FAIL from an agent is a hypothesis until cross-checked against the source, a screenshot or the database.
7. The regression ledger is re-run in full before the campaign closes.

## Every escaped bug

1. Write the regression test before the fix. Show it red on the current build.
2. Merge the fix with the test. Show it green.
3. Add the bug to the ledger with the date and the check that would have caught it.
4. Ask which gate should have stopped it, and change that gate, not just the code.

*Evidence.* The checklists are [designed]; each item restates a rule from the chapter that derives it.

# Boundaries

What this book measured is small and specific. The example repository is one service, about a hundred lines, with two test suites written to a brief; it ships under `examples/` with pinned versions, so its outputs can be re-run, but they show the mechanism, not a rate you can expect on your codebase. The agent-style suite is a composite of the patterns coding agents produce, written by hand for the comparison, not captured from a real agent session. The Prague campaign is one campaign on one product at one build, and its own two records disagree on the closing totals; the closing report's numbers are used here and the disagreement is stated in Chapter 9.

The rules about what agents do and why rest on the cited studies: the over-mocking rate is measured across commits, the length preference is measured in reward models and judges, self-preference and the failure of unaided self-correction are measured in controlled settings. The rules about what to do instead are the practice of the sources named in Chapter 7 and the standard testing literature. None of this measures whether a team following the book ships faster. The controlled evidence on speed points the other way: experienced developers were slower with early-2025 AI tools in a randomised trial, and higher AI adoption correlated with lower delivery stability in the 2024 DORA data (Becker et al. 2025; DORA and Google Cloud 2024). The claim here is narrower: that a green suite from an agent means nothing until you have made it possible for it to be red, and that doing so is cheap.

# Edition history

- **2.0.0** (2026-09-21) — rewrite for engineers. Derivation boxes and notation removed; executed example repository, scripts, agent rules, CI gates and checklists added. Supersedes 1.0.0.
- **1.0.0** (2026-09-21) — first edition.

# References

Alshahwan, Nadia, Jubin Chheda, Anastasia Finegenova, et al. 2024. "Automated Unit Test Improvement Using Large Language Models at Meta." In *ACM International Conference on the Foundations of Software Engineering (FSE), Industry Track*. <https://arxiv.org/abs/2402.09171>.

Anthropic. 2025. "Claude Code: Best Practices." <https://code.claude.com/docs/en/best-practices>.

Becker, Joel, Nate Rush, Elizabeth Barnes, and David Rein. 2025. "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity." *arXiv Preprint arXiv:2507.09089*. <https://arxiv.org/abs/2507.09089>.

DORA, and Google Cloud. 2024. "Accelerate State of DevOps Report 2024." <https://dora.dev/research/2024/dora-report/>.

Dubois, Yann, Balázs Galambosi, Percy Liang, and Tatsunori B. Hashimoto. 2024. "Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators." *arXiv Preprint arXiv:2404.04475*. <https://arxiv.org/abs/2404.04475>.

Foster, Christopher et al. 2025. "Mutation-Guided LLM-Based Test Generation at Meta." In *ACM International Conference on the Foundations of Software Engineering (FSE), Industry Track*. <https://arxiv.org/abs/2501.12862>.

Google Testing Blog. 2013. "Testing on the Toilet: Don't Overuse Mocks." <https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html>.

Hora, Andre, and Romain Robbes. 2026. "Are Coding Agents Generating Over-Mocked Tests? An Empirical Study." IEEE/ACM International Conference on Mining Software Repositories (MSR). <https://arxiv.org/abs/2602.00409>.

Huang, Jie, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2024. "Large Language Models Cannot Self-Correct Reasoning Yet." In *International Conference on Learning Representations (ICLR)*. <https://arxiv.org/abs/2310.01798>.

Microsoft. 2026. "Playwright MCP Documentation." <https://playwright.dev/docs/getting-started-mcp>.

Panickssery, Arjun, Samuel R. Bowman, and Shi Feng. 2024. "LLM Evaluators Recognize and Favor Their Own Generations." In *Advances in Neural Information Processing Systems (NeurIPS)*. <https://arxiv.org/abs/2404.13076>.

Petrović, Goran, and Marko Ivanković. 2018. "State of Mutation Testing at Google." In *International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP)*.

Singhal, Prasann, Tanya Goyal, Jiacheng Xu, and Greg Durrett. 2024. "A Long Way to Go: Investigating Length Correlations in RLHF." In *Conference on Language Modeling (COLM)*. <https://arxiv.org/abs/2310.03716>.

Spadini, Davide, Maurı́cio Aniche, Magiel Bruntink, and Alberto Bacchelli. 2017. "To Mock or Not to Mock? An Empirical Study on Mocking Practices." In *IEEE/ACM International Conference on Mining Software Repositories (MSR)*. <https://doi.org/10.1109/MSR.2017.61>.
