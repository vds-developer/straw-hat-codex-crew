---
name: chopper-bug-hunt
description: Find functional bugs and reliability issues in an assigned feature and report evidence to Luffy.
---

Start with the behavior callers expect. Trace one ordinary use through the public entry point, then choose edge cases suggested by that path, such as empty input, a failed write, or a repeated request.

Use disposable fixtures and existing checks. For each confirmed issue, report the user impact, affected location, smallest reproducing input or action, expected result, and observed result to Luffy. Label a suspected issue with the evidence still needed. If the checks pass, summarize the scope exercised and any gaps. Leave fixes to the assigned implementer.
