# EN-00 — Conformance

## Normative language

**must** / **must not** — a requirement. Violating it without a recorded
deviation is a defect.
**should** / **should not** — a strong default. Departing from it needs a reason
stated at the site, but not a registered deviation.
**may** — permission, no obligation either way.

## Rule format

Every rule in this standard states four things:

- **Statement** — the requirement, stated briefly.
- **Rationale** — what goes wrong without it. A rule whose rationale is "it is
  the convention" is not worth having.
- **Enforcement** — the named check, compiler flag or gate that catches a
  violation, or `review` when nothing can.
- **Deviation** — *permitted*, *permitted with record*, or *never*,
  optionally with the conditions.

A rule marked `review` is not weaker; it is the subset review
exists to cover, because tooling cannot.

## EN-00.1 — Rule IDs are stable

**Statement.** Rule IDs must never be renumbered or reused. A retired rule keeps
its number and is marked withdrawn.

**Rationale.** Code, review comments and deviation records cite IDs. Renumbering
invalidates every citation at once, silently — the citation still parses, it
just now points at a different rule.

**Enforcement.** review.
**Deviation.** never.

## EN-00.2 — The lowest layer that covers it

**Statement.** A rule must live in exactly one layer: this standard for
anything language-independent, the language tier for a language rule,
the repository's own orientation document for a rule true only of that
repository.

**Rationale.** Duplication across layers is how guidance drifts: two copies are
edited at different times and then disagree, and there is no way to tell which
one is current.

**Enforcement.** review.
**Deviation.** never.

---

## EN-00.3 — Fix before suppressing

**Statement.** A finding must be fixed unless the rule genuinely does not apply.
A suppression is the last option, not the quick one.

**Rationale.** Most suppressions are a design smell wearing a comment. The check
fired because the code has the shape the check describes; usually the honest
answer is that the shape is wrong.

**Enforcement.** gate:deviations (partial), review.
**Deviation.** never.

**Mechanism.** review, plus the ceiling in EN-00.6.

## EN-00.4 — A suppression names its rule and carries a justification

**Statement.** Every per-site suppression must name the exact rule or rules it
suppresses, must carry a justification on the line immediately above it, and
must have specific approval.

**Rationale.** A suppression that names nothing disables an unknown set, forever,
and cannot be reviewed — nobody can tell later whether it is still needed or what
it was hiding. Naming the rule also makes the suppression fail loudly if the
rule is renamed, which is the correct outcome.

Where two rules fire on one site, name both rather than going bare. A reserved
identifier typically trips both a naming rule and a reserved-identifier rule;
listing the pair is precise, and a bare suppression there is simply the lazier
option, not a necessary one.

The justification says why the rule's *purpose* is not served here. "the linter
complains" is not a justification.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks the exact check names, preceding justification,
specific approval and scope at the suppression site.

## EN-00.5 — Scope-wide suppression is a standing deviation

**Statement.** Turning a rule off for a whole directory, module or file must be
registered in `docs/deviations.md` with the check name, the scope, a rationale, a
risk assessment, specific approval and a review date in the future. Review
rejects an unregistered scope-wide disable.

The first column holds **the name the linter uses for the check**, not this
standard's rule ID. Review compares it with the tool configuration to
establish which check is disabled. Cite the governing rule ID in the rationale,
where a reader looking for it will find it. Each language tier gives the concrete spelling.

**Rationale.** Scope-wide suppression is sometimes correct — a tree that
transcribes a wire format really is outside a naming rule. What is never correct
is doing it invisibly. A per-directory config disable is unbounded in *time* and
in *coverage*: every file added to that tree later loses the rule for free, and
nobody is ever told. The rationale is usually written and then buried in a
config file nobody re-reads.

Registration changes three things: it is visible in one place, it carries a risk
assessment saying what is lost and what covers it instead, and it expires.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review keeps the register consistent with the configuration and
checks approval, rationale, risk assessment and future review dates.

## EN-00.6 — Deviation counts ratchet down

**Statement.** Suppression counts must not rise. One ceiling per language lives in
`docs/deviation-budget.txt`. A count below its ceiling must lower that ceiling
in the same change. Raising a ceiling needs specific approval and its own
commit, with the reason in the commit message.

**Rationale.** Individually justified suppressions accumulate. Each one is
defensible and the total is not, and without a number nobody notices the total.
A ceiling makes the trend visible and puts the cost of a new suppression where
it belongs: on the change that needs it, in a commit that has to say why.

Ratcheting down after removing suppressions is routine and needs no ceremony.

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

**Rationale.** "We never follow this rule" is a stronger claim than "this
directory does not", and it deserves more visibility, not less. In the root
configuration it applies predictably and its reason sits next to it. Scattered,
the same decision reads as many small local judgements and nobody ever
re-examines the whole.

The expiry is what EN-00.5 requires of the narrower case, and the argument for
it holds a fortiori here: a disable with no date is unbounded in time, and the
wider its scope the more a stale one costs. The date does not force the rule
back on — it forces the claim to be made again.

Keep that list short. A long one means the rule set was chosen badly.

**Enforcement.** review.
**Deviation.** never.

---

## EN-00.8 — Shared components depend on no consumer's identity or layout

**Statement.** A shared component must depend on no consumer's identity or
file layout. Consumers supply their configuration through declared extension
points. Shared rules may name open conventions and language tools.

**Rationale.** An assumption about a particular consumer makes reuse depend on
imitating that consumer. An explicit extension point keeps the dependency in
the direction of the component being consumed.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks consumer identity assumptions, layout dependence and
extension imports.

## Attribution

This standard is original wording. Where it derives from published guidance:

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

MISRA C++:2023 is a paid, copyright-restricted document and its text is **not**
reproduced anywhere in this standard — no quotations, and no MISRA rule numbers
presented as ours. Where a constrained-target rule here serves a similar purpose,
it was written independently from the underlying engineering reason.
