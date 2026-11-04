# EN-04 — Testing

## EN-04.1 — One seam per platform dependency, with a fake behind it

**Statement.** Access to hardware, the network, the filesystem, the clock or any
other environment dependency must sit behind a single interface, with a fake
implementation in the project's own testing module. Only the platform glue may
require the real thing.

**Rationale.** An interface isolates the environment so the behaviour can be
tested quickly on a developer machine. Only a thin platform adapter needs the
real environment. Tests that all need hardware or network access become slow
and unreliable, and eventually stop being run.

Two interfaces to one dependency can leave a real path outside the fake's
coverage. The fake belongs in shipped source, outside the test directory, so
downstream projects can use it to test their code.

**Enforcement.** review.
**Deviation.** permitted with record.

## EN-04.2 — Tests cite the requirement they establish

**Statement.** A test that exists to establish a specified behaviour must cite
its requirement ID.

**Rationale.** The citation lets specification review verify coverage. It
also helps readers distinguish a broken guarantee from an over-specified test
when the test fails.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** Review checks that each requirement has test citations and that
the tests establish its criterion.

## EN-04.3 — One behaviour per test

**Statement.** A test should establish one behaviour, and its name should say
which.

**Rationale.** A test reports its first failing assertion and hides later
failures. A name that identifies the behaviour can make the failure output
enough to locate the defect.

**Enforcement.** review.
**Deviation.** permitted.

## EN-04.4 — Test the boundaries, not the middle

**Statement.** Where a component has capacity limits, size thresholds, or
wrap-around arithmetic, tests must cover the boundary values and the values
either side, including the overflow behaviour.

**Rationale.** Defects cluster at boundaries: one below capacity, at capacity,
one above it, and at a counter's wrap point. Normal operation can take weeks
to reach the wrap point.

**Enforcement.** review.
**Deviation.** never.

## EN-04.5 — An incremental consumer is tested at every split

**Statement.** A component that consumes input incrementally must be tested with
the input delivered whole and delivered in the smallest possible pieces, and
must reach the same verdict either way.

**Rationale.** The network chooses segmentation, so development inputs can
miss failures at call boundaries. Feeding the smallest pieces exercises the
state retained between calls.

**Enforcement.** review.
**Deviation.** permitted with record.

## EN-04.6 — Untrusted input is fuzzed

**Statement.** A component that parses input from outside the program's trust
boundary must have a fuzz target, with a corpus carried between CI runs.

**Rationale.** Hand-written tests cover anticipated cases. Fuzzing explores
unanticipated inputs where memory-safety defects can hide. Sanitisers make
those defects easier to detect.

**Enforcement.** build (-fsanitize=fuzzer), gate:synced-files (partial), review.
**Deviation.** permitted with record.

**Mechanism.** CI job.

## EN-04.7 — A test's literal values are the case under test

**Statement.** Under a standing deviation registered per `EN-00.5`, literal
sizes, offsets and expected values in a test may sit at the assertion rather
than being hoisted to named constants.

**Rationale.** In production code, an unexplained shared constant hides its
meaning. In a test, a literal states the case. Keeping it at the assertion makes
the case easier to check.

The exception still needs registration and a review date under EN-00.5.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** permitted with record.

**Mechanism.** Review checks the scope, justification and registration; the
`deviations` gate counts suppressions against the language ceiling.
