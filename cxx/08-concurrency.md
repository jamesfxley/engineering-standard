# CXX-08 — Concurrency and interrupt context

## CXX-08.1 — Shared mutable state is synchronised or eliminated

**Statement.** State reachable from more than one execution context must be
protected by a lock, expressed as an atomic with a stated memory order, or made
immutable. Unsynchronised access is a data race and therefore undefined
behaviour.

**Rationale.** A race is not "an occasional wrong value". It is undefined
behaviour, so the compiler may reorder, duplicate or elide the accesses; the
observed symptom often has no relationship to the racing code.

Eliminating the sharing is usually better than protecting it. Ownership handoff
through a queue has no race to reason about.

**Enforcement.** build (-fsanitize=thread), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** ThreadSanitizer where the platform supports it; `concurrency-*`;
review otherwise.

## CXX-08.2 — Memory order is chosen, not defaulted past

**Statement.** Every atomic operation must use a memory order the author chose
and can justify. `memory_order_relaxed` requires a statement of why no ordering
is needed.

**Rationale.** The sequentially-consistent default is correct and sometimes
expensive; `relaxed` is cheap and frequently wrong. A counter incremented for
statistics is genuinely relaxed. A flag publishing that a buffer is ready is
not — it needs release/acquire, and getting it wrong produces a reader that sees
the flag before the data.

**Enforcement.** review.
**Deviation.** never.

## CXX-08.3 — Interrupt context is a separate execution context

**Statement.** Data shared between an interrupt handler and mainline code must
be synchronised as though between threads. The handler must not allocate, block,
take a lock the mainline holds, or call anything not documented as safe from
that context.

**Rationale.** An interrupt handler pre-empts mainline code at an arbitrary
instruction — including halfway through a non-atomic update. `volatile` does not
help: it prevents the compiler caching the value but provides no atomicity and
no ordering.

A handler that blocks on a lock the interrupted code holds deadlocks with no way
out.

**Enforcement.** review.
**Deviation.** never.

## CXX-08.4 — Multi-word values crossing contexts need a publication protocol

**Statement.** A value wider than the platform's atomic word size shared across
contexts must be published through a protocol that makes tearing impossible — a
seqlock, double-buffering, or an atomic of adequate width.

**Rationale.** A 64-bit timestamp written as two 32-bit stores on a 32-bit
machine can be read between them, producing a value that never existed. The
result is plausible, and typically appears as an implausible time interval much
later.

A seqlock is the usual answer for one writer and many readers: the writer
brackets the update with an odd/even counter, and a reader retries when the
counter changed or was odd.

**Enforcement.** review.
**Deviation.** never.

## CXX-08.5 — A lock is held for as little as possible

**Statement.** Work that does not require a lock must be done outside it. User
callbacks must not run while a lock is held.

**Rationale.** When a queue is serialised by one lock, hold
time adds latency to every producer and consumer. A user callback under the lock is
unbounded hold time by an unknown party, and is also how re-entrant deadlock
happens — the callback calls back into the locked subsystem.

Where hold time matters, measure it: a p99 hold-time budget is a testable
requirement, an intention is not.

**Enforcement.** build (ctest), review.
**Deviation.** permitted with record.

**Mechanism.** an instrumented measurement in a debug build.

## CXX-08.6 — Deadline arithmetic is wrap-safe

**Statement.** A comparison against a deadline derived from a wrapping clock
must use signed-difference comparison, never a direct magnitude comparison.

**Rationale.** A millisecond tick in 32 bits wraps after about 49 days. `now >=
deadline` fails across the wrap and the timeout either fires immediately or
never — after seven weeks of uptime, on a system nobody is watching.
`static_cast<std::int32_t>(now - deadline) >= 0` is correct across it.

**Enforcement.** build (ctest), review.
**Deviation.** never.

**Mechanism.** tests that cross the wrap boundary explicitly.
