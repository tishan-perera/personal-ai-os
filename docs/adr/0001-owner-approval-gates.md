# ADR 0001: Owner approval gates

- Status: Accepted
- Date: Not published
- Decider: Tishan Perera, owner

## Context

The org has one owner and a chief of staff, Amanda, who runs the day-to-day work and people ops. Seats draft and prepare work. Some steps affect other people, money, jobs, or security.

## Decision

These actions need explicit owner approval:

- Send a message or an email
- Post
- Apply to a job
- Trade
- Hire
- Change security

Outbound messages are drafts for the owner to send.

The org cannot hire or restructure without owner authorization. Amanda's people ops stop at that line.

GitHub changes go only through pull requests the owner merges.

Private financial data is shared only with the owner. Account numbers are masked to the last 4.

## Consequences

- A seat can finish inside work and a draft, and the owner remains the sender.
- A hire or a restructure waits for the owner.
- The default branch changes when the owner merges a pull request.
- Private financial data stays with the owner.
- The working matrix is in [the approval gates doc](../approval-gates.md).

## Related

- [ADR 0002: Chief KPIs and cost discipline](0002-chief-kpis-and-cost-discipline.md)
- [ADR 0003: Shutting down the Trading pilot](0003-shutting-down-the-trading-pilot.md)
