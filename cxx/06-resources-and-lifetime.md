# CXX-06 — Resources and lifetime

## CXX-06.1 — Every resource has an owner, and ownership is in the type

**Statement.** Every resource must be owned by exactly one object whose type
states the ownership. Raw `new` and `delete` must not appear outside a resource
type's own implementation.

**Rationale.** RAII means "resource acquisition is initialisation". It binds a
resource's lifetime to its owner and releases the resource on every exit from
the owner's scope.
A raw `new`/`delete` pair requires each intervening path to release correctly.
Expressing ownership in types leaves raw pointers unambiguously non-owning.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record — an allocator test that overrides global
`operator new` is malloc and free by definition.

**Mechanism.** `cppcoreguidelines-owning-memory`, `cppcoreguidelines-no-malloc`,
`modernize-make-unique`.

## CXX-06.2 — Fixed capacity over dynamic growth

**Statement.** Storage whose maximum size is known should be fixed-capacity.
Exceeding capacity must be reported as an error (`CXX-07.2`), never accommodated
by growing and never by truncating.

**Rationale.** Fixed capacity establishes worst-case resource use at compile
time. On a constrained target it is required. On other targets, it prevents
untrusted input from exhausting memory through a growing buffer.

**Enforcement.** gate:footprint (partial), review.
**Deviation.** permitted.

**Mechanism.** review; the footprint gate where one exists.

## CXX-06.3 — Every subscript is reached past a capacity guard

**Statement.** Every index into fixed-capacity storage must be reached only past
an explicit guard: a loop bound derived from the capacity, an early return on
`index >= capacity`, or an index whose type makes out-of-range values
unrepresentable.

**Rationale.** This standard rejects
`cppcoreguidelines-pro-bounds-constant-array-index` under EN-00.7 because its
prescribed remedy, `gsl::at`, throws and cannot be used without exceptions.
Review and design establish bounds safety in place of that check.

Prefer making bounds safety structural: an index type with 256 representable
values indexing a 256-entry table cannot be out of range and needs no further
guard.

**Enforcement.** build (-fsanitize=address), review.
**Deviation.** never.

**Mechanism.** The review checklist covers capacity guards. AddressSanitizer
(ASan) in CI detects out-of-bounds accesses that occur during tests.

## CXX-06.4 — No allocation on steady-state paths

**Statement.** Where the project commits to it, no allocation may occur after
initialisation on the paths that run repeatedly. Initialisation-time allocation
is budgeted separately.

**Rationale.** Repeated allocation can cause fragmentation and latency. On a
constrained target without a memory management unit (MMU), allocation can
eventually fail without recovery. Separating initialisation from repeated work
allows a test to count allocations and require zero after startup.

**Enforcement.** build (ctest), review.
**Deviation.** permitted with record.

**Mechanism.** an allocation-counting test; a heap-watermark check.

## CXX-06.5 — A view's referent outlives the view

**Statement.** A `std::span`, `std::string_view` or raw pointer must not outlive
the storage it refers to. Where one is stored in a member, the owning
relationship must be documented at the declaration.

**Rationale.** Views can dangle without a compiler diagnostic. For example,
`std::string_view sv = get_string();` dangles immediately if `get_string`
returns a string by value. The storage can remain readable long enough to hide
the defect.

**Enforcement.** build (-fsanitize=address), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `bugprone-dangling-handle`; `clang-analyzer-*`; ASan.

## CXX-06.6 — A moved-from object is only destroyed or reassigned

**Statement.** After an object has been moved from, it must only be destroyed or
assigned a new value.

**Rationale.** A moved-from object has a valid but unspecified state. Reading
it can produce a plausible wrong value without crashing.

Forwarding a reference more than once can move from it on the first call and
pass the moved-from object on later calls.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record,
for the multi-invocation forwarding case where forwarding would be wrong.

**Mechanism.** `bugprone-use-after-move`,
`cppcoreguidelines-missing-std-forward`.

## CXX-06.7 — Zero-copy buffers stay valid until released

**Statement.** Where a buffer is handed to a lower layer without copying, its
storage must remain valid and unmodified until that layer signals it is done.

**Rationale.** A zero-copy network transmit can retain a buffer pointer until
the data is acknowledged. Reusing the storage early changes what is transmitted
and can cause corruption that appears only under load.

The backing ring or pool is therefore sized by in-flight data, not message size.

**Enforcement.** review.
**Deviation.** never.
