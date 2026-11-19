<#
.SYNOPSIS
Lists the Straw Hat crew profiles and checks their TOML and required fields.
.DESCRIPTION
Requires Python on PATH with tomllib (Python 3.11+) or tomli installed.
Returns exit code 0 for a valid roster and 1 on failure.
.PARAMETER ProfilesPath
Directory containing the nine TOML files. Defaults to this repository's profiles.
.EXAMPLE
.\tools\Test-CrewProfiles.ps1
#>
[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string]$ProfilesPath = (Join-Path $PSScriptRoot '../.codex/agents')
)

$python = Get-Command python -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $python) {
    [Console]::Error.WriteLine('Python is required. Install Python 3.11+ or Python 3 with tomli.')
    exit 1
}

$validator = @'
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        sys.exit("The profile checker requires Python 3.11+ or the tomli package.")

crew = {"brook", "chopper", "franky", "jinbe", "nami", "robin", "sanji", "usopp", "zoro"}
required_fields = ("name", "description", "developer_instructions")
profiles_dir = Path(sys.argv[1])
errors = []

try:
    files = sorted(path for path in profiles_dir.iterdir() if path.suffix.lower() == ".toml")
except OSError as error:
    sys.exit(str(error))

for missing in sorted(crew - {path.stem for path in files}):
    errors.append(f"{missing}.toml is missing")

for path in files:
    if path.stem not in crew:
        errors.append(f"{path.name} is outside the crew roster")
        continue
    try:
        with path.open("rb") as profile_file:
            profile = tomllib.load(profile_file)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        errors.append(f"{path.name}: {error}")
        continue

    problems = []
    for field in required_fields:
        value = profile.get(field)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"{field} must be a nonempty string")
    if "name" in profile and profile["name"] != path.stem:
        problems.append(f"name must match the filename ({path.stem})")
    if problems:
        errors.append(f"{path.name}: " + ", ".join(problems))
    else:
        print(f"{path.stem} - {profile['description']}")

if errors:
    sys.exit("\n".join(errors))
print(f"Validated {len(files)} crew profiles.")
'@

$validator | & $python.Source -I - $ProfilesPath
exit $LASTEXITCODE
