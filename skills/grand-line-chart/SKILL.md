---
name: grand-line-chart
description: Have Nami interview the user to shape a plan, optionally record glossary terms and architecture decisions, and review the resulting plan visually with Lavish.
---

# Grand Line Chart

Start with the requested outcome and a concrete example of success. Follow the sibling Forge skill to discover a suitable planning or review CLI. Inspect relevant code, tests, glossary and prior decisions before asking the user to supply facts.

**Interview.** Work out which choices depend on earlier choices. In each round ask only questions whose prerequisites are settled. For each, give your recommended answer, why it matters, and a realistic alternative when the trade-off is material. Wait for the user's answers and adapt the next round. Test an ambiguous answer against an ordinary use case and a failure case. Carry settled answers forward.

**Document when requested.** Keep a conversation-only plan by default. In “with docs” mode use the project's existing glossary and ADR conventions. Capture agreed meanings when an ambiguous term is resolved. Record a consequential design choice with its alternatives and rationale. Distinguish a proposal from an adopted decision; avoid duplicating existing documents.

**Visual review.** Once the first coherent draft exists, create a local HTML review copy with the goal, constraints, choices, unresolved questions, first implementation slice and observable acceptance checks. Use the installed Lavish skill when available. With Lavish Axi on PATH, open the HTML using lavish-axi "<plan.html>" and follow its installed CLI help to poll that same session for annotations and replies. Keep one listener, revise the same artifact, and ask for confirmation of the revised plan. Honor an ended session. Keep review local unless the user requests sharing. If Lavish is unavailable, offer the installed plan-canvas equivalent or use the same review loop in chat and identify which surface was used.

**Handoff.** Summarize the accepted plan, outstanding decisions, verification criteria and suggested crew owner. An annotation requests discussion or revision. Treat the plan as approved only on an explicit user decision. Implementation starts when authorized.
