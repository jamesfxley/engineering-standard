# CXX-12 — Security

Not safety-critical, but security-conscious: input is assumed hostile, and a
defect that a tool can find is assumed to be findable by someone else too.

## CXX-12.1 — Name the trust boundary

**Statement.** Every entry point taking data from outside the program must be
identified as a trust boundary, and everything crossing it must be validated
before use.

**Rationale.** Most input-handling defects come from data that was validated
*somewhere* and then used somewhere else that assumed a different invariant.
Naming the boundary makes the validation site explicit, so "was this checked?"
has an answer.

Inside the boundary, code may assume validated input. That assumption is only
safe if the boundary is real.

**Enforcement.** build (-fsanitize=fuzzer), review.
**Deviation.** never.

**Mechanism.** review; fuzzing at each boundary.

## CXX-12.2 — Validate into a type that cannot be invalid

**Statement.** Data crossing a trust boundary should be validated once into a
type whose representable values are all valid, rather than checked repeatedly at
each use.

**Rationale.** Repeated checking is repeated opportunity to forget. A decoded
wire value converted into an `enum class` after a range check cannot later be out
of range; a length validated into a bounded type cannot later exceed capacity.
This turns a discipline into a property.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-12.3 — Length is taken from the frame, never from the buffer

**Statement.** When parsing, the number of bytes consumed must be bounded by the
bytes actually received, never by a length field alone. A length field must be
validated against the remaining input before it is used.

**Rationale.** The canonical remote read primitive. A declared length larger
than the data present, used without checking, reads past the buffer — and with a
`std::span` correctly carried through, the check is one comparison that cannot
be forgotten.

**Enforcement.** build (-fsanitize=address -fsanitize=fuzzer), review.
**Deviation.** never.

**Mechanism.** fuzzing; ASan; `std::span`-carrying interfaces (`CXX-04.1`).

## CXX-12.4 — Integer arithmetic on untrusted values is checked

**Statement.** Arithmetic combining untrusted values — adding a length to an
offset, multiplying a count by a size — must be checked for overflow before the
result is used as a size or an index.

**Rationale.** `offset + length` wrapping produces a small number that passes a
bounds check, and the access then happens somewhere entirely different. Signed
overflow is additionally undefined, so the check may be optimised away if written
after the fact — check *before*, not after.

**Enforcement.** build (-fsanitize=undefined), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** UBSan; `bugprone-*`.

## CXX-12.5 — No format-string or varargs interfaces on untrusted data

**Statement.** A value from outside the program must never be used as a format
string. Variadic C interfaces should be avoided in library code entirely.

**Rationale.** A user-controlled format string is an arbitrary read and often an
arbitrary write. Varargs generally have no type checking, so a mismatch between
specifier and argument is undefined behaviour the compiler cannot see.

Diagnostic and example code may use `printf`; library code may not. That
distinction is a scope deviation, registered rather than assumed.

**Enforcement.** gate:lint (partial), compiler (-Wformat=2 -Werror=format-security), review.
**Deviation.** permitted with record, outside library
code.

**Mechanism.** `cppcoreguidelines-pro-type-vararg`; `-Wformat=2`,
`-Werror=format-security`.

## CXX-12.6 — Prefer parsing to scanning

**Statement.** Use `std::from_chars` rather than `sscanf` or `atoi`. Use
`std::string_view` and `std::span` rather than pointer arithmetic over raw
buffers.

**Rationale.** `atoi` has no error reporting — it returns 0 for both "zero" and
"not a number". `sscanf` combines that with a varargs interface and no bounds
checking. `std::from_chars` reports where it stopped and why, allocates nothing,
and cannot overrun.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `cert-err34-c`, `cppcoreguidelines-pro-type-vararg`.

## CXX-12.7 — Resource exhaustion is a security property

**Statement.** Every per-connection, per-request or per-peer resource must be
bounded, and exhaustion must degrade predictably — refusing new work — rather
than failing the whole system.

**Rationale.** On a fixed-capacity system, the cheapest attack is not memory
corruption but taking every slot and holding it. Bounded resources plus timeouts
on every phase turn that from an outage into a refusal.

Timeouts are the part most often missing: a peer that opens a connection and
sends one byte per minute holds a slot indefinitely unless a header-phase timeout
exists.

**Enforcement.** build (ctest), review.
**Deviation.** never.

**Mechanism.** timeout and capacity requirement IDs, with tests.

## CXX-12.8 — Secrets are not logged and not committed

**Statement.** Credentials, keys and tokens must not be written to logs, encoded
into artefacts, or committed. Where a build consumes them, the mechanism must
keep them out of the source tree and out of the binary where possible.

**Rationale.** Logs get shared, artefacts get published, and history is forever.

A build-time trap worth stating: a value consumed at configure time is baked
into the artefact and a stale build cache silently produces one built with the
*wrong* value. Verify the artefact carries what was intended rather than assuming.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; `.gitignore` for credential files.
