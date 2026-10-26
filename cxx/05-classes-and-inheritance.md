# CXX-05 — Classes and inheritance

## CXX-05.1 — Rule of zero, then rule of five

**Statement.** A type should declare no special member functions. If it must
declare one of destructor, copy constructor, copy assignment, move constructor
or move assignment, it must declare or delete all five.

**Rationale.** Declaring one suppresses others in ways that are easy to get
wrong: a user-declared destructor suppresses the implicit move operations, so a
type that was cheap to move silently starts copying — a performance change with
no diagnostic.

Rule of zero is the goal. A type that owns nothing raw needs none of the five,
and the compiler's versions are correct by construction.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, in test doubles constructed on the stack
and never copied.

**Mechanism.** `cppcoreguidelines-special-member-functions`.

## CXX-05.2 — Single-argument constructors are `explicit`

**Statement.** A constructor callable with one argument must be `explicit`,
unless implicit conversion is the type's deliberate purpose.

**Rationale.** Implicit conversion turns an unrelated argument into a valid call
at a distance, and changes overload resolution in code that never mentioned the
type.

Conversion operators are the same rule; mark them `explicit` too.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with
record, for a deliberate conversion type.

**Mechanism.** `google-explicit-constructor`.

## CXX-05.3 — Polymorphic destruction

**Statement.** A class with virtual functions must have either a public virtual
destructor or a protected non-virtual one. A class not designed for inheritance
should be `final`.

**Rationale.** Deleting through a base pointer with a non-virtual destructor is
undefined behaviour and typically leaks the derived part silently. The protected
non-virtual form is the correct choice for an interface never deleted
polymorphically, and says so.

`final` on a leaf class devirtualises calls and states intent.

**Enforcement.** gate:lint (partial), compiler (-Wnon-virtual-dtor), review.
**Deviation.** never.

**Mechanism.** `cppcoreguidelines-virtual-class-destructor`;
`-Wnon-virtual-dtor`.

## CXX-05.4 — `override`, never repeated `virtual`

**Statement.** An overriding function must be marked `override` and must not
repeat `virtual`.

**Rationale.** `override` makes a signature mismatch a compile error. Without
it, changing a base signature silently creates a new function that is never
called, and the derived behaviour disappears with no diagnostic.

**Enforcement.** gate:lint (partial), compiler (-Woverloaded-virtual), review.
**Deviation.** never.

**Mechanism.** `modernize-use-override`; `-Woverloaded-virtual`.

## CXX-05.5 — Data members are private in a class with behaviour

**Statement.** A type with invariants must keep its data private. An aggregate
with no invariants may have public data and should be a `struct`.

**Rationale.** The distinction is whether there is an invariant to protect. A
struct that is purely a bundle of values has none, and wrapping it in accessors
adds noise without adding safety. A type that maintains a relationship between
its members must control every write to them.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `misc-non-private-member-variables-in-classes`, configured to
permit the all-public aggregate.

## CXX-05.6 — Reference members only where the reference is the design

**Statement.** A class may hold a reference member only where the referent
outlives it by construction and the class is non-copyable. Otherwise hold a
pointer or a value.

**Rationale.** A reference member deletes copy assignment and cannot be
rebound, which is either exactly what you want or a problem discovered much
later. It is right when a component is handed a collaborator that outlives it
and null is not a valid state — storing a pointer there would add a state that
cannot occur.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record — and this is a common legitimate one.

**Mechanism.** `cppcoreguidelines-avoid-const-or-ref-data-members`.

## CXX-05.7 — Interfaces are narrow and abstract

**Statement.** An interface used as a seam should declare only the operations
its consumers call, with no data members and no implementation beyond defaulted
no-ops where a default genuinely applies.

**Rationale.** Every method on a seam is a method every fake and every real
implementation must provide. A wide interface makes writing a second
implementation expensive, which is the thing the seam existed to make cheap.

Defaulted no-op methods are a real convenience for an event sink with many
optional callbacks — an implementer overrides the two they care about.

**Enforcement.** review.
**Deviation.** permitted.
