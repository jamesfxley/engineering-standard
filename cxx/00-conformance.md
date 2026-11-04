# CXX-00 — Conformance and enforcement bindings

This chapter inherits `EN-00` and defines its C++ bindings.

## CXX-00.1 — Resolving a diagnostic

**Statement.** A clang-tidy or compiler diagnostic must be resolved in this
order: fix the code; change the design so the rule no longer applies; suppress
at the site. Only when none of those is right does a scope-wide deviation apply.

**Rationale.** A diagnostic usually identifies a problem in the code's design.
A suppression leaves that problem in place.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** never.

**Mechanism.** review, plus the ceilings in `EN-00.6`.

## CXX-00.2 — Suppression syntax

**Statement.** A per-site suppression must be `NOLINTNEXTLINE(check[,check…])`
on the line above the offending line, or `NOLINT(check[,check…])` trailing it,
with a justification comment on the preceding line. A bare `NOLINT` naming no
check is never permitted.

**Rationale.** EN-00.4 requires each suppressed check to be named. A reserved or
ABI-mandated identifier can trigger both `bugprone-reserved-identifier` and
`readability-identifier-naming`. Name both when both apply.

`NOLINTBEGIN(check)` / `NOLINTEND(check)` are permitted for a contiguous region,
such as a generated table or a shim, and count as two suppressions.

`NOLINTNEXTLINE` applies to the next line. A justification on the directive's
line can wrap onto the following line:

```cpp
// NOLINTNEXTLINE(cppcoreguidelines-pro-type-vararg) - a smoke binary with no
// dependency beyond the package under test; iostreams would add one.
std::printf(...);          // NOT suppressed - the "next line" was the comment
```

The directive then applies to the continuation comment and suppresses nothing.
Put the justification first and the directive immediately above the code:

```cpp
// A smoke binary with no dependency beyond the package under test; iostreams
// would add one.
// NOLINTNEXTLINE(cppcoreguidelines-pro-type-vararg)
std::printf(...);
```

Review checks that the justification precedes the directive. A wrapped
same-line justification has no preceding reason; blocking lint also exposes
the unsuppressed diagnostic.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Review checks named suppressions and the preceding justification;
blocking clang-tidy checks the enabled diagnostics.

## CXX-00.3 — Scope-wide disables are registered, not added

**Statement.** A `.clang-tidy` below the repository root that disables a check
must correspond to a row in `docs/deviations.md`.

**Rationale.** A nested `.clang-tidy` with `InheritParentConfig: true` can
disable a check indefinitely without drawing attention to the decision.
Registration under EN-00.5 makes the decision visible.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review cross-checks configuration and register in both directions.

## CXX-00.4 — Do not trust `clang-tidy --fix`

**Statement.** After running `clang-tidy --fix`, the full build must be run —
host and cross where both exist — before committing.

**Rationale.** Automatic fixes can rename a declaration while missing a use,
leaving code that does not compile. They can also apply conflicting edits to a
header processed by concurrent translation units. Serialising `--fix` prevents
the conflicting edits but cannot prevent an incomplete rename.

**Enforcement.** review.
**Deviation.** never.

## CXX-00.5 — New files must be tracked before formatting

**Statement.** A new file must be tracked by version control before the
format and lint gates run on the change that adds it.

**Rationale.** Commands using `git ls-files` skip untracked files. A new file
can therefore pass local checks without being checked, then fail CI once it is
tracked. `git add -N <path>` records intent to add without staging content.

**Enforcement.** gate:format (partial), review.
**Deviation.** never.

**Mechanism.** The CI format job catches unchecked formatting after the file is
committed.

## CXX-00.6 — A translation unit missing from the compile database is not linted

**Statement.** Every tracked translation unit must appear in the merged compile
database before lint is considered meaningful. A project with a cross tree must
build both trees in its lint job.

**Rationale.** Without a compile command, clang-tidy guesses flags and can
stop at an unresolved include. The job produces output without checking the code.

A header included by no translation unit is also invisible to clang-tidy, even
if clangd diagnoses it in the editor using a guessed command. Failing on such
orphan headers exposes the gap.

**Enforcement.** gate:compile-db (full).
**Deviation.** never.

**Mechanism.** The compile-database coverage check refuses a missing translation
unit.
