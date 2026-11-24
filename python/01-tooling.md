# PY-01 — Tooling and supported versions

This chapter binds `EN-01` and `EN-06.5` to Python.

## PY-01.1 — Ruff selects every rule and runs without warnings

**Statement.** The lint gate must run Ruff with `select = ["ALL"]` and an
`ignore` list in which each entry states its reason. The exclusions must
resolve every incompatibility Ruff reports, so that Ruff prints no warning.
The gate must fail on any finding and on any warning.

**Rationale.** EN-01.1 requires starting from every check. Ruff's `ALL`
selects every stable rule, including rules a later version adds when the pin
moves.

Some rules conflict. Ruff reports each conflicting pair, such as `D203` with
`D211` and `D212` with `D213`, and each rule that conflicts with its formatter,
such as `COM812`. It then ignores one rule of the pair, prints a warning and
exits 0. A gate that reads only the exit status passes while the configuration
names a rule that is not applied. Excluding one rule of each pair records the
choice; the other rule still enforces the convention.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** The lint gate runs `ruff check` without `--exit-zero` or
`--fix`, and fails on non-empty warning output. Review checks the reasons in
the `ignore` list.

## PY-01.2 — `ruff format` is the formatter

**Statement.** Owned Python must be formatted by `ruff format` at the pinned
Ruff version. The format gate runs `ruff format --check`.

**Rationale.** One formatter at one version produces one layout, so a diff
shows only meaning. Ruff's formatter shares the linter's version and
configuration, so a second pinned tool is not needed.

**Enforcement.** gate:format (full).
**Deviation.** never.

**Mechanism.** `ruff format --check` fails on any file it would change.

## PY-01.3 — Ruff and mypy versions are pinned in the repository

**Statement.** The Ruff configuration must set `required-version` to one exact
version. mypy must be an exact development dependency in the hash-locked lock
file (`PY-05.2`). Local commands and CI must use those versions.

**Rationale.** EN-01.7 requires a pin for each blocking linter. A new Ruff or
mypy release adds rules and inference changes that can fail an unchanged tree.
With the pin, that change arrives only in the commit that moves it.

**Enforcement.** gate:lint (partial), gate:type-check (partial), review.
**Deviation.** never.

**Mechanism.** Ruff refuses to run when its version does not satisfy
`required-version`. The type-check gate runs mypy from the locked environment.
Review checks that CI uses the same commands.

## PY-01.4 — The oldest and newest supported versions are tested

**Statement.** `requires-python` must declare the oldest supported CPython
version. That version must still receive security fixes from CPython. Tests
must pass on the oldest supported version and on the newest CPython feature
release. Ruff's target version and mypy's `python_version` must equal the
oldest supported version.

**Rationale.** Code that uses a newer feature passes on a developer's newer
interpreter and fails for a user on the oldest declared one. The type checker
and linter judge syntax and the standard library against one version, so
that version must be the oldest. Testing the newest release exposes removals
and new deprecation warnings before users meet them.

A version past its end of life receives no security fixes. Supporting it
keeps workarounds that no supported user needs.

**Enforcement.** build (pytest), review.
**Deviation.** permitted with record — a tool that a pinned external
environment runs may keep that environment's version as its oldest.

**Mechanism.** CI runs the tests on both versions. Review checks the
declarations against CPython's published support status.
