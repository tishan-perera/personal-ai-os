#!/usr/bin/env python3
"""Check relative links, anchors, and public http(s) links in markdown and HTML."""

from __future__ import annotations

import re
import ssl
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
BARE_URL = re.compile(r"https?://[^\s)>\]]+")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
FENCE = re.compile(r"```.*?```", re.S)
USER_AGENT = "personal-ai-os-link-check"


class HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key.lower() == "id" and value:
                self.ids.add(value)
            if tag.lower() == "a" and key.lower() == "href" and value:
                self.hrefs.append(value)


def github_slug(heading: str) -> str:
    text = heading.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def headings(text: str) -> set[str]:
    slugs: set[str] = set()
    seen: dict[str, int] = {}
    for match in HEADING.finditer(text):
        slug = github_slug(match.group(2))
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        slugs.add(slug if count == 0 else f"{slug}-{count}")
    return slugs


def strip_fences(text: str) -> str:
    return FENCE.sub("", text)


def files() -> list[Path]:
    found: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() in {".md", ".html"}:
            found.append(path)
    return found


def targets_in(path: Path) -> tuple[list[str], set[str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        visible = strip_fences(text)
        found = [match.group(1) for match in MD_LINK.finditer(visible)]
        found.extend(BARE_URL.findall(visible))
        return found, headings(text)
    parser = HrefParser()
    parser.feed(text)
    return parser.hrefs, parser.ids


def fetch(url: str) -> tuple[bool, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl.create_default_context()
    last = "no attempt"
    for _ in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25, context=context) as response:
                response.read(64)
                status = getattr(response, "status", 200)
                if status >= 400:
                    last = f"status {status}"
                    continue
                return True, str(status)
        except urllib.error.HTTPError as error:
            last = f"status {error.code}"
            if error.code < 500 and error.code != 429:
                return False, last
        except Exception as error:  # noqa: BLE001 - report the network failure
            last = str(error)
    return False, last


def main() -> int:
    failures: list[str] = []
    external: dict[str, list[str]] = {}
    for path in files():
        raw_targets, page_anchors = targets_in(path)
        for raw in raw_targets:
            target = raw.strip()
            if target.startswith("#"):
                slug = target[1:]
                if slug not in page_anchors:
                    failures.append(f"{path.relative_to(ROOT).as_posix()}: missing anchor {target}")
                continue
            url, _, fragment = target.partition("#")
            if url.startswith(("http://", "https://")):
                external.setdefault(url, []).append(path.relative_to(ROOT).as_posix())
                continue
            if url.startswith("mailto:"):
                failures.append(f"{path.relative_to(ROOT).as_posix()}: mailto link {target}")
                continue
            if not url:
                continue
            dest = (path.parent / url).resolve()
            try:
                dest.relative_to(ROOT)
            except ValueError:
                failures.append(f"{path.relative_to(ROOT).as_posix()}: link escapes the repo {target}")
                continue
            if not dest.is_file():
                failures.append(f"{path.relative_to(ROOT).as_posix()}: missing file {target}")
                continue
            if fragment and dest.suffix.lower() == ".md":
                if fragment not in headings(dest.read_text(encoding="utf-8")):
                    failures.append(
                        f"{path.relative_to(ROOT).as_posix()}: missing anchor {target}"
                    )
    for url, sources in sorted(external.items()):
        ok, detail = fetch(url)
        if not ok:
            failures.append(f"{url}: {detail} (from {', '.join(sorted(set(sources)))})")
        else:
            print(f"ok {url}")
    if failures:
        print("link check failed:")
        for item in failures:
            print(f"  {item}")
        return 1
    print("link check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
