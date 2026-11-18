#!/usr/bin/env python3
"""Render the approval-flow PNG, the stacked org-chart PNG, and the HQ mock PNG.

The mermaid sources live in docs/diagrams. The approval figure is rendered
with mermaid-cli. The org-chart figure is drawn from data/org.json so the
names stay readable in a narrow column. The HQ PNG is a screenshot of
docs/hq-mock/index.html.
"""

from __future__ import annotations

import html
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORG = json.loads((ROOT / "data" / "org.json").read_text(encoding="utf-8"))
CHROME = os.environ.get("CHROME_PATH", "/usr/local/bin/google-chrome")
MMDC = os.environ.get("MMDC", "/tmp/render-tools/node_modules/.bin/mmdc")
PUPPETEER = os.environ.get(
    "PUPPETEER_CORE",
    "/tmp/render-tools/node_modules/puppeteer-core",
)


def seat(seat_id: str) -> dict:
    for item in ORG["seats"]:
        if item["id"] == seat_id:
            return item
    raise KeyError(seat_id)


def department(dept_id: str) -> dict:
    for item in ORG["departments"]:
        if item["id"] == dept_id:
            return item
    raise KeyError(dept_id)


def box(title: str, lines: list[str], kind: str = "") -> str:
    body = "".join(f"<span>{html.escape(line)}</span>" for line in lines if line)
    klass = f"box {kind}".strip()
    return f'<div class="{klass}"><strong>{html.escape(title)}</strong>{body}</div>'


def seat_box(seat_id: str, kind: str = "") -> str:
    item = seat(seat_id)
    lines: list[str] = []
    if item["role"] != item["name"]:
        lines.append(item["role"])
    note = (item.get("notes") or "").strip()
    comparable = {item["role"].rstrip("."), item["name"].rstrip("."), "Reports to Amanda"}
    if note.rstrip(".") not in comparable and len(note) <= 80:
        lines.append(note.rstrip("."))
    if item["state"] == "pending":
        kind = "pending"
        lines.append("Pending")
    return box(item["name"], lines, kind)


def figure_html() -> str:
    trading = department("trading")
    research = department("research")
    teams = [
        ("Mailroom", seat_box("chief-of-mailroom"), [seat_box("head-of-gmail"), seat_box("head-of-whatsapp")]),
        ("YouTube", seat_box("chief-of-youtube"), [seat_box("youtube-analyst"), seat_box("script-writer")]),
        ("Storage", seat_box("storage-seat"), []),
        ("Investments", seat_box("chief-of-investments"), []),
        ("Gold Fundamentals", seat_box("gold-researcher"), []),
        ("Credit", seat_box("credit-seat"), []),
        ("AI Systems", seat_box("rio"), []),
        ("Design", seat_box("lex"), []),
        ("OS Tester", seat_box("os-tester-seat"), []),
        ("Clay Avatar Artist", seat_box("clay-avatar-artist"), []),
        (
            "LinkedIn Growth & Career Acquisition",
            seat_box("linkedin-director"),
            [
                seat_box("linkedin-profile-branding"),
                seat_box("linkedin-content"),
                seat_box("linkedin-career-networking"),
            ],
        ),
        (
            "Research",
            box(research["name"], ["Closed", "No seat names are published"], "closed"),
            [],
        ),
        (
            "Trading",
            box(
                trading["name"],
                ["Closed 17 November 2026", "Agents deleted", "Paper-only pilot"],
                "closed",
            ),
            [],
        ),
    ]
    team_html = []
    for label, lead, children in teams:
        kids = f'<div class="row">{"".join(children)}</div>' if children else ""
        team_html.append(
            f'<section class="team"><p class="kicker">{html.escape(label)}</p>{lead}{kids}</section>'
        )
    owner = ORG["owner"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    html, body {{ margin: 0; background: #ffffff; }}
    body {{
      width: 840px;
      color: #1c2430;
      font-family: Inter, "Liberation Sans", sans-serif;
    }}
    .wrap {{ padding: 28px 32px 32px; }}
    h1 {{ font-size: 22px; margin: 0 0 4px; }}
    .sub {{ margin: 0 0 18px; color: #5c6570; font-size: 14px; }}
    .top {{ width: 420px; }}
    .box {{
      border: 1px solid #d5dbe3;
      border-radius: 8px;
      padding: 8px 10px;
      background: #ffffff;
    }}
    .box strong {{ display: block; font-size: 15px; }}
    .box span {{ display: block; color: #5c6570; font-size: 13px; margin-top: 2px; }}
    .human {{ background: #e7eef6; border-color: #1f4e79; }}
    .lead {{ background: #e8f0ea; border-color: #245c45; }}
    .pending {{ background: #f8f1dc; border-color: #8a5a12; }}
    .closed {{ background: #f8ecec; border-color: #8d3d3d; }}
    .stem {{ width: 2px; height: 16px; background: #1f4e79; margin: 0 0 0 24px; }}
    .teams {{
      margin-left: 8px;
      border-left: 2px solid #d5dbe3;
      padding-left: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .kicker {{
      margin: 0 0 6px;
      font-size: 12px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #5c6570;
    }}
    .row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }}
    .row .box {{ flex: 1 1 180px; }}
    .caption {{ margin: 16px 0 0; color: #5c6570; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="wrap" id="chart">
    <h1>Org chart</h1>
    <p class="sub">Personal AI Operating System. Public case study.</p>
    <div class="top">{box(owner["name"], [owner["role"]], "human")}</div>
    <div class="stem"></div>
    <div class="top">{seat_box("amanda", "lead")}</div>
    <div class="stem"></div>
    <div class="teams">{"".join(team_html)}</div>
    <p class="caption">Boxes other than Pending and Closed have no live state in this public chart. Credit is Pending. Research and Trading are Closed.</p>
  </div>
</body>
</html>
"""


def shot(file_url: str, out: Path, selector: str, width: str) -> None:
    env = os.environ.copy()
    env["PUPPETEER_CORE"] = PUPPETEER
    env["CHROME_PATH"] = CHROME
    subprocess.run(
        ["node", str(ROOT / "scripts" / "shot.cjs"), file_url, str(out), selector, width],
        check=True,
        env=env,
    )


def render_approval() -> None:
    config = {
        "executablePath": CHROME,
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
    }
    puppeteer_config = Path("/tmp/puppeteer-config.json")
    puppeteer_config.write_text(json.dumps(config), encoding="utf-8")
    mermaid_config = {
        "theme": "neutral",
        "themeVariables": {"fontSize": "18px"},
        "flowchart": {
            "htmlLabels": True,
            "nodeSpacing": 20,
            "rankSpacing": 36,
            "padding": 12,
            "useMaxWidth": False,
        },
    }
    mermaid_path = Path("/tmp/mermaid-config.json")
    mermaid_path.write_text(json.dumps(mermaid_config), encoding="utf-8")
    out = ROOT / "assets" / "approval-flow.png"
    subprocess.run(
        [
            MMDC,
            "-i",
            str(ROOT / "docs" / "diagrams" / "approval-flow.mmd"),
            "-o",
            str(out),
            "-b",
            "white",
            "-s",
            "1",
            "-t",
            "neutral",
            "-c",
            str(mermaid_path),
            "-p",
            str(puppeteer_config),
            "-q",
        ],
        check=True,
    )


def main() -> None:
    (ROOT / "assets").mkdir(exist_ok=True)
    figure = Path("/tmp/org-chart-figure.html")
    figure.write_text(figure_html(), encoding="utf-8")
    shot(figure.as_uri(), ROOT / "assets" / "org-chart.png", "#chart", "840")
    shot(
        (ROOT / "docs" / "hq-mock" / "index.html").resolve().as_uri(),
        ROOT / "assets" / "hq-mock.png",
        "#sheet",
        "960",
    )
    render_approval()
    print("rendered assets")


if __name__ == "__main__":
    main()
