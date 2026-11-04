# CXX-13 — Repository layout

This chapter defines the repository layout outside `docs/`, which EN-03.3
covers. A consistent layout helps readers find files across a family.

Neither the C++ Core Guidelines nor the Google C++ Style Guide prescribes a
layout. A shared convention prevents repositories from making different choices.

## CXX-13.1 — The tree

**Statement.** A library package has this shape. In a multi-package repository,
paths are relative to the package root.

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
tests are directly under `tests/`.

A module is a target that installs public headers through a `FILE_SET HEADERS`.
A package is single-module when it has exactly one module and multi-module
otherwise. The umbrella target belongs to no module and is excluded from the
count. A target carrying only flags or configuration installs no headers and
is not a module.

Each module has one directory. Two unrelated installed header sets in one
directory are two modules that need separating, regardless of their targets'
linkage.

The module count determines the layout. Applying the count consistently avoids
repeated reassessment and tree-wide moves to correct a misclassified package.

**Rationale.** Keeping a target's sources, headers and `CMakeLists.txt` in one
directory lets a reader find its contents in one place.

The umbrella header belongs to no module. It provides the project entry point
and version constants (CXX-13.5) at `src/include/<project>/`.

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

**Rationale.** Matching directory names make a module's tests easy to find.
Deleting a module without its tests leaves a visibly orphaned directory.

Keeping tests outside `src/` also lets installation, footprint, lint and coverage
tools treat `src/` as shippable code. Tests placed beside sources would require
exclusions in every such tool, with omissions liable to go unnoticed.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; an install or footprint rule over `src/` that needs no
test exclusion is the standing check.

## CXX-13.3 — A module's headers belong to the module

**Statement.** A module's public headers live under
`src/<module>/include/<project>/<module>/`, not in a project-wide `include/`
directory. Implementation-detail headers live beside the sources that use them,
or under `detail/` per `CXX-10.2`.

**Rationale.** Keeping headers beside their module's implementation lets the
module move as one unit. A project-wide header directory makes changes span
distant paths and can leave headers behind when a module is removed.

`target_include_directories` still exports `<project>/<module>/thing.hpp`.
The on-disk location does not change the consumer's include path or the API.

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

**Rationale.** A declared development contract lets readers and tools discover
requirements consistently. Different development tools can implement the same
contract without repository-specific discovery rules.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** Review checks the presence and meaning of the development contract.

## CXX-13.5 — The advertised version is bound to the build system

**Statement.** A library advertising its version in a header must bind those
constants to the version the build system holds, by `static_assert` in a
translation unit of the library itself.

A header-only library, having no translation unit, binds them in its test suite
instead, and records why.

**Rationale.** The build version reaches package consumers through
`find_package`; the header version reaches callers reading its constants.
Updating only one misreports the version to some consumers.

Firmware and consumer builds commonly disable tests. A library-level
`static_assert` checks agreement in every build that compiles the library,
including those configurations.

**Enforcement.** compiler (static_assert), build (ctest), review.
**Deviation.** permitted with record — a header-only library, per the statement.

**Mechanism.** `static_assert` in the library; the version test as a host-side
second check.

## CXX-13.6 — Withdrawn

Shared-file distribution belongs to the consuming development tools.
