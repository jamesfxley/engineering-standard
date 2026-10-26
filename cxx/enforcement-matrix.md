# Enforcement matrix

This table records each clause's declared coverage. It does not certify any
consumer implementation. See the README for the vocabulary and gate contract.
Concrete diagnostic names and check boundaries are in each clause.

| Rule | Full gate coverage | Partial gate coverage | Other checks |
|---|---|---|---|
| CXX-00.1 — Resolving a diagnostic | — | gate:deviations (partial) | review |
| CXX-00.2 — Suppression syntax | — | gate:lint (partial) | review |
| CXX-00.3 — Scope-wide disables are registered, not added | — | — | review |
| CXX-00.4 — Do not trust `clang-tidy --fix` | — | — | review |
| CXX-00.5 — New files must be tracked before formatting | — | gate:format (partial) | review |
| CXX-00.6 — A translation unit missing from the compile database is not linted | gate:compile-db (full) | — | — |
| CXX-01.1 — `#pragma once`, on line 1 | — | — | review |
| CXX-01.2 — Identifier case | — | gate:lint (partial) | review |
| CXX-01.3 — Names say what, not how | — | gate:lint (partial) | review |
| CXX-01.4 — Include order | — | gate:format (partial); gate:lint (partial) | review |
| CXX-01.5 — Include what you use | — | gate:lint (partial) | review |
| CXX-01.6 — No `using namespace` at namespace scope in a header | — | gate:lint (partial) | review |
| CXX-01.7 — Braces are not optional | — | gate:lint (partial) | review |
| CXX-02.1 — Fixed-width integers where width matters | — | gate:lint (partial) | review |
| CXX-02.2 — `enum class`, never plain `enum` | — | — | review |
| CXX-02.3 — No implicit narrowing | — | gate:lint (partial) | compiler (-Wconversion -Wsign-conversion); review |
| CXX-02.4 — Initialise everything | — | gate:lint (partial) | review |
| CXX-02.5 — `constexpr` where it can be | — | — | review |
| CXX-02.6 — `auto` where the type is evident or irrelevant | — | gate:lint (partial) | review |
| CXX-02.7 — `std::array` over C arrays | — | gate:lint (partial) | review |
| CXX-02.8 — Named constants, not literals | — | gate:lint (partial) | review |
| CXX-03.1 — No C casts | — | gate:lint (partial) | compiler (-Wold-style-cast); review |
| CXX-03.2 — No undefined behaviour, ever | — | gate:lint (partial) | build (-fsanitize=undefined); review |
| CXX-03.3 — Integer promotion is not a defence | — | gate:lint (partial) | compiler (-Wconversion); review |
| CXX-03.4 — Loops are bounded | — | gate:lint (partial) | review |
| CXX-03.5 — No recursion where the depth is not statically bounded | — | gate:lint (partial) | review |
| CXX-03.6 — Every `switch` over an enumeration is exhaustive | — | gate:lint (partial) | compiler (-Wswitch); review |
| CXX-03.7 — No fallthrough without saying so | — | — | compiler (-Wimplicit-fallthrough); review |
| CXX-03.8 — Comparisons and conditions are explicit | — | gate:lint (partial) | review |
| CXX-04.1 — Parameter passing | — | gate:lint (partial) | review |
| CXX-04.2 — A view parameter does not outlive the call | — | gate:lint (partial) | review |
| CXX-04.3 — `[[nodiscard]]` on anything that reports | — | gate:lint (partial) | review |
| CXX-04.4 — Return values, not out-parameters | — | — | review |
| CXX-04.5 — Preconditions are checked or documented as caller obligations | — | — | review |
| CXX-04.6 — Functions stay small enough to hold in the head | — | gate:lint (partial) | review |
| CXX-04.7 — Distinguish parameters that could be confused | — | — | review |
| CXX-05.1 — Rule of zero, then rule of five | — | gate:lint (partial) | review |
| CXX-05.2 — Single-argument constructors are `explicit` | — | gate:lint (partial) | review |
| CXX-05.3 — Polymorphic destruction | — | gate:lint (partial) | compiler (-Wnon-virtual-dtor); review |
| CXX-05.4 — `override`, never repeated `virtual` | — | gate:lint (partial) | compiler (-Woverloaded-virtual); review |
| CXX-05.5 — Data members are private in a class with behaviour | — | gate:lint (partial) | review |
| CXX-05.6 — Reference members only where the reference is the design | — | gate:lint (partial) | review |
| CXX-05.7 — Interfaces are narrow and abstract | — | — | review |
| CXX-06.1 — Every resource has an owner, and ownership is in the type | — | gate:lint (partial) | review |
| CXX-06.2 — Fixed capacity over dynamic growth | — | gate:footprint (partial) | review |
| CXX-06.3 — Every subscript is reached past a capacity guard | — | — | build (-fsanitize=address); review |
| CXX-06.4 — No allocation on steady-state paths | — | — | build (ctest); review |
| CXX-06.5 — A view's referent outlives the view | — | gate:lint (partial) | build (-fsanitize=address); review |
| CXX-06.6 — A moved-from object is only destroyed or reassigned | — | gate:lint (partial) | review |
| CXX-06.7 — Zero-copy buffers stay valid until released | — | — | review |
| CXX-07.1 — One error strategy per target class, stated | — | — | compiler (-fno-exceptions); review |
| CXX-07.2 — Reject, never truncate | — | — | build (ctest -fsanitize=fuzzer); review |
| CXX-07.3 — Any tolerance needs a citation | — | — | review |
| CXX-07.4 — Errors are not swallowed | — | gate:lint (partial) | review |
| CXX-07.5 — Destructors and move operations do not throw | — | gate:lint (partial) | review |
| CXX-07.6 — Failures are observable | — | — | review |
| CXX-08.1 — Shared mutable state is synchronised or eliminated | — | gate:lint (partial) | build (-fsanitize=thread); review |
| CXX-08.2 — Memory order is chosen, not defaulted past | — | — | review |
| CXX-08.3 — Interrupt context is a separate execution context | — | — | review |
| CXX-08.4 — Multi-word values crossing contexts need a publication protocol | — | — | review |
| CXX-08.5 — A lock is held for as little as possible | — | — | build (ctest); review |
| CXX-08.6 — Deadline arithmetic is wrap-safe | — | — | build (ctest); review |
| CXX-09.1 — Constrain with concepts | — | — | review |
| CXX-09.2 — `if constexpr` over tag dispatch and specialisation | — | — | review |
| CXX-09.3 — Forwarding references are forwarded exactly once | — | gate:lint (partial) | review |
| CXX-09.4 — Instantiation cost is a design consideration | — | gate:footprint (partial) | review |
| CXX-09.5 — Compile-time tables are `constexpr`, and checked | — | — | compiler (static_assert); review |
| CXX-09.6 — Bind compile-time configuration with `static_assert` | — | — | compiler (static_assert); review |
| CXX-10.1 — Every header is self-contained | — | gate:lint (partial) | review |
| CXX-10.2 — Public headers are a namespaced tree | — | — | review |
| CXX-10.3 — A consumer-visible macro is a `PUBLIC` compile definition on the owning target | — | gate:consumer (partial) | review |
| CXX-10.4 — Exported target names match in-tree names | — | gate:consumer (partial) | review |
| CXX-10.5 — Header-only where the cost is genuinely zero | — | — | review |
| CXX-10.6 — Do not open namespaces you do not own | — | gate:lint (partial) | review |
| CXX-10.7 — Anonymous namespaces do not appear in headers | — | gate:lint (partial) | review |
| CXX-11.1 — No allocation after initialisation | — | — | build (ctest); review |
| CXX-11.2 — Static sizes come from a compile-time profile | — | gate:consumer (partial) | compiler (static_assert); review |
| CXX-11.3 — No recursion | — | gate:lint (partial) | review |
| CXX-11.4 — Stack usage is bounded and known | — | gate:footprint (partial) | review |
| CXX-11.5 — Exceptions and RTTI are unavailable | — | — | compiler (-fno-exceptions -fno-rtti); review |
| CXX-11.6 — Static RAM has a budget, gated in CI | gate:footprint (full) | — | — |
| CXX-11.7 — Hardware sits behind one seam with a fake | — | — | review |
| CXX-11.8 — A macro from a platform header may collide with your identifier | — | — | build (cross-compile); review |
| CXX-12.1 — Name the trust boundary | — | — | build (-fsanitize=fuzzer); review |
| CXX-12.2 — Validate into a type that cannot be invalid | — | — | review |
| CXX-12.3 — Length is taken from the frame, never from the buffer | — | — | build (-fsanitize=address -fsanitize=fuzzer); review |
| CXX-12.4 — Integer arithmetic on untrusted values is checked | — | gate:lint (partial) | build (-fsanitize=undefined); review |
| CXX-12.5 — No format-string or varargs interfaces on untrusted data | — | gate:lint (partial) | compiler (-Wformat=2 -Werror=format-security); review |
| CXX-12.6 — Prefer parsing to scanning | — | gate:lint (partial) | review |
| CXX-12.7 — Resource exhaustion is a security property | — | — | build (ctest); review |
| CXX-12.8 — Secrets are not logged and not committed | — | — | review |
| CXX-13.1 — The tree | — | — | review |
| CXX-13.2 — Tests mirror the source tree | — | — | review |
| CXX-13.3 — A module's headers belong to the module | — | — | review |
| CXX-13.4 — The root declares its development contract | — | — | review |
| CXX-13.5 — The advertised version is bound to the build system | — | — | compiler (static_assert); build (ctest); review |
| CXX-13.6 — Withdrawn | — | — | reserved |
