# EN-06 — Release and versioning

## EN-06.1 — Semantic versioning, with the break confined to the leading component

**Statement.** A project's public surface must follow semantic versioning.
Breaking changes land only at a major version bump, or, while the major
version is 0, at a minor version bump. While the major version is 0, every other
change bumps the patch.

**Rationale.** Version numbers tell consumers whether an upgrade can break
compatibility. An unannounced break makes future upgrades harder to assess.

Semantic versioning makes no compatibility promise below 1.0.0. Comparing only
the major version would therefore accept any 0.x release. Treating the 0.x minor
version as the breaking component lets consumers check compatibility
mechanically. Version 1.0.0 declares the public surface stable.

**Enforcement.** review.
**Deviation.** never.

## EN-06.2 — Version declarations agree and are tested

**Statement.** Where a repository has a build definition or code version
constants, its version must be declared in both and asserted by a test. All
three change in one commit. A repository with neither is identified by its
release tag (EN-07.7).

**Rationale.** Build metadata and code constants can drift when changed
separately. Consumers then see different versions depending on which they read,
which can cause conditional-compilation defects. A test exposes disagreement
as soon as one declaration changes.

**Enforcement.** build (version test where applicable), review.
**Deviation.** never.

**Mechanism.** the version test where declarations are required; release-tag
review otherwise.

## EN-06.3 — Release notes say what to change, not what happened

**Statement.** A release must carry notes, written at the tag. Each breaking
entry must state what a consumer has to change in their code, not only what
changed in this project. Non-breaking notes may be generated from merged
changes. Breaking entries are written by hand.

**Rationale.** Consumers need instructions for upgrading. Saying that
`Queue::append` returns `Result<T>` identifies a change. Telling consumers to
check the result because a full queue rejects an append and retains its contents
explains how to respond. Generated notes cannot supply those instructions.

Writing notes at the tag avoids maintaining an unreleased section throughout
development. Such a section can become stale while every gate still passes.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; the release is not cut without them.

## EN-06.4 — Withdrawn

Dependency resolution belongs to the consuming build configuration.

## EN-06.5 — A release is validated against every supported configuration

**Statement.** Before a release, the full test suite must pass under every
supported build configuration, and any hardware-dependent claim must be
re-validated on the target.

**Rationale.** An untested configuration can fail despite a passing default
build. Compile-time alternatives can cause size or ABI mismatches without a
diagnostic.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** CI matrix; hardware validation is review and needs a device run.

## EN-06.6 — Never claim hardware validation without a device run

**Statement.** A statement that behaviour is hardware-validated must be backed
by a run on the target. Host tests, a cross-compile and a static gate are not
validation; `EN-06.9` sets what a change to target code needs before merge.

**Rationale.** Host tests cannot establish target timing, interrupt behaviour,
memory pressure or peripheral behaviour. Marking them as validated discourages
the device run that could detect a defect.

**Enforcement.** review.
**Deviation.** never.

## EN-06.7 — A run record carries its conditions

**Statement.** A committed measurement must record the conditions that produced
it: build type, target, configuration, date, and anything that changes the
result.

**Rationale.** Conditions make measurements comparable. Build type alone can
change a result several-fold or determine whether instrumentation is possible.

**Enforcement.** review.
**Deviation.** never.

## EN-06.8 — Every source file names its licence

**Statement.** Every tracked source and header must carry an SPDX licence
identifier as its first line, in the machine-readable form
`SPDX-License-Identifier: <id>`, matching the repository's `LICENSE`.

**Rationale.** A source file can be copied without the root licence. An SPDX
identifier carries the licensing information with it without changing the legal
terms. Its fixed spelling lets licence scanners read it.

**Enforcement.** gate:spdx (partial), review.
**Deviation.** never.

**Mechanism.** The `spdx` gate for C and C++ sources under an MIT licence;
review otherwise.

## EN-06.9 — Target code passes its device tests before merge

**Statement.** A change to code compiled only for a target must pass, on that
target and before merge, the device tests that cover the changed code. A
requirement the change adds or alters whose behaviour a host test cannot
establish must gain a device test in the same change. A device test runs on
the target and reports pass or fail per requirement ID with an exit status;
it measures nothing.

**Rationale.** Host tests cannot reach target-only behaviour such as
peripheral bring-up, error paths, interrupt context and reset. Finding a failure
before merge attributes it to one change and keeps the default branch passing.
Waiting for a release can require searching many changes, with a flash at each
step.

Device tests are deterministic and take minutes. Keeping measurements separate
prevents verdicts from depending on thresholds that vary with the board or bench.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** The pull request's device level under `EN-07.8` names the
board, the image's source commit, the commands and the result per
requirement ID; review checks that the cases cover the changed code and each
added or altered requirement.

## EN-06.10 — A change that risks a measured figure runs its benchmarks before merge

**Statement.** A change that claims a performance figure, or that alters code
on a path whose figure the specification gates, must run the benchmarks that
measure that figure before merge and record the result with its conditions
(`EN-06.7`). Every benchmark runs before a release (`EN-06.5`).

**Rationale.** Small regressions can accumulate across changes, so a release
run compares them with the previous baseline. A change that claims a figure or
alters its path is more likely to cause a large regression. Running the relevant
benchmarks before merge attributes that regression to the change.

**Enforcement.** review.
**Deviation.** never.
