# EN-00 — Conformance

## Normative language

- **must** / **must not** states a requirement. Violating it without a recorded
  deviation is a defect.
- **should** / **should not** states a strong default. Departing from it needs a
  reason at the site but no registered deviation.
- **may** grants permission without an obligation.

## Rule format

Every rule in this standard states four things:

- **Statement** — the requirement, stated briefly.
- **Rationale** — what goes wrong without the rule. Convention alone does not
  justify a rule.
- **Enforcement** — the named check, compiler flag or gate that catches a
  violation, or `review` when nothing can.
- **Deviation** — *permitted*, *permitted with record*, or *never*,
  optionally with the conditions.

Review covers requirements that tools cannot check.

## EN-00.1 — Rule IDs are stable

**Statement.** Rule IDs must never be renumbered or reused. A retired rule keeps
its number and is marked withdrawn.

**Rationale.** Code, review comments and deviation records cite IDs.
Renumbering leaves those citations pointing at a different rule without making
them visibly invalid.

**Enforcement.** review.
**Deviation.** never.

## EN-00.2 — The lowest layer that covers it

**Statement.** A rule must live in exactly one layer: this standard for
anything language-independent, the language tier for a language rule,
the repository's own orientation document for a rule true only of that
repository.

**Rationale.** Copies in different layers drift when edited separately. Readers
cannot tell which copy is current.

**Enforcement.** review.
**Deviation.** never.

---

## EN-00.3 — Fix before suppressing

**Statement.** A finding must be fixed unless the rule genuinely does not apply.
A suppression is the last option.

**Rationale.** A diagnostic usually identifies a problem in the code's design.
Suppressing it preserves that problem.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** never.

**Mechanism.** review, plus the ceiling in EN-00.6.

## EN-00.4 — A suppression names its rule and carries a justification

**Statement.** Every per-site suppression must name the exact rule or rules it
suppresses, must carry a justification on the line immediately above it, and
must have specific approval.

**Rationale.** An unnamed suppression disables an unknown set of checks.
Readers cannot tell what it hides or whether it is still needed. Naming the
check also exposes a renamed check as a failure.

Where two rules fire at one site, name both. A reserved identifier typically
triggers both a naming rule and a reserved-identifier rule.

The justification explains why the rule's purpose does not apply at the site.
"The linter complains" gives no such reason.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks the exact check names, preceding justification,
specific approval and scope at the suppression site.

## EN-00.5 — Scope-wide suppression is a standing deviation

**Statement.** Turning a rule off for a whole directory, module or file must be
registered in `docs/deviations.md` with the check name, the scope, a rationale, a
risk assessment, specific approval and a review date in the future. Review
rejects an unregistered scope-wide disable.

The first column holds the linter's check name. Review compares the name with
the tool configuration to establish which check is disabled. Cite the governing
rule ID in the rationale. Each language tier gives the check's spelling.

**Rationale.** Some code needs a scope-wide suppression. A tree that
transcribes a wire format can need an exception to a naming rule. A directory
configuration can disable the check indefinitely for every file later added to
that directory.

Registration makes the suppression visible, records the risk and the checks
that cover it, and gives it an expiry.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review keeps the register consistent with the configuration and
checks approval, rationale, risk assessment and future review dates.

## EN-00.6 — Deviation counts ratchet down

**Statement.** Suppression counts must not rise. One ceiling per language lives in
`docs/deviation-budget.txt`. A count below its ceiling must lower that ceiling
in the same change. Raising a ceiling needs specific approval and its own
commit, with the reason in the commit message.

**Rationale.** Individually justified suppressions can accumulate unnoticed.
A ceiling makes the total visible and assigns the cost of an increase to the
change that needs it. Removing suppressions and lowering the ceiling is routine.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** permitted with record — that is what raising the ceiling is.

**Mechanism.** The `deviations` gate counts suppressions per language, refuses
counts above a ceiling and reports a lower count with the ceiling to commit.
Review checks approval and the separate commit for an increase.

## EN-00.7 — Disabling a rule everywhere belongs in the shared configuration

**Statement.** A rule the project will not follow anywhere must be disabled in
the root tool configuration, with its reason written there and a review date in
the future — not repeated as per-directory disables or scattered per-site
suppressions.

**Rationale.** The root configuration makes a project-wide decision visible
and applies it consistently. Scattered suppressions obscure its scope and make
it harder to re-examine.

As in EN-00.5, a future review date requires the decision to be re-examined. It
does not automatically re-enable the rule. A stale decision costs more as its
scope grows.

Keep the list short. A long list indicates a poorly chosen rule set.

**Enforcement.** review.
**Deviation.** never.

---

## EN-00.8 — Shared components depend on no consumer's identity or layout

**Statement.** A shared component must depend on no consumer's identity or
file layout. Consumers supply their configuration through declared extension
points. Shared rules may name open conventions and language tools.

**Rationale.** Assumptions about one consumer require other consumers to
imitate it. Explicit extension points let consumers configure the component
without making the component depend on them.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks consumer identity assumptions, layout dependence and
extension imports.

## Attribution

This standard uses original wording and draws on the following published
guidance:

- Design and lifetime rules draw on the
  [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
  (Bjarne Stroustrup and Herb Sutter, Standard C++ Foundation). No guideline
  text is reproduced.
- Formatting follows the
  [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
  (CC BY 3.0) through clang-format's `BasedOnStyle: Google`.
- Security rules draw on the
  [SEI CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/display/cplusplus).
- Hardening options follow the
  [OpenSSF Compiler Options Hardening Guide for C and C++](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html).

MISRA C++:2023 is a paid, copyright-restricted document. This standard reproduces
none of its text and presents no MISRA rule numbers as its own. Constrained-target
rules with similar purposes are written independently from engineering reasons.

## EN-00.9 — Source code cites a rule only to suppress or check it

**Statement.** In source code, the ID of a rule in this standard or a language
tier must appear only in a suppression justification, or in code that checks
that rule. Code that follows a rule does not cite it.

**Rationale.** A citation in ordinary code argues that the code complies, which
is review's job. Such citations accumulate beside the comment the reader needs
and make it harder to find.

**Enforcement.** review.
**Deviation.** never.
