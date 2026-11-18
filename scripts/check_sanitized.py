#!/usr/bin/env python3
"""Fail if publish-unsafe patterns appear outside the checklist.

Scans text files other than docs/never-publish.md. That checklist is the
only skipped path, because it has to name the patterns. The secret scan
still reads it.

Blocked patterns:
- email addresses
- phone numbers
- digit runs of length 6 or more
- two whole words, assembled below so this file does not contain them
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOW_REL = "docs/never-publish.md"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".woff",
    ".woff2",
    ".zip",
    ".gz",
}

BANNED_WORDS = ("pass" + "word", "to" + "ken")

EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
DIGITS = re.compile(r"\d{6,}")
PHONE = re.compile(
    r"(?<!\w)(?:"
    r"\+\d{1,3}[\s.\-]?\(?\d{2,4}\)?(?:[\s.\-]\d{2,4}){2,}"
    r"|\(\d{3}\)[\s.\-]?\d{3}[\s.\-]\d{4}"
    r"|\b\d{3}[-.]\d{3}[-.]\d{4}\b"
    r")"
)
WORDS = re.compile(r"\b(?:" + "|".join(re.escape(word) for word in BANNED_WORDS) + r")\b", re.IGNORECASE)


def scan_text(text: str) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in (
            ("email", EMAIL),
            ("phone", PHONE),
            ("digits", DIGITS),
            ("word", WORDS),
        ):
            match = pattern.search(line)
            if match:
                hits.append((lineno, kind, match.group(0)))
    return hits


def iter_files() -> list[Path]:
    found: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == ALLOW_REL:
            continue
        found.append(path)
    return found


def scan_repo() -> list[str]:
    failures: list[str] = []
    allow = ROOT / ALLOW_REL
    if not allow.is_file():
        failures.append(f"missing checklist: {ALLOW_REL}")
    else:
        checklist = allow.read_text(encoding="utf-8")
        for word in BANNED_WORDS:
            if word.lower() not in checklist.lower():
                failures.append(f"checklist does not name the blocked word {word}")
    for path in iter_files():
        data = path.read_bytes()
        if b"\0" in data:
            failures.append(f"{path.relative_to(ROOT).as_posix()}: unexpected binary file")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            failures.append(f"{path.relative_to(ROOT).as_posix()}: file is not utf-8 text")
            continue
        for lineno, kind, snippet in scan_text(text):
            failures.append(
                f"{path.relative_to(ROOT).as_posix()}:{lineno}: {kind}: {snippet}"
            )
    return failures


def _join(parts: list[str]) -> str:
    return "".join(parts)


def self_test() -> list[str]:
    failures: list[str] = []
    bad = {
        "email": _join(["person", "@", "example.com"]),
        "phone": _join(["(", "202", ") ", "555", "-0100"]),
        "digits": "9" * 6,
        "word-a": _join(["Pass", "word"]),
        "word-b": _join(["TO", "KEN"]),
    }
    clean = [
        "17 November 2026",
        "2026-11-17",
        "v8.30.1",
        "last 4",
        "09:10 to 09:30",
        "40 percent",
        "Blocked-on-owner",
        "tokenize",
        "account numbers are masked",
    ]
    for label, sample in bad.items():
        if not scan_text(sample):
            failures.append(f"self-test missed a bad sample: {label}")
    for sample in clean:
        hits = scan_text(sample)
        if hits:
            failures.append(f"self-test flagged a clean sample: {sample} -> {hits}")
    source = Path(__file__).read_text(encoding="utf-8")
    if scan_text(source):
        failures.append("self-test: this script contains a blocked pattern")
    return failures


def main() -> int:
    failures: list[str] = []
    if "--self-test" in sys.argv:
        failures.extend(self_test())
    failures.extend(scan_repo())
    if failures:
        print("sanitization check failed:")
        for item in failures:
            print(f"  {item}")
        return 1
    print("sanitization check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
