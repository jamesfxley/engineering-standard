# CXX-07 — Error handling

## CXX-07.1 — One error strategy per target class, stated

**Statement.** A project must state whether it uses exceptions, and must be
consistent. A library that may be consumed on a target without exception support
must not require them on any path.

**Rationale.** Mixing strategies means every call site has to handle both, which
in practice means it handles neither. The decision is driven by the target: a
freestanding build commonly disables exceptions and RTTI, so a library that
throws is simply unusable there.

Where exceptions are unavailable, `Result<T>`-style returns with `[[nodiscard]]`
are the consistent pattern.

**Enforcement.** compiler (-fno-exceptions), review.
**Deviation.** never.

**Mechanism.** review; a compile-smoke build with exceptions disabled.

## CXX-07.2 — Reject, never truncate

**Statement.** Input that exceeds a capacity, or is otherwise invalid, must be
rejected with the correct error. It must not be truncated, clamped, or silently
partially accepted.

Diagnostic text a program emits about itself — a log message, a trace
annotation — is not input in this sense. It may be shortened to fit a fixed
buffer, on two conditions: every cut is marked in the emitted text itself, so a
reader can see the text is incomplete, and no cut removes a field a reader or a
parser locates the text by, such as a severity or a source line number.

**Rationale.** This is the most important rule in this chapter. Truncation
produces a value that passes every subsequent check and is wrong — a record cut
to fit, a sequence accepted in part, a lookup key stored short so it names
something else. The failure surfaces far from the cause, disguised as something else.

Diagnostic text is carved out because the alternative is worse for the same
reason: rejecting an overlong log line discards the whole diagnostic, and a
visible cut marker is exactly what keeps a shortened line from passing as
complete. A marked cut is observable (`CXX-07.6`); an unmarked one is not.

The correct error is part of the requirement. Where a protocol defines a status
for the condition, use that one: an invalid record length is not the same
failure as a checksum mismatch, and reporting either as a generic error loses
information the caller needs.

Rejection carries whatever the protocol requires to leave the peer in a defined
state — the correct status and a connection-close indication where the framing
can no longer be trusted.

**Enforcement.** build (ctest -fsanitize=fuzzer), review.
**Deviation.** never.

**Mechanism.** boundary tests per requirement ID; fuzzing.

## CXX-07.3 — Any tolerance needs a citation

**Statement.** Where an implementation accepts input a strict reading of its
specification forbids, the tolerance must be justified by a citation to the
governing document, recorded in the project's specification.

**Rationale.** Tolerances accumulate. Each one is individually reasonable and
collectively they mean the implementation accepts a dialect nobody has written
down — and the tolerance becomes a compatibility obligation nobody chose.

Requiring the citation forces the question of whether the specification permits
the tolerance, and often it does not.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; the specification row.

## CXX-07.4 — Errors are not swallowed

**Statement.** An error must be handled or propagated. It must not be discarded,
logged-and-continued where continuing is not valid, or converted to a default
value.

**Rationale.** `catch (...) {}` and an ignored return code are the same defect.
The system continues in a state its author did not consider, which is where
corruption comes from.

Logging is not handling. A log line and a continue is only correct where
continuing is genuinely valid.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `bugprone-empty-catch`, `bugprone-unused-return-value`,
`cert-err33-c`.

## CXX-07.5 — Destructors and move operations do not throw

**Statement.** A destructor must not throw. Move operations should be `noexcept`.

**Rationale.** A throwing destructor during stack unwinding terminates the
program. A non-`noexcept` move means standard containers silently fall back to
copying on reallocation — a large performance change with no diagnostic.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `performance-noexcept-move-constructor`,
`bugprone-exception-escape`.

## CXX-07.6 — Failures are observable

**Statement.** A rejection or an internal failure must increment a counter or
otherwise be observable, so its rate can be measured in a running system.

**Rationale.** A correctly-rejected malformed request and a systematic
misparsing of valid input look identical from outside. A counter is what
distinguishes them, and it is the only way to notice the second case before a
user reports it.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** observability requirement IDs; review.
