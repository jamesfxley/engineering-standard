# CXX-10 — Headers, modularity and ABI

## CXX-10.1 — Every header is self-contained

**Statement.** A header must compile on its own, including everything it needs
and depending on no particular include order.

**Rationale.** A header that depends on include order can fail after an
unrelated include is moved. Including the matching header first in each `.cpp`
checks self-containment continuously (CXX-01.4).

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** the include-order rule; `misc-include-cleaner`.

## CXX-10.2 — Public headers are a namespaced tree

**Statement.** Public headers must live under a directory named for the project,
and must be included as `<project/module/thing.hpp>`. Implementation details
live under a `detail/` subdirectory outside the public surface.

**Rationale.** The project prefix prevents header-name collisions and
identifies the owner of each include. `detail/` marks reachable headers that
consumers may not depend on, allowing their implementation to change.

**Enforcement.** review.
**Deviation.** never.

## CXX-10.3 — A consumer-visible macro is a `PUBLIC` compile definition on the owning target

**Statement.** A macro that changes a type's layout, size or behaviour as seen by
a consumer must be a `PUBLIC` `target_compile_definitions` on the target owning
the header that reads it. `add_compile_definitions` at directory scope must not
be used for it.

**Rationale.** A directory-scoped definition reaches only the project's own
targets. A consumer can compile a public header without the definition and use
a different structure size, causing stack corruption far from its cause.

A `PUBLIC` definition on the owning target propagates to consumers through the
link graph. Verify it by configuring a consumer with a non-default value and
checking each translation unit's entry in `compile_commands.json`.

**Enforcement.** gate:consumer (partial), review.
**Deviation.** never.

**Mechanism.** the consumer CI job (`EN-05.1`) is what catches it.

## CXX-10.4 — Exported target names match in-tree names

**Statement.** An installed target's exported name must be identical to its
in-tree `ALIAS`. Strip the namespace prefix from the target name when setting
`EXPORT_NAME`.

**Rationale.** A target `mylib_core` with alias `mylib::core` exports by default
as `mylib::mylib_core`. Different names make a documented link command fail for
either in-tree or installed-package consumers.

**Enforcement.** gate:consumer (partial), review.
**Deviation.** never.

**Mechanism.** the installed-package consumer checks exported target names.

## CXX-10.5 — Header-only where the cost is genuinely zero

**Statement.** A component should be header-only only where it is a template, a
handful of inline functions, or a `constexpr` table. Anything with a real
implementation belongs in a `.cpp`.

**Rationale.** Header-only code makes every consumer parse the implementation
and recompile when it changes. The simpler build rarely offsets that
compilation cost as the implementation grows.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-10.6 — Do not open namespaces you do not own

**Statement.** `std` must not be modified. A specialisation for a user type may
be added only where the standard explicitly permits it.

**Rationale.** Unpermitted declarations in `std` cause undefined behaviour.
Symptoms include link conflicts and different overload choices in different
translation units.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `cert-dcl58-cpp`.

## CXX-10.7 — Anonymous namespaces do not appear in headers

**Statement.** An anonymous namespace must not be used in a header. Use `inline`
or `constexpr` for a header-scope entity instead.

**Rationale.** Each translation unit gets a distinct copy with its own
address and state. Address comparisons can then disagree across translation
units in ways that affect the one definition rule (ODR).

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** `google-build-namespaces`.
