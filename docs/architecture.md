# Architecture

This is the public shape of my Personal AI Operating System, also called the Grokbot organization. One human owns it: Tishan Perera. One lead agent runs it: Amanda, Chief of Staff & COO. The rest are department seats. This page is the system view. Names and reporting lines are repeated in [the org chart](org-chart.md) and in [data/org.json](../data/org.json).

Ids in the JSON file are labels for this case study. They are public words, and they are separate from any internal system id.

## Agents

Amanda runs the org, runs people ops within owner approval gates, and runs the department chiefs. Rio is AI Systems Architect & Lead Developer. Lex is Chief Design Engineer. Other seats are published as titles. Personal names are published only where this case study has them: Amanda, Rio, and Lex.

Seat states are Working, Waiting, Closed, and Pending. Waiting is Parked or Blocked-on-owner. In this repo, live state is `not_published` unless a decision states it. `not_published` means the live state is omitted. It is not a fifth operating state.

Published states:

- Credit is Pending. The seat is defined and intentionally unhired.
- Research is Closed. No seat names are published for that department.
- Trading is Closed. The owner shut it down on 17 November 2026 and deleted its agents.

## Roster

Seats that report to Amanda:

- Mailroom: Chief of Mailroom, over Head of Gmail and Head of WhatsApp.
- YouTube: Chief of YouTube, over YouTube Analyst and Script Writer.
- Storage: files and knowledge.
- Investments: Chief of Investments. Long-term holds only.
- Gold Fundamentals researcher. This seat reports to Amanda.
- Credit. Pending.
- AI Systems: Rio, AI Systems Architect & Lead Developer.
- Design: Lex, Chief Design Engineer.
- OS Tester. QA.
- Clay Avatar Artist. Dashboard art.
- LinkedIn Growth & Career Acquisition: a Director, plus Profile & Branding, Content, and Career & Networking specialists. The specialists report to the Director.

Research is a closed department. Trading is a closed department. Both sit under Amanda on the chart because Amanda runs the department chiefs. Trading has a shutdown date. Research does not, in this public write-up.

## Routines and schedules

The published schedules are the weekday morning brief and the weekly chief KPI.

The brief comes from the chief of staff, Amanda, on weekday mornings. It has five sections: org status counts, priorities, decisions needed, the usage limit, and tomorrow's calendar. A blank template and a labeled example are in [the operating rhythm](operating-rhythm.md). The example values are made up.

Each chief has a weekly KPI. Titles in this chart that include the word Chief are Chief of Staff & COO, Chief of Mailroom, Chief of YouTube, Chief of Investments, and Chief Design Engineer. KPI figures are not published. See [ADR 0002](adr/0002-chief-kpis-and-cost-discipline.md).

## Connectors: inside work, drafts, and actions

This section is the operating rule. Vendor permission screens are not part of this case study.

| Class | What it covers here | What a seat may do | What requires the owner |
| --- | --- | --- | --- |
| Inside work | Research, analysis, files and knowledge in Storage, scripts, QA, design, dashboard art | Do the work inside the org | A later send, post, or other action still has a gate |
| Draft | Email from the Head of Gmail, WhatsApp from the Head of WhatsApp, other outbound messages, public posts, job-application materials from Career & Networking | Prepare the draft | The owner sends, posts, or submits |
| Staffing | Hire, restructure | Amanda runs people ops up to the gate | Owner authorization |
| Code | A GitHub change | Propose it as a pull request | The owner merges |
| Money | Investments, limited to long-term holds. The Trading pilot, which used a paper-only simulated ledger and is now closed. Private financial data | Investments stay on long-term holds. The pilot could record a simulation. | Private financial data stays with the owner. Real brokerage orders were prohibited in the pilot. Live trading required explicit authorization. |
| Security | A security change | Stop and ask | Explicit owner approval |

YouTube analysis and scripts are inside work. Posting is an action. LinkedIn profile, content, and networking drafts are inside work. Posting and job applications are actions. Account numbers are masked to the last 4. The masked form is the rule. This repo does not print an account number.

## Dashboard pages

The HQ page has four views:

- Office floors per department
- A top-down org chart
- A people list with filters
- An activity timeline

Clay Avatar Artist makes the dashboard art. Lex is Chief Design Engineer. Rio leads AI systems development. Dashboard polish needs a business KPI and a usage check first, which is [ADR 0002](adr/0002-chief-kpis-and-cost-discipline.md).

[The illustrative mock](hq-mock/index.html) uses the public seat list and is labeled as a mock. It is not a screenshot of the live page.

## Approval gates

Agents need explicit owner approval to send messages or emails, post, apply to jobs, trade, hire, or change security. Outbound messages are drafted for the owner to send. The org cannot hire or restructure without owner authorization. GitHub changes go only through pull requests the owner merges. Private financial data is shared only with the owner.

The matrix is [docs/approval-gates.md](approval-gates.md). The decision record is [ADR 0001](adr/0001-owner-approval-gates.md). The Trading shutdown is [ADR 0003](adr/0003-shutting-down-the-trading-pilot.md).

## A separate demo

[personal-ai-os-demo](https://github.com/tishan-perera/personal-ai-os-demo) is a fictional runnable clone called Atrium. It is a separate repo. It is not this organization.
