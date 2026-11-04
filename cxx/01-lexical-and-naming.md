# CXX-01 — Lexical structure and naming

## CXX-01.1 — `#pragma once`, after the licence line

**Statement.** In every header, `#pragma once` must be the first line after the
SPDX licence identifier EN-06.8 requires. An `#ifndef` include guard must not be
used. Any other file-level comment goes after the pragma.

**Rationale.** Every supported compiler recognises `#pragma once`. Include
guards require names to be maintained when headers move or are renamed. Duplicate
guard names can cause a header to expand to nothing without a diagnostic.

`#ifndef` remains valid for a configuration macro with a default, such as
`#ifndef PROJECT_MAX_HEADERS`. That use is not an include guard.

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
| `const`-qualified local | `lower_case` | `const std::size_t length = n * 2;` |

**Rationale.** A `const` local is not reassigned, but need not be a program
constant. Keeping it `lower_case` preserves that distinction without discouraging
`const`.

A local `constexpr` is a compile-time program constant and uses `UPPER_CASE`.
clang-tidy's more specific `ConstexprVariableCase` option takes precedence when
both rules apply.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with
record — an ABI-mandated or externally-specified identifier.

**Mechanism.** `readability-identifier-naming`.

## CXX-01.3 — Names say what, not how

**Statement.** A name must describe what the entity is or does, not its
representation or the mechanism behind it.

**Rationale.** Names based on representation become misleading when it
changes. `deadline_ms` remains accurate if its type becomes
`std::chrono::milliseconds`; `timeout_uint32` does not.

Short conventional names are appropriate in small scopes where their meaning
is established, such as loop indices, coordinates and iterators.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `readability-identifier-length` (tuned to permit the conventional
short names).

## CXX-01.4 — Include order

**Statement.** Includes must be ordered: the matching header for this translation
unit; then C++ standard library; then external dependencies; then this project's
headers. Each group is alphabetised and separated from the next by a blank line.

**Rationale.** Including the matching header first checks that it is
self-contained. A missing include then fails in the owning translation unit
before it affects a consumer.

**Enforcement.** gate:format (partial), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** clang-format's `IncludeCategories`; `misc-include-cleaner` for
completeness.

## CXX-01.5 — Include what you use

**Statement.** A file must include every header providing something it names,
and must not include headers it does not use.

**Rationale.** Transitive declarations can disappear when an intermediate
header changes, causing an error in an apparently unrelated file. Unused
includes slow compilation and imply dependencies the file does not need.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `misc-include-cleaner`; clangd `UnusedIncludes: Strict`.

## CXX-01.6 — No `using namespace` at namespace scope in a header

**Statement.** `using namespace` must not appear at namespace scope in a header.
Inside a function body, or in a `.cpp`, it is permitted.

**Rationale.** A namespace directive in a header reaches every transitive
consumer. It can change overload resolution without a diagnostic in code far
from the directive.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with
record, in test files.

**Mechanism.** `google-build-using-namespace`.

## CXX-01.7 — Braces are not optional

**Statement.** Every `if`, `else`, `for`, `while` and `do` body must be braced,
including single statements.

**Rationale.** An edit to an unbraced body can leave a statement looking
conditional when it is unconditional. Braces prevent that ambiguity at no
runtime cost.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `readability-braces-around-statements`.
