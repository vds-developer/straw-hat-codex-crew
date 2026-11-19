"""Report the recorded pass/fail results for a crew trial."""

import argparse
import json
from pathlib import Path
from textwrap import indent


def read_checks(path: Path) -> list[tuple[str, bool, str]]:
    scorecard = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(scorecard, dict):
        raise ValueError("The scorecard must be a JSON object.")

    checks = scorecard.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("'checks' must be a nonempty array.")

    results = []
    for index, check in enumerate(checks, start=1):
        if not isinstance(check, dict):
            raise ValueError(f"Check {index} must be an object.")

        name = check.get("name")
        if not isinstance(name, str) or not name.strip() or len(name.splitlines()) != 1:
            raise ValueError(f"Check {index} must have a nonempty, single-line 'name'.")

        passed = check.get("passed")
        if not isinstance(passed, bool):
            raise ValueError(f"Check {index} must have a boolean 'passed' value.")

        notes = check.get("notes", "")
        if not isinstance(notes, str):
            raise ValueError(f"Check {index} must have string 'notes' when provided.")

        results.append((name.strip(), passed, notes.strip()))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report the recorded pass/fail results for a crew trial.",
        epilog="Exit codes: 0 all checks passed, 1 any check failed, 2 invalid input.",
    )
    parser.add_argument("scorecard", type=Path, help="path to the JSON scorecard")
    args = parser.parse_args()

    try:
        checks = read_checks(args.scorecard)
    except (OSError, ValueError) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")

    for name, passed, notes in checks:
        status = "PASS" if passed else "FAIL"
        print(f"{status} {name}")
        if notes:
            print(indent(notes, "  "))

    passed_count = sum(passed for _, passed, _ in checks)
    failed_count = len(checks) - passed_count
    print(f"Total: {len(checks)} checks, {passed_count} passed, {failed_count} failed")
    return 1 if failed_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
