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

**Rationale.** The signature is the documentation of what a function does with
its argument, and it is the only part a caller cannot ignore. `std::span` and
`std::string_view` in particular replace a pointer/length pair whose two halves
can disagree — the most common source of buffer defects — with one object that
cannot.

Do not take `const T&` to a type smaller than a pointer; the indirection costs
more than the copy.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `performance-unnecessary-value-param`,
`performance-unnecessary-copy-initialization`.

## CXX-04.2 — A view parameter does not outlive the call

**Statement.** A `std::span` or `std::string_view` parameter must not be stored
beyond the call unless the interface documents that the caller keeps the storage
alive, and names who owns it.

**Rationale.** They are non-owning. Storing one is a dangling reference waiting
for the caller to do something reasonable, and the failure is a use-after-free
that appears unrelated to the storing code.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `bugprone-dangling-handle`; `clang-analyzer-*`; review for the
documented case.

## CXX-04.3 — `[[nodiscard]]` on anything that reports

**Statement.** A function whose return value carries a failure indication, or
whose result is the only reason to call it, must be `[[nodiscard]]`.

**Rationale.** An ignored error return is a silent failure by construction. The
attribute costs nothing and converts it into a compile error.

This applies especially to capacity-limited operations: a `Queue::append` that
returns `false` when the queue is full must have its result checked, or a caller
can report work accepted even though the queue contains no new item.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `modernize-use-nodiscard`; `bugprone-unused-return-value`.

## CXX-04.4 — Return values, not out-parameters

**Statement.** A function should return its result. Out-parameters are permitted
only where a return is impossible — multiple results of different lifetimes, or
writing into caller-provided storage on a no-allocation path.

**Rationale.** An out-parameter cannot be `[[nodiscard]]`, cannot be used in an
expression, and gives no indication at the call site whether it was written.
`std::optional`, a small struct, or a `Result<T>` are all clearer.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-04.5 — Preconditions are checked or documented as caller obligations

**Statement.** A function must either validate its preconditions and report a
failure, or document them as caller obligations. It must not silently do
something else when they are violated.

**Rationale.** The third option — clamping, truncating, returning a default — is
the one that produces defects with no diagnostic anywhere. See `CXX-07.2`.

**Enforcement.** review.
**Deviation.** never.

## CXX-04.6 — Functions stay small enough to hold in the head

**Statement.** A function should stay within the configured line and cognitive
complexity limits. Exceeding them is a signal to decompose, not to raise the
limit.

**Rationale.** Cognitive complexity tracks nesting and branching, which is what
actually makes a function hard to reason about — closer to reviewability than a
raw line count.

A long flat table or a switch over a wire format is genuinely fine and is what
the exemptions exist for.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `readability-function-size`,
`readability-function-cognitive-complexity`.

## CXX-04.7 — Distinguish parameters that could be confused

**Statement.** Where two adjacent parameters have the same type and swapping
them would compile but be wrong, they should be given distinct types or
combined into one object.

**Rationale.** `copy(dst, src, n)` and `copy(src, dst, n)` both compile. A
strong typedef or a small struct makes the mistake impossible rather than
merely discouraged.

The generic check for this fires on every two-same-typed-parameter function,
which is most well-typed interfaces. This standard places
`bugprone-easily-swappable-parameters` on the rejected list (`EN-01.1`,
`EN-00.7`); the judgement is a review item.

**Enforcement.** review.
**Deviation.** permitted.

**Mechanism.** review; the check is excluded with that reason in the root tool
configuration.
