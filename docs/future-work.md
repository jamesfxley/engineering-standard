# Future work

Work deliberately not done in this repository, one entry per deferral, in the
form `EN-03.7` defines.

## FW-1 — Python and Rust language tiers

### What is absent

No `PY-` or `RS-` rules exist; both prefixes are reserved. Python code under
the standard follows only the `EN-` rules and its repository's strict tooling:
House and pico-tooling, each product repository's `dev.py` and its test and
bench scripts, and this repository's `check.py`.

### Why it is not built

The tiers are wanted but not yet written.

### What would have to be true to build it

Time to write them. The Python tier comes first, because every repository
under the standard contains Python and none contains Rust.

### Version cost

Not breaking under `EN-06.1`.

### Affected repositories

engineering-standard. Consumers adopt a tier by moving their pin.
