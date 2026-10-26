# CXX-03 — Expressions and statements

## CXX-03.1 — No C casts

**Statement.** C-style casts must not be used. Use `static_cast`, `const_cast`,
`reinterpret_cast` or `std::bit_cast` as appropriate, and prefer the weakest
that works.

**Rationale.** A C cast silently selects whichever of those it needs, including
`const_cast` and `reinterpret_cast`. The reader cannot tell which, and neither
can a grep — so the dangerous casts become unfindable.

`std::bit_cast` is the correct tool for reinterpreting an object
representation. Accessing an object through a pointer `reinterpret_cast` to an
unrelated type is undefined behaviour that usually appears to work.

**Enforcement.** gate:lint (partial), compiler (-Wold-style-cast), review.
**Deviation.** never.

**Mechanism.** `google-readability-casting`,
`cppcoreguidelines-pro-type-cstyle-cast`; `-Wold-style-cast`.

## CXX-03.2 — No undefined behaviour, ever

**Statement.** Code must not rely on undefined behaviour: signed overflow,
out-of-bounds access, use after free or after move, strict-aliasing violation,
shift by an amount at or beyond the operand width, misaligned access, reading an
indeterminate value.

**Rationale.** The optimiser is entitled to assume undefined behaviour does not
occur, so the consequence is not a wrong answer at the site — it is the compiler
deleting a bounds check *somewhere else* because the only path reaching it was
undefined. This is why "it works" is not evidence.

**Enforcement.** build (-fsanitize=undefined), gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** UBSan in CI (`halt_on_error=1`); `bugprone-*`;
`clang-analyzer-*`.

## CXX-03.3 — Integer promotion is not a defence

**Statement.** Arithmetic on values narrower than `int` must account for
promotion. A shift or multiply that can exceed the result type's range must be
performed in a wide enough type, chosen explicitly.

**Rationale.** `uint16_t a = 0xFFFF; a * a` is computed in `int` and overflows —
signed overflow, undefined. The promotion rules are surprising precisely where
wire-format code lives.

**Enforcement.** gate:lint (partial), compiler (-Wconversion), review.
**Deviation.** never.

**Mechanism.** `bugprone-misplaced-widening-cast`,
`bugprone-implicit-widening-of-multiplication-result`; `-Wconversion`.

## CXX-03.4 — Loops are bounded

**Statement.** Every loop must have a bound evident to the reader: a container's
size, a capacity constant, or an explicit iteration limit. A loop whose
termination depends on external input must carry an independent limit.

**Rationale.** An unbounded loop driven by input is a denial of service. On a
constrained target with no scheduler it is a hang, and there is nothing to
recover it.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never for input-driven loops.

**Mechanism.** review; `misc-no-recursion` for the recursive form.

## CXX-03.5 — No recursion where the depth is not statically bounded

**Statement.** Recursion must not be used unless its maximum depth is a
compile-time constant. On a constrained target, recursion must not be used at
all (`CXX-11.3`).

**Rationale.** Recursion converts input size into stack depth. Without a
guard page — which many freestanding targets lack — the failure mode is
silent corruption of whatever sits below the stack, not a crash.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record on a hosted target
only.

**Mechanism.** `misc-no-recursion`, which cannot distinguish target class and so
enforces CXX-11.3's stricter regime everywhere it runs; the hosted deviation is
granted at review.

## CXX-03.6 — Every `switch` over an enumeration is exhaustive

**Statement.** A `switch` over an `enum class` must handle every enumerator, and
should omit `default` so that adding an enumerator produces a diagnostic.

**Rationale.** A `default` that silently absorbs a new enumerator is how a new
state gets handled as though it were an old one. Omitting it turns the next
addition into a compile error listing every site that needs attention.

Where a value may legitimately arrive out of range — a decoded wire value — that
is not an enumeration yet; validate it into one first (`CXX-12.2`).

**Enforcement.** compiler (-Wswitch), gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `-Wswitch`; `bugprone-switch-missing-default-case` where a
default is genuinely needed.

## CXX-03.7 — No fallthrough without saying so

**Statement.** A `switch` case that falls through must be marked
`[[fallthrough]]`.

**Rationale.** Unmarked fallthrough is far more often a missing `break` than an
intention, and the two are indistinguishable on reading.

**Enforcement.** compiler (-Wimplicit-fallthrough), review.
**Deviation.** never.

**Mechanism.** `-Wimplicit-fallthrough`.

## CXX-03.8 — Comparisons and conditions are explicit

**Statement.** Conditions on non-boolean values must compare explicitly. Do not
rely on implicit conversion of a pointer or integer to `bool`.

**Rationale.** `if (count)` and `if (ptr)` read identically and mean different
things, and `if (count)` in particular hides an unintended assignment or a
signedness bug that `if (count > 0)` would expose.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `readability-implicit-bool-conversion`.
