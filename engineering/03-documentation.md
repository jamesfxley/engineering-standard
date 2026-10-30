# EN-03 — Documentation

## EN-03.1 — Documents state what is true now

**Statement.** Documentation, specifications and code comments must state the
present state. No history, no version narrative, no justification of a decision
relative to what came before, and no ticket reference standing in for an
explanation. The bare reference EN-03.7 requires is not an exception to this: it
points at where the reasoning is kept, and carries none of it.

A date is not narrative. Where another rule requires one — the conditions on a
committed measurement (EN-06.7), the expiry on a standing deviation
(EN-00.5) — it is a fact the reader needs, and it stays.

A commit body is outside this rule. EN-07.3 requires it to state what was true
before that made the change right, which is the one place the reasoning
belongs.

**Rationale.** Narrative documentation decays the moment the thing it narrates
changes, and it decays silently — the prose still reads fine, it is just no
longer true. A reader cannot tell which sentences are current. Version control
already holds the history, more accurately and with attribution.

"Prefer no comment to a narrative one" is the operational form. A comment saying
*what an invariant is* earns its place; one saying *what this used to do* does
not.

**Enforcement.** review.
**Deviation.** never.

## EN-03.2 — The specification is normative and carries no measurements

**Statement.** The specification may state a normative gate ("at most 64 queued items,
CI-enforced"). It must not state a measured value.

**Rationale.** The two look alike and behave oppositely. A gate is a decision and
stays true until deliberately changed; a measurement is an observation of one run
on one build of one machine, and is stale immediately. Mixing them means readers
cannot tell which numbers they may rely on.

Measurements belong in a run record beside whatever produced them, with the
conditions attached — build type, hardware, date. Conditions are not a detail:
the same suite on a debug build and a release build are not comparable, and a
run record that omits which one it was is unusable.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; specification review checks this.

## EN-03.3 — `docs/` has a known shape

**Statement.** A project's `docs/` must contain a routing `README.md` and follow
the standard file set.

| File | Role |
|---|---|
| `README.md` | Routing table: what each document is, and when to read it |
| `technical-specification.md` | Normative. Requirements, budgets, traceability matrix |
| `architecture.md` | How the implementation works. Descriptive, not normative |
| `usage-guide.md` | Practical use of the public surface |
| `future-work.md` | Deferred work, one entry per deferral (`EN-03.7`) |
| `deviations.md` | Standing deviations from the coding standard (`EN-00.5`) |
| `deviation-budget.txt` | The per-language ceilings the ratchet holds (`EN-00.6`) |
| `requirement-prefixes.txt` | The pinned ID prefix set (`EN-02.4`) |
| `traceability-exceptions.txt` | Uncitable requirements (`EN-02.7`) |
| `orientation.md` | Rules true only of this repository (`EN-00.2`) |
| `Doxyfile`, `api/` | The generated reference and its output (`EN-03.4`) |

**Rationale.** The split that matters is normative versus descriptive.
Collapsing them produces a document where a reader cannot tell a commitment from
a description of how something happens to work today, and the descriptive
sentence gets implemented against as though it were specified. What is merely
planned does not belong in the normative or descriptive files; it is recorded
in `future-work.md` — see EN-03.7.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Review checks the document set and the specification structure.

## EN-03.4 — Generate the API reference from the source

**Statement.** Reference documentation for a public API must be generated from
the declarations, not maintained by hand.

**Rationale.** A hand-written reference is a second copy of the signatures, and
the copy drifts. Generation makes drift impossible, and turning on
"warn if undocumented" converts a missing doc comment into a build warning
rather than a silent omission.

**Enforcement.** gate:api-docs (partial), review.
**Deviation.** permitted.

**Mechanism.** documentation build in CI.

## EN-03.5 — Examples in documentation are compiled

**Statement.** A code example in documentation should be compiled by the test
suite rather than pasted.

**Rationale.** Pasted examples are the first thing to break on an API change and
the last thing anyone checks. An example that is a real compiled fixture cannot
go stale without failing.

**Enforcement.** build (ctest), review.
**Deviation.** permitted.

**Mechanism.** the test suite.

## EN-03.6 — Markdown destined elsewhere goes in a fenced block

**Statement.** Markdown written for somewhere else — an issue body, a pull
request description, a commit message, a snippet for another document — must be
presented inside a fenced code block.

**Rationale.** Otherwise it renders in the conversation and has to be
reconstructed by hand to be used, usually losing formatting.

**Enforcement.** review.
**Deviation.** never.

## EN-03.7 — A deferral is a `docs/future-work.md` entry, cited by its ID

**Statement.** Work deliberately not done must be recorded as an entry in the
project's `docs/future-work.md`. Each entry has a stable ID, `FW-<n>`. IDs are
append-only: an ID is never renumbered or reused, and an entry that is built or
dropped is removed without its ID being reused. Each entry has exactly these
five headings, in this order: `What is absent`, `Why it is not built`,
`What would have to be true to build it`, `Version cost`, and
`Affected repositories`.

Where the tree acknowledges a deferral — a `DEFER` note, a requirement that
stops short, a document explaining an absence — it carries the entry ID and
nothing else. The reasoning lives in the entry. A reference to another
repository's entry takes the form `<repository> FW-<n>`.

The issue tracker holds defects only.

**Rationale.** An entry in the tree is versioned with the requirement it
qualifies, so a reader of a pinned revision sees the deferral and its reasoning
together. An issue lives outside that revision and can be closed, moved or lost
without the tree changing. Append-only IDs keep every citation resolvable: a
reused ID would point an existing citation at a different deferral without any
visible change. Restricting the tracker to defects keeps its open items a list
of things that are broken.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** Review follows each `FW-<n>` reference to its heading in
`docs/future-work.md`, checks that the entry has the five headings in order,
checks that no ID was renumbered or reused, and checks that the issue tracker
holds no deferred work.

## EN-03.8 — A link between documents resolves

**Statement.** A relative link in a tracked document must name a path that
exists within the repository. An absolute URL and a bare fragment are outside
this rule.

**Rationale.** Deleting or moving a document breaks every link to it,
including links inside a normative specification, while every other gate stays
green. A reader following one cannot reach the document that was supposed to
explain the thing they were reading about. It reads as a promise the project
has already broken.

Absolute URLs are somebody else's uptime and a fragment is a heading, so neither
is checked here; the rule is about the paths a project controls.

**Enforcement.** gate:doc-links (full).
**Deviation.** never.

**Mechanism.** The `doc-links` gate.
