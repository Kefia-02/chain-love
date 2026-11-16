"""Offline policy regression; optional Lychee integration uses loopback only."""
import re
import shlex
import shutil
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / "workflows/link-check-analysis.yaml"


def lychee_args():
    text = WORKFLOW.read_text(encoding="utf-8")
    section = text.split("      - name: Run Lychee on CSV files\n", 1)[1]
    section = section.split("      - name: Save PR metadata\n", 1)[0]
    block = re.search(r"(?m)^          args: >\n((?:            .*\n)+)", section)
    if not block:
        raise AssertionError("Missing Lychee action args")
    args = shlex.split(" ".join(line.strip() for line in block.group(1).splitlines()))
    return section, args


class PrivateTargetPolicy(unittest.TestCase):
    def test_direct_private_ranges_are_excluded(self):
        section, args = lychee_args()
        self.assertIn("lycheeVersion: v0.24.2", section)
        self.assertEqual(args.count("--exclude-all-private"), 1)
        self.assertFalse(any(x.startswith("--exclude-all-private=") for x in args))

    def test_existing_public_link_check_settings_remain(self):
        _, args = lychee_args()
        for option, value in (
            ("--extensions", "csv"), ("--method", "GET"), ("--timeout", "15"),
            ("--accept", "200,202,204,400,401,403,405,429"),
        ):
            self.assertEqual(args[args.index(option) + 1], value)

    @unittest.skipUnless(shutil.which("lychee"), "Pinned Lychee binary unavailable")
    def test_lychee_does_not_contact_loopback(self):
        class Handler(BaseHTTPRequestHandler):
            count = 0

            def do_GET(self):
                type(self).count += 1
                self.send_response(200)
                self.end_headers()

            def log_message(self, *_):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                file = Path(tmp) / "links.csv"
                file.write_text(f"url\nhttp://127.0.0.1:{server.server_port}/\n")
                base = ["lychee", "--extensions", "csv", "--method", "GET",
                        "--timeout", "2", "--max-retries", "0", "--no-progress"]
                # Control: without the safety flag, the local test server receives GET.
                first = subprocess.run([*base, str(file)], cwd=tmp,
                                       capture_output=True, text=True, timeout=15)
                self.assertGreater(Handler.count, 0, first.stdout + first.stderr)
                before = Handler.count
                _, configured = lychee_args()
                flags = [x for x in configured if x == "--exclude-all-private"]
                second = subprocess.run([*base, *flags, str(file)], cwd=tmp,
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(Handler.count, before, second.stdout + second.stderr)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
