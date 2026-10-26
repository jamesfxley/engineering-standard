<!--
`main` is protected, so this arrives from a branch. Run python3 check.py
(py -3 check.py on Windows);
the checklist records the semantic review that structural checks cannot do.
-->

## What this changes

Rule IDs affected.

## Why

What was untrue, unenforced, or missing.

## Checklist

- [ ] `python3 check.py` (`py -3 check.py` on Windows) passes
- [ ] No existing rule ID was renumbered (`EN-00.1`) — a new rule appends to its
      chapter
- [ ] Every rule added or changed has all four parts: statement, rationale,
      enforcement, deviation
- [ ] The enforcement column names something that exists, and I have checked
      that it does
- [ ] `engineering/enforcement-matrix.md` and `cxx/enforcement-matrix.md`
      have the rows for their tiers, including every rule added or whose
      enforcement changed
- [ ] The prose states the present, with no history, dates, or explanation by
      the incident that prompted it (`EN-03.1`)
- [ ] Consumers pinning this repository will need their pin bumped, and I have
      said so if the change is one they must take
