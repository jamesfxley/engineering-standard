# CXX-05 — Classes and inheritance

## CXX-05.1 — Rule of zero, then rule of five

**Statement.** A type should declare no special member functions. If it must
declare one of destructor, copy constructor, copy assignment, move constructor
or move assignment, it must declare or delete all five.

**Rationale.** Declaring one special member can suppress others. A
user-declared destructor suppresses implicit move operations, which can make a
type copy instead of move without a diagnostic.

A type without raw ownership needs none of the five; compiler-generated members
handle its resources correctly.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, in test doubles constructed on the stack
and never copied.

**Mechanism.** `cppcoreguidelines-special-member-functions`.

## CXX-05.2 — Single-argument constructors are `explicit`

**Statement.** A constructor callable with one argument must be `explicit`,
unless implicit conversion is the type's deliberate purpose.

**Rationale.** Implicit conversion can make an unrelated argument a valid call
and change overload resolution in code that does not mention the type.

The same rule applies to conversion operators.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with
record, for a deliberate conversion type.

**Mechanism.** `google-explicit-constructor`.

## CXX-05.3 — Polymorphic destruction

**Statement.** A class with virtual functions must have either a public virtual
destructor or a protected non-virtual one. A class not designed for inheritance
should be `final`.

**Rationale.** Deleting through a base pointer with a non-virtual destructor
is undefined behaviour and can leak the derived part. A protected non-virtual
destructor prevents deletion through the interface.

`final` states that inheritance ends at the class and allows devirtualisation.

**Enforcement.** gate:lint (partial), compiler (-Wnon-virtual-dtor), review.
**Deviation.** never.

**Mechanism.** `cppcoreguidelines-virtual-class-destructor`;
`-Wnon-virtual-dtor`.

## CXX-05.4 — `override`, never repeated `virtual`

**Statement.** An overriding function must be marked `override` and must not
repeat `virtual`.

**Rationale.** `override` exposes signature mismatches at compile time.
Without it, a base-signature change can leave a derived function that no longer
overrides and is never called.

**Enforcement.** gate:lint (partial), compiler (-Woverloaded-virtual), review.
**Deviation.** never.

**Mechanism.** `modernize-use-override`; `-Woverloaded-virtual`.

## CXX-05.5 — Data members are private in a class with behaviour

**Statement.** A type with invariants must keep its data private. An aggregate
with no invariants may have public data and should be a `struct`.

**Rationale.** A type with relationships between its members needs to control
every write. Accessors add no safety to an aggregate that has no invariant.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `misc-non-private-member-variables-in-classes`, configured to
permit the all-public aggregate.

## CXX-05.6 — Reference members only where the reference is the design

**Statement.** A class may hold a reference member only where the referent
outlives it by construction and the class is non-copyable. Otherwise hold a
pointer or a value.

**Rationale.** A reference member cannot be rebound and deletes copy
assignment. Those properties suit a component whose non-null collaborator
outlives it. A pointer would add a null state that the design does not use.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record — and this is a common legitimate one.

**Mechanism.** `cppcoreguidelines-avoid-const-or-ref-data-members`.

## CXX-05.7 — Interfaces are narrow and abstract

**Statement.** An interface used as a seam should declare only the operations
its consumers call, with no data members and no implementation beyond defaulted
no-ops where a default genuinely applies.

**Rationale.** Every fake and every real implementation must provide every
method on a seam. A wide interface makes a second implementation expensive,
which defeats the purpose of the seam.

Default no-op callbacks let an event sink implement only the optional events
it needs.

**Enforcement.** review.
**Deviation.** permitted.
