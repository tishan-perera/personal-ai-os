# Approval gates

Agents prepare work. The owner, Tishan Perera, approves anything that leaves the org, moves money, hires, or changes security. Amanda, Chief of Staff & COO, runs people ops up to the hire and restructure line.

Outbound messages are drafts. The owner sends them.

## Matrix

| Action | Who prepares it | Who approves | If approval is missing |
| --- | --- | --- | --- |
| Send an email | Head of Gmail can draft | Owner sends | The email stays a draft |
| Send a message, including WhatsApp | Head of WhatsApp, or the seat that holds the thread, can draft | Owner sends | The message stays a draft |
| Post in public | The seat can draft | Owner posts | It stays a draft |
| Apply to a job | Career & Networking can prepare materials | Owner | No application is submitted |
| Hire a seat | Amanda runs people ops up to this gate | Owner | The seat stays unfilled |
| Restructure the org | Amanda runs people ops up to this gate | Owner | The chart stays as last authorized |
| Trade or place a brokerage order | The Trading pilot could record a paper-only simulated ledger. That department is closed. | Owner. Live trading needs explicit authorization. | No real brokerage order. The pilot rule prohibited real brokerage orders. |
| Change security | The seat stops and asks | Owner | No security change |
| Change GitHub | Open a pull request | Owner merges | The default branch stays as the owner left it |
| Share private financial data | Keep it with the owner | Owner holds it | It is not copied to other seats or to a public page. Account numbers are masked to the last 4. |
| Polish the dashboard | Design (Lex, Chief Design Engineer) and AI Systems (Rio) can propose the change | A business KPI and a usage check come first | Polish waits |

The last row is a sequencing rule from [ADR 0002](adr/0002-chief-kpis-and-cost-discipline.md). It sits beside the weekly KPI for each chief. It is not a license to skip the other rows.

## Flow

```mermaid
flowchart TD
  start["Seat prepares work"] --> gate{"Does a later step need the owner?"}
  gate -->|Work stays inside the org| inside["Continue. Drafts remain drafts."]
  gate -->|Sending a message, email, or post| draft["Hand the owner a draft"]
  draft --> send["Owner sends or posts"]
  gate -->|Job application, hire, restructure, trade, or security change| ask["Ask for explicit owner approval"]
  ask -->|Approved| act["Do the approved action"]
  ask -->|Not approved| stop["Leave it undone"]
  gate -->|GitHub change| pr["Open a pull request"]
  pr --> merge["Owner merges"]
  gate -->|Private financial data| money["Share it with the owner only. Mask account numbers to the last 4."]
  classDef owner fill:#e7eef6,stroke:#1f4e79,color:#1c2430
  classDef inside fill:#e8f0ea,stroke:#245c45,color:#1c2430
  classDef stop fill:#f8ecec,stroke:#8d3d3d,color:#2b1d1d
  class send,merge,ask,money,act owner
  class inside inside
  class stop stop
```

![Approval flow from seat work to owner approval](../assets/approval-flow.png)

## Where this is recorded

- [ADR 0001: Owner approval gates](adr/0001-owner-approval-gates.md)
- [ADR 0002: Chief KPIs and cost discipline](adr/0002-chief-kpis-and-cost-discipline.md)
- [ADR 0003: Shutting down the Trading pilot](adr/0003-shutting-down-the-trading-pilot.md)

The Trading row is a closed pilot, not an open desk. The shutdown date is 17 November 2026. Results from that pilot are omitted on purpose, and the lesson is in ADR 0003.
