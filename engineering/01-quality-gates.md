# EN-01 — Quality gates

Development aims for maximum quality by default and assumes hostile input.
The work is security-conscious but not safety-critical. It assumes attackers
can find defects that tools can detect. Finding a defect with a tool costs far
less than finding it later.

## EN-01.1 — Start from every check, exclude with a reason

**Statement.** A linter must enable every check except those in an enumerated
exclusion list whose entries state their reasons. Configuring a
hand-picked subset is not permitted.

**Rationale.** An opt-in list omits checks nobody thought to enable, including
checks for unfamiliar mistakes. An exclusion list records a finite, reviewable
set of decisions.

Exclusions fall into three kinds:

1. Inapplicable checks concern platforms or libraries the project does not use.
2. Aliases name checks already enabled. Enabling both reports each finding
   twice. Alias tables depend on the tool version and must be re-derived on an
   upgrade; alias direction has reversed between releases.
3. Rejected rules are rules the project will not follow anywhere. These
   decisions need scrutiny under EN-00.7.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks the configuration policy. The tool's configuration
dump verifies the resulting checks.

## EN-01.2 — Lint blocks

**Statement.** Lint findings must fail the build. A lint job must not carry
`continue-on-error`, and the linter must be configured to treat findings as
errors.

**Rationale.** Non-blocking findings accumulate until readers ignore them.
Blocking lint interrupts unrelated work, but ensures a finding is fixed,
suppressed with a named reason, or rejected in the shared configuration.

**Enforcement.** gate:lint (partial), gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** CI job configuration; linter `WarningsAsErrors`.

## EN-01.3 — Warnings are errors

**Statement.** Compiler warnings must be errors for the project's own targets,
by default. An opt-in flag is insufficient.

**Rationale.** Compiler warnings identify suspect code. The compiler's default
warning set misses defects that a wider, explicit shared set can catch.

A target that compiles third-party sources, such as a vendored amalgamation,
cannot carry the flag because the project cannot fix that code. Build that
target without the flag and check its build log for warnings in owned paths.
Capture the log and fail if a warning names a file under a maintained directory.
The global flag remains strict. The language binding gives the mechanism.

**Enforcement.** compiler (-Werror), gate:build-warnings (partial), review.
**Deviation.** permitted with record, for the escape above only.

**Mechanism.** build configuration; the `build-warnings` gate where the escape
applies.

## EN-01.4 — Harden the build

**Statement.** A hosted build must enable the compiler and linker hardening
options appropriate to its toolchain. Where a target cannot take an option, the
build must report which options it dropped.

**Rationale.** Hardening turns exploitable memory errors into deterministic
crashes, usually at little measurable cost. Reporting dropped options prevents
a build from claiming protection it lacks, particularly on freestanding targets.

**Enforcement.** build (-D_FORTIFY_SOURCE=3 -fstack-protector-strong), gate:compile-db (partial), review.
**Deviation.** permitted with record.

**Mechanism.** Build configuration enables the flags. A search of the compile
database verifies their presence.

## EN-01.5 — Dynamic analysis is a gate, not an exercise

**Statement.** The test suite must run under the toolchain's sanitisers in CI,
configured to fail on the first report. Fuzzing
requirements are defined by `EN-04.6`.

**Rationale.** Sanitisers expose runtime defects that static analysis misses,
including use after free, races and undefined behaviour on rarely used paths.
Failing on a report ensures those defects are addressed.

A retained corpus of fuzzing inputs lets scheduled runs reach deeper states. Starting
from an empty corpus repeatedly tests the same shallow states.

**Enforcement.** build (-fsanitize=address -fsanitize=undefined), gate:synced-files (partial), review.
**Deviation.** permitted with record, per project.

**Mechanism.** CI job configuration.

## EN-01.6 — Coverage is reported, never gated

**Statement.** Test coverage may be measured and reported. It must not be a
merge gate.

**Rationale.** Tests can execute code without checking its behaviour, so a
coverage threshold rewards tests that raise the number. The trend and the list
of uncovered code help identify gaps without that incentive.

**Enforcement.** review.
**Deviation.** never.

## EN-01.7 — Pin the tools that must agree

**Statement.** A formatter's version must be pinned, and a blocking linter's
version must be pinned. The pin lives in the repository and both local scripts
and CI read it.

**Rationale.** Formatter versions can produce different output. Without a pin,
a check depends on which version ran last and unrelated changes acquire
formatting differences.

A new linter version can add checks and fail a previously passing commit after
a routine package upgrade. A pin keeps that change explicit.

An upgrade is a deliberate commit: bump the pin and re-derive version-specific
data such as alias lists. Reformat in a separate commit so review can skip it,
and fix or record every new finding. Never silently widen the deviation budget to absorb
an upgrade.

**Enforcement.** gate:format (partial), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Format and lint commands verify the resolved binary version
against the declared pin and refuse a mismatch. Review checks that both local
runs and CI use that pin.

## EN-01.8 — A change is complete when its gates have run

**Statement.** A change must not be described as complete until the project's own
gates have run against its final state. These include the build, tests,
formatter check, linter and any repository-specific gate script. Reports must
state what the tooling printed, without predicting its output.

**Rationale.** Blocking gates define how CI handles findings. Running them
before handover also avoids passing defects to another person or session.

A gate run before the last edit checks an earlier state. Even a small edit can
invalidate a formatter or linter result.

Predicted results are indistinguishable from measured results once reported.
Identifying an unrun gate and the reason it was not run lets the reader act on
what remains unknown. A plain failure report states what the gate detected.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** Local review checks gate evidence; CI runs the gates again.

## Binding

| | C++ | Python | Rust |
|---|---|---|---|
| Linter | clang-tidy, `Checks: *` minus exclusions, `WarningsAsErrors: '*'` | — | — |
| Compiler strictness | `-Werror` + shared warning set (applied by one shared helper, not per target) | — | — |
| Hardening | `_FORTIFY_SOURCE=3`, stack protector, RELRO/BIND_NOW, hardened stdlib assertions | — | — |
| Sanitisers | ASan + UBSan + LSan, `halt_on_error=1` | — | — |
| Fuzzing | libFuzzer, cached corpus | — | — |
| Version pin | `.clang-version` | — | — |
