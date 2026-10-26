# EN-04 — Testing

## EN-04.1 — One seam per platform dependency, with a fake behind it

**Statement.** Access to hardware, the network, the filesystem, the clock or any
other environment dependency must sit behind a single interface, with a fake
implementation in the project's own testing module. Only the platform glue may
require the real thing.

**Rationale.** This is the highest-leverage structural decision in a project
that touches an environment. With it, the whole behavioural surface is testable
on a developer machine in milliseconds, and the part that genuinely needs
hardware shrinks to a thin adapter. Without it, every test needs the
environment, so the suite is slow, flaky and eventually not run.

*Single* is the load-bearing word. Two seams for the same dependency means the
fake covers one path and reality covers the other, which is worse than one seam
because it looks like coverage.

The fake belongs in the shipped source tree, not in the test directory:
downstream projects need it to test their own code against this one.

**Enforcement.** review.
**Deviation.** permitted with record.

## EN-04.2 — Tests cite the requirement they establish

**Statement.** A test that exists to establish a specified behaviour must cite
its requirement ID.

**Rationale.** It closes the loop specification review checks, and it tells the
next person whether a failing test is a broken guarantee or an over-specified
test. Those call for opposite responses.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** Review checks that each requirement has test citations and that
the tests establish its criterion.

## EN-04.3 — One behaviour per test

**Statement.** A test should establish one behaviour, and its name should say
which.

**Rationale.** A test asserting five things reports the first failure and hides
the rest, so fixing it is iterative. A name that describes the behaviour also
means the failure output alone often identifies the defect.

**Enforcement.** review.
**Deviation.** permitted.

## EN-04.4 — Test the boundaries, not the middle

**Statement.** Where a component has capacity limits, size thresholds, or
wrap-around arithmetic, tests must cover the boundary values and the values
either side, including the overflow behaviour.

**Rationale.** Defects cluster at boundaries. The interesting cases are one
below capacity, exactly capacity, one above, and — for anything with a counter —
the wrap point, which is otherwise reached only in production after weeks of
uptime.

**Enforcement.** review.
**Deviation.** never.

## EN-04.5 — An incremental consumer is tested at every split

**Statement.** A component that consumes input incrementally must be tested with
the input delivered whole and delivered in the smallest possible pieces, and
must reach the same verdict either way.

**Rationale.** This is the single most productive test shape for a parser or
protocol engine. Segmentation is chosen by the network, not by the caller, so
any state the implementation keeps across a call boundary is exercised by
feeding one byte at a time and by nothing else. The bugs it finds are exactly
the ones that appear in production and not in development.

**Enforcement.** review.
**Deviation.** permitted with record.

## EN-04.6 — Untrusted input is fuzzed

**Statement.** A component that parses input from outside the program's trust
boundary must have a fuzz target, with a corpus carried between CI runs.

**Rationale.** Hand-written tests cover the cases someone thought of.
Fuzzing covers the ones nobody did, which is where the memory-safety defects
are. Combined with sanitizers it is the highest-yield technique available for
this class of code.

**Enforcement.** build (-fsanitize=fuzzer), gate:synced-files (partial), review.
**Deviation.** permitted with record.

**Mechanism.** CI job.

## EN-04.7 — A test's literal values are the case under test

**Statement.** Under a standing deviation registered per `EN-00.5`, literal
sizes, offsets and expected values in a test may sit at the assertion rather
than being hoisted to named constants.

**Rationale.** A magic-number rule exists to stop an unexplained constant being
shared across production code. In a test the literal *is* the specification of
the case, and moving it away from the assertion that reads it makes the test
harder to check, not easier.

This is the most common legitimate scope-wide deviation. It is still registered
under EN-00.5 — with a review date — rather than assumed.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** permitted with record.

**Mechanism.** Review checks the scope, justification and registration; the
`deviations` gate counts suppressions against the language ceiling.
