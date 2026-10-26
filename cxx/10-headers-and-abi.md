# CXX-10 — Headers, modularity and ABI

## CXX-10.1 — Every header is self-contained

**Statement.** A header must compile on its own, including everything it needs
and depending on no particular include order.

**Rationale.** Order-dependent headers work until someone reorders an unrelated
include, at which point a header far away fails to compile. Including the
matching header first in each `.cpp` (`CXX-01.4`) proves this continuously.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** the include-order rule; `misc-include-cleaner`.

## CXX-10.2 — Public headers are a namespaced tree

**Statement.** Public headers must live under a directory named for the project,
and must be included as `<project/module/thing.hpp>`. Implementation detail lives under a
`detail/` subdirectory and is not part of the public surface.

**Rationale.** The prefix prevents collisions with other libraries' headers and
makes every include self-describing. `detail/` states what consumers may not
depend on — without it, everything reachable becomes de facto public and cannot
be changed.

**Enforcement.** review.
**Deviation.** never.

## CXX-10.3 — A consumer-visible macro is a `PUBLIC` compile definition on the owning target

**Statement.** A macro that changes a type's layout, size or behaviour as seen by
a consumer must be a `PUBLIC` `target_compile_definitions` on the target owning
the header that reads it. `add_compile_definitions` at directory scope must not
be used for it.

**Rationale.** This is the highest-severity build-system defect in this
standard, because it fails silently and catastrophically.

A directory-scoped definition reaches only the defining project's own targets.
A consumer that includes the header compiles it *without* the definition, so the
consumer and the library disagree about a structure's size — and the result is
stack corruption in the consumer, at a point unrelated to the cause.

`PUBLIC` on the owning target propagates through the link graph to every
consumer that links it, which is the only mechanism that gets this right.

Verify rather than assume: configure a consumer with a non-default value and
grep its `compile_commands.json` for the definition, per translation unit.

**Enforcement.** gate:consumer (partial), review.
**Deviation.** never.

**Mechanism.** the consumer CI job (`EN-05.1`) is what catches it.

## CXX-10.4 — Exported target names match in-tree names

**Statement.** An installed target's exported name must be identical to its
in-tree `ALIAS`. Strip the namespace prefix from the target name when setting
`EXPORT_NAME`.

**Rationale.** A target named `mylib_core` with an alias `mylib::core` exports by
default as `mylib::mylib_core`. In-tree consumers link `mylib::core` and
`find_package` consumers must write `mylib::mylib_core` — so every documented
link line is wrong for exactly one of the two audiences, and the failure only
appears once someone consumes the installed package.

**Enforcement.** gate:consumer (partial), review.
**Deviation.** never.

**Mechanism.** the installed-package consumer checks exported target names.

## CXX-10.5 — Header-only where the cost is genuinely zero

**Statement.** A component should be header-only only where it is a template, a
handful of inline functions, or a `constexpr` table. Anything with a real
implementation belongs in a `.cpp`.

**Rationale.** Header-only means recompiling every consumer on every change, and
every consumer paying the parse cost. It buys a simpler build, which is worth
little compared to the compile-time cost at any size.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-10.6 — Do not open namespaces you do not own

**Statement.** `std` must not be modified. A specialisation for a user type may
be added only where the standard explicitly permits it.

**Rationale.** Adding declarations to `std` is undefined behaviour, and the
usual symptom is a link-time conflict or a silently different overload chosen in
a different translation unit.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `cert-dcl58-cpp`.

## CXX-10.7 — Anonymous namespaces do not appear in headers

**Statement.** An anonymous namespace must not be used in a header. Use `inline`
or `constexpr` for a header-scope entity instead.

**Rationale.** It gives every translation unit including the header its own
distinct copy with a distinct address — so an ODR-relevant comparison of
addresses disagrees between translation units, and any state in it is silently
per-TU.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `google-build-namespaces`.
