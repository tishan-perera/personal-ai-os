# ADR 0003: Shutting down the Trading pilot

- Status: Accepted
- Date: 17 November 2026
- Decider: Tishan Perera, owner

## Context

The org piloted a Trading department. The ledger was paper only, which means simulated. A hard rule sat on the pilot: no real brokerage orders. Live trading required explicit owner authorization.

## Decision

On 17 November 2026 the owner shut the department down and deleted its agents.

## Lesson

Scope an experiment before you staff it. Write the hard rule in the same decision as the pilot. Here the rule was a simulated ledger and no real brokerage orders. The owner then closed the department and deleted its agents. Ending the experiment is part of running it.

## Consequences

- Trading is Closed.
- Its agents are deleted.
- The public record keeps the fence and the shutdown date.
- Profit, loss, tickers, and trade history are omitted.
- This ADR does not reopen the department.

## Related

- [ADR 0001: Owner approval gates](0001-owner-approval-gates.md)
- [Org chart](../org-chart.md)
