# CXX-08 — Concurrency and interrupt context

## CXX-08.1 — Shared mutable state is synchronised or eliminated

**Statement.** State reachable from more than one execution context must be
protected by a lock, expressed as an atomic with a stated memory order, or made
immutable. Unsynchronised access is a data race and therefore undefined
behaviour.

**Rationale.** A data race permits the compiler to reorder, duplicate or
remove accesses. Symptoms can appear unrelated to the racing code.

Eliminating sharing is usually preferable to protecting it. Handing ownership
through a queue removes the need to reason about those races.

**Enforcement.** build (-fsanitize=thread), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** ThreadSanitizer where the platform supports it; `concurrency-*`;
review otherwise.

## CXX-08.2 — Memory order is chosen, not defaulted past

**Statement.** Every atomic operation must use a memory order the author chose
and can justify. `memory_order_relaxed` requires a statement of why no ordering
is needed.

**Rationale.** Sequential consistency is correct but can be expensive. Relaxed
ordering suits an independent statistics counter. Publishing a ready buffer
needs release/acquire ordering so the reader sees the data before using it.

**Enforcement.** review.
**Deviation.** never.

## CXX-08.3 — Interrupt context is a separate execution context

**Statement.** Data shared between an interrupt handler and mainline code must
be synchronised as though between threads. The handler must not allocate, block,
take a lock the mainline holds, or call anything not documented as safe from
that context.

**Rationale.** An interrupt can pre-empt a non-atomic update. `volatile`
prevents caching but provides neither atomicity nor ordering. A handler waiting
on a lock held by interrupted code deadlocks.

**Enforcement.** review.
**Deviation.** never.

## CXX-08.4 — Multi-word values crossing contexts need a publication protocol

**Statement.** A value wider than the platform's atomic word size shared across
contexts must be published through a protocol that prevents readers from
seeing a partial update. Suitable protocols include a seqlock, double-buffering
or an atomic of adequate width.

**Rationale.** A reader can interrupt two 32-bit stores of a 64-bit timestamp
and see a value that was never written. The defect can appear later as an
implausible interval.

For one writer and many readers, a seqlock brackets each write with an odd/even
counter. A reader retries if the counter changed or was odd.

**Enforcement.** review.
**Deviation.** never.

## CXX-08.5 — A lock is held for as little as possible

**Statement.** Work that does not require a lock must be done outside it. User
callbacks must not run while a lock is held.

**Rationale.** Lock hold time adds latency to every producer and consumer of
a serialised queue. A user callback can hold the lock for an unbounded time or
re-enter the subsystem and deadlock.

Measure hold time where it matters. A p99 budget, bounding the 99th percentile,
can be tested.

**Enforcement.** build (ctest), review.
**Deviation.** permitted with record.

**Mechanism.** an instrumented measurement in a debug build.

## CXX-08.6 — Deadline arithmetic is wrap-safe

**Statement.** A comparison against a deadline derived from a wrapping clock
must use signed-difference comparison, never a direct magnitude comparison.

**Rationale.** A 32-bit millisecond clock wraps after about 49 days. Direct
comparison with `now >= deadline` can fire a timeout immediately or leave it
waiting indefinitely across the wrap.
`static_cast<std::int32_t>(now - deadline) >= 0` compares across that boundary.

**Enforcement.** build (ctest), review.
**Deviation.** never.

**Mechanism.** tests that cross the wrap boundary explicitly.
