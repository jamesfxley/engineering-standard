# PY-04 — Testing

This chapter binds `EN-04` to Python. The test runner is pytest.

## PY-04.1 — Tests mirror the package

**Statement.** Tests must live under `tests/`, in a directory structure
mirroring the package under `src/`. A test module is named
`test_<subject>.py`. The package contains no test code; a fake required by
`EN-04.1` is shipped code and lives in the package.

**Rationale.** Matching paths make a module's tests easy to find, and a module
deleted without its tests leaves a visibly orphaned file. A package free of
test code can be built, linted and measured without exclusions.

**Enforcement.** review.
**Deviation.** never.

## PY-04.2 — pytest runs strict, with warnings as errors

**Statement.** The pytest configuration in `pyproject.toml` must set
`strict = true` and `filterwarnings = ["error"]`. An `ignore` filter for a
warning the project cannot fix must name the warning's category and module,
and is a scope-wide disable under `PY-00.2`.

**Rationale.** EN-01.3 makes warnings errors. In Python, a deprecation warning
is the only notice before a removal breaks the code. Setting the filter in
the configuration applies it to every run, not only to the gate command.

Strict mode refuses an unknown marker, a configuration warning, an ambiguous
parametrisation ID and an expected failure that passes. Each would otherwise
let a test run differently from how it reads.

**Enforcement.** build (pytest), review.
**Deviation.** never.

**Mechanism.** pytest's `strict` option, available from pytest 9.0, enables
`strict_config`, `strict_markers`, `strict_parametrization_ids` and
`strict_xfail`. Review checks the configuration and each `ignore` filter.

## PY-04.3 — The core is pure and the environment sits behind a protocol

**Statement.** Parsing, state and computation must take values and return
values, with no input or output. Each environment dependency required by
`EN-04.1` must be a `typing.Protocol` with a fake in the package. A
user-interface layer must bind the model to widgets without logic of its own,
and is tested through its framework's headless test client. A test must not
replace a module's internals with `unittest.mock.patch` where a seam exists.

**Rationale.** A pure core is tested fast and exhaustively without hardware,
network or display. Patching a module's internals couples the test to the
implementation, so a refactor breaks the test without changing behaviour.
A protocol is checked by mypy against both the real implementation and the
fake, so the fake cannot drift unnoticed.

**Enforcement.** gate:type-check (partial), review.
**Deviation.** permitted with record.

**Mechanism.** mypy checks the fake and the real implementation against the
protocol. Review checks the layering.

## PY-04.4 — A stream consumer is tested from recordings

**Statement.** A component that consumes a device or network stream must be
tested by replaying recorded input. A recording must use the stream's own
format, so a captured session can become a fixture without conversion.
Committed recordings must contain no private data.

**Rationale.** Hand-written input covers the cases the author anticipated. A
recording carries what the source really sends, including timing and
interleaving. Keeping the stream's own format means one parser serves the
live path and the tests.

**Enforcement.** review.
**Deviation.** permitted with record.

## PY-04.5 — Tests are deterministic

**Statement.** A test must not call `time.sleep` to wait for an event, read
the wall clock through `time.time` or `datetime.now`, or depend on test
order. Time must come from an injected clock and randomness from a seeded
`random.Random` instance.

**Rationale.** A test that depends on timing passes on a fast machine and
fails on a loaded CI runner. Readers learn to rerun it instead of reading the
failure, and a real defect is then dismissed as noise.

**Enforcement.** review.
**Deviation.** never.
