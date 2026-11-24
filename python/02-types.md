# PY-02 — Types and interfaces

## PY-02.1 — mypy runs in strict mode over sources and tests

**Statement.** The type-check gate must run mypy with `strict = true`,
`warn_unreachable = true` and `enable_error_code = ["ignore-without-code"]`,
over the package sources and the tests. Ruff's `ANN` rules stay enabled.

A third-party import without type information must be resolved by a pinned
stub package or a typed wrapper module at the seam. An override that ignores
the missing import is a scope-wide disable under `PY-00.2`.

**Rationale.** Without a checker, a wrong argument type reaches a call that
tests may not exercise, and the failure appears at run time far from its
cause. Strict mode requires every function to be annotated and checks the
calls between them. Tests are included because a fake that drifts from the
interface it replaces passes tests that prove nothing.

The cost is annotation work and a further pinned tool. Code written under the
rule from the start carries little extra cost; a repository adopting it later
registers its unannotated scope under EN-00.5 and reduces it.

**Enforcement.** gate:type-check (partial), gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** The type-check gate fails on any mypy error. Ruff `ANN` rules
report missing annotations. Review checks the configuration and its scope.

## PY-02.2 — `Any` and `cast` appear only where untyped data enters

**Statement.** `typing.Any` and `typing.cast` must appear only where data
enters from an untyped source, such as decoded JSON or an untyped library,
and the value must be narrowed to a precise type at that site.

**Rationale.** `Any` switches off checking for every use of the value it
reaches. `cast` asserts a type without checking it. Confined to the point of
entry, each needs one review; spread through the code, each hides the errors
the checker exists to find.

**Enforcement.** gate:lint (partial), gate:type-check (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `ANN401` reports `Any` in an annotation. mypy's strict
mode reports `Any` returned from a typed function and unparameterised generic
types, and `warn_redundant_casts` reports a cast that does nothing. Review
checks each remaining `cast` and `Any`.

## PY-02.3 — Data crossing a module boundary has a declared type

**Statement.** A record passed between modules must be a frozen dataclass, a
`NamedTuple`, or a `TypedDict` for an external mapping. A closed set of values
must be an `enum.Enum`. A bare `dict`, `tuple` or string must not stand for
either.

**Rationale.** A dictionary with conventional keys gives the checker nothing
to check, so a misspelt key fails at run time. A string standing for one of
a few values accepts every other string. A declared type names its fields
once and lets the checker find each use.

**Enforcement.** review.
**Deviation.** permitted.

## PY-02.4 — The public interface is explicit

**Statement.** A package must mark what is private: a name outside the public
interface starts with an underscore, or lives in a module whose name starts
with one. A package that others import must ship a `py.typed` marker.

**Rationale.** EN-06.1 ties the version to the public interface, so the
interface must be visible. Without the convention, every importable name is
a candidate, and a consumer's import of a helper turns a private change into
a break. Without `py.typed`, a consumer's type checker ignores the package's
annotations.

**Enforcement.** review.
**Deviation.** never.

## PY-02.5 — Text input and output names its encoding

**Statement.** Every text-mode `open`, `read_text`, `write_text` and
subprocess text stream must name its encoding.

**Rationale.** The default encoding depends on the platform and locale, so a
file written on one machine can fail to decode on another. Naming it makes
the behaviour the same everywhere.

**Enforcement.** build (pytest), review.
**Deviation.** never.

**Mechanism.** With `PYTHONWARNDEFAULTENCODING=1` set for the test run, Python
emits an `EncodingWarning` when `open` or `io.TextIOWrapper` runs without an
encoding, and the warning filter in `PY-04.2` turns it into a failure. Review
covers subprocess streams and paths the tests do not reach.
