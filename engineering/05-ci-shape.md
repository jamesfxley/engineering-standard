# EN-05 — CI shape

## EN-05.1 — The standard job set

**Statement.** A project's CI must cover, as separate jobs: build and test
across supported configurations, formatting, linting, and standards gates
(deviations and synced files). A library must also have a separate consumer
build against the installed package.

**Rationale.** A single job reports one failure and hides the rest. The job
names in the failure list should say what broke without opening a log.

An in-tree build does not test exported target names or whether public compile
definitions survive installation. An installed-package consumer catches those
defects before a downstream project does. Missing compile definitions can cause
an ABI mismatch without a link error.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.**
permitted with record.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review verifies that the declared jobs and configurations
cover the supported surface.

## EN-05.2 — Nothing gates advisorily

**Statement.** A job that is not allowed to fail the build must not exist.

**Rationale.** Readers learn to ignore a job that remains non-blocking. It
consumes CI time without resolving findings. Narrow an unready check's scope
until it can block.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.3 — Scheduled runs get their own concurrency group

**Statement.** A workflow with both branch-triggered and scheduled runs must
place the scheduled run in its own concurrency group.

**Rationale.** A shared group with `cancel-in-progress` lets a push cancel a
scheduled run. Long fuzzing runs and extended soaks are expensive to repeat,
and cancellation can go unnoticed.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.4 — Time-boxed work gets a short budget on push and a long one on schedule

**Statement.** Fuzzing, soaks and anything else time-boxed must use a short
budget on push and pull request, and a long budget on the schedule.

**Rationale.** Short runs catch obvious regressions without delaying every
push. Scheduled runs allow deeper testing without keeping a developer waiting.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** permitted.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.5 — Checkout does not persist credentials

**Statement.** A CI checkout must set `persist-credentials: false` unless a
later step genuinely needs to push.

**Rationale.** The default leaves a usable token in the runner's Git
configuration. Every later step, including third-party actions and build
scripts, can access it.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** permitted with record.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.6 — Dependency fetches are pinned by content where possible

**Statement.** A dependency fetched by URL must be pinned by content hash. A
dependency fetched by git must be pinned to a tag or commit, never a branch.

**Rationale.** An unpinned archive can be moved or replaced after compromise.
A branch can change between builds, so a passing run does not establish the
result of the next one.

A version update changes the URL and hash together. A mismatch exposes
an inconsistent pin.

**Enforcement.** review.
**Deviation.** never.

## EN-05.7 — Withdrawn

Private-dependency authentication is a repository configuration choice.
