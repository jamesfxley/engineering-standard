# CXX-04 — Functions and interfaces

## CXX-04.1 — Parameter passing

**Statement.**

| Intent | Signature |
|---|---|
| Read a small, cheaply-copied value | by value |
| Read a large object, no ownership | `const T&` |
| Read a contiguous sequence | `std::span<const T>` |
| Read a string, no ownership | `std::string_view` |
| Modify in place | `T&` |
| Take ownership | by value, then move; or `std::unique_ptr<T>` |
| Optional, no ownership | `const T*` (null means absent) |

**Rationale.** The signature tells callers how the function uses an argument.
`std::span` and `std::string_view` combine a pointer and length in one object so
separately passed values cannot disagree.

Do not pass a type smaller than a pointer by `const T&`; the indirection costs
more than copying it.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `performance-unnecessary-value-param`,
`performance-unnecessary-copy-initialization`.

## CXX-04.2 — A view parameter does not outlive the call

**Statement.** A `std::span` or `std::string_view` parameter must not be stored
beyond the call unless the interface documents that the caller keeps the storage
alive, and names who owns it.

**Rationale.** Views do not own their storage. A stored view can dangle when
the caller releases the storage, causing a use after free far from the site
that stored it.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `bugprone-dangling-handle`; `clang-analyzer-*`; review for the
documented case.

## CXX-04.3 — `[[nodiscard]]` on anything that reports

**Statement.** A function whose return value carries a failure indication, or
whose result is the only reason to call it, must be `[[nodiscard]]`.

**Rationale.** `[[nodiscard]]` exposes ignored results at compile time. An
unchecked capacity-limited operation can otherwise appear to accept work when
it rejected it. For example, a `Queue::append` operation that reports a full
queue with `false` must have its result checked.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `modernize-use-nodiscard`; `bugprone-unused-return-value`.

## CXX-04.4 — Return values, not out-parameters

**Statement.** A function should return its result. Out-parameters are permitted
only where a return is impossible, for example multiple results of different
lifetimes, or writing into caller-provided storage on a no-allocation path.

**Rationale.** Out-parameters cannot be `[[nodiscard]]` or used as expression
results. The call also does not show whether they were written. `std::optional`,
a small struct or `Result<T>` states the result more clearly.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-04.5 — Preconditions are checked or documented as caller obligations

**Statement.** A function must either validate its preconditions and report a
failure, or document them as caller obligations. It must not silently do
something else when they are violated.

**Rationale.** Clamping, truncating or returning a default after a precondition
failure can hide the defect without a diagnostic. See CXX-07.2.

**Enforcement.** review.
**Deviation.** never.

## CXX-04.6 — Functions stay small enough to hold in the head

**Statement.** A function should stay within the configured line and cognitive
complexity limits. Exceeding a limit signals a need to decompose the function.
It does not justify raising the limit.

**Rationale.** Cognitive complexity tracks nesting and branching, which affect
how easily a function can be reviewed. Line count alone does not capture them.

Exemptions allow long, flat tables and switches over wire formats.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `readability-function-size`,
`readability-function-cognitive-complexity`.

## CXX-04.7 — Distinguish parameters that could be confused

**Statement.** Where two adjacent parameters have the same type and swapping
them would compile but be wrong, they should be given distinct types or
combined into one object.

**Rationale.** `copy(dst, src, n)` and `copy(src, dst, n)` both compile.
Distinct types or a struct prevent a swapped-argument error.

`bugprone-easily-swappable-parameters` reports every function with two
same-typed parameters, including valid interfaces. This standard rejects the
check under EN-01.1 and EN-00.7 and leaves the judgement to review.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** review; the check is excluded with that reason in the root tool
configuration.
