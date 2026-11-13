# Engineering standard

This repository defines the engineering and C++ rules used by this author's
projects. It is the source for their `EN-` and `CXX-` citations.

Keeping the rules here lets readers resolve citations independently of any
project or developer's tool configuration.

## The two tiers

Separate engineering and language tiers allow languages to be added without
restructuring the standard.

| Tier | IDs | Contents |
|---|---|---|
| [`engineering/`](engineering/) | `EN-<chapter>.<n>` | Engineering rules. |
| [`cxx/`](cxx/) | `CXX-<chapter>.<n>` | C++ language rules, with citations to `EN-*`. |

The engineering rules are language-independent. They cover conformance and
deviations, gates, traceability, documentation, testing, CI, releases and
version control. Where an enforcement field needs a concrete mechanism, it names
the C++ binding, the one bound language.

[FW-1](docs/future-work.md#fw-1--python-and-rust-language-tiers) covers the
reserved Python and Rust tiers.

## Rule format

[EN-00's rule format](engineering/00-conformance.md#rule-format) defines each
clause's four fields. [EN-00.1](engineering/00-conformance.md#en-001--rule-ids-are-stable)
governs IDs. Rationales include the argument against a rule where one exists.

## Chapters

### `engineering/` — `EN-*`

| Chapter | Covers |
|---|---|
| [00-conformance.md](engineering/00-conformance.md) | Normative force, the deviation procedure, standing deviations |
| [01-quality-gates.md](engineering/01-quality-gates.md) | Linting, warnings, sanitisers, coverage |
| [02-spec-and-traceability.md](engineering/02-spec-and-traceability.md) | Requirement IDs, citations and review |
| [03-documentation.md](engineering/03-documentation.md) | Structure and style of `docs/` |
| [04-testing.md](engineering/04-testing.md) | What to test, seams, what to fake |
| [05-ci-shape.md](engineering/05-ci-shape.md) | Workflow structure and required jobs |
| [06-release-and-versioning.md](engineering/06-release-and-versioning.md) | Version bumps, public API changes, release mechanics, device tests and benchmarks |
| [07-version-control.md](engineering/07-version-control.md) | Branch names, commit and issue form, pull request verification, merge and tag policy |
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

## Selected rules

- [EN-01.1](engineering/01-quality-gates.md#en-011--start-from-every-check-exclude-with-a-reason)
  governs linter configuration.
- [EN-00.4](engineering/00-conformance.md#en-004--a-suppression-names-its-rule-and-carries-a-justification)
  governs site suppressions.
- [EN-00.5](engineering/00-conformance.md#en-005--scope-wide-suppression-is-a-standing-deviation)
  governs standing deviations.
- [EN-02.1](engineering/02-spec-and-traceability.md#en-021--every-behavioural-guarantee-has-an-id)
  governs requirement IDs and citations.
- [EN-02.2](engineering/02-spec-and-traceability.md#en-022--cite-the-id-never-a-section-number)
  governs the form of requirement citations.

## Where the C++ rules come from

[Attribution](engineering/00-conformance.md#attribution) names the published
sources and explains their use. None is adopted in full.

The maintained Core Guidelines map near one-to-one to `cppcoreguidelines-*`
checks, making most of the design, lifetime, bounds and type-safety layer
machine-checked. Security checks use `bugprone-*` and the static analyser.

Google's language restrictions reflect its internal history and are not adopted. Naming and
include guards follow
[CXX-01.2](cxx/01-lexical-and-naming.md#cxx-012--identifier-case) and
[CXX-01.1](cxx/01-lexical-and-naming.md#cxx-011--pragma-once-on-line-1).
Google uses `CamelCase` functions, `kConstantName` constants and `#ifndef`
include guards. The linked rules explain this standard's choices.
[CXX-13](cxx/13-repository-layout.md) defines the repository layout.

## Binding to a language

Binding tables give language-specific mechanisms for `EN-` rules. C++ is the
only populated column:

| | C++ | Python | Rust |
|---|---|---|---|
| Standard | `cxx/` | — | — |
| Linter | [EN-01 binding](engineering/01-quality-gates.md#binding) | — | — |
| Per-site suppression | [CXX-00.2](cxx/00-conformance.md#cxx-002--suppression-syntax) | — | — |
| Scope-wide disable | [CXX-00.3](cxx/00-conformance.md#cxx-003--scope-wide-disables-are-registered-not-added) | — | — |
| Compiler strictness | [EN-01 binding](engineering/01-quality-gates.md#binding) | — | — |

Adding a language requires a binding column and a `<lang>/` tier. The tier
binds `EN-*` policies to the language's linter, site suppressions, scope-wide
disables and strictness flags.

## Citing a rule

[EN-00.9](engineering/00-conformance.md#en-009--source-code-cites-a-rule-only-to-suppress-or-check-it)
governs rule citations in source code.
[EN-02.2](engineering/02-spec-and-traceability.md#en-022--cite-the-id-never-a-section-number)
governs requirement citations.

```cpp
// CXX-06.3: the span does not own the buffer, so the caller outlives it.
```

| Where | Form |
|---|---|
| Code comment | See EN-00.9 above. |
| Deviation rationale | See [EN-00.5](engineering/00-conformance.md#en-005--scope-wide-suppression-is-a-standing-deviation). |
| Specification row | The `EN-` ID governing the requirement's structure. |

## Consuming this repository

Consumers pin a revision of this standard. A change is adopted when that pin
moves. Rule IDs, the enforcement vocabulary and the gate-name table are the
versioned contract. EN-00.1 governs withdrawn IDs.

Run `python3 check.py` (`py -3 check.py` on Windows) with Python 3.11 or later
to check the rule structure, enforcement declarations, withdrawn IDs, matrix
and relative links. Exit status 0 means pass, 1 means a defect, and 2 means an
input could not be read.

### Enforcement vocabulary

Each `Enforcement` field is a comma-separated list of:

- `review`;
- `compiler (<flags or assertions>)` or `build (<flags or named test command>)`;
- `gate:<name> (full)` or `gate:<name> (partial)`.

Full means the gate covers the stated rule within its declared applicability.
Partial means a check covers only the part named in the mechanism paragraph.
Review covers the remainder. A registered name declares a gate interface.
Consumers must verify their implementation with negative controls and record
unsupported gates.

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

This project uses AI assistance to write and refactor text under human
direction. People make design decisions and decide whether to accept changes.
Every change is reviewed against this standard before it lands.

The terms in [LICENSE](LICENSE) apply, including the disclaimer of warranties.
