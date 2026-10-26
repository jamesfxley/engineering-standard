# CXX-00 — Conformance and enforcement bindings

Inherits `EN-00` entirely. This chapter records only what is specific to C++.

## CXX-00.1 — Resolving a diagnostic

**Statement.** A clang-tidy or compiler diagnostic must be resolved in this
order: fix the code; change the design so the rule no longer applies; suppress
at the site. Only when none of those is right does a scope-wide deviation apply.

**Rationale.** The check fired because the code has the shape it describes. Most
of the time the shape is the problem — a suppression preserves it and adds a
comment claiming it is fine.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** never.

**Mechanism.** review, plus the ceilings in `EN-00.6`.

## CXX-00.2 — Suppression syntax

**Statement.** A per-site suppression must be `NOLINTNEXTLINE(check[,check…])`
on the line above the offending line, or `NOLINT(check[,check…])` trailing it,
with a justification comment on the preceding line. A bare `NOLINT` naming no
check is never permitted.

**Rationale.** `EN-00.4`. The C++-specific point: where two checks fire on one
site, *name both*. A reserved or ABI-mandated identifier typically trips both
`bugprone-reserved-identifier` and `readability-identifier-naming`, and the
temptation is a bare `NOLINT` because naming one leaves the other firing. Naming
the pair is precise and the bare form is merely the lazier option.

`NOLINTBEGIN(check)` / `NOLINTEND(check)` are permitted for a genuinely
contiguous region — a generated table, a shim — and count as two suppressions.

**The wrapped-comment trap.** `NOLINTNEXTLINE` applies to the *next line*,
literally. Writing the justification on the same line so that it wraps:

```cpp
// NOLINTNEXTLINE(cppcoreguidelines-pro-type-vararg) - a smoke binary with no
// dependency beyond the package under test; iostreams would add one.
std::printf(...);          // NOT suppressed - the "next line" was the comment
```

silently suppresses nothing, because the next line is the continuation comment.
It looks correct in review and in the diff. Put the justification *first* and
the directive immediately above the code:

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

**Rationale.** `EN-00.5`. This is where the mechanism most commonly leaks in
C++: nested `.clang-tidy` files with `InheritParentConfig: true` are easy to
add, invisible in review unless someone opens them, and permanent.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review cross-checks configuration and register in both directions.

## CXX-00.4 — Do not trust `clang-tidy --fix`

**Statement.** After running `clang-tidy --fix`, the full build must be run —
host and cross where both exist — before committing.

**Rationale.** Automatic fixes can leave a partial rename that does not
compile: a declaration updated and a use missed. They can also apply conflicting
edits to a header shared by two concurrently processed translation units.
A lint command that serialises under `--fix` removes the second case; it cannot
remove the first. `--fix` is a labour saver, not an authority.

**Enforcement.** review.
**Deviation.** never.

## CXX-00.5 — New files must be tracked before formatting

**Statement.** A new file must be tracked by version control before the
format and lint gates run on the change that adds it.

**Rationale.** Commands that enumerate tracked files (`git ls-files`) do not
see an untracked file. `git add -N <path>` records the intent to add without
staging content. A file invisible to the gates can pass review unformatted and
fail CI as soon as it becomes tracked.

**Enforcement.** gate:format (partial), review.
**Deviation.** never.

**Mechanism.** CI format job catches it, one commit late.

## CXX-00.6 — A translation unit missing from the compile database is not linted

**Statement.** Every tracked translation unit must appear in the merged compile
database before lint is considered meaningful. A project with a cross tree must
build both trees in its lint job.

**Rationale.** clang-tidy invents flags for a file it has no entry for, stops at
the first unresolvable include, and reports a missing header. That is not a
finding about the code — but it *looks* like output, so a lint job can appear to
run while checking nothing.

The related trap is a header no translation unit includes yet: it is invisible
to clang-tidy entirely, while clangd happily diagnoses it in the editor by
guessing a command. A lint command failing on such orphans, rather than skipping
them, closes that gap.

**Enforcement.** gate:compile-db (full).
**Deviation.** never.

**Mechanism.** The compile-database coverage check refuses a missing translation
unit.
