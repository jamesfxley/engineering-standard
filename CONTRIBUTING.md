# Contributing

This repository defines engineering rules, language tiers and the enforcement
contract. A change is complete when `python3 check.py` (`py -3 check.py` on
Windows) passes in the final state and the diff has been reviewed for rule
meaning and honest enforcement claims. The checker validates structure; it
cannot establish that a consumer enforces a rule.

`main` is protected. Follow [EN-07.1](engineering/07-version-control.md#en-071--a-branch-names-its-issue)
for branches and [EN-07.5](engineering/07-version-control.md#en-075--main-advances-only-by-squash-merge)
for pull requests and merges.

## What a rule looks like

[EN-00's rule format](engineering/00-conformance.md#rule-format) defines the
four fields required for a new rule. An enforcement declaration names an
existing mechanism.

## Rules to follow when changing the rules

- [EN-00.1](engineering/00-conformance.md#en-001--rule-ids-are-stable)
  governs IDs. Each new rule appends to its chapter. A withdrawal keeps the
  heading `## <ID> — Withdrawn` and a reason.
- [EN-03.1](engineering/03-documentation.md#en-031--documents-state-what-is-true-now)
  governs current-state prose.
- Add a matrix row for each new rule. Update the row when enforcement changes.
  Each row accurately names the mechanism that exists.
- Explain in the pull request what would cite a proposed rule if no repository
  would cite it yet. The tiers exist for citation from code, tests and documents.

## Proposing a rule or a change to one

Propose changes through a pull request. Start an existing rule's revision with
its rationale, and change the other fields only as far as the argument requires.
The same process applies to a rationale that does not support its statement.
[EN-03.7](engineering/03-documentation.md#en-037--a-deferral-is-a-docsfuture-workmd-entry-cited-by-its-id)
governs issue scope.

## Consumers

Consumer adoption follows [README.md](README.md#consuming-this-repository).
Document contract changes so consumers can decide when to adopt them. Under
[EN-06.1](engineering/06-release-and-versioning.md#en-061--semantic-versioning-with-the-break-confined-to-the-leading-component),
a tightened rule, withdrawal or vocabulary change requires a minor release
while pre-1.0. Wording-only changes require a patch.
