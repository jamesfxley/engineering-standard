# EN-02 — Specification and traceability

## EN-02.1 — Every behavioural guarantee has an ID

**Statement.** Each behavioural guarantee must have an identifier defined in the
project's normative specification, and the code and tests that implement and
exercise it must cite that identifier.

Cite the ID where the guarantee is implemented and where it is tested, not on
every line that contributes. In a comment the ID is a trailing tag after the
sentence it supports; it does not replace the explanation. Outside the
specification, a heading carries no ID, and neither does a README.

**Rationale.** A citation lets readers find the specification from the code.
They can establish which guarantees a change affects and whether a behaviour is
required or incidental.

**Enforcement.** review.
**Deviation.** permitted with record in `docs/traceability-exceptions.txt`,
for requirements no source file can express.

**Mechanism.** Review checks definitions, implementation and test citations in
both directions.

## EN-02.2 — Cite the ID, never a section number

**Statement.** Code, tests, commit messages and review comments must cite the
requirement ID, not a specification section number.

**Rationale.** Section numbers change when a document is reorganised. A
citation to a moved section can still look valid while pointing elsewhere.

**Enforcement.** review.
**Deviation.** never.

## EN-02.3 — IDs are stable and never renumbered

**Statement.** A requirement ID must never be reused or renumbered. A withdrawn
requirement keeps its number, marked withdrawn.

**Rationale.** A reused ID leaves an old citation pointing at a different
requirement that can still look plausible.

**Enforcement.** review.
**Deviation.** never.

## EN-02.4 — Prefixes classify

**Statement.** IDs must be a two-letter prefix and a number, where the prefix
names the class of requirement. The prefix set must be pinned in
`docs/requirement-prefixes.txt`. `FW` names future-work entries (`EN-03.7`)
and is not a requirement prefix.

**Rationale.** A prefix identifies the kind of guarantee without requiring
the reader to open the specification. It also groups related entries in the
traceability matrix.

Projects choose their prefixes. Common choices include `AR` for architecture
and resources, `PR` for performance, `RR` for reliability, `BR` for boundaries
and input handling, `TR` for timing, `CR` for protocol conformance, `OR` for
observability and `HR` for hardware.

Do not use one prefix for everything; it cannot classify requirements.
The prefix file distinguishes the project's requirement vocabulary from
protocol names and citations of this standard.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks the prefix set and its use in the specification.

## EN-02.5 — Every requirement has a pass criterion and a test

**Statement.** The specification must carry a traceability matrix mapping each
ID to the test that establishes it and the criterion that test applies.

**Rationale.** A pass criterion makes a requirement testable. Writing it
also exposes requirements too vague to implement.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Specification review checks the matrix, test citations and pass
criteria.

## EN-02.6 — A behaviour change lands as one change

**Statement.** Changing a behavioural guarantee must update the specification
row, the test, and the affected documents in the same change.

**Rationale.** Separate changes leave a specification that disagrees with the
implementation. A forgotten follow-up can leave that disagreement in a release.

**Enforcement.** review.
**Deviation.** never.

## EN-02.7 — The exceptions list is a backlog

**Statement.** A requirement that no source file can cite may be listed in
`docs/traceability-exceptions.txt` with a reason. An entry that becomes cited
must be reported so the list shrinks.

**Rationale.** Measurement procedures and design-review sign-offs can need
entries because no source file can cite them. The list must not hold
requirements that merely lack tests; review must identify those as uncited.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review identifies stale entries and removes them when a source
citation becomes available.

## EN-02.8 — A cross-package citation is qualified

**Statement.** A citation of a requirement defined in another package must
qualify the ID with that package's declared name, for example `codec:BR-2`.
An unqualified ID resolves within the citing package. Each qualified citation
must resolve against the specification of the dependency version being used.

**Rationale.** Packages can assign the same ID to different guarantees.
Qualification identifies the owner and prevents resolution to the wrong
guarantee. Declared package names and dependency pins make resolution
independent of sibling checkouts.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Review checks ownership and resolution against the pinned
dependency specification; there is no automated resolver.
