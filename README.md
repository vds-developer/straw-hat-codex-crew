# Straw Hat Pirates for Codex

A project template for coordinating nine engineering specialists. Luffy takes a goal, assigns scoped work, and checks what the crew delivers. See [the crew roster](AGENTS.md) for each specialist's responsibilities.

## One-line install for macOS

With the Codex CLI installed, run this in Terminal:

```sh
codex plugin marketplace add vds-developer/straw-hat-codex-crew && codex plugin add straw-hat-crew@straw-hat-crew
```

Open your project in Codex and invoke the **setup-straw-hat-crew** skill once per project. It installs the nine specialist profiles and Luffy’s routing instructions while preserving customized files. Start a new chat in that project to use the crew.

## Grand Line Chart

Ask “Nami, use Grand Line Chart with docs to plan this feature and review it in Lavish.” Omit “with docs” for a conversation-only decision record. Lavish Axi provides the optional local browser review. When unavailable, the interview and review can continue in chat.

## Log Pose

Ask “Luffy, run Log Pose on this task.” The crew reviews what happened and proposes evidence-backed edits to the skills involved. You choose which changes to apply.

## Forge

Crew skills first check `$CODEX_HOME/scripts` (default `~/.codex/scripts`) for a suitable CLI. When one is unavailable, the skill continues normally. Forge turns repeatable scripted work into reusable commands there. For example, ask “Forge the manifest reconciliation step into a CLI and use it on this shipment.” Rerun crew setup in existing projects to add Forge.

## Start a project

Download and extract this repository, or clone it with Git. Open the extracted project root in Codex and start a new chat. Use a Codex installation with custom agent support. The profiles specify model names and reasoning settings; if your account uses different models, adjust those fields in the TOML files before launching the crew.

Try this prompt:

> Luffy, send Robin to inspect the shipment CLI and Usopp to verify its retry behavior. Have each return one finding without changing files. Tell me which specialists actually ran.

To adopt the crew in an existing project, copy the nine TOML files from `.codex/agents/` into the same relative directory and merge the routing instructions from `AGENTS.md` into your project instructions. Copy the skills/forge, skills/log-pose, skills/grand-line-chart, and skills/chopper-bug-hunt directories into the same relative location for proactive bug hunts. Review existing files with matching names before copying. The examples and validator are optional.

## Verify the installation

After running project setup, open a terminal in the project root. Choose your operating system below to check that all nine profiles and both instruction files are present and nonempty.

### macOS (Terminal)

```sh
(
  set -e
  for name in brook chopper franky jinbe nami robin sanji usopp zoro; do
    test -s ".codex/agents/$name.toml" || { echo "Missing profile: $name"; exit 1; }
  done
  test -s AGENTS.md && test -s skills/chopper-bug-hunt/SKILL.md || { echo "Missing crew instructions or bug-hunt skill"; exit 1; }
  echo "Found all nine profiles, crew instructions, and bug-hunt skill."
)
```

### Windows (PowerShell)

```powershell
$files = @('AGENTS.md', 'skills/chopper-bug-hunt/SKILL.md')
$files += 'brook','chopper','franky','jinbe','nami','robin','sanji','usopp','zoro' | ForEach-Object { ".codex/agents/$_.toml" }
foreach ($file in $files) {
    if (!(Test-Path -LiteralPath $file -PathType Leaf) -or (Get-Item -LiteralPath $file).Length -eq 0) { throw "Missing or empty: $file" }
}
'Found all nine profiles, crew instructions, and bug-hunt skill.'
```

### Linux (terminal)

```sh
(
  set -e
  for name in brook chopper franky jinbe nami robin sanji usopp zoro; do
    test -s ".codex/agents/$name.toml" || { echo "Missing profile: $name"; exit 1; }
  done
  test -s AGENTS.md && test -s skills/chopper-bug-hunt/SKILL.md || { echo "Missing crew instructions or bug-hunt skill"; exit 1; }
  echo "Found all nine profiles, crew instructions, and bug-hunt skill."
)
```

A successful check prints `Found all nine profiles, crew instructions, and bug-hunt skill.` To check that Codex can launch a specialist, start a fresh chat in the project and ask: “Luffy, send Robin to read AGENTS.md and report one finding.”

### Optional template tests

From a clone or extracted ZIP, run the shipment tests with Python 3.10 or later. Use `python3` on macOS or Linux and `python` on Windows.

    python3 -B -m unittest discover -s exercises -p "test_shipment*.py" -v

The concurrency examples use a local filesystem with hard-link support. See [the exercises](exercises/README.md) for more project briefs and the trial scorer.
