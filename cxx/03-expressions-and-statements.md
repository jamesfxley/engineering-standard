# CXX-03 — Expressions and statements

## CXX-03.1 — No C casts

**Statement.** C-style casts must not be used. Use `static_cast`, `const_cast`,
`reinterpret_cast` or `std::bit_cast` as appropriate, and prefer the weakest
that works.

**Rationale.** A C-style cast can remove `const` or reinterpret a type without
showing which conversion it performs. Named casts expose those operations and
make them searchable.

`std::bit_cast` reinterprets an object representation. Access through a
pointer cast to an unrelated type is undefined behaviour even when it appears
to work.

**Enforcement.** gate:lint (partial), compiler (-Wold-style-cast), review.
**Deviation.** never.

**Mechanism.** `google-readability-casting`,
`cppcoreguidelines-pro-type-cstyle-cast`; `-Wold-style-cast`.

## CXX-03.2 — No undefined behaviour, ever

**Statement.** Code must not rely on undefined behaviour: signed overflow,
out-of-bounds access, use after free or after move, strict-aliasing violation,
shift by an amount at or beyond the operand width, misaligned access, reading an
indeterminate value.

**Rationale.** The optimiser assumes undefined behaviour does not occur. It
can therefore delete a bounds check elsewhere if the only path to it has
undefined behaviour. An apparently correct result does not establish validity.

**Enforcement.** build (-fsanitize=undefined), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** UBSan in CI (`halt_on_error=1`); `bugprone-*`;
`clang-analyzer-*`.

## CXX-03.3 — Integer promotion is not a defence

**Statement.** Arithmetic on values narrower than `int` must account for
promotion. A shift or multiply that can exceed the result type's range must be
performed in a wide enough type, chosen explicitly.

**Rationale.** `uint16_t a = 0xFFFF; a * a` is computed in `int` and overflows,
causing undefined behaviour. These promotion rules particularly affect
wire-format code.

**Enforcement.** gate:lint (partial), compiler (-Wconversion), review.
**Deviation.** never.

**Mechanism.** `bugprone-misplaced-widening-cast`,
`bugprone-implicit-widening-of-multiplication-result`; `-Wconversion`.

## CXX-03.4 — Loops are bounded

**Statement.** Every loop must have a bound evident to the reader: a container's
size, a capacity constant, or an explicit iteration limit. A loop whose
termination depends on external input must carry an independent limit.

**Rationale.** An input-driven loop without a bound permits denial of service.
On a constrained target without a scheduler, it can hang without recovery.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never for input-driven loops.

**Mechanism.** review; `misc-no-recursion` for the recursive form.

## CXX-03.5 — No recursion where the depth is not statically bounded

**Statement.** Recursion must not be used unless its maximum depth is a
compile-time constant. On a constrained target, recursion must not be used at
all (`CXX-11.3`).

**Rationale.** Recursion converts input size into stack depth. Freestanding
targets often lack guard pages, so a stack overflow can corrupt adjacent memory
without a crash.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record on a hosted target
only.

**Mechanism.** `misc-no-recursion`, which cannot distinguish target class and so
enforces CXX-11.3's stricter regime everywhere it runs; the hosted deviation is
granted at review.

## CXX-03.6 — Every `switch` over an enumeration is exhaustive

**Statement.** A `switch` over an `enum class` must handle every enumerator, and
should omit `default` so that adding an enumerator produces a diagnostic.

**Rationale.** A `default` can handle a new enumerator as though it were an
old one. Omitting it exposes affected switches when the enumerator is added.

Validate potentially out-of-range values, such as decoded wire values, before
converting them to an enumeration (CXX-12.2).

**Enforcement.** compiler (-Wswitch), gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `-Wswitch`; `bugprone-switch-missing-default-case` where a
default is genuinely needed.

## CXX-03.7 — No fallthrough without saying so

**Statement.** A `switch` case that falls through must be marked
`[[fallthrough]]`.

**Rationale.** Readers cannot distinguish intentional unmarked fallthrough
from a missing `break`.

**Enforcement.** compiler (-Wimplicit-fallthrough), review.
**Deviation.** never.

**Mechanism.** `-Wimplicit-fallthrough`.

## CXX-03.8 — Comparisons and conditions are explicit

**Statement.** Conditions on non-boolean values must compare explicitly. Do not
rely on implicit conversion of a pointer or integer to `bool`.

**Rationale.** `if (count)` and `if (ptr)` hide different tests behind the
same syntax. An explicit comparison such as `if (count > 0)` can expose an
assignment or signedness error.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `readability-implicit-bool-conversion`.
