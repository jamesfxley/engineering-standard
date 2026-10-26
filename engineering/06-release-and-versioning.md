# EN-06 — Release and versioning

## EN-06.1 — Semantic versioning, with the break confined to the leading component

**Statement.** A project's public surface must follow semantic versioning.
Breaking changes land only at a major version bump, or, while the major
version is 0, at a minor version bump. While the major version is 0, every other
change bumps the patch.

**Rationale.** The version is a promise to consumers about what upgrading costs.
A break in a release whose number does not announce it makes every version
number uninformative, and the next upgrade is then approached as though it might
break — which costs more than the break did.

Semantic versioning itself promises nothing below 1.0.0: anything may change at
any time. Read that way, every 0.x upgrade has to be treated as a possible
break, and a compatibility check that compares the major alone accepts any
0.x release at all. Treating the 0.x minor as the major keeps the promise for a
project that is not yet stable, and lets a check refuse the break mechanically.
1.0.0 then means something of its own: that the surface is stable.

**Enforcement.** review.
**Deviation.** never.

## EN-06.2 — Version declarations agree and are tested

**Statement.** Where a repository has a build definition or code version
constants, its version must be declared in both and asserted by a test. All
three change in one commit. A repository with neither is identified by its
release tag (EN-07.7).

**Rationale.** Where present, the build definition and the code constants are two independent
copies, and independent copies drift. A consumer reading the constant then gets
a different answer from the package metadata, which is the kind of defect that
surfaces as an inexplicable conditional-compilation bug months later.

The test is what makes this real rather than a convention: it is impossible to
bump one and forget the others, because the suite goes red immediately.

**Enforcement.** build (version test where applicable), review.
**Deviation.** never.

**Mechanism.** the version test where declarations are required; release-tag
review otherwise.

## EN-06.3 — Release notes say what to change, not what happened

**Statement.** A release must carry notes, written at the tag. Each breaking
entry must state what a consumer has to change in their code, not only what
changed in this project. Notes may be generated from the merged changes, except
the breaking entries, which are written.

**Rationale.** The reader is someone deciding whether and how to upgrade.
"`Queue::append` now returns `Result<T>`" tells them something changed; "check the
result — appending to a full queue reports failure and leaves its contents
unchanged" tells them what to do and why it matters. The second takes a
sentence more and saves an afternoon. Generation cannot produce that sentence,
which is why the breaking entries are the half that stays hand-written.

Writing them at the tag rather than maintaining a document between tags is
deliberate. A file carrying an unreleased section has to be kept current by
every change, is enforced by nothing, and is therefore the document most
reliably found stale — a project can pass every gate it has while its changelog
sits many releases behind its tree. Notes written once, at the moment the
version becomes real, have no interval in which to drift.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review; the release is not cut without them.

## EN-06.4 — Withdrawn

Dependency resolution belongs to the consuming build configuration.

## EN-06.5 — A release is validated against every supported configuration

**Statement.** Before a release, the full test suite must pass under every
supported build configuration, and any hardware-dependent claim must be
re-validated on the target.

**Rationale.** A configuration that is not tested is not supported, whatever the
documentation says. Compile-time configuration in particular fails
asymmetrically: the default configuration passes and an alternative one produces
a silent size or ABI mismatch.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** CI matrix; hardware validation is review and needs a device run.

## EN-06.6 — Never claim hardware validation without a device run

**Statement.** A statement that behaviour is hardware-validated must be backed
by a run on the target. Host tests, a cross-compile and a static gate are the
pre-merge minimum, and they are not validation.

**Rationale.** The classes of defect that only appear on target — timing,
interrupt context, memory pressure, peripheral behaviour — are exactly the ones
a host suite cannot reach. Recording them as validated makes the record worse
than absent, because it stops anyone checking.

**Enforcement.** review.
**Deviation.** never.

## EN-06.7 — A run record carries its conditions

**Statement.** A committed measurement must record the conditions that produced
it: build type, target, configuration, date, and anything that changes the
result.

**Rationale.** A measurement without conditions cannot be compared with the next
one, which is the only thing measurements are for. Build type alone can move a
result several-fold, and can decide whether an instrumented measurement was
possible at all.

**Enforcement.** review.
**Deviation.** never.

## EN-06.8 — Every source file names its licence

**Statement.** Every tracked source and header must carry an SPDX licence
identifier as its first line, in the machine-readable form
`SPDX-License-Identifier: <id>`, matching the repository's `LICENSE`.

**Rationale.** The root `LICENSE` governs the work, so the identifier changes
nothing legally. What it changes is what travels. The file is the unit that gets
lifted — a header dropped into somebody else's tree arrives with no trace of
where it came from or what terms came with it, and the root licence it was
governed by stays behind. The fixed spelling rather than a sentence saying the
same thing is what makes it readable by SPDX tooling and every licence scanner
that follows the convention.

**Enforcement.** gate:spdx (partial), review.
**Deviation.** never.

**Mechanism.** The `spdx` gate for C and C++ sources under an MIT licence;
review otherwise.
