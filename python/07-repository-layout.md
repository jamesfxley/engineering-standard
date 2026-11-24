# PY-07 — Repository layout

This chapter defines the layout of a Python project outside `docs/`, which
`EN-03.3` covers.

## PY-07.1 — The tree

**Statement.** A Python project has this shape:

```
pyproject.toml          metadata, dependencies and tool configuration
uv.lock                 PY-05.2
src/<package>/          the import package
src/<package>/py.typed  PY-02.4, where others import the package
tests/                  PY-04.1
docs/                   EN-03.3
```

A project embedded in a larger repository has this shape below its own
directory.

**Rationale.** A package at the root is importable from the working directory
whether or not its packaging metadata is correct. Under `src/` it is importable
only once installed, so every test run exercises that metadata. One shape lets
readers and tools find the configuration and the tests in every project.

**Enforcement.** review.
**Deviation.** permitted with record — a tool that runs from a pinned checkout
without installation keeps its package at the root.

## PY-07.2 — Automation is written in Python

**Statement.** A repository's own automation, including gate runners,
development commands and test helpers, must be written in Python under this
tier, not in shell scripts.

**Rationale.** A shell script escapes the lint, type and test gates that
govern the rest of the code, and its behaviour differs between shells and
operating systems. Written in Python, the automation is checked and tested
like the product.

**Enforcement.** review.
**Deviation.** permitted with record — a file that its host requires in
another language.
