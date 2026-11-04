# CXX-11 — Constrained targets

This chapter applies to freestanding, embedded, real-time and fixed-capacity
work. Its restricted subset makes some advice for other targets mandatory here.

[Attribution](../engineering/00-conformance.md#attribution) explains the sources
and independent wording of these rules.

## CXX-11.1 — No allocation after initialisation

**Statement.** Heap allocation must not occur on a steady-state path after
initialisation completes. Allocation during initialisation is permitted and
budgeted separately.

**Rationale.** Constrained targets often lack a memory management unit (MMU),
swap or a way to recover from allocation failure. Fragmentation can eventually make a previously
successful request fail. Separate initialisation and steady-state budgets allow
tests to require zero allocations and a stable heap watermark after startup.

Capacity failures therefore surface as errors under CXX-07.2 because storage
cannot grow.

**Enforcement.** build (ctest), review.
**Deviation.** never.

**Mechanism.** an allocation-counting test; a heap-watermark check on device.

## CXX-11.2 — Static sizes come from a compile-time profile

**Statement.** Every static size must derive from a named compile-time profile.
Every profile invariant must be bound by `static_assert` to whatever
configuration it must agree with.

**Rationale.** Sizes in different files can drift. Binding assertions expose
a configuration change that leaves a buffer sized for a different window.
The profile must also reach consumers as CXX-10.3 requires.

**Enforcement.** compiler (static_assert), gate:consumer (partial), review.
**Deviation.** never.

**Mechanism.** `static_assert`; the consumer CI job.

## CXX-11.3 — No recursion

**Statement.** Recursion must not be used. Convert to iteration with an explicit
bound, or to an explicit stack of fixed capacity.

**Rationale.** Recursion converts input size into stack depth. Without a guard
page, overflow can corrupt the heap or another task's data. The crash can occur
much later and elsewhere.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `misc-no-recursion`.

## CXX-11.4 — Stack usage is bounded and known

**Statement.** Large local buffers must not be placed on the stack. Worst-case
stack depth must be understood, and anything sizeable must be static storage or
a caller-provided buffer.

**Rationale.** A stack of a few kilobytes shares its address space with other
data. A large local buffer can overflow it on the deepest call path, often an
untested error path.

**Enforcement.** gate:footprint (partial), review.
**Deviation.** never.

**Mechanism.** review; the footprint gate for static storage.

## CXX-11.5 — Exceptions and RTTI are unavailable

**Statement.** Where the build disables exceptions and RTTI, no path may require
them. A library intended for such consumers must compile and function with both
disabled.

**Rationale.** Exceptions add code size. Throwing with exceptions disabled
terminates the program. A compile-smoke build exposes an unusable library error
path before a consumer encounters it.

**Enforcement.** compiler (-fno-exceptions -fno-rtti), review.
**Deviation.** never.

**Mechanism.** a freestanding compile-smoke build in CI.

## CXX-11.6 — Static RAM has a budget, gated in CI

**Statement.** A project producing a firmware image must have a static RAM
budget, enforced in CI against the linked artefact.

**Rationale.** Small increases in static RAM use can accumulate until linking
fails or the stack has no room. A gate exposes each increase.

State the gate in the specification and keep measurements in run records
under EN-03.2.

**Enforcement.** gate:footprint (full).
**Deviation.** permitted with record.

**Mechanism.** The `footprint` gate, with the budget declared in the gate
configuration.

## CXX-11.7 — Hardware sits behind one seam with a fake

**Statement.** All hardware access must go through one interface per device,
with a fake implementation in the project's testing module. Only the platform
adapter may touch registers.

**Rationale.** The interface permits host tests under EN-04.1. Without it,
tests depend on the board and compete for one device, making them slow and less
likely to run.

The fake and real adapter must share the contract as well as the signature.
For example, an adapter returning an error for an idle bus when the contract
requires success can hang or fault a drain loop. A fake following the contract
will not expose that adapter defect.

**Enforcement.** review.
**Deviation.** permitted with record.

**Mechanism.** review; on-device validation.

## CXX-11.8 — A macro from a platform header may collide with your identifier

**Statement.** Before choosing an identifier that is a common short word in
upper case, you must check that no platform or vendor header defines it as a
macro.

**Rationale.** Vendor headers define macros such as `STATIC`, `MIN`, `ERROR`
and `INTERFACE`. A collision can appear only during cross-compilation as a
syntax error at a use of the identifier, without identifying the macro.

**Enforcement.** build (cross-compile), review.
**Deviation.** never.

**Mechanism.** the cross build.
