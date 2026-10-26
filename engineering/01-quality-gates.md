# EN-01 — Quality gates

Development is security-conscious: not safety-critical, but aiming at maximum
quality by default, on the assumption that input is hostile and that a defect
found by a tool is orders of magnitude cheaper than one found later.

## EN-01.1 — Start from every check, exclude with a reason

**Statement.** A linter must be configured as *everything on*, minus an
enumerated exclusion list where each entry states its reason. Configuring a
hand-picked subset is not permitted.

**Rationale.** The two configurations look similar and are not. An opt-in subset
omits every check nobody thought to enable — which is most of what the tool
knows, and specifically the checks covering the mistakes the team has not made
*yet*. An opt-out list is a finite set of decisions someone actually took, each
reviewable.

Exclusions fall into three kinds, and keeping them separate keeps the list
honest:

1. **Inapplicable** — checks for a platform or library the project does not use.
   Not judgements; they simply cannot fire usefully.
2. **Aliases** — a second name for a check already enabled. Both enabled means
   every finding reported twice. Alias tables are version-specific and must be
   re-derived on a tool upgrade; direction has reversed between releases.
3. **Rejected** — rules the project will not follow anywhere. This is the list
   to be suspicious of, and it is governed by EN-00.7.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** review for the shape; the tool's own config dump verifies the
result.

## EN-01.2 — Lint blocks

**Statement.** Lint findings must fail the build. A lint job must not carry
`continue-on-error`, and the linter must be configured to treat findings as
errors.

**Rationale.** Advisory lint is decoration. Findings scroll past in a green run,
accumulate, and the signal is gone within weeks — at which point the honest
description is that the project does not lint.

The objection to blocking lint is that it stops unrelated work. That is a real
cost and it is the point: it forces the finding to be dealt with — fixed,
suppressed with a named reason, or the rule rejected in the shared config —
rather than deferred indefinitely.

**Enforcement.** gate:lint (partial), gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** CI job configuration; linter `WarningsAsErrors`.

## EN-01.3 — Warnings are errors

**Statement.** Compiler warnings must be errors for the project's own targets,
by default rather than behind an opt-in flag.

**Rationale.** A warning is the compiler saying it has understood the code well
enough to doubt it. The set that ships enabled by default is far narrower than
the set that catches real defects, so the shared set is explicit and wide.

**The one documented escape.** A target that compiles third-party sources into
itself — a vendored amalgamation, a dependency that ships sources rather than a
built artefact — cannot carry the flag, because it lands on code the project
cannot fix. The remedy is *not* to weaken the flag globally. Build that target
without it and gate on the build log instead, scoped to paths the project owns:
capture the log, and fail if any warning line names a file under a directory the
project maintains. The language binding gives the concrete form.

**Enforcement.** compiler (-Werror), gate:build-warnings (partial), review.
**Deviation.** permitted with record, for the escape above only.

**Mechanism.** build configuration; the `build-warnings` gate where the escape
applies.

## EN-01.4 — Harden the build

**Statement.** A hosted build must enable the compiler and linker hardening
options appropriate to its toolchain. Where a target cannot take an option, the
build must report which options it dropped.

**Rationale.** Hardening turns a class of exploitable memory error into a
deterministic crash, for a cost that is usually not measurable. The reporting
requirement matters as much as the options: a hardening set that silently thins
out on a freestanding target reads as protection that is not there, which is
worse than no protection at all.

**Enforcement.** build (-D_FORTIFY_SOURCE=3 -fstack-protector-strong), gate:compile-db (partial), review.
**Deviation.** permitted with record.

**Mechanism.** build configuration; a compile-database grep verifies the flags
land.

## EN-01.5 — Dynamic analysis is a gate, not an exercise

**Statement.** The test suite must run under the toolchain's sanitizers in CI,
configured to fail on the first report rather than to count reports. Fuzzing
requirements are defined by `EN-04.6`.

**Rationale.** Static analysis cannot see what only happens at run time —
use-after-free, races, undefined behaviour on a path taken once in a thousand.
Sanitizers do, but only if a report fails the run; a sanitizer whose output is
logged and ignored is a slow build with no benefit.

Corpus carry-over is what makes fuzzing worth doing on a schedule. Starting from
an empty corpus every night rediscovers the shallow states and never reaches the
deep ones, which is where the bugs are.

**Enforcement.** build (-fsanitize=address -fsanitize=undefined), gate:synced-files (partial), review.
**Deviation.** permitted with record, per project.

**Mechanism.** CI job configuration.

## EN-01.6 — Coverage is reported, never gated

**Statement.** Test coverage may be measured and reported. It must not be a
merge gate.

**Rationale.** A coverage threshold is trivially satisfied by tests that execute
code without asserting anything about it, so gating on it selects for tests that
raise the number. The signal worth having is the *trend* and the *uncovered
list*, both of which a report gives and a gate does not.

**Enforcement.** review.
**Deviation.** never.

## EN-01.7 — Pin the tools that must agree

**Statement.** A formatter's version must be pinned, and a blocking linter's
version must be pinned. The pin lives in the repository and both local scripts
and CI read it.

**Rationale.** Two different failure modes, one answer.

Formatting is a consensus artifact: two versions produce different output, so an
unpinned formatter makes a `--check` job pass or fail depending on who ran it
last, and produces reformatting churn in unrelated diffs.

A blocking linter is worse. A newer version adds checks, so an unpinned one
turns a routine package upgrade on one machine into a red build on a commit that
did not touch the failing code. That trains people to distrust the gate.

Upgrading is then a deliberate commit: bump the pin, re-derive anything
version-specific (alias lists), reformat in a commit of its own so review can
skip it, and fix or record every new finding. Never widen the deviation budget
to absorb an upgrade silently.

**Enforcement.** gate:format (partial), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Format and lint commands verify the resolved binary version
against the declared pin and refuse a mismatch. Review checks that both local
runs and CI use that pin.

## EN-01.8 — A change is complete when its gates have run

**Statement.** A change must not be described as complete until the project's own
gates — build, tests, formatter check, linter, and any repository-specific gate
script — have been run against it in its final state. What is reported must be
what the tooling printed, not a prediction of what it would print.

**Rationale.** The gates in this chapter are configured to block, which decides
what CI does with a finding. It does not decide when a change is finished, and
without that second half the gates are simply relocated: the work is handed over
looking right, the finding surfaces in CI or in someone else's session, and the
cost of the round trip is paid by whoever is furthest from the code.

"Final state" is the load-bearing part. Gates run before the last few edits
measured something that no longer exists, and a formatter or linter is exactly
the kind of tool a small follow-up edit invalidates.

The reporting half is a separate failure. An asserted result and a measured one
are indistinguishable after the fact — both read as "tests pass" — so a habit of
predicting output destroys the value of every honest report alongside it. A gate
that was not run is not a lesser pass; it is an unknown, and saying which gate is
unrun and why leaves the reader able to act. Reporting a failure plainly costs
nothing and is the outcome the gate exists to produce.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** review locally; CI is the backstop.

## Binding

| | C++ | Python | Rust |
|---|---|---|---|
| Linter | clang-tidy, `Checks: *` minus exclusions, `WarningsAsErrors: '*'` | — | — |
| Compiler strictness | `-Werror` + shared warning set (applied by one shared helper, not per target) | — | — |
| Hardening | `_FORTIFY_SOURCE=3`, stack protector, RELRO/BIND_NOW, hardened stdlib assertions | — | — |
| Sanitizers | ASan + UBSan + LSan, `halt_on_error=1` | — | — |
| Fuzzing | libFuzzer, cached corpus | — | — |
| Version pin | `.clang-version` | — | — |
