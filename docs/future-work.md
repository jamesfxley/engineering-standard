# Future work

This file records deferred work in the form EN-03.7 defines.

## FW-1 — Rust language tier

### What is absent

No `RS-` rules exist; the prefix is reserved. The Rust column of each binding
table is empty.

### Why it is not built

No repository under the standard contains Rust, so no rule would be cited.

### What would have to be true to build it

A repository under the standard adopts Rust.

### Version cost

The change is not breaking under EN-06.1.

### Affected repositories

The work affects engineering-standard. Consumer adoption follows
[README.md](../README.md#consuming-this-repository).

## FW-2 — Python fuzzing binding

### What is absent

The Python tier binds no fuzzing tool. EN-04.6 still applies to Python code
that parses untrusted input; until a tool is bound, each such component
records a deviation under EN-04.6.

### Why it is not built

Each candidate, coverage-guided or property-based, is a further development
dependency for every consumer, and no repository under the standard has yet
measured one against its parsers.

### What would have to be true to build it

A consumer runs a candidate tool against a Python parser with a corpus
carried between CI runs, and records what it found and what it cost.

### Version cost

Binding a tool tightens EN-04.6 for Python. The change is not breaking under
EN-06.1.

### Affected repositories

The work affects engineering-standard. Consumer adoption follows
[README.md](../README.md#consuming-this-repository).
