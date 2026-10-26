# CXX-09 — Templates and compile-time programming

## CXX-09.1 — Constrain with concepts

**Statement.** A template parameter with requirements must state them with a
concept or a `requires` clause. SFINAE must not be used where a concept works.

**Rationale.** An unconstrained template accepts anything and fails deep inside
its own body, producing an error naming internals the caller has never heard of.
A concept moves the failure to the call site and names the requirement that was
not met.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-09.2 — `if constexpr` over tag dispatch and specialisation

**Statement.** Compile-time branching should use `if constexpr` where it
applies, rather than overload sets or explicit specialisation.

**Rationale.** The alternatives spread one decision across several declarations
that must be read together to understand any of them. `if constexpr` keeps it in
one function where the branches are adjacent.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-09.3 — Forwarding references are forwarded exactly once

**Statement.** A forwarding reference parameter must be `std::forward`ed on the
path that consumes it, and must not be forwarded on a path that may run more than
once.

**Rationale.** Two opposite defects. Not forwarding silently copies what the
caller offered to move. Forwarding inside a loop moves on the first iteration and
passes a moved-from object to every one after — and because a moved-from object
is valid, the result is plausible wrong values rather than a crash.

A visitor invoked once per element is the common instance of the second: it must
*not* be forwarded.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, for the
multi-invocation case.

**Mechanism.** `cppcoreguidelines-missing-std-forward`,
`bugprone-use-after-move`.

## CXX-09.4 — Instantiation cost is a design consideration

**Statement.** A template instantiated over many types should keep its
type-dependent part small, moving type-independent logic into a non-template
function.

**Rationale.** Every instantiation is a fresh copy of the whole body in the
binary. On a size-constrained target this is a footprint problem; everywhere it
is a compile-time problem. Splitting the type-dependent shell from the shared
implementation costs little and removes most of the duplication.

**Enforcement.** gate:footprint (partial), review.
**Deviation.** permitted.

**Mechanism.** the footprint gate where one exists; review otherwise.

## CXX-09.5 — Compile-time tables are `constexpr`, and checked

**Statement.** A lookup table derivable at compile time must be `constexpr`, and
its invariants must be asserted with `static_assert`.

**Rationale.** A `constexpr` table lives in read-only storage and costs nothing
at startup. `static_assert` on its properties — size, monotonicity, no gaps —
turns a transcription error into a compile error rather than a wrong answer at
run time, which for a table transcribed from a specification is the difference
between finding the mistake now and finding it on hardware.

**Enforcement.** compiler (static_assert), review.
**Deviation.** never.

**Mechanism.** `static_assert`.

## CXX-09.6 — Bind compile-time configuration with `static_assert`

**Statement.** Where a compile-time configuration value must agree with another
configuration value — in a different header, a different module, or a
dependency's configuration — a `static_assert` must bind them.

**Rationale.** Two knobs that must agree and are set in different files *will*
diverge. The `static_assert` converts that from a subtle runtime misbehaviour —
a buffer sized for one window and a stack advertising another — into a build
failure naming both values.

Adding a new knob without its binding assertion is how the next drift happens.

**Enforcement.** compiler (static_assert), review.
**Deviation.** never.

**Mechanism.** `static_assert`.
