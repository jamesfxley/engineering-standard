# SPDX-License-Identifier: MIT
"""Validate the rule, enforcement and link contracts using only the stdlib."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

RULE = re.compile(r"^## ((?:EN|CXX)-\d{2}\.\d+) — (.+)$", re.MULTILINE)
CANDIDATE = re.compile(r"^## (?:EN|CXX)-[^\n]+$", re.MULTILINE)
WITHDRAWN = frozenset({"EN-05.7", "EN-06.4", "CXX-13.6"})
TERM = re.compile(
    r"review|(?:compiler|build) \([^()\n]+\)|gate:([a-z][a-z-]*) \((full|partial)\)",
)
MATRIX_COLUMNS = ("Full gate coverage", "Partial gate coverage", "Other checks")


def markdown(root: Path) -> list[Path]:
    """Include hidden template directories, excluding version-control metadata."""
    return sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.relative_to(root).parts
    )


def gate_names(readme: str, faults: list[str]) -> set[str]:
    section = re.search(
        r"^## Gate names\n(.*?)(?=^## |\Z)", readme, re.MULTILINE | re.DOTALL,
    )
    if not section:
        faults.append("README.md: missing gate-name table")
        return set()
    names = re.findall(
        r"^\| `([a-z][a-z-]*)` \| (shared|family-provided) \|$",
        section[1],
        re.MULTILINE,
    )
    counts = Counter(name for name, _ in names)
    if not names:
        faults.append("README.md: empty gate-name table")
    for name, count in counts.items():
        if count != 1:
            faults.append(f"README.md: gate name {name!r} occurs {count} times")
    return set(counts)


def enforcement(
    value: str, names: set[str], where: str, faults: list[str],
) -> list[str]:
    value = value.strip().removesuffix(".")
    terms = re.split(r",\s*(?![^()]*\))", value)
    for term in terms:
        match = TERM.fullmatch(term)
        if not match:
            faults.append(f"{where}: invalid enforcement term {term!r}")
        elif match[1] and match[1] not in names:
            faults.append(f"{where}: unknown gate {match[1]!r}")
    if len(set(terms)) != len(terms):
        faults.append(f"{where}: repeated enforcement term")
    return terms


def clause_fields(body: str, where: str, names: set[str], faults: list[str]):
    labels = ("Statement", "Rationale", "Enforcement", "Deviation")
    faults.extend(
        f"{where}: expected one {label} field"
        for label in labels
        if len(re.findall(rf"\*\*{label}\.\*\*", body)) != 1
    )
    order = re.findall(
        r"\*\*(Statement|Rationale|Enforcement|Deviation)\.\*\*", body,
    )
    if order != list(labels):
        faults.append(
            f"{where}: fields must be in order " + ", ".join(labels),
        )
    field = re.search(
        r"\*\*Enforcement\.\*\*\s*(.*?)(?=\*\*Deviation\.\*\*|\Z)",
        body,
        re.DOTALL,
    )
    return enforcement(field[1] if field else "", names, where, faults)


def clauses(documents: dict[Path, str], root: Path, names: set[str], faults: list[str]):
    found = {}
    for path, text in documents.items():
        relative = path.relative_to(root)
        if len(relative.parts) != 2 or relative.parts[0] not in {"engineering", "cxx"}:
            continue
        faults.extend(
            f"{relative}: malformed rule heading {candidate[0]!r}"
            for candidate in CANDIDATE.finditer(text)
            if not RULE.fullmatch(candidate[0])
        )
        headings = list(RULE.finditer(text))
        for index, heading in enumerate(headings):
            ident, title = heading.groups()
            where = f"{relative}:{ident}"
            if ident in found:
                faults.append(f"{where}: duplicate rule ID")
            end = (
                headings[index + 1].start() if index + 1 < len(headings) else len(text)
            )
            body = text[heading.end() : end]
            if title == "Withdrawn":
                if not body.strip():
                    faults.append(f"{where}: withdrawal needs a reason")
                terms = []
            else:
                terms = clause_fields(body, where, names, faults)
            found[ident] = (title, terms)
    if not found:
        faults.append("no rule definitions found")
    faults.extend(
        f"{ident}: required withdrawn stub is missing"
        for ident in sorted(WITHDRAWN)
        if ident not in found or found[ident][0] != "Withdrawn"
    )
    return found


def check_matrix(text: str, found, faults: list[str], path: str) -> None:
    header = "| Rule | " + " | ".join(MATRIX_COLUMNS) + " |"
    if header not in text:
        faults.append(f"{path}: missing coverage columns")
    rows = {}
    for line in text.splitlines():
        if not re.match(r"\| (?:EN|CXX)-", line):
            continue
        columns = [part.strip() for part in line.strip("|").split("|")]
        if len(columns) != 4:
            faults.append(f"{path}: expected four columns")
            continue
        ident = columns[0].split(" ", 1)[0]
        if ident in rows:
            faults.append(f"{path}: duplicate row {ident}")
        rows[ident] = columns
    if set(rows) != set(found):
        faults.append(
            f"{path}: missing {sorted(set(found) - set(rows))}; "
            f"unknown {sorted(set(rows) - set(found))}",
        )
    for ident in rows.keys() & found.keys():
        title, terms = found[ident]
        full = [term for term in terms if term.endswith("(full)")]
        partial = [term for term in terms if term.endswith("(partial)")]
        other = [term for term in terms if not term.startswith("gate:")]
        expected = [
            f"{ident} — {title}",
            "; ".join(full) or "—",
            "; ".join(partial) or "—",
            "reserved" if title == "Withdrawn" else "; ".join(other) or "—",
        ]
        if rows[ident] != expected:
            faults.append(f"{path}:{ident}: row differs from clause")


def links(documents: dict[Path, str], root: Path, faults: list[str]) -> None:
    for path, text in documents.items():
        # These are path checks, not fragment or remote-URL validation (EN-03.8).
        visible = re.sub(
            r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text, flags=re.MULTILINE | re.DOTALL,
        )
        targets = re.findall(r"\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", visible)
        targets += re.findall(r"^\s*\[[^]]+\]:\s*(<[^>]+>|\S+)", visible, re.MULTILINE)
        for target in targets:
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root):
                faults.append(
                    f"{path.relative_to(root)}: "
                    f"relative link leaves the repository {target!r}",
                )
            elif not resolved.exists():
                faults.append(
                    f"{path.relative_to(root)}: broken relative link {target!r}",
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root", nargs="?", type=Path, default=Path(__file__).resolve().parent,
    )
    root = parser.parse_args(argv).root.resolve()
    faults: list[str] = []
    if not root.is_dir():
        print(f"cannot run: not a directory: {root}", file=sys.stderr)
        return 2
    try:
        documents = {path: path.read_text(encoding="utf-8") for path in markdown(root)}
        readme = (root / "README.md").read_text(encoding="utf-8")
        names = gate_names(readme, faults)
        found = clauses(documents, root, names, faults)
        for tier, prefix in (("engineering", "EN-"), ("cxx", "CXX-")):
            path = f"{tier}/enforcement-matrix.md"
            matrix = (root / path).read_text(encoding="utf-8")
            tier_rules = {
                key: value for key, value in found.items() if key.startswith(prefix)
            }
            check_matrix(matrix, tier_rules, faults, path)
        links(documents, root, faults)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"cannot run: {error}", file=sys.stderr)
        return 2
    for fault in faults:
        print(fault)
    if faults:
        print(f"{len(faults)} fault(s)")
        return 1
    print(
        f"ok: {len(found)} rule IDs, {len(WITHDRAWN)} required withdrawn stubs, "
        f"{len(names)} gate names; matrix and relative links resolve",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
