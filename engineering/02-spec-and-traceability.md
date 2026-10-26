# EN-02 — Specification and traceability

## EN-02.1 — Every behavioural guarantee has an ID

**Statement.** Each behavioural guarantee must have an identifier defined in the
project's normative specification, and the code and tests that implement and
exercise it must cite that identifier.

**Rationale.** Without it there is no way to answer two questions that come up
constantly: *what breaks if I change this?* and *is this behaviour required or
incidental?* A cited ID answers both from the code, and makes the specification
findable from the place that matters.

**Enforcement.** review.
**Deviation.** permitted with record in `docs/traceability-exceptions.txt`,
for requirements no source file can express.

**Mechanism.** Review checks definitions, implementation and test citations in
both directions.

## EN-02.2 — Cite the ID, never a section number

**Statement.** Code, tests, commit messages and review comments must cite the
requirement ID, not a specification section number.

**Rationale.** IDs survive a reorganisation of the document; section numbers do
not. When §7.3 becomes §8.1, every citation of §7.3 is now silently wrong — it
still reads as a valid reference and points somewhere else.

**Enforcement.** review.
**Deviation.** never.

## EN-02.3 — IDs are stable and never renumbered

**Statement.** A requirement ID must never be reused or renumbered. A withdrawn
requirement keeps its number, marked withdrawn.

**Rationale.** Same failure as EN-02.2, but worse: a reused ID makes an old
citation point at a *different requirement* that reads as plausible.

**Enforcement.** review.
**Deviation.** never.

## EN-02.4 — Prefixes classify

**Statement.** IDs must be a two-letter prefix and a number, where the prefix
names the class of requirement. The prefix set must be pinned in
`docs/requirement-prefixes.txt`.

**Rationale.** The prefix makes a citation self-describing at the point of use:
seeing `AR-1` in a comment tells you it is an architecture/resource guarantee
without opening the document. It also groups the traceability matrix
usefully.

Common prefixes, though a project picks its own: `AR` architecture and resource,
`PR` performance, `RR` reliability, `BR` boundary and input handling, `TR`
timing, `CR` protocol conformance, `OR` observability, `HR` hardware.

Do not use one prefix for everything. A single undifferentiated space defeats
the purpose.

The file identifies the project requirement vocabulary for readers, distinct
from protocol names and citations of this standard.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks the prefix set and its use in the specification.

## EN-02.5 — Every requirement has a pass criterion and a test

**Statement.** The specification must carry a traceability matrix mapping each
ID to the test that establishes it and the criterion that test applies.

**Rationale.** A requirement with no pass criterion is an aspiration. Writing
the criterion is also the cheapest review of the requirement itself: one that
cannot be stated as a criterion is usually too vague to implement.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Specification review checks the matrix, test citations and pass
criteria.

## EN-02.6 — A behaviour change lands as one change

**Statement.** Changing a behavioural guarantee must update the specification
row, the test, and the affected documents in the same change.

**Rationale.** Split across commits, the intermediate state is a specification
that lies. It is also the state that gets shipped, because the follow-up commit
is the one that gets forgotten.

**Enforcement.** review.
**Deviation.** never.

## EN-02.7 — The exceptions list is a backlog

**Statement.** A requirement that no source file can cite may be listed in
`docs/traceability-exceptions.txt` with a reason. An entry that becomes cited
must be reported so the list shrinks.

**Rationale.** Legitimate entries exist: a measurement procedure, a
design-review sign-off. What the file must not become is a place to park
requirements that simply have no test yet — that is an uncited requirement,
which review must identify.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review identifies stale entries and removes them when a source
citation becomes available.

## EN-02.8 — A cross-package citation is qualified

**Statement.** A citation of a requirement defined in another package must
qualify the ID with that package's declared name, for example `codec:BR-2`.
An unqualified ID resolves within the citing package. Each qualified citation
must resolve against the specification of the dependency version being used.

**Rationale.** Two packages may assign the same ID to different guarantees.
Qualification makes the owner explicit and prevents a plausible citation from
silently resolving to the wrong guarantee. Package names and dependency pins
determine resolution without relying on sibling checkouts.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Review checks ownership and resolution against the pinned
dependency specification; there is no automated resolver.
