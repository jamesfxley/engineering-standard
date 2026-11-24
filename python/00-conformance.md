# PY-00 — Conformance and enforcement bindings

This chapter inherits `EN-00` and defines its Python bindings. The linter is
Ruff and the type checker is mypy (`PY-01.1`, `PY-02.1`).

## PY-00.1 — Suppression syntax

**Statement.** A per-site suppression must be `# noqa: <code>[, <code>…]` for a
Ruff finding or `# type: ignore[<code>[, <code>…]]` for a mypy finding, on the
offending line, with a justification comment on the line above it. A bare
`# noqa` or a bare `# type: ignore` naming no code is never permitted.

**Rationale.** EN-00.4 requires each suppressed check to be named. A bare
`# noqa` silences every Ruff rule on the line, including rules added by a
later version. A bare `# type: ignore` hides every type error on the line,
including the next one introduced there.

Python has no next-line form, so the directive sits on the code line and the
justification above it:

```python
# The fixture file is synthetic and written by this test.
data = pickle.loads(path.read_bytes())  # noqa: S301
```

Each named code counts as one suppression against the language ceiling in
EN-00.6.

**Enforcement.** gate:lint (partial), gate:type-check (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `PGH004` refuses a bare `noqa`, `PGH003` refuses a bare
`type: ignore` and `RUF100` refuses an unused `noqa`. mypy's strict mode
reports an unused `type: ignore` (`warn_unused_ignores`), and the error code
`ignore-without-code`, enabled in the configuration, refuses an ignore without
a code. Review checks the justification and approval.

## PY-00.2 — Scope-wide disables are registered

**Statement.** Each of these is a scope-wide disable and must correspond to a
row in `docs/deviations.md`:

- a Ruff `per-file-ignores` or `extend-per-file-ignores` entry;
- a Ruff configuration below the repository root that ignores a rule;
- a file-level `# ruff: noqa` comment, which must name its codes;
- a mypy per-module override that sets `ignore_errors`,
  `ignore_missing_imports` or `disable_error_code`;
- a file-level `# mypy:` comment that relaxes a check.

A rule disabled everywhere belongs in the root `ignore` list under EN-00.7.

**Rationale.** These settings disable a check for every line now in their
scope and for every line later added to it. Registration under EN-00.5 makes
the decision visible and gives it a review date.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review cross-checks the Ruff and mypy configuration, and
file-level comments, against the register in both directions.
