#!/usr/bin/env python3
"""Check the public org data, the prose, and the diagram copies."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORG_PATH = ROOT / "data" / "org.json"

OPERATING_STATES = {"working", "waiting", "closed", "pending", "not_published"}
CHILD_OF = {
    "head-of-gmail": "chief-of-mailroom",
    "head-of-whatsapp": "chief-of-mailroom",
    "youtube-analyst": "chief-of-youtube",
    "script-writer": "chief-of-youtube",
    "linkedin-profile-branding": "linkedin-director",
    "linkedin-content": "linkedin-director",
    "linkedin-career-networking": "linkedin-director",
}
NAME_FILES = [
    "README.md",
    "docs/org-chart.md",
    "docs/architecture.md",
    "docs/hq-mock/index.html",
    "docs/how-i-run-an-ai-team.md",
]
REQUIRED_LINKS = [
    "https://github.com/tishan-perera/personal-ai-os-demo",
    "https://github.com/tishan-perera/close-recon-assistant",
    "https://github.com/tishan-perera/fpa-driver-model",
    "https://github.com/tishan-perera/poc.mcp-finance-tools",
]
TODOS = [
    "TODO(Tishan): add one finance or FP&A task this org took from request to an output you approved, and the time you actually spent.",
    "TODO(Tishan): add one control that stopped a bad outbound draft. Describe the gate. Leave the message text out.",
    "TODO(Tishan): add one weekly chief KPI you will show a hiring manager, and how you measure it.",
    "TODO(Tishan): add the usage limit you read in the weekday morning brief, in the unit you actually use.",
]


def norm(text: str) -> str:
    text = text.replace("&amp;", "&")
    text = text.replace(" & ", " and ")
    return text.lower()


def mermaid_blocks(text: str) -> list[str]:
    return [block.strip() for block in re.findall(r"```mermaid\n(.*?)```", text, flags=re.S)]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    org = json.loads(ORG_PATH.read_text(encoding="utf-8"))
    owner = org["owner"]
    seats = org["seats"]
    departments = org["departments"]
    seat_ids = [seat["id"] for seat in seats]
    dept_ids = [dept["id"] for dept in departments]
    if len(seat_ids) != len(set(seat_ids)):
        fail(errors, "duplicate seat id")
    if len(dept_ids) != len(set(dept_ids)):
        fail(errors, "duplicate department id")
    seats_by_id = {seat["id"]: seat for seat in seats}
    depts_by_id = {dept["id"]: dept for dept in departments}
    if owner["id"] != "tishan" or owner["name"] != "Tishan Perera" or owner["kind"] != "human":
        fail(errors, "owner record drifted")
    known_parents = set(seat_ids) | {owner["id"]}
    for seat in seats:
        if seat["kind"] != "agent":
            fail(errors, f"{seat['id']} is not an agent seat")
        if seat["state"] not in OPERATING_STATES:
            fail(errors, f"{seat['id']} has an unknown state")
        if seat["reports_to"] not in known_parents:
            fail(errors, f"{seat['id']} reports to an unknown id")
        dept_id = seat["department_id"]
        if dept_id is not None and dept_id not in depts_by_id:
            fail(errors, f"{seat['id']} has an unknown department")
        if seat["state"] == "waiting" and seat.get("waiting_substate") not in {
            "Parked",
            "Blocked-on-owner",
        }:
            fail(errors, f"{seat['id']} is Waiting without a substate")
    if seats_by_id["amanda"]["reports_to"] != "tishan":
        fail(errors, "Amanda reports to the owner")
    if seats_by_id["amanda"]["department_id"] is not None:
        fail(errors, "Amanda is the only seat without a department id")
    for seat in seats:
        if seat["id"] == "amanda":
            continue
        expected = CHILD_OF.get(seat["id"], "amanda")
        if seat["reports_to"] != expected:
            fail(errors, f"{seat['id']} reports_to is {seat['reports_to']}, expected {expected}")
        if seat["id"] != "amanda" and seat["department_id"] is None:
            fail(errors, f"{seat['id']} is missing a department")
    for dept in departments:
        if dept["reports_to"] != "amanda":
            fail(errors, f"department {dept['id']} does not report to Amanda")
        if dept["state"] not in OPERATING_STATES:
            fail(errors, f"department {dept['id']} has an unknown state")
    if depts_by_id["credit"]["state"] != "pending" or seats_by_id["credit-seat"]["state"] != "pending":
        fail(errors, "Credit is Pending")
    if depts_by_id["research"]["state"] != "closed" or depts_by_id["trading"]["state"] != "closed":
        fail(errors, "Research and Trading are Closed")
    if depts_by_id["trading"].get("closed_on") != "2026-11-17":
        fail(errors, "Trading closed_on drifted")
    seated = {seat["department_id"] for seat in seats}
    if "research" in seated or "trading" in seated:
        fail(errors, "Research and Trading publish no seat names")
    for seat in seats:
        if seat["id"] == "credit-seat":
            continue
        if seat["state"] != "not_published":
            fail(errors, f"unexpected published state on {seat['id']}")
    for dept in departments:
        if dept["id"] in {"credit", "research", "trading"}:
            continue
        if dept["state"] != "not_published":
            fail(errors, f"unexpected published state on department {dept['id']}")
    if "Long-term holds only." not in seats_by_id["chief-of-investments"]["notes"]:
        fail(errors, "Investments note drifted")

    texts = {rel: (ROOT / rel).read_text(encoding="utf-8") for rel in NAME_FILES}
    for rel, text in texts.items():
        blob = norm(text)
        for seat in seats:
            if norm(seat["name"]) not in blob:
                fail(errors, f"{rel} is missing seat {seat['name']}")
        for dept in departments:
            if norm(dept["name"]) not in blob:
                fail(errors, f"{rel} is missing department {dept['name']}")
        if "tishan perera" not in blob:
            fail(errors, f"{rel} is missing the owner name")

    readme = texts["README.md"]
    for url in REQUIRED_LINKS:
        if url not in readme:
            fail(errors, f"README is missing {url}")
    if "Atrium" not in readme:
        fail(errors, "README is missing the Atrium note")
    for item in TODOS:
        if readme.count(item) != 1:
            fail(errors, f"README Outcomes fill-in drifted: {item}")
    if "Illustrative mock" not in readme or "assets/hq-mock.png" not in readme:
        fail(errors, "README is missing the HQ mock")
    if "What this shows about how I work" not in readme:
        fail(errors, "README is missing the skim bullets")

    essay = texts["docs/how-i-run-an-ai-team.md"]
    if "DRAFT" not in essay.splitlines()[0] and "DRAFT" not in essay[:400]:
        fail(errors, "essay is missing the DRAFT marker")
    words = re.findall(r"[A-Za-z0-9'&+-]+", essay)
    if not 700 <= len(words) <= 950:
        fail(errors, f"essay word count is {len(words)}; keep it near 800")

    diagrams = {
        "org-chart": (ROOT / "docs/diagrams/org-chart.mmd").read_text(encoding="utf-8").strip(),
        "approval-flow": (ROOT / "docs/diagrams/approval-flow.mmd").read_text(encoding="utf-8").strip(),
    }
    for rel in ("README.md", "docs/org-chart.md", "docs/approval-gates.md", "docs/architecture.md"):
        for block in mermaid_blocks((ROOT / rel).read_text(encoding="utf-8")):
            if block not in diagrams.values():
                fail(errors, f"{rel} has a mermaid block that does not match docs/diagrams")
    readme_blocks = mermaid_blocks(readme)
    if diagrams["org-chart"] not in readme_blocks or diagrams["approval-flow"] not in readme_blocks:
        fail(errors, "README is missing a diagram from docs/diagrams")

    for rel in (
        "LICENSE",
        "docs/never-publish.md",
        "docs/operating-rhythm.md",
        "docs/adr/0001-owner-approval-gates.md",
        "docs/adr/0002-chief-kpis-and-cost-discipline.md",
        "docs/adr/0003-shutting-down-the-trading-pilot.md",
        "assets/org-chart.png",
        "assets/approval-flow.png",
        "assets/hq-mock.png",
    ):
        path = ROOT / rel
        if not path.is_file():
            fail(errors, f"missing {rel}")
            continue
        if path.suffix == ".png":
            data = path.read_bytes()
            if not data.startswith(b"\x89PNG") or len(data) < 8 * 1000:
                fail(errors, f"{rel} is not a usable PNG")

    if "17 November 2026" not in (ROOT / "docs/adr/0003-shutting-down-the-trading-pilot.md").read_text(encoding="utf-8"):
        fail(errors, "Trading ADR is missing the shutdown date")
    if "MIT License" not in (ROOT / "LICENSE").read_text(encoding="utf-8"):
        fail(errors, "LICENSE drifted")

    if errors:
        print("org sync failed:")
        for item in errors:
            print(f"  {item}")
        return 1
    print("org sync passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
