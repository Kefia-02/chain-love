"""Safety-only SSRF regression for pinned Lychee. All HTTP is local loopback.

Never probes third-party services or metadata endpoints and never logs token values.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import shutil
import socket
import subprocess
import tempfile
from threading import Lock, Thread

counts = {"target": 0, "redirect": 0}
auth_seen = []
lock = Lock()
target_port = None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with lock:
            counts[self.server.kind] += 1
            auth_seen.append("authorization" in {x.lower() for x in self.headers})
        if self.server.kind == "redirect":
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{target_port}/only-local")
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "10")
        self.end_headers()
        if self.server.kind == "target":
            self.wfile.write(b"LOCAL_ONLY")

    def log_message(self, fmt, *args):
        pass


def serve(kind):
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.kind = kind
    Thread(target=server.serve_forever, daemon=True).start()
    return server


def invoke(url, exclude, tempdir):
    env = os.environ.copy()
    env.update({"NO_PROXY": "*", "no_proxy": "*",
                "HTTP_PROXY": "", "HTTPS_PROXY": "",
                "http_proxy": "", "https_proxy": "",
                "ALL_PROXY": "", "all_proxy": ""})
    cmd = [shutil.which("lychee"), "--format", "json", "--no-progress",
           "--method", "GET", "--timeout", "5", "--max-retries", "0"]
    if exclude:
        cmd.append("--exclude-all-private")
    Path(tempdir, "probe.csv").write_text(url + "\n", encoding="utf-8")
    cmd.extend(["--extensions", "csv", "."])
    p = subprocess.run(cmd, cwd=tempdir, capture_output=True, text=True,
                       env=env, timeout=30)
    if p.returncode != 0:
        # Report only redacted status, not raw output/headers
        raise AssertionError(f"Lychee command returned {p.returncode} for case {url.split(':')[0]}")
    return p.returncode


def main():
    global target_port
    assert shutil.which("lychee"), "Pinned Lychee binary unavailable"
    # Bind both hostnames strictly to the disposable local loopback server.
    hosts = "127.0.0.1 lychee-alias.sandbox-runner.net lychee-redirect.sandbox-runner.net\n"
    subprocess.run(["sudo", "tee", "-a", "/etc/hosts"], input=hosts, text=True,
                   capture_output=True, check=True)
    for name in ("lychee-alias.sandbox-runner.net", "lychee-redirect.sandbox-runner.net"):
        assert socket.gethostbyname(name) == "127.0.0.1", "Nonlocal DNS resolution"
    target = serve("target")
    target_port = target.server_address[1]
    redirect = serve("redirect")
    redirect_port = redirect.server_address[1]
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            # Baseline: unfiltered Lychee can access our disposable local server.
            invoke(f"http://127.0.0.1:{target_port}/baseline", False, tempdir)
            assert counts["target"] == 1, "Baseline local request did not arrive"
            print("BASELINE_GET=PASS")

            # With the added flag, literal loopback must be blocked.
            # Excluded links can produce a nonzero 'empty input' code on some versions.
            # Capture separately without requiring status=0.
            try:
                invoke(f"http://127.0.0.1:{target_port}/blocked", True, tempdir)
            except AssertionError:
                pass
            assert counts["target"] == 1, "Literal loopback bypassed exclusion"
            print("LITERAL_LOOPBACK_BLOCK=PASS")

            # DNS alias is locally pinned in /etc/hosts; no real DNS lookup needed.
            invoke(f"http://lychee-alias.sandbox-runner.net:{target_port}/alias", True, tempdir)
            assert counts["target"] == 2, "DNS-host alias was not delivered"
            print("DNS_ALIAS_BYPASS=CONFIRMED_IN_ISOLATED_TEST")

            # The redirecting endpoint and its destination are both our loopback servers.
            invoke(f"http://lychee-redirect.sandbox-runner.net:{redirect_port}/go", True, tempdir)
            assert counts["redirect"] == 1 and counts["target"] == 3, "Redirect was not followed"
            print("REDIRECT_TO_LOOPBACK_BYPASS=CONFIRMED_IN_ISOLATED_TEST")

            assert not any(auth_seen), "Authorization header unexpectedly reached test server"
            print("AUTHORIZATION_HEADER_TO_ARBITRARY_LOCAL_TARGET=NOT_OBSERVED")
    finally:
        redirect.shutdown()
        target.shutdown()


if __name__ == "__main__":
    main()
