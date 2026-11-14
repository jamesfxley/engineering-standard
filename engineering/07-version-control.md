# EN-07 — Version control

## EN-07.1 — A branch names its issue

**Statement.** A branch name must use only lowercase letters, digits and hyphens.
Where the work has an issue, the name must begin with that issue's number
followed by a hyphen, as in `47-queue-index-can-wrap`. Work with no issue takes a
descriptive slug alone.

**Rationale.** The tracker proposes this form for branches created from
issues, and the proposal cannot be configured. Accepting it keeps branches,
issues and pull requests linked without repeated manual edits.

The restricted character set makes names usable in paths, URLs and shell
arguments. A slash can prevent a branch from coexisting with another branch
whose name is its prefix.

**Enforcement.** review.
**Deviation.** permitted for a branch created by
an automated tool, which takes the name that tool gives it; never otherwise.

## EN-07.2 — A commit subject names the area it changes

**Statement.** A commit subject must have the form `<area>: <summary>`. The area
is lowercase and names a location in the repository: a directory under `src/`,
a top-level content directory where the repository has no `src/`, or one of
`build`, `ci`, `deps`, `docs`, `examples`, `release`, `tests`, `tooling`. A
change touching several takes the name of its principal one. The summary states
what the change does, in the imperative, beginning lowercase, with no trailing
full stop. The whole line is at most 72 characters.

Dependency updates use `deps: take <dependency> <version>`. Releases use
`release: <version>`.

**Rationale.** The area helps readers locate a change in the repository.
A change-type prefix such as fix, feature or chore duplicates the version
consequence already recorded under EN-06.1 and EN-02.6, without a check to keep
the third copy consistent. It also describes an event, whereas EN-03.1 calls
for the current state.

A 72-character subject fits tools that indent, quote or display it in columns.
Naming the principal area keeps the prefix short. A change with no principal
area can need splitting under EN-02.6.

**Enforcement.** gate:commits (partial), review.
**Deviation.** never.

**Mechanism.** The commits gate checks subject format, lowercase opening, length
and punctuation. Review checks the area against the changed tree and checks
the summary’s meaning and imperative wording.

## EN-07.3 — A commit body argues the change

**Statement.** Where the subject does not fully account for the change, the
commit must carry a body, separated by a blank line and hard-wrapped at 80
columns. The body states what was true before that made this the right change,
and cites the requirement IDs the change establishes or alters (`EN-02.2`).

**Rationale.** The diff records the change but not the reason for it. A body
preserves the reasoning needed to assess a later reversal, when the original
authors might have forgotten it. Restating the diff obscures that reasoning.

**Enforcement.** review.
**Deviation.** never.

## EN-07.4 — A commit message carries no trailers

**Statement.** A commit message must contain no trailer lines: no attribution,
no tool-generated footer, no sign-off, and no issue reference. An issue
reference belongs in the pull request description.

**Rationale.** The pull request is where an issue reference is read and acted
on. A second copy in a commit closes nothing and links nowhere. Author and
committer fields already record attribution; a trailer can only repeat or
contradict them.

A blanket rule prevents additional metadata conventions from accumulating in
the message and obscuring the argument for the change.

**Enforcement.** gate:commits (full).
**Deviation.** never.

**Mechanism.** The commit-message hook and the commits range check refuse
trailer and attribution lines, tool footers and issue references, apart from
the squash suffix `EN-07.5` permits.

## EN-07.5 — `main` advances only by squash merge

**Statement.** The default branch must be protected, and must advance only by
squash-merging a pull request. Each merge lands one commit, whose subject is the
pull request's title and is therefore governed by `EN-07.2`. The subject may end
with the pull request number the hosting service appends, ` (#<n>)`; that suffix
is not part of the subject under `EN-07.2` and is not an issue reference under
`EN-07.4`. Commits on a branch
are working state, but their subjects and trailers are still checked under
`EN-07.2` and `EN-07.4`. The root commit that creates the repository is
pushed before protection exists; it is the one commit that does not arrive by
squash merge.

**Rationale.** One commit per reviewed change makes the default branch
readable, bisectable and revertible at the unit EN-02.6 requires. Reverting an
intermediate commit can leave a partially completed change.

Using the pull request title as the subject gives both one form and one place
to check it. Checking branch commits exposes message-policy violations before
merge. The squash commit holds the final argument for the reviewed change.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review verifies branch protection and that each default-branch
change after the root commit comes from a squash-merged pull request.

## EN-07.6 — An issue title states the fact, and the issue is labelled `defect`

**Statement.** An issue title must state the observable fact, in the present
tense, with no bracketed or prefixed classification. Every open issue carries
the label `defect`. This standard defines no other label; an issue may also
carry labels the standard does not define.

**Rationale.** The tracker holds defects under EN-03.7. The label makes those
reports filterable alongside hosting-service labels. Repeating a classification
in the title consumes space without adding information.

A suspected cause can remain in the title after investigation disproves it.
An observable fact remains useful.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review of each newly opened issue, and of the open issues
before each release, edits a title that names a type or a suspected cause so
that it states the fact, and adds the label `defect` where it is missing.

## EN-07.7 — A release is a tag named `v<semver>`

**Statement.** A release must be a tag whose name is `v` followed by the
semantic version, with no further suffix, as in `v1.4.2`. No other reference
names the release.

**Rationale.** Consumers pin release names, gates parse them for freshness,
and CI resolves reusable workflows through them. Inconsistent spelling breaks
those comparisons. A fixed tag also makes content pinning under EN-05.6 possible.

**Enforcement.** review.
**Deviation.** never.

## EN-07.8 — A pull request states its verification by level

**Statement.** A pull request description must state, for each verification
level the repository has, what was run against the final state of the change
and the result lines it printed. The levels are host (the gates and tests),
target build (the targets built) and device (the board, the image's source
commit, the commands and the result per requirement ID). A level that was not
run must be stated as not run, with the reason and the behaviour it leaves
unverified. A repository that builds for no target states the host level only.

**Rationale.** An omitted verification level leaves the reviewer unable to
tell whether it passed or was irrelevant. EN-06.6 forbids unsupported validation
claims, but does not expose an omitted claim. Host evidence alone can therefore
hide a target defect until after merge.

Naming each level makes the author identify gaps while the change is available
to test. Printed result lines let the reviewer verify EN-01.8 from the description.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review reads the description against the change. A level
missing from the description, a level stated without its result lines, and a
change to target code whose device level is absent are findings.
