---
name: setup-straw-hat-crew
description: Install the Straw Hat specialist profiles and captain instructions into the current project when the user requests crew setup.
---

Resolve the installed plugin root two directories above this SKILL.md's containing directory. Use that root as the source and the user's current project as the destination.

Copy the nine bundled .codex/agents/*.toml files and skills/chopper-bug-hunt/SKILL.md into matching project-relative paths. Create missing directories. Skip identical files. Preserve customized files and report any conflicts. Avoid following destination symlinks outside the project.

Read the bundled AGENTS.md. If the project has no AGENTS.md, copy it. Otherwise preserve its instructions and append the crew section once. If a Straw Hat Pirates heading is already present, preserve the existing section and report that it was found. Verify all nine names and the bug-hunt skill exist, report changes and conflicts, and tell the user to start a new project chat to load the profiles.
