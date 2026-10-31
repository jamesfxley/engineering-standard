# Engineering standard

The normative rules this author's projects are written against, and the
resolvable target of every `EN-` and `CXX-` citation in them.

A repository cites a rule by ID — in a code comment, in a deviation rationale,
in a specification row. That citation is only worth writing if a reader can
follow it, so the rules live here rather than inside any one project or any one
developer's tool configuration.

## The two tiers

Practice and language are separated so that a second language is additive rather
than a restructure.

| Tier | IDs | Contents |
|---|---|---|
| [`engineering/`](engineering/) | `EN-<chapter>.<n>` | Engineering rules. |
| [`cxx/`](cxx/) | `CXX-<chapter>.<n>` | C++ language rules only. Cites `EN-*` rather than restating it. |

The engineering rules are language-independent. They cover conformance and
deviations, gates, traceability, documentation, testing, CI, releases and
version control. Where an enforcement field needs a concrete mechanism, it names
the C++ binding, the one bound language.

`PY-` and `RS-` are reserved for unwritten tiers (FW-1).

## Rule format

Every rule is a numbered clause with four fields. The ID is the stable part:
rules are never renumbered, because a citation must survive a reorganisation of
the document.

The fields are defined in
[EN-00's rule format](engineering/00-conformance.md#rule-format).
The rationale includes the argument against the rule where one exists.

## Chapters

### `engineering/` — `EN-*`

| Chapter | Covers |
|---|---|
| [00-conformance.md](engineering/00-conformance.md) | Normative force, the deviation procedure, standing deviations |
| [01-quality-gates.md](engineering/01-quality-gates.md) | Linting, warnings, sanitizers, coverage |
| [02-spec-and-traceability.md](engineering/02-spec-and-traceability.md) | Requirement IDs, citations and review |
| [03-documentation.md](engineering/03-documentation.md) | Structure and style of `docs/` |
| [04-testing.md](engineering/04-testing.md) | What to test, seams, what to fake |
| [05-ci-shape.md](engineering/05-ci-shape.md) | Workflow structure and required jobs |
| [06-release-and-versioning.md](engineering/06-release-and-versioning.md) | Version bumps, public API changes, release mechanics |
| [07-version-control.md](engineering/07-version-control.md) | Branch names, commit and issue form, merge and tag policy |
| [enforcement-matrix.md](engineering/enforcement-matrix.md) | Declared coverage of the engineering rules |

### `cxx/` — `CXX-*`

| Chapter | Covers |
|---|---|
| [00-conformance.md](cxx/00-conformance.md) | Resolving a diagnostic; how to suppress one |
| [01-lexical-and-naming.md](cxx/01-lexical-and-naming.md) | Naming; headers; include order |
| [02-types-and-declarations.md](cxx/02-types-and-declarations.md) | Type choice; constants; initialisation |
| [03-expressions-and-statements.md](cxx/03-expressions-and-statements.md) | Casts, arithmetic, loops, control flow |
| [04-functions-and-interfaces.md](cxx/04-functions-and-interfaces.md) | Signatures; parameter passing; preconditions |
| [05-classes-and-inheritance.md](cxx/05-classes-and-inheritance.md) | Special members; virtual functions |
| [06-resources-and-lifetime.md](cxx/06-resources-and-lifetime.md) | Ownership, allocation, spans and views, dangling |
| [07-error-handling.md](cxx/07-error-handling.md) | Reporting failure; capacity limits; input validation |
| [08-concurrency.md](cxx/08-concurrency.md) | Shared state, atomics, interrupt context |
| [09-templates.md](cxx/09-templates.md) | Writing and constraining a template; forwarding |
| [10-headers-and-abi.md](cxx/10-headers-and-abi.md) | Header layout; compile definitions; export names |
| [11-constrained-targets.md](cxx/11-constrained-targets.md) | Freestanding, embedded, fixed-capacity work |
| [12-security.md](cxx/12-security.md) | Untrusted input; trust boundaries |
| [13-repository-layout.md](cxx/13-repository-layout.md) | Where files go; test placement; the fixed root file set |
| [enforcement-matrix.md](cxx/enforcement-matrix.md) | Declared coverage of the C++ rules |

## The ones that matter most

Everything else is elaboration. If only these survive:

**EN-01.1 — Start from every check, exclude with a reason.** A tool
configuration that enables a hand-picked subset silently omits everything nobody
thought of, which is most of what the tool knows.

**EN-00.4 — A suppression names its rule and carries a justification.** It names
the exact rule and applies to one site, with the reason on the line above it.

**EN-00.5 — A rule turned off for a scope is a standing deviation.** Registered
with approval, a rationale, a risk assessment and a future review date,
checked by review.

**EN-02.1 — Every behavioural guarantee has an ID, and the code cites it.** The
ID is defined in the project's specification, and the code and tests that
implement and exercise the guarantee cite it.

**EN-02.2 — Cite the ID, never a section number.** IDs survive a reorganisation
of the document; section numbers do not.

## Where the C++ rules come from

Three sources, layered by what each is good at. None is adopted whole.

- **Design, lifetime, bounds and type safety** follow the C++ Core Guidelines.
  They are modern, maintained, and map near one-to-one onto `cppcoreguidelines-*`
  checks, so most of the layer is machine-checked.
- **Formatting** follows the Google C++ Style Guide, via clang-format's
  `BasedOnStyle: Google`. Its *language restrictions* are not adopted: they
  encode Google's internal history rather than a principle. Neither is its
  naming — `CXX-01.2` uses `lower_case` functions and `UPPER_CASE` constants
  where Google uses `CamelCase` and `kConstantName`, and `CXX-01.1` requires
  `#pragma once` where Google requires an `#ifndef` guard. Both departures are
  deliberate and carry their reasoning in the rule.
- **Security** draws on CERT C++, `bugprone-*` and the static analyzer.

Neither source prescribes a repository layout. `CXX-13` decides it, and says so
rather than implying a lineage it does not have.

MISRA C++:2023 is a paid, copyright-restricted document. Its text appears
nowhere here. Where `cxx/11-constrained-targets.md` serves a similar purpose — a
restricted subset for a constrained target — it was written from the underlying
engineering reason rather than derived from MISRA's wording.

## Binding to a language

Each `EN-` rule that needs a mechanism carries a binding table. One column is
populated today:

| | C++ | Python | Rust |
|---|---|---|---|
| Standard | `cxx/` | — | — |
| Linter | clang-tidy, `WarningsAsErrors: '*'` | — | — |
| Per-site suppression | `NOLINTNEXTLINE(check)` | — | — |
| Scope-wide disable | nested `.clang-tidy` | — | — |
| Compiler strictness | `-Werror` plus the shared warning set | — | — |

Adding a language means filling a column and adding a `<lang>/` tier that binds
the `EN-*` policies to that language's mechanisms — its linter, its per-site
suppression syntax, its scope-wide disable mechanism, its strictness flags.

## Citing a rule

Cite the ID alone. It is stable; paths, section numbers and chapter titles are
not.

```cpp
// CXX-06.3: the span does not own the buffer, so the caller outlives it.
```

| Where | Form |
|---|---|
| Code comment | `CXX-06.3` at the site the rule governs |
| Deviation rationale | the standard's rule ID in the prose; the **linter's own check name** in the register's first column, checked by review |
| Specification row | the `EN-` ID the requirement's structure follows |

## Consuming this repository

Consumers pin a revision of this standard. A change is adopted when that pin
moves. Rule IDs, the enforcement vocabulary and the gate-name table are the
versioned contract. A withdrawn ID remains reserved.

Run `python3 check.py` (`py -3 check.py` on Windows) with Python 3.11 or later
to check the rule structure, enforcement declarations, withdrawn IDs, matrix
and relative links. Exit 0
means pass, 1 means a defect, and 2 means an input could not be read.

### Enforcement vocabulary

Each `Enforcement` field is a comma-separated list of:

- `review`;
- `compiler (<flags or assertions>)` or `build (<flags or named test command>)`;
- `gate:<name> (full)` or `gate:<name> (partial)`.

Full means the gate covers the stated rule within its declared applicability.
Partial means a check covers only a stated part; the mechanism paragraph names
the boundary and review covers the remainder. A registered gate name declares
an interface, not proof that a particular tool implements it. Consumers must
verify their implementation with negative controls and record unsupported gates.

The matrix separates full gate coverage, partial gate coverage and other
checks. Concrete diagnostic names remain in each rule's mechanism paragraph.

## Gate names

Consumers implement these interfaces or identify the family-provided ones.

| Name | Provision |
|---|---|
| `deviations` | shared |
| `synced-files` | shared |
| `doc-links` | shared |
| `spdx` | shared |
| `commits` | shared |
| `format` | shared |
| `lint` | shared |
| `build-warnings` | shared |
| `compile-db` | shared |
| `api-docs` | shared |
| `consumer` | shared |
| `footprint` | family-provided |
| `symbols` | family-provided |

## AI-assisted development

This project is developed with AI assistance. Design decisions, review and
acceptance are human; an AI agent writes and refactors text under direction and
against a written engineering standard. Every change is reviewed against the
standard this repository defines before it lands.

This section is disclosure, not a warranty. The terms in [LICENSE](LICENSE)
apply unchanged, including its disclaimer of warranties.
