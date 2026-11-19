# Straw Hat Pirates for Codex

A project template for coordinating nine engineering specialists. Luffy takes a goal, assigns scoped work, and checks what the crew delivers. See [the crew roster](AGENTS.md) for each specialist's responsibilities.

## One-line install for macOS

Run this in Terminal from the folder where you keep your projects. It uses Git to install the complete crew in a new project folder and enters that folder. Git stops if the destination already contains files.

```sh
git clone https://github.com/vds-developer/straw-hat-codex-crew.git straw-hat-codex-crew && cd straw-hat-codex-crew
```

If macOS prompts you to install its command-line developer tools, finish that installation and run the command again. Open the new folder in Codex and start a chat.

## Start a project

Download and extract this repository, or clone it with Git. Open the extracted project root in Codex and start a new chat. Use a Codex installation with custom agent support. The profiles specify model names and reasoning settings; if your account uses different models, adjust those fields in the TOML files before launching the crew.

Try this prompt:

> Luffy, send Robin to inspect the shipment CLI and Usopp to verify its retry behavior. Have each return one finding without changing files. Tell me which specialists actually ran.

To adopt the crew in an existing project, copy the nine TOML files from `.codex/agents/` into the same relative directory and merge the routing instructions from `AGENTS.md` into your project instructions. Copy the skills/chopper-bug-hunt directory into the same relative location for proactive bug hunts. Review existing files with matching names before copying. The examples and validator are optional.

## Verify the installation

From the project root, run the profile check with PowerShell and Python 3.11+ (or Python 3.10 with tomli installed).

    pwsh -NoProfile -File tools/Test-CrewProfiles.ps1

Expect nine valid profiles. To exercise the bundled shipment example, run:

    python -B -m unittest discover -s exercises -p "test_shipment*.py" -v

The concurrency examples use a local filesystem with hard-link support. See [the exercises](exercises/README.md) for more project briefs and the trial scorer.
