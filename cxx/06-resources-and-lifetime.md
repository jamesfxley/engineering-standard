# CXX-06 — Resources and lifetime

## CXX-06.1 — Every resource has an owner, and ownership is in the type

**Statement.** Every resource must be owned by exactly one object whose type
states the ownership. Raw `new` and `delete` must not appear outside a resource
type's own implementation.

**Rationale.** RAII makes the release path unconditional — it happens on every
exit from the scope, including the ones nobody thought about. A raw
`new`/`delete` pair requires every path between them to be correct, and the
paths multiply.

A raw pointer is then unambiguously non-owning, which is what makes it safe to
pass around.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record — an allocator test that overrides global
`operator new` is malloc and free by definition.

**Mechanism.** `cppcoreguidelines-owning-memory`, `cppcoreguidelines-no-malloc`,
`modernize-make-unique`.

## CXX-06.2 — Fixed capacity over dynamic growth

**Statement.** Storage whose maximum size is known should be fixed-capacity.
Exceeding capacity must be reported as an error (`CXX-07.2`), never accommodated
by growing and never by truncating.

**Rationale.** Fixed capacity makes the worst case the same as the typical case,
so the resource question is answered at compile time rather than discovered
under load. It is a hard requirement on a constrained target and good practice
everywhere: a growable buffer fed by untrusted input is a memory-exhaustion
vector.

**Enforcement.** gate:footprint (partial), review.
**Deviation.** permitted.

**Mechanism.** review; the footprint gate where one exists.

## CXX-06.3 — Every subscript is reached past a capacity guard

**Statement.** Every index into fixed-capacity storage must be reached only past
an explicit guard: a loop bound derived from the capacity, an early return on
`index >= capacity`, or an index whose type makes out-of-range values
unrepresentable.

**Rationale.** This rule carries the weight that
`cppcoreguidelines-pro-bounds-constant-array-index` would, because this standard
rejects that check (`EN-00.7`) — its prescribed remedy is `gsl::at`, which
reports failure by throwing and so cannot be used in a build without exceptions.
The safety property still has to hold; it is enforced by review and by design
rather than by the check.

Prefer making it structural: an index type with 256 representable values
indexing a 256-entry table cannot be out of range, and needs no guard at all.

**Enforcement.** build (-fsanitize=address), review.
**Deviation.** never.

**Mechanism.** review — on the review checklist. ASan in CI catches the failures
that do occur.

## CXX-06.4 — No allocation on steady-state paths

**Statement.** Where the project commits to it, no allocation may occur after
initialisation on the paths that run repeatedly. Initialisation-time allocation
is budgeted separately.

**Rationale.** Post-initialisation allocation on a long-running program is a
fragmentation and latency source, and on a constrained target with no MMU it is
an eventual hard failure with no recovery. Separating the two pools is what makes
the commitment testable: a counter that must read zero after startup.

**Enforcement.** build (ctest), review.
**Deviation.** permitted with record.

**Mechanism.** an allocation-counting test; a heap-watermark check.

## CXX-06.5 — A view's referent outlives the view

**Statement.** A `std::span`, `std::string_view` or raw pointer must not outlive
the storage it refers to. Where one is stored in a member, the owning
relationship must be documented at the declaration.

**Rationale.** The compiler will not tell you. A view into a temporary is the
canonical case — `std::string_view sv = get_string();` where `get_string`
returns by value dangles immediately, and usually appears to work because the
memory is still there.

**Enforcement.** build (-fsanitize=address), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `bugprone-dangling-handle`; `clang-analyzer-*`; ASan.

## CXX-06.6 — A moved-from object is only destroyed or reassigned

**Statement.** After moving from an object, it must not be read except to
destroy or reassign it.

**Rationale.** A moved-from object is in a valid but unspecified state. Reading
it is not undefined behaviour, which is worse in practice — it produces a
plausible wrong value rather than a crash.

The subtle case is a forwarding reference invoked more than once: forwarding it
on the first call moves from it and passes a moved-from object to the rest.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record,
for the multi-invocation forwarding case where forwarding would be wrong.

**Mechanism.** `bugprone-use-after-move`,
`cppcoreguidelines-missing-std-forward`.

## CXX-06.7 — Zero-copy buffers stay valid until released

**Statement.** Where a buffer is handed to a lower layer without copying, its
storage must remain valid and unmodified until that layer signals it is done.

**Rationale.** Zero-copy transmit is the usual case: the network stack keeps a
pointer into the buffer until the data is acknowledged. Reusing the storage
before then transmits whatever is now there — silent corruption on the wire that
reproduces only under load.

This is why the ring or pool backing such a path is sized by in-flight data, not
by message size.

**Enforcement.** review.
**Deviation.** never.
