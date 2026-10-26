# CXX-11 — Constrained targets

Applies to freestanding, embedded, real-time and fixed-capacity work. This is
the restricted subset: rules that are advice elsewhere and requirements here.

Written from the underlying engineering reasons. No MISRA text is reproduced.

## CXX-11.1 — No allocation after initialisation

**Statement.** On the steady-state paths, no heap allocation must occur after the
start or begin call. Initialisation-time allocation is permitted and budgeted
separately.

**Rationale.** There is often no MMU or swap, and nothing to recover an
allocation failure. Fragmentation on a long-running system eventually fails a
request that succeeded a million times, at a point with no sensible handler.
Splitting the two pools makes the commitment testable rather than aspirational:
a counter that must read zero after startup, and a heap watermark that must stop
growing.

The corollary is that capacity failures surface as errors (`CXX-07.2`), because
growing is not an option.

**Enforcement.** build (ctest), review.
**Deviation.** never.

**Mechanism.** an allocation-counting test; a heap-watermark check on device.

## CXX-11.2 — Static sizes come from a compile-time profile

**Statement.** Every static size must derive from a named compile-time profile
rather than a scattered literal, and every profile invariant must be bound by
`static_assert` to whatever configuration it must agree with.

**Rationale.** Sizes that must agree and live in different files diverge. The
binding assertion is what makes a new knob safe to add — without it, the next
configuration change leaves one of the pair behind and produces a buffer sized
for a window nobody advertises.

The profile must reach consumers correctly; see `CXX-10.3`, which is the failure
mode this rule most often meets.

**Enforcement.** compiler (static_assert), gate:consumer (partial), review.
**Deviation.** never.

**Mechanism.** `static_assert`; the consumer CI job.

## CXX-11.3 — No recursion

**Statement.** Recursion must not be used. Convert to iteration with an explicit
bound, or to an explicit stack of fixed capacity.

**Rationale.** Recursion converts input size into stack depth, and there is
often no guard page. Overflow silently corrupts whatever is below the stack —
often the heap or another task's data — and the crash is somewhere else
entirely, minutes later.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `misc-no-recursion`.

## CXX-11.4 — Stack usage is bounded and known

**Statement.** Large local buffers must not be placed on the stack. Worst-case
stack depth must be understood, and anything sizeable must be static storage or
a caller-provided buffer.

**Rationale.** The stack is small — often kilobytes — and shares its address
space with everything else. A multi-kilobyte local looks harmless and is a
silent overflow on the deepest call path, which is usually the error path nobody
tested.

**Enforcement.** gate:footprint (partial), review.
**Deviation.** never.

**Mechanism.** review; the footprint gate for static storage.

## CXX-11.5 — Exceptions and RTTI are unavailable

**Statement.** Where the build disables exceptions and RTTI, no path may require
them. A library intended for such consumers must compile and function with both
disabled.

**Rationale.** Beyond the code-size cost, a `throw` on a build with exceptions
disabled terminates. A library that throws on its error path is unusable, and
this is discovered by the consumer rather than by its own tests unless a
compile-smoke build enforces it.

**Enforcement.** compiler (-fno-exceptions -fno-rtti), review.
**Deviation.** never.

**Mechanism.** a freestanding compile-smoke build in CI.

## CXX-11.6 — Static RAM has a budget, gated in CI

**Statement.** A project producing a firmware image must have a static RAM
budget, enforced in CI against the linked artefact.

**Rationale.** Static footprint grows a few hundred bytes at a time and nobody
notices until a link fails or a stack has nowhere left to go. A gate turns each
increment into a decision.

State the gate in the specification; keep the measured value in the run record
(`EN-03.2`).

**Enforcement.** gate:footprint (full).
**Deviation.** permitted with record.

**Mechanism.** The `footprint` gate, with the budget declared in the gate
configuration.

## CXX-11.7 — Hardware sits behind one seam with a fake

**Statement.** All hardware access must go through one interface per device,
with a fake implementation in the project's testing module. Only the platform
adapter may touch registers.

**Rationale.** `EN-04.1`, and it matters most here: without it, nothing is
testable without the board, so the suite is slow, serialised on one piece of
hardware, and eventually not run.

A specific trap: the fake and the real adapter must agree on the *contract*, not
just the signature. An adapter that returns an error for an idle bus where the
contract says success will wedge or fault a drain loop — and the fake, written to
the contract, will never show it.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** review; on-device validation.

## CXX-11.8 — A macro from a platform header may collide with your identifier

**Statement.** Before choosing an identifier that is a common short word in
upper case, you must check that no platform or vendor header defines it as a
macro.

**Rationale.** Vendor headers define macros with names like `STATIC`, `MIN`,
`ERROR` and `INTERFACE`. The collision does not appear on a host build — only on
the cross build, as a syntax error somewhere the name is used, with no
indication that a macro is responsible.

**Enforcement.** build (cross-compile), review.
**Deviation.** never.

**Mechanism.** the cross build.
