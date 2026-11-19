"""Exercise process termination just before and after the real file replacement."""

from pathlib import Path
import subprocess
import sys
import tempfile
from textwrap import dedent
import time
import unittest


SHIPMENT = Path(__file__).with_name("shipment.py").resolve()
WRAPPER = dedent("""
    from pathlib import Path
    import runpy
    import sys
    import time

    cut, marker, script, *arguments = sys.argv[1:]
    filesystem_replace = Path.replace

    def await_termination():
        Path(marker).touch()
        while True:
            time.sleep(0.1)

    def replace(path, target):
        if cut == "before":
            await_termination()
        result = filesystem_replace(path, target)
        if cut == "after":
            await_termination()
        return result

    Path.replace = replace
    sys.argv = [script, *arguments]
    runpy.run_path(script, run_name="__main__")
""")


class ShipmentInterruptionTests(unittest.TestCase):
    def assert_interrupted_replacement(self, cut: str):
        # The child performs real filesystem I/O. Only the timing of its stop is controlled.
        with tempfile.TemporaryDirectory(prefix="monkey-shipment-stop-") as folder:
            root = Path(folder)
            source = root / "manifest.csv"
            destination = root / "totals.csv"
            marker = root / "reached-cut"
            old_bytes = b"prior destination\r\n\xff"
            new_bytes = b"item,total\r\nrope,2\r\n"
            source.write_bytes(b"item,quantity\r\nrope,3\r\nrope,-1\r\n")
            destination.write_bytes(old_bytes)
            command = [str(SHIPMENT), str(source), "--output", str(destination)]

            with subprocess.Popen(
                [sys.executable, "-B", "-c", WRAPPER, cut, str(marker), *command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ) as child:
                try:
                    deadline = time.monotonic() + 10
                    while not marker.exists() and child.poll() is None:
                        if time.monotonic() >= deadline:
                            break
                        time.sleep(0.01)
                    reached_cut = marker.exists() and child.poll() is None
                finally:
                    if child.poll() is None:
                        child.kill()
                    stdout, stderr = child.communicate(timeout=10)

            self.assertTrue(reached_cut, (cut, child.returncode, stdout, stderr))
            self.assertNotEqual(child.returncode, 0)
            self.assertEqual(destination.read_bytes(), old_bytes if cut == "before" else new_bytes)

            retry = subprocess.run(
                [sys.executable, "-B", *command],
                capture_output=True,
                timeout=10,
            )
            self.assertEqual(retry.returncode, 0, retry.stderr)
            self.assertEqual(retry.stdout, b"")
            self.assertEqual(retry.stderr, b"")
            self.assertEqual(destination.read_bytes(), new_bytes)

    def test_interruption_before_replace_preserves_old_output_then_retry_publishes(self):
        self.assert_interrupted_replacement("before")

    def test_interruption_after_replace_leaves_complete_new_output_and_retry_succeeds(self):
        self.assert_interrupted_replacement("after")


if __name__ == "__main__":
    unittest.main()
