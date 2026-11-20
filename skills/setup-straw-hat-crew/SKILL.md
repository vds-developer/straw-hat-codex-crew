---
name: setup-straw-hat-crew
description: Install the Straw Hat specialist profiles and captain instructions into the current project when the user requests crew setup.
---

Before carrying out this skill, follow the script discovery and fallback rules in the sibling forge/SKILL.md. Look for a compatible crew setup CLI.

Resolve the installed plugin root two directories above this SKILL.md's containing directory. Use that root as the source and the user's current project as the destination.

Copy the nine bundled .codex/agents/*.toml files and the bundled skills/chopper-bug-hunt and skills/forge directories (including their scripts) into matching project-relative paths. Create missing directories. Skip identical files. Preserve customized files and report any conflicts. Avoid following destination symlinks outside the project.

Read the bundled AGENTS.md. If the project has no AGENTS.md, copy it. Otherwise preserve its instructions and append the crew section once. If a Straw Hat Pirates heading is already present, preserve the existing section. If its Forge routing paragraph is missing, add that paragraph once. Verify all nine names and both project skills exist, report changes and conflicts, and tell the user to start a new project chat to load the profiles.
