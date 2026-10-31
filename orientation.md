# Engineering standard

The `engineering/` tier defines language-independent `EN-` rules. The `cxx/`
tier adds C++ `CXX-` rules. `PY-` and `RS-` are reserved, unwritten tiers (FW-1).

`engineering/00-conformance.md` defines the rule format. `README.md` defines
the gate-name contract.
The standard's only executable code is the stdlib-only `check.py`.

Rule IDs are stable (`EN-00.1`). Append new IDs and keep withdrawn stubs.
Enforcement declarations distinguish review, compiler/build checks, and full or
partial gate coverage. A declaration is a claim to verify in each consumer.

Run `python3 check.py` (`py -3 check.py` on Windows) before marking a change
done. A consumer adopts a change by moving its pin; a local edit here does not
change any consumer's revision.
