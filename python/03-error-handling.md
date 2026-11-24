# PY-03 — Error handling

Python reports failure by exception. These rules govern where exceptions are
caught and what a boundary turns them into.

## PY-03.1 — Errors are not swallowed

**Statement.** A handler must catch the narrowest exception types that the
code can recover from. Bare `except:`, `except BaseException` and
`except Exception` are permitted only at a boundary under `PY-03.3`. A handler
must not discard the exception with `pass` or `continue` without acting on it.

**Rationale.** A broad handler catches the defect it was not written for,
such as a `TypeError` or a `KeyError` from a misspelt name, and turns it into
the recovery path. The program then continues with wrong state, and the
traceback that would have located the defect is lost.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `E722` reports a bare `except`, `BLE001` a blind
`except Exception` and `S110` and `S112` a handler that only passes or
continues. Review checks that each handler can recover from what it catches.

## PY-03.2 — A translated exception keeps its cause

**Statement.** An exception raised inside a handler must chain the one being
handled with `raise … from error`. `from None` is permitted only where the
cause would mislead, with a comment saying why.

**Rationale.** Without the chain, the traceback shows the new exception as if
it arose in the handler, and the original cause is hidden.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `B904` reports a raise without `from` inside a handler.

## PY-03.3 — A boundary turns an expected failure into its error form

**Statement.** Each boundary must convert an expected failure into the
boundary's error form and let a defect propagate. Boundaries are a program's
entry point, a request or event handler, a user-interface callback, and the
entry function of a thread or task. The error forms are:

- a command: one message on standard error naming the input that failed, and
  a documented non-zero exit status;
- a user interface: a visible error state, with the detail logged;
- a service: the protocol's error response, with the detail logged.

An expected failure is one the specification or documentation anticipates,
such as invalid input, a missing file or an absent device. A defect is any
other exception.

**Rationale.** A traceback is the wrong report of an expected failure: it
tells a user that the program is broken when the input was. A defect hidden
behind a friendly message cannot be located. Separating the two keeps both
reports useful.

**Enforcement.** review.
**Deviation.** never.

**Mechanism.** Review checks each boundary's handlers. Tests of expected
failures assert the message and status.

## PY-03.4 — `assert` does not validate input

**Statement.** Input, configuration and caller arguments must be checked with
an explicit condition that raises. `assert` may state an internal invariant
only, and must not be the only check that guards behaviour.

**Rationale.** Python removes `assert` statements when run with `-O`, so a
check written as an assertion disappears in that mode. A test framework's
assertions are a separate case: tests are never run with `-O`.

**Enforcement.** gate:lint (partial), review.
**Deviation.** permitted with record — tests, whose assertions the test
framework reports.

**Mechanism.** Ruff `S101` reports every `assert`. The test tree's exclusion
is a scope-wide disable under `PY-00.2`.

## PY-03.5 — A thread's or task's failure is observed

**Statement.** Every thread, `asyncio` task and executor future must be held
by a reference until it finishes, and its result or exception must be
retrieved or handled at its boundary (`PY-03.3`).

**Rationale.** An exception in a thread ends only that thread, with a
traceback the user may never see. An `asyncio` task without a reference can
be garbage-collected before it finishes, and an exception in an unawaited task
is reported only when the task is destroyed, if at all. The program goes on
without the work it started.

**Enforcement.** gate:lint (partial), review.
**Deviation.** never.

**Mechanism.** Ruff `RUF006` reports an `asyncio.create_task` result that is
not stored. Review covers threads and futures.
