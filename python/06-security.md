# PY-06 — Security

The security assumptions are defined in
[EN-01](../engineering/01-quality-gates.md).

## PY-06.1 — A subprocess takes an argument list, never a shell

**Statement.** A subprocess must be started with an argument list and without
a shell. `shell=True`, `os.system` and `os.popen` are never permitted. An
untrusted value must not be placed where the program reads options, and must
follow a `--` separator where the program accepts one. Each call must check
the exit status or handle it explicitly, and must set a timeout where the
child can hang.

**Rationale.** A shell parses its command line, so data containing quotes,
semicolons or substitutions becomes code. An argument list passes each value
as one argument. A value beginning with `-` can still be read as an option,
which the separator prevents. An unchecked exit status turns the child's
failure into the parent's silent success.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `S602`, `S604` and `S605` report a shell, and
`PLW1510` a `subprocess.run` without `check`. Review checks argument
placement, separators and timeouts.

## PY-06.2 — Data is never executed

**Statement.** Untrusted data must not reach `eval`, `exec`, `pickle`,
`marshal`, `shelve`, or a YAML loader other than a safe one. An archive must
not be extracted from an untrusted source without a member filter that
refuses absolute paths, parent-directory components and links that leave the
destination.

**Rationale.** Each of these runs code or writes files chosen by whoever
produced the data. Validation after loading is too late: the code has already
run or the file has already been written.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `S102` reports `exec`, `S307` `eval`, `S301` `pickle`,
`S506` an unsafe YAML load and `S202` unfiltered tar extraction. Review covers
other loaders.

## PY-06.3 — Input is parsed once, at the boundary, with limits

**Statement.** Data from outside the program, including serial lines,
network messages, files and command-line arguments, must be parsed at the
trust boundary into the declared types of `PY-02.3`, rejecting malformed
input with a specific error. Each read from an untrusted source must have a
size limit, and each buffer fed from one must have a capacity.

**Rationale.** Validation spread through the code repeats checks and misses
some. A value parsed once into a precise type cannot be invalid later.
Python's unbounded strings and lists turn a peer that never sends a line
terminator into memory exhaustion.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks each boundary; `EN-04.6` governs fuzzing.

## PY-06.4 — Secrets are not logged and not committed

**Statement.** Credentials, keys and tokens must not appear in source, logs,
exception messages, fixtures or recordings. They are read at run time from
the environment or from a file outside the repository. An object that holds
a secret must not reveal it in its `repr`.

**Rationale.** Logs and recordings are shared and committed history is
retained indefinitely. A traceback or a debugger prints objects through
`repr`, so a secret in an attribute escapes through it.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `S105`, `S106` and `S107` report hard-coded passwords.
Review covers logs, fixtures and representations.
