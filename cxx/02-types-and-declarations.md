# CXX-02 — Types and declarations

## CXX-02.1 — Fixed-width integers where width matters

**Statement.** Use `std::uint8_t`, `std::int32_t` and friends wherever a width
is part of the meaning — wire formats, register layouts, anything serialised.
Use `std::size_t` for sizes and indices, `std::ptrdiff_t` for differences. Plain
`short`, `long` and `unsigned` must not appear in an interface.

**Rationale.** `long` is 32-bit on one supported platform and 64-bit on another.
Code that works on the developer machine and corrupts a frame on the target is
the predictable result, and it is invisible in review.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, for
an external API's own types.

**Mechanism.** `google-runtime-int`.

## CXX-02.2 — `enum class`, never plain `enum`

**Statement.** Enumerations must be scoped (`enum class`). An unscoped `enum`
must not be introduced.

**Rationale.** Unscoped enumerators leak into the surrounding scope and convert
implicitly to integers, so two unrelated enumerations compare equal without a
diagnostic and an enumerator collides with a variable name from elsewhere.

Give the enumeration an explicit underlying type where it is stored or
transmitted.

**Enforcement.** review.
**Deviation.** permitted with record, for an
external API's own types.

## CXX-02.3 — No implicit narrowing

**Statement.** A narrowing conversion must be explicit, and must be preceded by
a check that the value fits — or be provably in range at that point.

**Rationale.** This is the single most common source of silent corruption in
code that handles sizes and lengths. A `std::size_t` truncated to `std::uint16_t`
produces a plausible small number, and every subsequent bounds check passes.

Signed/unsigned mixing is the same defect wearing a different hat: a negative
length becomes an enormous unsigned one and the capacity check succeeds.

**Enforcement.** gate:lint (partial), compiler (-Wconversion -Wsign-conversion), review.
**Deviation.** never.

**Mechanism.** `bugprone-narrowing-conversions`; `-Wconversion`,
`-Wsign-conversion`.

## CXX-02.4 — Initialise everything

**Statement.** Every variable and every data member must be initialised at the
point of declaration or in the constructor's member initialiser list. A
default-constructed member left indeterminate is a defect.

**Rationale.** Reading an indeterminate value is undefined behaviour, and the
usual symptom is that it works — because the stack happened to hold zero — until
a different call path leaves something else there.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, for a
deliberately uninitialised buffer where the cost is measured and the first use
is a full overwrite.

**Mechanism.** `cppcoreguidelines-pro-type-member-init`,
`cppcoreguidelines-init-variables`.

## CXX-02.5 — `constexpr` where it can be

**Statement.** A value computable at compile time should be `constexpr`. A
function that can be `constexpr` should be.

**Rationale.** It moves work and errors from run time to compile time, and on a
constrained target it is the difference between a table in flash and a table
built into RAM at startup.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-02.6 — `auto` where the type is evident or irrelevant

**Statement.** Use `auto` where the initialiser states the type, or where the
exact type is an implementation detail. Do not use it where the reader needs the
type and cannot infer it.

**Rationale.** `auto` prevents a whole class of accidental-conversion and
accidental-copy bugs, which is its real value — not brevity. Used where the type
carries meaning the reader needs, it hides that meaning.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `modernize-use-auto`, `readability-qualified-auto`.

## CXX-02.7 — `std::array` over C arrays

**Statement.** A fixed-size array must be `std::array`, not `T[N]`, except where
an external interface requires the C form.

**Rationale.** `std::array` knows its size, does not decay to a pointer when
passed, and supports the same aggregate initialisation. Decay is what makes a C
array's bounds unverifiable at the call site.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, at an external boundary.

**Mechanism.** `modernize-avoid-c-arrays`,
`cppcoreguidelines-pro-bounds-array-to-pointer-decay`.

## CXX-02.8 — Named constants, not literals

**Statement.** A literal appearing in logic must be a named constant. Small
structural values (0, 1, 2, powers of two used as widths or factors) are exempt.

**Rationale.** An unexplained constant cannot be reviewed — nobody can tell
whether `1500` is right. Naming it states the intent and makes a related
constant's relationship visible.

Two legitimate exemptions, both registered under `EN-00.5` rather than assumed:
literal expected values in a test (`EN-04.7`), and a tree transcribing a
published wire format, where naming each offset inserts an indirection between
the code and the document it must be checked against.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `readability-magic-numbers`.
