---
name: forge
description: Find and reuse Codex scripts before a crew task and turn repeatable scripted work into a reusable command-line tool.
---

Resolve the current user's Codex home from a nonempty CODEX_HOME, otherwise use .codex in the user's home directory. Look under its scripts directory. Match the requested operation first against the calling skill's script mapping, then against relevant existing script names and documented interfaces. Inspect a candidate's source or trusted documentation before running it. Use it only when its inputs, outputs, dependencies and effects fit the task and current permissions.

If a suitable script is available, invoke it by absolute path with explicit project inputs. Verify the result. Treat a genuine task failure as a finding. If the script is absent, incompatible or inaccessible, continue the calling skill's normal workflow.

When the work contains a repeatable scripted operation, turn that operation into a CLI under the resolved scripts directory. Prefer adapting an existing command. Give the CLI a descriptive name, documented arguments, --help, clear diagnostics and meaningful exit status. Pass project-specific paths as arguments. Keep credentials and project-private data out of shared scripts. Preserve unrelated files and existing customized commands. Read-only roles hand creation back to Luffy.

Run the command on a representative input and an expected failure. Add its filename, invocation and purpose to the owning skill's script mapping when editable. For a cached plugin skill, update its maintained source or project instructions. If writing to Codex home requires permission, use the normal approval mechanism. Continue the original task when installation is unavailable.

## Script mapping

For packaging this crew repository, use python (or python3) with the absolute path to crew-package.py in Codex home's scripts directory and the crew repository root as its argument. The CLI packages current working copies of Git-tracked files. Review the tracked file list before publishing. A maintained copy ships in scripts/crew-package.py beside this skill. When this packaging task recurs and the CLI is missing, install the bundled copy there if permitted.
