# Operating rhythm

The published rhythm has two parts: a weekday morning executive brief, and a weekly KPI for each chief.

## Weekday morning executive brief

Amanda, Chief of Staff & COO, gives this brief to Tishan Perera on weekday mornings.

The brief has five sections:

1. Org status counts
2. Priorities
3. Decisions needed
4. Usage limit
5. Tomorrow's calendar

Org status counts use the seat states: Working, Waiting (Parked or Blocked-on-owner), Closed, and Pending.

## Blank template

Copy this when you want to show a real brief. Replace the brackets. Keep private data out. Run `python scripts/check_sanitized.py` before you commit.

```text
Weekday morning executive brief
From: Amanda, Chief of Staff & COO
To: Tishan Perera

Org status counts:
- Working: [count]
- Waiting, Parked: [count]
- Waiting, Blocked-on-owner: [count]
- Pending: [count]
- Closed: [count]

Priorities:
1. [priority]

Decisions needed:
- [decision]

Usage limit:
- [limit and unit]

Tomorrow's calendar:
- [time and a public label for the block]
```

## Sample with example values

Every number and every work item below is an example. This is a fake brief. It is not a headcount, not a usage figure, and not a calendar. The counts are also unrelated to the states in [data/org.json](../data/org.json). In that file, live state is not_published except Credit (Pending), Research (Closed), and Trading (Closed).

```text
EXAMPLE BRIEF. FAKE VALUES. NOT A REAL DAY.

From: Amanda, Chief of Staff & COO
To: Tishan Perera

Org status counts (example):
- Working: 3 example
- Waiting, Parked: 1 example
- Waiting, Blocked-on-owner: 2 example
- Pending: 1 example
- Closed: 2 example

Priorities (example):
1. Example priority: clear items that are blocked on the owner.
2. Example priority: read the weekly chief KPI before any dashboard polish.

Decisions needed (example):
- Example decision: approve or hold one outbound draft. The draft text is not in this sample.

Usage limit (example):
- Example: 40 percent of an owner-set cap. The real cap and the real unit belong on the Outcomes lines in the README.

Tomorrow's calendar (example):
- Example block: 09:10 to 09:30, owner review. This block is fake.
```

## Weekly chief KPI

Each chief has a weekly KPI. The figures are not in this repo. Dashboard polish needs a business KPI and a usage check first. That rule is [ADR 0002](adr/0002-chief-kpis-and-cost-discipline.md).

The morning brief reports a usage limit. The polish rule asks for a usage check. This page does not claim those two are the same measurement.
