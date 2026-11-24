# PY-05 — Dependencies

This chapter binds `EN-05.6` to Python packages. The lock tool is uv.

## PY-05.1 — Only an application has runtime dependencies

**Statement.** A package that other projects import, or that runs from a
pinned checkout, must use only the standard library at run time. An
application, a program people run together with the packages it is built
from, may declare runtime dependencies. Development tools are dependencies
of a development group, never of the package.

**Rationale.** A library's dependencies become dependencies of every
consumer, constrain the versions those consumers can resolve and extend
their supply chain. An application is the end of that chain, so its
dependencies affect only itself.

**Enforcement.** review.
**Deviation.** permitted with record — a library whose purpose is to extend
a framework depends on that framework.

## PY-05.2 — Installed packages are hash-locked

**Statement.** A project that installs packages from an index, at run time or
for development, must commit a `uv.lock`. Every install and every gate must
use the lock unchanged, and CI must refuse a lock that does not match
`pyproject.toml`.

**Rationale.** EN-05.6 pins fetched dependencies by content. The lock records
the exact version and hash of every package, including transitive ones, so a
replaced or republished file fails the install instead of entering the
build. A lock left out of date lets two machines resolve different trees from
one commit.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Gates run through `uv run --locked` or `uv sync --locked`, which
refuse a lock that needs changing. CI runs `uv lock --check`. Review checks
that no install bypasses the lock.

## PY-05.3 — A lock update is its own reviewed change

**Statement.** A dependency update must be a separate commit that changes
only the version declarations and the lock. Its body must name each package
added to or removed from the lock, including transitive ones. A lock must not
be refreshed as part of an unrelated change.

**Rationale.** A refreshed lock inside a feature change hides new transitive
packages and version moves among unrelated edits. Review cannot see them,
and a regression bisects to the wrong change.

**Enforcement.** gate:commits (partial), review.
**Deviation.** never.

**Mechanism.** The commits gate checks the `deps:` subject form from EN-07.2.
Review checks the lock diff against the body.
