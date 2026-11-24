# Enforcement matrix

This table records each clause's declared coverage. It does not certify any
consumer implementation. See the README for the vocabulary and gate contract.
Concrete diagnostic names and check boundaries are in each clause.

| Rule | Full gate coverage | Partial gate coverage | Other checks |
|---|---|---|---|
| PY-00.1 — Suppression syntax | — | gate:lint (partial); gate:type-check (partial) | review |
| PY-00.2 — Scope-wide disables are registered | — | — | review |
| PY-01.1 — Ruff selects every rule and runs without warnings | — | gate:lint (partial) | review |
| PY-01.2 — `ruff format` is the formatter | gate:format (full) | — | — |
| PY-01.3 — Ruff and mypy versions are pinned in the repository | — | gate:lint (partial); gate:type-check (partial) | review |
| PY-01.4 — The oldest and newest supported versions are tested | — | — | build (pytest); review |
| PY-02.1 — mypy runs in strict mode over sources and tests | — | gate:type-check (partial); gate:lint (partial) | review |
| PY-02.2 — `Any` and `cast` appear only where untyped data enters | — | gate:lint (partial); gate:type-check (partial) | review |
| PY-02.3 — Data crossing a module boundary has a declared type | — | — | review |
| PY-02.4 — The public interface is explicit | — | — | review |
| PY-02.5 — Text input and output names its encoding | — | — | build (pytest); review |
| PY-03.1 — Errors are not swallowed | — | gate:lint (partial) | review |
| PY-03.2 — A translated exception keeps its cause | — | gate:lint (partial) | review |
| PY-03.3 — A boundary turns an expected failure into its error form | — | — | review |
| PY-03.4 — `assert` does not validate input | — | gate:lint (partial) | review |
| PY-03.5 — A thread's or task's failure is observed | — | gate:lint (partial) | review |
| PY-04.1 — Tests mirror the package | — | — | review |
| PY-04.2 — pytest runs strict, with warnings as errors | — | — | build (pytest); review |
| PY-04.3 — The core is pure and the environment sits behind a protocol | — | gate:type-check (partial) | review |
| PY-04.4 — A stream consumer is tested from recordings | — | — | review |
| PY-04.5 — Tests are deterministic | — | — | review |
| PY-05.1 — Only an application has runtime dependencies | — | — | review |
| PY-05.2 — Installed packages are hash-locked | — | — | review |
| PY-05.3 — A lock update is its own reviewed change | — | gate:commits (partial) | review |
| PY-06.1 — A subprocess takes an argument list, never a shell | — | gate:lint (partial) | review |
| PY-06.2 — Data is never executed | — | gate:lint (partial) | review |
| PY-06.3 — Input is parsed once, at the boundary, with limits | — | — | review |
| PY-06.4 — Secrets are not logged and not committed | — | gate:lint (partial) | review |
| PY-07.1 — The tree | — | — | review |
| PY-07.2 — Automation is written in Python | — | — | review |
