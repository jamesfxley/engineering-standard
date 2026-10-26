# EN-05 — CI shape

## EN-05.1 — The standard job set

**Statement.** A project's CI must cover, as separate jobs: build and test
(across the configurations the project supports), formatting, linting,
standards gates (deviations and synced files), and — for a library — a consumer
build against the installed package.

**Rationale.** Separate jobs because a single job reports one failure and hides
the rest, and because the names in the failure list should say what broke
without opening a log.

The consumer job is the one most often skipped and the one that catches the
worst class of defect: an in-tree build tests neither the exported target names
nor whether a public compile definition survives installation. Both are invisible
until a downstream project fails, and the compile-definition case fails as a
silent ABI mismatch rather than a link error.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.**
permitted with record.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review verifies that the declared jobs and configurations
cover the supported surface.

## EN-05.2 — Nothing gates advisorily

**Statement.** A job that is not allowed to fail the build must not exist. Either
it gates, or it is deleted.

**Rationale.** A permanently-yellow job is read as green within a week. Keeping
it costs CI minutes and buys nothing. If a check is genuinely not ready to gate,
the work is to make it gate — narrow its scope until it can.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.3 — Scheduled runs get their own concurrency group

**Statement.** A workflow with both branch-triggered and scheduled runs must
place the scheduled run in its own concurrency group.

**Rationale.** With a shared group and `cancel-in-progress`, a push to the
default branch cancels a nightly run in flight. That is precisely the run that
cannot be cheaply repeated — the long fuzz budget, the extended soak — and its
cancellation is invisible.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** never.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.4 — Time-boxed work gets a short budget on push and a long one on schedule

**Statement.** Fuzzing, soaks and anything else time-boxed must use a short
budget on push and pull request, and a long budget on the schedule.

**Rationale.** Per-push runs exist to catch an obvious regression immediately;
making them long makes every push slow and teaches people to skip CI. Depth
comes from the scheduled run, which nobody is waiting on.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** permitted.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.5 — Checkout does not persist credentials

**Statement.** A CI checkout must set `persist-credentials: false` unless a
later step genuinely needs to push.

**Rationale.** The default leaves a usable token in the runner's git
configuration for every subsequent step, including any third-party action and
anything a build script invokes. There is rarely a reason to want that.

**Enforcement.** gate:synced-files (partial), review.
**Deviation.** permitted with record.

**Mechanism.** The synced-files check compares the committed workflow with
generated output. Review checks this policy in the generator and configuration
and verifies that the declared obligations are sufficient.

## EN-05.6 — Dependency fetches are pinned by content where possible

**Statement.** A dependency fetched by URL must be pinned by content hash. A
dependency fetched by git must be pinned to a tag or commit, never a branch.

**Rationale.** A moved or compromised archive otherwise substitutes silently,
and a branch pin means the build is not reproducible — yesterday's green run
proves nothing about today's.

Bumping a version means updating the URL and the hash together; a mismatch is
the mechanism working.

**Enforcement.** review.
**Deviation.** never.

## EN-05.7 — Withdrawn

Private-dependency authentication is a repository configuration choice.
