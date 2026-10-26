# Engineering standard

This repository defines language-neutral engineering rules and a C++ tier.
Read [README.md](README.md), [orientation.md](orientation.md) and
[CONTRIBUTING.md](CONTRIBUTING.md) before editing the rules.

Done means `python3 check.py` (`py -3 check.py` on Windows) passes in the final
state and the diff has been reviewed for rule meaning and honest enforcement
claims. The checker validates
structure; it cannot establish that a consumer enforces a rule.

Append a new rule ID; never renumber or reuse one. A withdrawal keeps its heading
as `## <ID> — Withdrawn` and a reason. Keep the enforcement matrix consistent
with the clauses, and use only the vocabulary and gate names in the README.
