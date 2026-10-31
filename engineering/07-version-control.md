# EN-07 — Version control

## EN-07.1 — A branch names its issue

**Statement.** A branch name must be lowercase, using digits and hyphens only.
Where the work has an issue, the name must begin with that issue's number
followed by a hyphen — `47-queue-index-can-wrap`. Work with no issue takes a
descriptive slug alone.

**Rationale.** This is the name the tracker itself proposes when a branch is
created from an issue, and that proposal cannot be reconfigured. A scheme the
tracker does not propose is one that gets hand-edited on every branch, and a
scheme that is hand-edited on every branch is one that is skipped — on exactly
the path the work is most often started from. Taking the proposed form means the
linkage between branch, issue and pull request costs nothing to maintain, which
is the only reason it survives.

Restricting the character set is what makes the name safe as a filesystem path,
a URL component and a shell argument at once. Slashes in particular make a
branch name that cannot coexist with a branch of the same prefix.

**Enforcement.** review.
**Deviation.** permitted for a branch created by
an automated tool, which takes the name that tool gives it; never otherwise.

## EN-07.2 — A commit subject names the area it changes

**Statement.** A commit subject must have the form `<area>: <summary>`. The area
is lowercase and names a *location* in the repository: a directory under `src/`,
a top-level content directory where the repository has no `src/`, or one of
`build`, `ci`, `deps`, `docs`, `examples`, `release`, `tests`, `tooling`. A
change touching several takes the name of its principal one. The summary states
what the change does, in the imperative, beginning lowercase, with no trailing
full stop. The whole line is at most 72 characters.

Two forms are fixed, because they recur in every repository: taking a new
version of a dependency is `deps: take <dependency> <version>`, and cutting a
release is `release: <version>`.

**Rationale.** The prefix answers *where*, which is the question a reader of a
log actually has, and it is the one piece of metadata a subject can carry that
is cheap to write and never wrong.

The alternative convention prefixes a change *type* — a fix, a feature, a
chore. That is rejected here. A type is a claim about the version consequence of
the change, and that claim is already made in two places that are checked: the
version number under `EN-06.1` and the specification row under `EN-02.6`. A
third copy in the subject line is a third thing to keep in sync and the only one
nothing verifies. It is also a statement about the change as an event rather
than about what is now true, which is what `EN-03.1` excludes everywhere else.

The 72-character limit is the width at which a subject survives being indented,
quoted and columnised by the tools that display it, rather than being truncated
in the middle of a word.

Naming the principal area rather than every area touched keeps the prefix short
enough to be worth reading. A change that genuinely has no principal area is
usually two changes, and `EN-02.6` already decides where that line falls.

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

**Rationale.** The diff already says what changed; nothing else records why it
was the right thing to do. That reasoning is needed exactly once — when someone
later proposes to undo it — and by then everyone who held it has forgotten. A
body that restates the diff in prose is worse than no body, because it takes the
space where the argument would have been.

**Enforcement.** review.
**Deviation.** never.

## EN-07.4 — A commit message carries no trailers

**Statement.** A commit message must contain no trailer lines: no attribution,
no tool-generated footer, no sign-off, and no issue reference. An issue
reference belongs in the pull request description.

**Rationale.** The tracker is where an issue reference is read and acted on — a
reference in the commit is a second copy that closes nothing and links nowhere.
Attribution is already carried by the author and committer fields, accurately
and without a convention to maintain; a trailer restating it is redundant when
it agrees and misleading when it does not.

The rule is absolute rather than a list of banned trailers because a permitted
trailer is an invitation to a second one, and the value of the message being
exactly the argument for the change falls away as soon as it is also a place to
put metadata.

**Enforcement.** gate:commits (full).
**Deviation.** never.

**Mechanism.** The commit-message hook and the commits range check refuse
trailer and attribution lines, tool footers and issue references.

## EN-07.5 — `main` advances only by squash merge

**Statement.** The default branch must be protected, and must advance only by
squash-merging a pull request. Each merge lands one commit, whose subject is the
pull request's title and is therefore governed by `EN-07.2`. Commits on a branch
are working state, but their subjects and trailers are still checked under
`EN-07.2` and `EN-07.4`. The root commit that creates the repository is
pushed before protection exists; it is the one commit that does not arrive by
squash merge.

**Rationale.** It makes the history of the default branch one commit per
reviewed change, which is the unit `EN-02.6` already requires a behaviour change
to land as. A history at that granularity can be read, bisected and reverted a
change at a time; a history of intermediate commits cannot, because a revert
lands in the middle of a half-finished thought.

It also collapses two conventions into one. With the pull request title becoming
the commit subject, there is a single form to state, a single place to check it,
and no possibility of a title and a subject that disagree.

Checking branch commits catches message-policy violations before a merge. The
squash commit still carries the final argument for the reviewed change.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review verifies branch protection and that each default-branch
change after the root commit comes from a squash-merged pull request.

## EN-07.6 — An issue title states the fact, and the issue is labelled `defect`

**Statement.** An issue title must state the observable fact, in the present
tense, with no bracketed or prefixed classification. Every issue carries the
label `defect`. This standard defines no other label, and no label may classify
an issue as anything but a defect.

**Rationale.** The tracker holds defects only (`EN-03.7`), so a type in the
title carries no information, and the one label marks each issue as a defect
report where it is filterable, next to whatever labels a hosting service adds
by default. Repeating a classification in the title is the same duplication
`EN-07.2` rejects in a commit subject, and it costs the first several characters
of every line in a list view.

Stating the fact rather than the suspected cause matters more than the format
does: a title naming a cause is a diagnosis made before the investigation, and
it survives in the tracker long after the diagnosis is known to be wrong.

**Enforcement.** review.
**Deviation.** never.

## EN-07.7 — A release is a tag named `v<semver>`

**Statement.** A release must be a tag whose name is `v` followed by the
semantic version, with no further suffix — `v1.4.2`. The tag is the release: no
other reference names it.

**Rationale.** The prefix is not cosmetic. Consumers pin to this name, gate
scripts parse it to decide whether a pin is behind, and CI resolves reusable
workflow references through it, so the spelling is a machine interface with
several independent readers. A repository that tags some releases with the
prefix and some without breaks every one of them at the point where they compare
two names.

Naming the tag as the release, rather than a branch or a moving reference, is
what makes `EN-05.6`'s pinning rule possible to satisfy: a consumer can only pin
by content if there is a name that never moves.

**Enforcement.** review.
**Deviation.** never.
