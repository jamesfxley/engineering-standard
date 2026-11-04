# CXX-07 — Error handling

## CXX-07.1 — One error strategy per target class, stated

**Statement.** A project must state whether it uses exceptions, and must be
consistent. A library that may be consumed on a target without exception support
must not require them on any path.

**Rationale.** Mixed strategies require callers to handle both exceptions and
error returns, making omissions likely. Freestanding builds commonly disable
exceptions and run-time type information (RTTI), making a throwing library
unusable.

Without exceptions, `Result<T>`-style returns with `[[nodiscard]]` provide a
consistent strategy.

**Enforcement.** compiler (-fno-exceptions), review.
**Deviation.** never.

**Mechanism.** review; a compile-smoke build with exceptions disabled.

## CXX-07.2 — Reject, never truncate

**Statement.** Input that exceeds a capacity, or is otherwise invalid, must be
rejected with the correct error. It must not be truncated, clamped, or silently
partially accepted.

Diagnostic text a program emits about itself, such as logs and trace
annotations, is outside this input rule. It may be shortened to fit a fixed
buffer if each cut is marked in the emitted text. Each cut retains every field used to locate the
text, such as severity or source line number.

**Rationale.** Truncation can produce an incorrect value that passes later
checks. A shortened record, partially accepted sequence or shortened lookup key
can fail far from the original input.

Discarding an overlong diagnostic loses the entire message. A visible cut
marker preserves useful text without presenting it as complete (CXX-07.6).

Where the protocol defines a status for the condition, use it. An invalid
length and a checksum mismatch carry different information for the caller.
Rejection carries whatever the protocol requires to leave the peer in a defined
state, including a connection-close indication when framing can no longer be
trusted.

**Enforcement.** build (ctest -fsanitize=fuzzer), review.
**Deviation.** never.

**Mechanism.** boundary tests per requirement ID; fuzzing.

## CXX-07.3 — Any tolerance needs a citation

**Statement.** Where an implementation accepts input a strict reading of its
specification forbids, the tolerance must be justified by a citation to the
governing document, recorded in the project's specification.

**Rationale.** Undocumented tolerances accumulate into a dialect and create
compatibility obligations. A citation establishes whether the governing
specification permits each tolerance.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; the specification row.

## CXX-07.4 — Errors are not swallowed

**Statement.** An error must be handled or propagated. It must not be discarded,
logged-and-continued where continuing is not valid, or converted to a default
value.

**Rationale.** An empty `catch (...) {}` and an ignored error return both let
the system continue in an unhandled state, risking corruption. Logging alone
handles no error; continuing after a log is correct only when continuing is valid.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `bugprone-empty-catch`, `bugprone-unused-return-value`,
`cert-err33-c`.

## CXX-07.5 — Destructors and move operations do not throw

**Statement.** A destructor must not throw. Move operations should be `noexcept`.

**Rationale.** A destructor that throws during stack unwinding terminates the
program. A move that is not `noexcept` can make standard containers copy during
reallocation, changing performance without a diagnostic.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `performance-noexcept-move-constructor`,
`bugprone-exception-escape`.

## CXX-07.6 — Failures are observable

**Statement.** A rejection or an internal failure must increment a counter or
otherwise be observable, so its rate can be measured in a running system.

**Rationale.** Correct rejection of malformed requests and systematic
misparsing of valid input can look alike from outside. Observable failure rates let maintainers identify the
second case before users report it.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** observability requirement IDs; review.
