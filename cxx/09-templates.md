# CXX-09 — Templates and compile-time programming

## CXX-09.1 — Constrain with concepts

**Statement.** A template parameter with requirements must state them with a
concept or a `requires` clause. SFINAE (substitution failure is not an error)
must not be used where a concept works.

**Rationale.** An unconstrained template can fail inside its body with an
error naming unfamiliar internals. A concept reports the unmet requirement at
the call site.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-09.2 — `if constexpr` over tag dispatch and specialisation

**Statement.** Compile-time branching should use `if constexpr` where it
applies, rather than overload sets or explicit specialisation.

**Rationale.** Overloads and specialisations spread a decision across
declarations that must be read together. `if constexpr` keeps the branches
beside each other in one function.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-09.3 — Forwarding references are forwarded exactly once

**Statement.** A forwarding reference parameter must be passed with
`std::forward` on the path that consumes it. It must not be forwarded on a path
that may run more than once.

**Rationale.** Failing to forward can copy a value the caller offered to move.
Forwarding in a loop can move on the first iteration and pass a moved-from
object on later iterations, producing plausible wrong values.

A visitor invoked once per element must not be forwarded.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, for the
multi-invocation case.

**Mechanism.** `cppcoreguidelines-missing-std-forward`,
`bugprone-use-after-move`.

## CXX-09.4 — Instantiation cost is a design consideration

**Statement.** A template instantiated over many types should keep its
type-dependent part small, moving type-independent logic into a non-template
function.

**Rationale.** Each instantiation adds another copy of the body to the binary
and repeats compilation work. Sharing type-independent logic reduces both
costs, particularly binary size on constrained targets.

**Enforcement.** gate:footprint (partial), review.
**Deviation.** permitted.

**Mechanism.** the footprint gate where one exists; review otherwise.

## CXX-09.5 — Compile-time tables are `constexpr`, and checked

**Statement.** A lookup table derivable at compile time must be `constexpr`, and
its invariants must be asserted with `static_assert`.

**Rationale.** A `constexpr` table uses read-only storage and needs no startup
work. Assertions about size, monotonicity or missing entries expose
transcription errors during compilation instead of on hardware.

**Enforcement.** compiler (static_assert), review.
**Deviation.** never.

**Mechanism.** `static_assert`.

## CXX-09.6 — Bind compile-time configuration with `static_assert`

**Statement.** Where a compile-time configuration value must agree with another
configuration value, a `static_assert` must bind them. The values can be in
different headers, modules or dependency configurations.

**Rationale.** Configuration values in separate files can diverge. An
assertion exposes disagreement during the build, before a buffer sized for one
window meets a stack advertising another. Adding a new value without its binding
assertion leaves the same risk of drift.

**Enforcement.** compiler (static_assert), review.
**Deviation.** never.

**Mechanism.** `static_assert`.
