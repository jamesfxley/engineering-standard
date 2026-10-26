# CXX-13 — Repository layout

Where files go. `EN-03.3` fixes the shape of `docs/`; this chapter fixes the
rest of the tree, so that a reader arriving at any repository in a family finds
the same answer in the same place.

Layout is a convention, not a language feature, and neither the C++ Core
Guidelines nor the Google C++ Style Guide prescribes one. Left undecided it is
re-decided per repository, and the divergence is invisible until someone has to
work in two of them.

## CXX-13.1 — The tree

**Statement.** A library package has this shape. In a multi-package repository, paths in
this layout are relative to the package root.

```
CMakeLists.txt                             top-level configuration
cmake/                                     the build-system import shim
src/<module>/CMakeLists.txt                one target per module
src/<module>/include/<project>/<module>/   that module's headers
src/<module>/*.cpp
src/include/<project>/<project>.hpp        umbrella header
tests/<module>/                            mirrors src/, one directory per module
tests/consumer/                            the installed-package consumer
docs/                                      EN-03.3
examples/<name>/                           where the repository ships programs
```

A package whose library is a single module has no module subdirectories. Its
sources are `src/*.cpp`, its public headers are `include/<project>/`, and its
tests are `tests/` directly — which is the same rule, not an exception to it.

**Counting modules.** A module is a unit that installs public headers: a target
carrying a `FILE_SET HEADERS`. A package is single-module when it has exactly
one and multi-module otherwise. The umbrella target is not counted — the
umbrella belongs to no module. A target carrying only flags or configuration
installs no headers and is never a module, so a warning-set interface target
does not make a repository multi-module.

One module, one directory. A directory installing two unrelated header sets is
two modules that have not been separated yet, whatever the linkage between their
targets.

The count decides the whole layout, so it is settled by the rule above rather
than by judgement. A repository read as single-module while it already carries a
module subdirectory shipping an installed header takes a tree-wide move to
correct, and left to judgement the question is re-decided at every audit.

**Rationale.** The module is the unit of the build, so it is also the unit of
the tree: one directory carries a target's sources, its headers and its
`CMakeLists.txt`, and nothing about that target is anywhere else. A reader
answering "what is in this target?" reads one directory.

The umbrella header sits at `src/include/<project>/` rather than inside a
module because it belongs to no module. It is the project's front door and the
home of its version constants (`CXX-13.5`).

**Enforcement.** review.
**Deviation.** permitted with record — a vendored third-party tree keeps its own
layout.

**Mechanism.** Review checks one library per source directory and the declared
repository layout.

## CXX-13.2 — Tests mirror the source tree

**Statement.** Unit tests must live under `tests/`, in a directory structure
mirroring `src/`. A test for code in `src/<module>/` is in `tests/<module>/`.
Test sources are named `<subject>_test.cpp`; fuzz targets `<subject>_fuzz.cpp`.

`src/` contains no test code.

**Rationale.** Two properties, and the mirror is what gives both at once.

Tests stay adjacent to their subject: the directory name is the same, so the
test for a module is where a reader looks for it, and a module deleted without
its tests leaves an obviously orphaned directory.

`src/` stays exactly the shippable surface. An install rule, a footprint
measurement, a lint scope or a coverage filter over `src/` needs no exclusion
for test code, and a test file added later cannot silently enter one.

The alternative — tests beside sources inside each module — keeps adjacency but
loses the second property, and every tool pointed at `src/` then needs an
exclusion that is easy to forget and silent when wrong.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; an install or footprint rule over `src/` that needs no
test exclusion is the standing check.

## CXX-13.3 — A module's headers belong to the module

**Statement.** A module's public headers live under
`src/<module>/include/<project>/<module>/`, not in a project-wide `include/`
directory. Implementation-detail headers live beside the sources that use them,
or under `detail/` per `CXX-10.2`.

**Rationale.** A header collected into a project-wide `include/` is separated
from the code that owns it, so a change to a module touches two distant places
and a deleted module leaves its headers behind. Keeping them together means the
module directory is self-describing and moves as one unit.

The include *path* is unaffected: the directory nesting exists so that
`target_include_directories` on the module target exports
`<project>/<module>/thing.hpp` regardless of where the module sits on disk. The
consumer-visible spelling is the same either way, which is what makes this a
free choice rather than an API decision.

**Enforcement.** review.
**Deviation.** permitted — a single-module repository has one module, so
`include/<project>/` at the root is the same rule.

**Mechanism.** review; `CXX-10.2` governs the include path itself.

## CXX-13.4 — The root declares its development contract

**Statement.** A code repository root must provide:

- `AGENTS.md`, pointing to the same instructions and definition of done used
  by a human contributor;
- `README.md`, naming the command that runs every applicable gate;
- a declared, versioned configuration of those gates;
- formatter and analyser configuration at the root where the tools discover it;
- `LICENSE` and `docs/`, with documentation organised under `EN-03.3`.

The development tools choose the configuration filenames and command. A
contribution guide and security policy must also be available, either locally
or through the hosting service's default community files.

**Rationale.** A reader and a tool need a predictable way to discover the
repository's requirements. Declaring that contract avoids a special case for
every repository while allowing different development tools to implement it.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Review checks the presence and meaning of the development contract.

## CXX-13.5 — The advertised version is bound to the build system

**Statement.** A library advertising its version in a header must bind those
constants to the version the build system holds, by `static_assert` in a
translation unit of the library itself.

A header-only library, having no translation unit, binds them in its test suite
instead, and records why.

**Rationale.** Two records of one fact drift. The build system's version is the
one that reaches a package consumer through `find_package`; the header's is the
one reaching a consumer who reads it. A release that updates one and not the
other ships a library that misreports itself.

`static_assert` rather than a test because a test is skipped in exactly the
configurations that matter: a firmware build and a consumer build both configure
with tests off, so a test-only binding is checked only in the one tree that
never ships. The compile-time form is checked in every tree that compiles the
library at all.

**Enforcement.** compiler (static_assert), build (ctest), review.
**Deviation.** permitted with record — a header-only library, per the statement.

**Mechanism.** `static_assert` in the library; the version test as a host-side
second check.

## CXX-13.6 — Withdrawn

Shared-file distribution belongs to the consuming development tools.
