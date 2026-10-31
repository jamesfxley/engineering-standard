# Future work

Work deliberately not done in this repository, one entry per deferral, in the
form `EN-03.7` defines.

## FW-1 — Python and Rust language tiers

### What is absent

No `PY-` or `RS-` rules exist; both prefixes are reserved. Python code under
the standard, in House, pico-tooling and this repository's `check.py`, follows
only the `EN-` rules and its repository's strict tooling.

### Why it is not built

The tiers are wanted but not yet written.

### What would have to be true to build it

Time to write them. The Python tier comes first, because three repositories
under the standard contain Python and none contains Rust.

### Version cost

Additive to the rule set, but it tightens what consumers must meet, so it
needs a minor release while pre-1.0 (CONTRIBUTING).

### Affected repositories

engineering-standard. Consumers adopt a tier by moving their pin.
