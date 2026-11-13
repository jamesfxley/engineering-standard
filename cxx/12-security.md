# CXX-12 — Security

The security assumptions are defined in
[EN-01](../engineering/01-quality-gates.md).

## CXX-12.1 — Name the trust boundary

**Statement.** Every entry point taking data from outside the program must be
identified as a trust boundary, and everything crossing it must be validated
before use.

**Rationale.** Code can validate input against one invariant and then pass it
to code that assumes another. An explicit boundary identifies where validation
occurs. Inside it, code may assume validated input only if the boundary enforces
that assumption.

**Enforcement.** build (-fsanitize=fuzzer), review.
**Deviation.** never.

**Mechanism.** review; fuzzing at each boundary.

## CXX-12.2 — Validate into a type that cannot be invalid

**Statement.** Data crossing a trust boundary should be validated once into a
type whose representable values are all valid, rather than checked repeatedly at
each use.

**Rationale.** Repeated checks can be forgotten. A range-checked wire value
converted to an `enum class` cannot later be out of range. A bounded length type
likewise preserves its capacity guarantee.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-12.3 — Length is taken from the frame, never from the buffer

**Statement.** When parsing, the number of bytes consumed must be bounded by the
bytes actually received, never by a length field alone. A length field must be
validated against the remaining input before it is used.

**Rationale.** Trusting a declared length larger than the received input
permits a remote out-of-bounds read. Passing `std::span` through the interface
keeps the actual size available for comparison.

**Enforcement.** build (-fsanitize=address -fsanitize=fuzzer), review.
**Deviation.** never.

**Mechanism.** fuzzing; ASan; `std::span`-carrying interfaces (`CXX-04.1`).

## CXX-12.4 — Integer arithmetic on untrusted values is checked

**Statement.** Arithmetic combining untrusted values must be checked for
overflow before its result is used as a size or index. Examples include adding
a length to an offset and multiplying a count by a size.

**Rationale.** A wrapped `offset + length` can pass a bounds check and direct
an access elsewhere. Signed overflow is also undefined behaviour, so the
compiler can remove a check performed after overflow. Check before the operation.

**Enforcement.** build (-fsanitize=undefined), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** UBSan; `bugprone-*`.

## CXX-12.5 — No format-string or varargs interfaces on untrusted data

**Statement.** A value from outside the program must never be used as a format
string. Variadic C interfaces should be avoided in library code entirely.

**Rationale.** An attacker-controlled format string permits arbitrary reads
and often writes. Varargs lack type checking, so a mismatch between a format
specifier and its argument can cause undefined behaviour without a diagnostic.

Diagnostic and example code may use `printf`; library code may not. That scope
deviation is registered.

**Enforcement.** gate:lint (partial), compiler (-Wformat=2 -Werror=format-security), review.
**Deviation.** permitted with record, outside library
code.

**Mechanism.** `cppcoreguidelines-pro-type-vararg`; `-Wformat=2`,
`-Werror=format-security`.

## CXX-12.6 — Prefer parsing to scanning

**Statement.** Use `std::from_chars` rather than `sscanf` or `atoi`. Use
`std::string_view` and `std::span` rather than pointer arithmetic over raw
buffers.

**Rationale.** `atoi` returns zero for both zero and invalid input. `sscanf`
also uses varargs and lacks bounds checking. `std::from_chars` reports where it
stopped and why, without allocating or overrunning the input.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `cert-err34-c`, `cppcoreguidelines-pro-type-vararg`.

## CXX-12.7 — Resource exhaustion is a security property

**Statement.** Every per-connection, per-request or per-peer resource must be
bounded. Exhaustion must refuse new work predictably without failing the whole
system.

**Rationale.** An attacker can exhaust a fixed-capacity system by holding
every slot. Resource bounds and timeouts for every phase let the system reject
new work without failing.

A header-phase timeout prevents a peer from holding a connection indefinitely
by sending one byte per minute.

**Enforcement.** build (ctest), review.
**Deviation.** never.

**Mechanism.** timeout and capacity requirement IDs, with tests.

## CXX-12.8 — Secrets are not logged and not committed

**Statement.** Credentials, keys and tokens must not be written to logs, encoded
into artefacts, or committed. Where a build consumes them, the mechanism must
keep them out of the source tree and out of the binary where possible.

**Rationale.** Logs can be shared, artefacts published and committed history
retained indefinitely.

A value consumed at configure time becomes part of the artefact. A stale build
cache can retain an unintended value. Verify the value in the artefact.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; `.gitignore` for credential files.
