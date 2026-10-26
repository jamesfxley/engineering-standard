# CXX-01 — Lexical structure and naming

## CXX-01.1 — `#pragma once`, on line 1

**Statement.** Every header must begin with `#pragma once` on its first line. An
`#ifndef` include guard must not be used. A file-level comment goes *after* the
pragma, not before it.

**Rationale.** Every compiler this standard targets supports it, and it removes
guard-name bookkeeping that a moved or renamed header silently gets wrong — a
duplicated guard name makes one of the two headers expand to nothing, with no
diagnostic.

`#ifndef` remains correct for a *configuration macro with a default*
(`#ifndef PROJECT_MAX_HEADERS`). That is not an include guard.

**Enforcement.** review.
**Deviation.** never.

## CXX-01.2 — Identifier case

**Statement.** Identifiers follow this table.

| Kind | Case | Example |
|---|---|---|
| Namespace | `lower_case` | `mylib::detail` |
| Class, struct, enum, type alias, concept | `CamelCase` | `ResponseWriter` |
| Function, method | `lower_case` | `send_credit` |
| Variable, parameter | `lower_case` | `bytes_written` |
| Private data member | `lower_case_` | `capacity_` |
| Enum constant | `UPPER_CASE` | `ParseResult::INCOMPLETE` |
| Namespace- or class-scope constant | `UPPER_CASE` | `MAX_HEADERS` |
| `static` constant | `UPPER_CASE` | |
| `constexpr` variable, at any scope | `UPPER_CASE` | `constexpr auto LIMIT = 8;` |
| **`const`-qualified local** | **`lower_case`** | `const std::size_t length = n * 2;` |

**Rationale.** Two rows are counter-intuitive and both are deliberate.

A `const`-qualified *local* stays `lower_case`. `UPPER_CASE` says "constant of
the program"; a local that merely is not reassigned is not that, and naming a
table lookup `LENGTH` says something untrue about it. Worse, the rule pushes
people to drop the `const` to avoid the shouting, which loses real information.

A local `constexpr` *is* `UPPER_CASE`. It is a compile-time constant of the
program, which is exactly what the previous row is not about. clang-tidy's
`ConstexprVariableCase` is the more specific option and wins where both apply.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with
record — an ABI-mandated or externally-specified identifier.

**Mechanism.** `readability-identifier-naming`.

## CXX-01.3 — Names say what, not how

**Statement.** A name must describe what the entity is or does, not its
representation or the mechanism behind it.

**Rationale.** The representation changes and the name then lies. `deadline_ms`
survives becoming a `std::chrono::milliseconds`; `timeout_uint32` does not.

Short conventional names are fine where the scope is small and the meaning is
established: a loop index, a coordinate, an iterator. Padding them out adds
nothing.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `readability-identifier-length` (tuned to permit the conventional
short names).

## CXX-01.4 — Include order

**Statement.** Includes must be ordered: the matching header for this translation
unit; then C++ standard library; then external dependencies; then this project's
headers. Each group separated by a blank line, each group alphabetised.

**Rationale.** The matching header first is the load-bearing part: it proves the
header is self-contained, because anything it needs and does not include fails
here rather than at some unlucky consumer.

**Enforcement.** gate:format (partial), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** clang-format's `IncludeCategories`; `misc-include-cleaner` for
completeness.

## CXX-01.5 — Include what you use

**Statement.** A file must include every header providing something it names,
and must not include headers it does not use.

**Rationale.** Transitively-obtained declarations break when the intermediate
header changes something unrelated, and the resulting error points at the wrong
file. Unused includes slow compilation and imply dependencies that are not real.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `misc-include-cleaner`; clangd `UnusedIncludes: Strict`.

## CXX-01.6 — No `using namespace` at namespace scope in a header

**Statement.** `using namespace` must not appear at namespace scope in a header.
Inside a function body, or in a `.cpp`, it is permitted.

**Rationale.** In a header it is inflicted on every consumer transitively, and
can change overload resolution in code that never asked for it — silently, and
at a distance.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with
record, in test files.

**Mechanism.** `google-build-using-namespace`.

## CXX-01.7 — Braces are not optional

**Statement.** Every `if`, `else`, `for`, `while` and `do` body must be braced,
including single statements.

**Rationale.** The unbraced form is one careless edit away from a body that
looks conditional and is not — the class of defect that has shipped in
security-critical code more than once. The cost of the rule is zero.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `readability-braces-around-statements`.
