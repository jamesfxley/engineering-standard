# Enforcement matrix

This table records each clause's declared coverage. It does not certify any
consumer implementation. See the README for the vocabulary and gate contract.
Concrete diagnostic names and check boundaries are in each clause.

| Rule | Full gate coverage | Partial gate coverage | Other checks |
|---|---|---|---|
| EN-00.1 — Rule IDs are stable | — | — | review |
| EN-00.2 — The lowest layer that covers it | — | — | review |
| EN-00.3 — Fix before suppressing | — | gate:deviations (partial) | review |
| EN-00.4 — A suppression names its rule and carries a justification | — | — | review |
| EN-00.5 — Scope-wide suppression is a standing deviation | — | — | review |
| EN-00.6 — Deviation counts ratchet down | — | gate:deviations (partial) | review |
| EN-00.7 — Disabling a rule everywhere belongs in the shared configuration | — | — | review |
| EN-00.8 — Shared components depend on no consumer's identity or layout | — | — | review |
| EN-01.1 — Start from every check, exclude with a reason | — | — | review |
| EN-01.2 — Lint blocks | — | gate:lint (partial); gate:synced-files (partial) | review |
| EN-01.3 — Warnings are errors | — | gate:build-warnings (partial) | compiler (-Werror); review |
| EN-01.4 — Harden the build | — | gate:compile-db (partial) | build (-D_FORTIFY_SOURCE=3 -fstack-protector-strong); review |
| EN-01.5 — Dynamic analysis is a gate, not an exercise | — | gate:synced-files (partial) | build (-fsanitize=address -fsanitize=undefined); review |
| EN-01.6 — Coverage is reported, never gated | — | — | review |
| EN-01.7 — Pin the tools that must agree | — | gate:format (partial); gate:lint (partial) | review |
| EN-01.8 — A change is complete when its gates have run | — | gate:synced-files (partial) | review |
| EN-02.1 — Every behavioural guarantee has an ID | — | — | review |
| EN-02.2 — Cite the ID, never a section number | — | — | review |
| EN-02.3 — IDs are stable and never renumbered | — | — | review |
| EN-02.4 — Prefixes classify | — | — | review |
| EN-02.5 — Every requirement has a pass criterion and a test | — | — | review |
| EN-02.6 — A behaviour change lands as one change | — | — | review |
| EN-02.7 — The exceptions list is a backlog | — | — | review |
| EN-02.8 — A cross-package citation is qualified | — | — | review |
| EN-03.1 — Documents state what is true now | — | — | review |
| EN-03.2 — The specification is normative and carries no measurements | — | — | review |
| EN-03.3 — `docs/` has a known shape | — | — | review |
| EN-03.4 — Generate the API reference from the source | — | gate:api-docs (partial) | review |
| EN-03.5 — Examples in documentation are compiled | — | — | build (ctest); review |
| EN-03.6 — Markdown destined elsewhere goes in a fenced block | — | — | review |
| EN-03.7 — A deferral is a `docs/future-work.md` entry, cited by its ID | — | — | review |
| EN-03.8 — A link between documents resolves | gate:doc-links (full) | — | — |
| EN-04.1 — One seam per platform dependency, with a fake behind it | — | — | review |
| EN-04.2 — Tests cite the requirement they establish | — | — | review |
| EN-04.3 — One behaviour per test | — | — | review |
| EN-04.4 — Test the boundaries, not the middle | — | — | review |
| EN-04.5 — An incremental consumer is tested at every split | — | — | review |
| EN-04.6 — Untrusted input is fuzzed | — | gate:synced-files (partial) | build (-fsanitize=fuzzer); review |
| EN-04.7 — A test's literal values are the case under test | — | gate:deviations (partial) | review |
| EN-05.1 — The standard job set | — | gate:synced-files (partial) | review |
| EN-05.2 — Nothing gates advisorily | — | gate:synced-files (partial) | review |
| EN-05.3 — Scheduled runs get their own concurrency group | — | gate:synced-files (partial) | review |
| EN-05.4 — Time-boxed work gets a short budget on push and a long one on schedule | — | gate:synced-files (partial) | review |
| EN-05.5 — Checkout does not persist credentials | — | gate:synced-files (partial) | review |
| EN-05.6 — Dependency fetches are pinned by content where possible | — | — | review |
| EN-05.7 — Withdrawn | — | — | reserved |
| EN-06.1 — Semantic versioning, with the break confined to the leading component | — | — | review |
| EN-06.2 — Version declarations agree and are tested | — | — | build (version test where applicable); review |
| EN-06.3 — Release notes say what to change, not what happened | — | — | review |
| EN-06.4 — Withdrawn | — | — | reserved |
| EN-06.5 — A release is validated against every supported configuration | — | gate:synced-files (partial) | review |
| EN-06.6 — Never claim hardware validation without a device run | — | — | review |
| EN-06.7 — A run record carries its conditions | — | — | review |
| EN-06.8 — Every source file names its licence | — | gate:spdx (partial) | review |
| EN-07.1 — A branch names its issue | — | — | review |
| EN-07.2 — A commit subject names the area it changes | — | gate:commits (partial) | review |
| EN-07.3 — A commit body argues the change | — | — | review |
| EN-07.4 — A commit message carries no trailers | gate:commits (full) | — | — |
| EN-07.5 — `main` advances only by squash merge | — | — | review |
| EN-07.6 — An issue title states the fact, and the issue is labelled `defect` | — | — | review |
| EN-07.7 — A release is a tag named `v<semver>` | — | — | review |
