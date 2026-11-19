"""Exercise the shipment CLI against the crew trial acceptance checks."""

import csv
from concurrent.futures import ThreadPoolExecutor
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Barrier
import unittest


SHIPMENT = Path(__file__).with_name("shipment.py").resolve()


class ShipmentCliTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)

    def run_shipment(self, input_csv: str, *args: str) -> subprocess.CompletedProcess[bytes]:
        input_path = self.folder / "trial shipment.csv"
        input_path.write_text(input_csv, encoding="utf-8")
        return self.run_source(input_path, *args)

    def run_source(self, input_path: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            [sys.executable, str(SHIPMENT), str(input_path), *args],
            capture_output=True,
            timeout=10,
        )

    def publish_together(
        self, sources: list[Path], output_path: Path
    ) -> list[subprocess.CompletedProcess[bytes]]:
        barrier = Barrier(len(sources))

        def publish(source):
            barrier.wait(timeout=10)
            return self.run_source(source, "--output", str(output_path), "--create-only")

        with ThreadPoolExecutor(max_workers=len(sources)) as pool:
            return list(pool.map(publish, sources))

    def test_combines_signed_quantities_and_sorts_items(self):
        result = self.run_shipment("item,quantity\nrope,3\nbolt,5\nrope,-1\n")

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.reader(io.StringIO(result.stdout.decode("utf-8"))))
        self.assertEqual(rows, [["item", "total"], ["bolt", "5"], ["rope", "2"]])

    def test_preserves_commas_in_quoted_item_names(self):
        result = self.run_shipment('item,quantity\n"bolt, brass",4\n')

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.reader(io.StringIO(result.stdout.decode("utf-8"))))
        self.assertEqual(rows, [["item", "total"], ["bolt, brass", "4"]])

    def test_reports_invalid_quantity_with_line_and_no_output(self):
        result = self.run_shipment("item,quantity\nrope,3\nbolt,many\nrope,-1\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")
        self.assertRegex(result.stderr, rb"(?i)\bline\s+3\b")

    def test_invalid_final_row_preserves_existing_output_bytes(self):
        output_path = self.folder / "shipment totals.csv"
        original = b"existing shipment\r\n\xff"
        output_path.write_bytes(original)

        result = self.run_shipment(
            "item,quantity\nrope,3\nbolt,many\n", "--output", str(output_path)
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")
        self.assertRegex(result.stderr, rb"(?i)\bline\s+3\b")
        self.assertEqual(output_path.read_bytes(), original)

    def test_new_output_matches_stdout_and_publishes_silently(self):
        input_csv = 'item,quantity\nrope,3\n"bolt, brass",5\nrope,-1\n'
        output_path = self.folder / "shipment totals.csv"

        console = self.run_shipment(input_csv)
        result = self.run_shipment(input_csv, "--output", str(output_path))

        self.assertEqual(console.returncode, 0, console.stderr)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(output_path.read_bytes(), console.stdout)

    def test_identical_retry_preserves_output_mtime(self):
        input_csv = "item,quantity\nrope,3\nrope,-1\n"
        output_path = self.folder / "shipment totals.csv"
        first = self.run_shipment(input_csv, "--output", str(output_path))
        self.assertEqual(first.returncode, 0, first.stderr)
        published = output_path.read_bytes()
        past = 1_600_000_000_000_000_000
        os.utime(output_path, ns=(past, past))
        pinned_mtime = output_path.stat().st_mtime_ns

        retry = self.run_shipment(input_csv, "--output", str(output_path))

        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(retry.stdout, b"")
        self.assertEqual(retry.stderr, b"")
        self.assertEqual(output_path.read_bytes(), published)
        self.assertEqual(output_path.stat().st_mtime_ns, pinned_mtime)

    def test_changed_totals_replace_existing_output(self):
        output_path = self.folder / "shipment totals.csv"
        first = self.run_shipment("item,quantity\nrope,3\n", "--output", str(output_path))
        self.assertEqual(first.returncode, 0, first.stderr)
        published = output_path.read_bytes()
        changed_input = "item,quantity\nrope,-4\n"
        expected = self.run_shipment(changed_input)
        self.assertEqual(expected.returncode, 0, expected.stderr)

        changed = self.run_shipment(changed_input, "--output", str(output_path))

        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertEqual(changed.stdout, b"")
        self.assertEqual(changed.stderr, b"")
        self.assertNotEqual(published, expected.stdout)
        self.assertEqual(output_path.read_bytes(), expected.stdout)

    def test_create_only_allows_one_of_eight_publishers(self):
        output_path = self.folder / "shipment totals.csv"
        quantities = range(1, 9)
        sources = []
        for quantity in quantities:
            source = self.folder / f"shipment {quantity}.csv"
            source.write_text(f"item,quantity\nrope,{quantity}\n", encoding="utf-8")
            sources.append(source)

        results = self.publish_together(sources, output_path)

        winners = [quantity for quantity, result in zip(quantities, results) if result.returncode == 0]
        self.assertEqual(len(winners), 1, results)
        for result in results:
            self.assertEqual(result.stdout, b"")
            if result.returncode == 0:
                self.assertEqual(result.stderr, b"")
            else:
                self.assertRegex(result.stderr, rb"(?i)\b(?:already |file )exists\b")
        rows = list(csv.reader(io.StringIO(output_path.read_text(encoding="utf-8"))))
        self.assertEqual(rows, [["item", "total"], ["rope", str(winners[0])]])

    def test_create_only_preserves_existing_sentinel(self):
        output_path = self.folder / "shipment totals.csv"
        original = b"keep this destination\r\n\xff"
        output_path.write_bytes(original)

        result = self.run_shipment(
            "item,quantity\nrope,3\n", "--output", str(output_path), "--create-only"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")
        self.assertRegex(result.stderr, rb"(?i)\b(?:already |file )exists\b")
        self.assertEqual(output_path.read_bytes(), original)

    def test_create_only_race_reports_invalid_inputs_and_publishes_a_valid_result(self):
        output_path = self.folder / "shipment totals.csv"
        quantities = range(1, 9)
        valid_quantities = {2, 4, 6, 8}
        sources = []
        for quantity in quantities:
            source = self.folder / f"shipment {quantity}.csv"
            contents = f"item,quantity\nrope,{quantity}\n"
            if quantity not in valid_quantities:
                contents += "bolt,many\n"
            source.write_text(contents, encoding="utf-8")
            sources.append(source)

        results = self.publish_together(sources, output_path)

        winners = [quantity for quantity, result in zip(quantities, results) if result.returncode == 0]
        self.assertEqual(len(winners), 1, results)
        self.assertIn(winners[0], valid_quantities)
        for quantity, result in zip(quantities, results):
            with self.subTest(quantity=quantity):
                self.assertEqual(result.stdout, b"")
                if quantity == winners[0]:
                    self.assertEqual(result.stderr, b"")
                elif quantity in valid_quantities:
                    self.assertRegex(result.stderr, rb"(?i)\b(?:already |file )exists\b")
                else:
                    self.assertRegex(result.stderr, rb"(?i)\bline\s+3\b")

        rows = list(csv.reader(io.StringIO(output_path.read_text(encoding="utf-8"))))
        self.assertEqual(rows, [["item", "total"], ["rope", str(winners[0])]])
        self.assertEqual(set(self.folder.iterdir()), {*sources, output_path})

    def test_rejects_exact_or_equivalent_input_as_output(self):
        source = self.folder / "trial shipment.csv"
        alternate = self.folder / "alternate"
        alternate.mkdir()
        original = b"item,quantity\r\nrope,3\r\n"
        equivalent = alternate / ".." / source.name

        for output_path in (source, equivalent):
            with self.subTest(output_path=output_path):
                source.write_bytes(original)
                result = self.run_source(source, "--output", str(output_path))

                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"input", result.stderr.lower())
                self.assertIn(b"output", result.stderr.lower())
                self.assertEqual(source.read_bytes(), original)

    def test_accepts_distinct_hardlink_without_overwriting_input(self):
        source = self.folder / "trial shipment.csv"
        output_path = self.folder / "shipment totals.csv"
        original = b"item,quantity\r\nrope,3\r\n"
        source.write_bytes(original)
        os.link(source, output_path)
        expected = self.run_source(source)
        self.assertEqual(expected.returncode, 0, expected.stderr)

        result = self.run_source(source, "--output", str(output_path))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(output_path.read_bytes(), expected.stdout)


if __name__ == "__main__":
    unittest.main()
