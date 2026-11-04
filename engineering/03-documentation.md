# EN-03 — Documentation

## EN-03.1 — Documents state what is true now

**Statement.** Documentation, specifications and code comments must state the
present state. History, version narrative, justifications relative to a previous
state and ticket references in place of explanations are excluded.
The bare reference required by EN-03.7 points to the reasoning without copying it.

Dates are not narrative. Dates required by other rules remain, including
measurement conditions (EN-06.7) and standing-deviation expiry dates (EN-00.5).

Commit bodies are outside this rule. EN-07.3 requires them to explain the
previous state that justifies a change.

**Rationale.** History in documentation becomes stale as the implementation
changes. Readers cannot tell which sentences still apply. Version control
preserves history with attribution.

An invariant belongs in a comment. A description of what the code used to do
does not; prefer no comment to a narrative one.

**Enforcement.** review.
**Deviation.** never.

## EN-03.2 — The specification is normative and carries no measurements

**Statement.** The specification may state a normative gate ("at most 64 queued items,
CI-enforced"). It must not state a measured value.

**Rationale.** A gate is a decision that remains true until changed. A
measurement describes one run on one build and machine. Mixing the two makes
it hard to tell which numbers are commitments.

Measurements belong in a run record beside whatever produced them. The record
includes the build type, hardware and date. Results from debug and release
builds are not comparable without those conditions.

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
| `future-work.md` | Deferred work, one entry per deferral; always present (`EN-03.7`) |
| `deviations.md` | Standing deviations from the coding standard (`EN-00.5`) |
| `deviation-budget.txt` | The per-language ceilings the ratchet holds (`EN-00.6`) |
| `requirement-prefixes.txt` | The pinned ID prefix set (`EN-02.4`) |
| `traceability-exceptions.txt` | Uncitable requirements (`EN-02.7`) |
| `orientation.md` | Rules true only of this repository (`EN-00.2`) |
| `Doxyfile`, `api/` | The generated reference and its output (`EN-03.4`) |

**Rationale.** Separating normative and descriptive documents lets readers
distinguish commitments from implementation details. Planned work belongs in
`future-work.md` under EN-03.7.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Review checks the document set and the specification structure.

## EN-03.4 — Generate the API reference from the source

**Statement.** Reference documentation for a public API must be generated from
the declarations, not maintained by hand.

**Rationale.** A hand-written reference is a second copy of the signatures, and
the copy drifts. Generation makes drift impossible. Warn-if-undocumented turns a
missing doc comment into a build warning; it asks for a statement of the
contract, which for a simple member is one line (EN-03.12).

**Enforcement.** gate:api-docs (partial), review.
**Deviation.** permitted.

**Mechanism.** documentation build in CI.

## EN-03.5 — Examples in documentation are compiled

**Statement.** A code example in documentation should be compiled by the test
suite rather than pasted.

**Rationale.** An API change can break pasted examples without anyone noticing.
A compiled fixture exposes the break as a test-suite failure.

**Enforcement.** build (ctest), review.
**Deviation.** permitted.

**Mechanism.** the test suite.

## EN-03.6 — Markdown destined elsewhere goes in a fenced block

**Statement.** Markdown written for another destination must be presented in a
fenced code block. Destinations include issue bodies, pull request descriptions,
commit messages and snippets for other documents.

**Rationale.** A fence preserves Markdown for copying. Rendered Markdown needs
manual reconstruction, which can lose formatting.

**Enforcement.** review.
**Deviation.** never.

## EN-03.7 — A deferral is a `docs/future-work.md` entry, cited by its ID

**Statement.** Work deliberately not done, but which may still be built, is a
deferral. Deferrals include stated limitations and evidence gaps. An evidence
gap is a claim not yet measured or observed that the documentation presents as
unconfirmed. A defect is something wrong now: a crash
or hang the specification does not call for, other behaviour the specification
or documentation does not permit, or a statement in the code or documentation
that is untrue, including an unmeasured claim presented as established. Every
project keeps its deferrals in `docs/future-work.md`, which says so when it
has none. The issue tracker holds defects only.

Each entry is a heading `## FW-<n> — <title>` followed by exactly these five
`###` headings, in this order:

- `What is absent`.
- `Why it is not built`.
- `What would have to be true to build it`.
- `Version cost`: whether building it would be a breaking change under
  `EN-06.1`.
- `Affected repositories`: every repository the work touches, this one first,
  each other one with its entry ID where it has one.

IDs run from `FW-1` without gaps and are never renumbered or reused. An entry
that is built or dropped is replaced by a stub, `## FW-<n> — Built` or
`## FW-<n> — Dropped`, and one line saying what replaced it or why. The same
change removes the project's own citations of it. Dropped work is no longer
intended. Any remaining statement excluding that work from scope is a scope
decision.

Each acknowledgement of a deferral in the tree carries the entry ID and at most
a phrase naming the absence. Acknowledgements include `DEFER` notes,
requirements that stop short, specification exclusions and explanations of
absent features. The entry holds the reasoning.

Work that spans several repositories under this standard has an entry in each.
A citation of another repository's entry takes the form `<repository>:FW-<n>`,
for example `net-stack:FW-2`, and resolves against that repository's default
branch. When an entry is added, each other affected repository under this
standard gains a citation of it, in its existing partner entry or in a new one,
through a change opened together with the adding change. The adding change
merges first, so each partner change's citation resolves when it merges.

**Rationale.** An entry in the tree is versioned with the requirement it
qualifies. A reader of a pinned revision sees the deferral and its reasons
together. An issue can be closed, moved or lost independently of that revision.

Gapless IDs and stubs keep citations resolvable, including citations from other
repositories to built entries. They also expose removed or reused IDs. A deferral
is not a contract, so citations of another repository's entries resolve to its
current state. Only repositories under this standard can be required to keep
entries. Restricting the tracker to
defects makes its open items a list of things that are broken.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review of a change reads `docs/future-work.md` and checks that
it exists and that its IDs run from `FW-1` without gaps. For each entry the
change adds or alters, it checks the heading form and the five headings, or the
stub form, and that no ID was renumbered or reused against the base revision.
For an added entry, it checks that a change citing it is open or merged in each
other affected repository under this standard. For a new stub, it checks that the
project's citations of that ID are removed. For each acknowledgement or
citation the change adds, it checks that the ID resolves, a qualified one on
the cited repository's default branch, and that no reasoning is copied beside
it. Review of each newly opened issue, and of the open issues
before each release, closes any that does not report a defect, with a pointer
to a future-work entry or a pull request.

## EN-03.8 — A link between documents resolves

**Statement.** A relative link in a tracked document must name a path that
exists within the repository. An absolute URL and a bare fragment are outside
this rule.

**Rationale.** Moving or deleting a document can break links while other
gates still pass. A broken link prevents the reader from reaching the promised
explanation, even from a normative specification.

The project controls relative paths. Absolute URLs depend on external services,
and fragments identify headings; neither is checked by this rule.

**Enforcement.** gate:doc-links (full).
**Deviation.** never.

**Mechanism.** The `doc-links` gate.

## EN-03.9 — A document has one reader and one register

**Statement.** A document must serve the reader its routing row names, in one
register from start to end. Instructions to an agent belong in documents
written for agents, such as `AGENTS.md`, not in documents written for people.
An edit must leave the whole document in its register.

**Rationale.** A document written for two readers serves neither. Text added by
later edits in another register makes a document change tone mid-page.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review reads the whole document an edit touches, not only the
changed lines.

## EN-03.10 — Prose is plain and spare

**Statement.** Prose must use full sentences with one claim each, in the fewest
words that keep the reasons. It must not contain:

- fragments in running text (table cells, list items and field values may be
  phrases);
- stacked nouns or clauses the reader must reread to parse;
- a "this", "that" or "which" whose referent the reader must search for;
- filler or signposting ("Note that", "It is important to", "This section
  describes");
- slogans: aphorisms, "X, not Y" sentences written for effect, bold lead
  sentences, and headings written for effect instead of naming their topic;
- emphasis used for tone.

Prose uses British spelling. An identifier keeps its own spelling and is written
in code font.

**Rationale.** Compressed text costs the reader more time than it saves the
writer. Slogans and emphasis assert importance instead of explaining it.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review compares the text with the review guide's reference
examples.

## EN-03.11 — Terms are defined once and used consistently

**Statement.** A term the reader cannot be assumed to know must be defined at
its first use in the document, or in a glossary the document links. One concept
has one name within a project. Projects that share terms name them in one
shared document.

**Rationale.** An undefined term stops the reader. Two names for one thing make
the reader ask whether they are two things.

**Enforcement.** review.
**Deviation.** never.

## EN-03.12 — A comment states what the code cannot

**Statement.** A comment must state something the code does not show: a
contract, a unit, an invariant, a hazard, a required order, or an external
source. It must not restate the code, defend the code against an alternative
not taken, address a reviewer or a tool, or repeat the specification. A doc
comment is as long as its contract: a member whose name and type state the
contract takes a one-line brief. A change to code must update or remove the
comments it affects.

The justification EN-00.4 requires before a suppression is the one comment that
addresses a tool.

**Rationale.** A comment that defends a decision is never wrong, so it is never
removed. Such comments accumulate and bury the contract the reader needs.

**Enforcement.** review.
**Deviation.** never.

## EN-03.13 — Each fact has one owner

**Statement.** A fact must be stated in one document. Other documents link to
it. A policy this standard owns is cited by ID, not restated.

**Rationale.** Copies drift, and the reader cannot tell which copy is current.

**Enforcement.** review.
**Deviation.** never.
