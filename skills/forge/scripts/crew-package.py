"""Build the distributable crew ZIP from the Git-tracked project files."""

import argparse
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="crew repository root")
    args = parser.parse_args()
    root = args.project.resolve()
    output = root / "straw-hat-codex-crew.zip"
    if not (root / ".codex-plugin/plugin.json").is_file():
        parser.error("expected the crew repository root")
    names = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    paths = [Path(name.decode("utf-8")) for name in names.split(b"\0") if name]
    with NamedTemporaryFile(dir=root, delete=False) as staging:
        temporary = Path(staging.name)
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
            for path in paths:
                if path != Path(output.name):
                    archive.write(root / path, Path("straw-hat-codex-crew") / path)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
