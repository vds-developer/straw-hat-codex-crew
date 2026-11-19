"""Summarize signed shipment quantities by item."""

import argparse
import csv
import filecmp
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile


def read_totals(source):
    totals = {}
    with source.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        try:
            if next(reader, None) != ["item", "quantity"]:
                raise ValueError("line 1: expected the header item,quantity")
            for row in reader:
                if len(row) != 2 or not row[0].strip():
                    raise ValueError(f"line {reader.line_num}: expected an item and quantity")
                item, quantity = row
                if not re.fullmatch(r"[+-]?[0-9]+", quantity.strip()):
                    raise ValueError(f"line {reader.line_num}: quantity must be a signed integer")
                totals[item] = totals.get(item, 0) + int(quantity)
        except csv.Error as error:
            raise ValueError(f"line {reader.line_num}: {error}") from error
    return totals


def write_totals(stream, totals):
    writer = csv.writer(stream)
    writer.writerow(("item", "total"))
    writer.writerows(sorted(totals.items()))


def commit_output(temporary, destination, create_only):
    if create_only:
        try:
            os.link(temporary, destination)
        except FileExistsError as error:
            raise ValueError(f"{destination}: output already exists") from error
        return
    try:
        if filecmp.cmp(temporary, destination, shallow=False):
            return
    except FileNotFoundError:
        pass
    temporary.replace(destination)


def publish_output(destination, totals, create_only):
    stream = NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=destination.parent, delete=False
    )
    temporary = Path(stream.name)
    try:
        with stream:
            write_totals(stream, totals)
        commit_output(temporary, destination, create_only)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="UTF-8 CSV file with columns item,quantity")
    parser.add_argument(
        "--output", type=Path, help="publish to a path distinct from the input after resolving symlinks"
    )
    parser.add_argument(
        "--create-only", action="store_true", help="fail if the output path already exists"
    )
    args = parser.parse_args()
    if args.create_only and args.output is None:
        parser.error("--create-only requires --output")
    try:
        totals = read_totals(args.source)
        if args.output is not None:
            # Resolve symbolic aliases while keeping distinct hard-link names eligible for replacement.
            if Path(os.path.realpath(args.source)) == Path(os.path.realpath(args.output)):
                raise ValueError("input and output resolve to the same path")
            publish_output(args.output, totals, args.create_only)
        else:
            sys.stdout.reconfigure(encoding="utf-8", newline="")
            write_totals(sys.stdout, totals)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
