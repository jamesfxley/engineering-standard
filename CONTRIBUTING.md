# Contributing

This repository defines engineering rules, language tiers and the enforcement
contract. Run `python3 check.py` (`py -3 check.py` on Windows) to validate
structure, then review the rule meaning and the limits of each enforcement claim.

`main` is protected, so work on a branch and open a pull request from it,
named as `EN-07.1` requires. It lands as a single squash-merged commit whose
subject is the pull request's title, so that title is the commit subject and
`EN-07.2` governs it.

## What a rule looks like

Each rule is a section with four fields, defined in
[EN-00's rule format](engineering/00-conformance.md#rule-format). A change that
adds a rule supplies all four.

The rationale decides whether the rule survives an argument: say what goes
wrong without it rather than restating the statement. The enforcement field is
a claim about reality, so name something that exists.

## Rules to follow when changing the rules

- **IDs are never renumbered** (`EN-00.1`). A new rule appends to its chapter. It
  does not take a number in the middle and push the rest down: every citation in
  every consuming repository is a link to a number.
- **A chapter states the present** (`EN-03.1`). No history, and no explaining a
  rule by the incident that prompted it. State the rule and the
  consequence; the incident belongs in the pull request that adds it.
- **The enforcement matrix is not decoration.** If you add a rule, add its row.
  If you change what enforces a rule, change the row with it. A row naming a
  script that does not exist is worse than a row saying `review`, because
  it reads as a guarantee.
- **A rule with no citation is a proposal.** The tiers exist to be cited from
  code, tests and documents. If nothing in any repository would cite the rule you
  are adding, say in the pull request what would.

## Proposing rather than writing

Open an issue. A disagreement with an existing rule is more useful as an issue
than as a pull request — the rationale field is where the argument actually is,
and changing it is a bigger thing than changing the statement.

## Consumers

Consumers adopt a change by moving their pinned revision. Document a contract
change so that consumers can decide when to take it. A tightened rule,
withdrawal or vocabulary change requires a minor release while pre-1.0;
wording-only changes require a patch.
