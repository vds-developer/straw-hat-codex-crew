"""Check 100 mixed CLI operations against a small in-memory model."""

from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest


SHIPMENT = Path(__file__).with_name("shipment.py").resolve()
SEED = 20261119
INPUTS = (
    (b"item,quantity\nrope,3\nbolt,4\nrope,-1\n", b"item,total\r\nbolt,4\r\nrope,2\r\n"),
    (b"item,quantity\nrope,0\n", b"item,total\r\nrope,0\r\n"),
    (b'item,quantity\n"bolt, brass",-3\n', b'item,total\r\n"bolt, brass",-3\r\n'),
)
INVALID = b"item,quantity\nrope,1\nbolt,many\n"


class ShipmentSequenceTests(unittest.TestCase):
    def test_seeded_publication_sequence(self):
        rng = random.Random(SEED)
        operations = ["create", "replace", "retry", "invalid", "same-entry"] * 20
        rng.shuffle(operations)

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "source.csv"
            reports = [root / f"report-{index}.csv" for index in range(6)]
            # Each modeled report holds the index of the last published input.
            published = {}
            for step, operation in enumerate(operations, 1):
                output = rng.choice(reports)
                if operation == "retry" and published:
                    output = rng.choice(list(published))
                    shipment = published[output]
                else:
                    shipment = rng.randrange(len(INPUTS))
                raw, _ = INPUTS[shipment]
                if operation == "invalid":
                    raw = INVALID
                target = source if operation == "same-entry" else output
                create_only = operation == "create" or (operation == "invalid" and rng.choice([True, False]))
                expected_error = None
                if operation == "invalid":
                    expected_error = rb"(?i)line 3\b"
                elif operation == "same-entry":
                    expected_error = rb"\S"
                elif create_only and output in published:
                    expected_error = rb"(?i)exists\b"
                else:
                    published[output] = shipment

                source.write_bytes(raw)
                command = [sys.executable, str(SHIPMENT), str(source), "--output", str(target)]
                if create_only:
                    command.append("--create-only")
                result = subprocess.run(command, capture_output=True, timeout=10)
                context = f"seed={SEED} step={step} operation={operation} output={target.name}"
                self.assertEqual(result.returncode, 1 if expected_error else 0, (context, result.stderr))
                self.assertEqual(result.stdout, b"", context)
                if expected_error:
                    self.assertRegex(result.stderr, expected_error, context)
                else:
                    self.assertEqual(result.stderr, b"", context)
                self.assertEqual(source.read_bytes(), raw, context)
                self.assertEqual(set(root.iterdir()), {source, *published}, context)
                for report, index in published.items():
                    self.assertEqual(report.read_bytes(), INPUTS[index][1], (context, report.name))


if __name__ == "__main__":
    unittest.main()
