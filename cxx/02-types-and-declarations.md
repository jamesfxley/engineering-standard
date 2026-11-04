# CXX-02 — Types and declarations

## CXX-02.1 — Fixed-width integers where width matters

**Statement.** Use fixed-width types such as `std::uint8_t` and `std::int32_t`
where width is part of the meaning, including wire formats, register layouts
and serialised data.
Use `std::size_t` for sizes and indices, `std::ptrdiff_t` for differences. Plain
`short`, `long` and `unsigned` must not appear in an interface.

**Rationale.** `long` is 32-bit on one supported platform and 64-bit on
another. Depending on its width can corrupt frames on the target despite
working on the developer's machine.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, for
an external API's own types.

**Mechanism.** `google-runtime-int`.

## CXX-02.2 — `enum class`, never plain `enum`

**Statement.** Enumerations must be scoped (`enum class`). An unscoped `enum`
must not be introduced.

**Rationale.** Unscoped enumerators enter the surrounding scope and convert
implicitly to integers. Unrelated enumerations can compare equal without a
diagnostic, and enumerator names can collide with variables.

Give an enumeration an explicit underlying type where it is stored or
transmitted.

**Enforcement.** review.
**Deviation.** permitted with record, for an
external API's own types.

## CXX-02.3 — No implicit narrowing

**Statement.** A narrowing conversion must be explicit. It must be preceded by a
check that the value fits, unless the value is provably in range at that point.

**Rationale.** Truncating a `std::size_t` to `std::uint16_t` can produce a
plausible small value that passes later bounds checks. Mixing signed and
unsigned values can turn a negative length into a large unsigned value and
invalidate capacity checks.

**Enforcement.** gate:lint (partial), compiler (-Wconversion -Wsign-conversion), review.
**Deviation.** never.

**Mechanism.** `bugprone-narrowing-conversions`; `-Wconversion`,
`-Wsign-conversion`.

## CXX-02.4 — Initialise everything

**Statement.** Every variable and every data member must be initialised at the
point of declaration or in the constructor's member initialiser list. A
default-constructed member left indeterminate is a defect.

**Rationale.** Reading an indeterminate value is undefined behaviour. A
variable can appear to work while its stack slot happens to contain zero, then
fail on a different call path.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, for a
deliberately uninitialised buffer where the cost is measured and the first use
is a full overwrite.

**Mechanism.** `cppcoreguidelines-pro-type-member-init`,
`cppcoreguidelines-init-variables`.

## CXX-02.5 — `constexpr` where it can be

**Statement.** A value computable at compile time should be `constexpr`. A
function that can be `constexpr` should be.

**Rationale.** `constexpr` moves computation and errors to compile time. On a
constrained target, it can place a table in flash instead of building it in RAM
at startup.

**Enforcement.** review.
**Deviation.** permitted.

## CXX-02.6 — `auto` where the type is evident or irrelevant

**Statement.** Use `auto` where the initialiser states the type, or where the
exact type is an implementation detail. Do not use it where the reader needs the
type and cannot infer it.

**Rationale.** `auto` prevents accidental conversions and copies. It can also
hide information when the reader needs the exact type.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted.

**Mechanism.** `modernize-use-auto`, `readability-qualified-auto`.

## CXX-02.7 — `std::array` over C arrays

**Statement.** A fixed-size array must be `std::array`, not `T[N]`, except where
an external interface requires the C form.

**Rationale.** `std::array` retains its size and does not decay to a pointer
when passed. It supports aggregate initialisation. A decayed C array loses the
bounds needed to check the call.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record, at an external boundary.

**Mechanism.** `modernize-avoid-c-arrays`,
`cppcoreguidelines-pro-bounds-array-to-pointer-decay`.

## CXX-02.8 — Named constants, not literals

**Statement.** A literal appearing in logic must be a named constant. Small
structural values (0, 1, 2, powers of two used as widths or factors) are exempt.

**Rationale.** Naming a constant explains its purpose and its relationship to
other constants. An unexplained `1500` gives a reviewer no basis for checking it.

Two exemptions need registration under EN-00.5: literal expected values in tests
(EN-04.7), and a tree transcribing a published wire format. Wire-format code
must be checked against its source document, and naming every offset puts an
indirection between the two.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record.

**Mechanism.** `readability-magic-numbers`.
