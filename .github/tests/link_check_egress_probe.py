"""Isolated GitHub runner regression for Lychee outbound IP protections.

Servers use only disposable 127.0.0.1 listeners; no cloud metadata or
third-party internal services are touched.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import os
import shutil
import socket
import subprocess
import tempfile

hits = {"target": 0, "redirect": 0}
target_port = 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        kind = self.server.kind
        hits[kind] += 1
        if kind == "redirect":
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{target_port}/target")
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"LOCAL_ONLY")

    def log_message(self, *args):
        pass


def server(kind):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    srv.kind = kind
    Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def lychee(url, exclude=True):
    with tempfile.TemporaryDirectory() as directory:
        Path(directory, "links.csv").write_text(url + "\n", encoding="utf-8")
        cmd = [shutil.which("lychee"), "--format", "json", "--no-progress",
               "--extensions", "csv", "--method", "GET",
               "--timeout", "2", "--max-retries", "0"]
        if exclude:
            cmd.append("--exclude-all-private")
        cmd.append(".")
        env = os.environ.copy()
        for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
            env.pop(name, None)
        env["NO_PROXY"] = "*"
        env["no_proxy"] = "*"
        return subprocess.run(cmd, cwd=directory, env=env,
                              capture_output=True, text=True, timeout=20).returncode


def sudo(*parts):
    return subprocess.run(["sudo", "-n", *parts], check=True, capture_output=True, text=True)


def main():
    global target_port
    script = os.environ["EGRESS_SCRIPT"]
    assert shutil.which("lychee"), "Lychee v0.24.2 not installed"
    target = server("target")
    target_port = target.server_address[1]
    redirect = server("redirect")
    redirect_port = redirect.server_address[1]

    # Resolve a public-looking domain to the test's own disposable local server.
    mapping = ("127.0.0.1 lychee-egress-alias.sandbox-runner.net "
               "lychee-egress-redirect.sandbox-runner.net\n")
    subprocess.run(["sudo", "-n", "tee", "-a", "/etc/hosts"], input=mapping,
                   capture_output=True, text=True, check=True)
    assert socket.gethostbyname("lychee-egress-alias.sandbox-runner.net") == "127.0.0.1"
    assert socket.gethostbyname("lychee-egress-redirect.sandbox-runner.net") == "127.0.0.1"

    try:
        lychee(f"http://127.0.0.1:{target_port}/baseline", exclude=False)
        assert hits["target"] == 1, f"Baseline failed: {hits}"
        print("BASELINE_LOCAL_GET=PASS", flush=True)

        # Must fail closed if the required kernel enforcement is unavailable.
        sudo("bash", script, "install")
        try:
            lychee(f"http://127.0.0.1:{target_port}/direct", exclude=False)
            assert hits["target"] == 1, "Firewall permitted direct loopback GET"
            print("KERNEL_BLOCK_DIRECT_IP=PASS", flush=True)

            lychee(f"http://lychee-egress-alias.sandbox-runner.net:{target_port}/alias")
            assert hits["target"] == 1, "Firewall permitted DNS-alias loopback GET"
            print("KERNEL_BLOCK_DNS_ALIAS=PASS", flush=True)

            # Test-only exception lets the *redirecting* local server answer,
            # but the new connection to the actual target must still be denied.
            sudo("iptables", "-w", "-I", "LC_PRIVATE_V4", "1",
                 "-d", "127.0.0.1/32", "-p", "tcp",
                 "--dport", str(redirect_port), "-j", "RETURN")
            # Validate that the exception admits the redirect source itself.
            check = subprocess.run(
                ["curl", "--noproxy", "*", "-sS", "--max-time", "4",
                 "-o", "/dev/null", f"http://127.0.0.1:{redirect_port}/go"],
                capture_output=True, text=True)
            print(f"REDIRECT_SOURCE_DIAGNOSTIC=rc:{check.returncode},hits:{hits[\'redirect\']},port:{redirect_port},err:{check.stderr[:200]}", flush=True)
            print(sudo("iptables", "-w", "-nvL", "LC_PRIVATE_V4").stdout[:2400], flush=True)
            assert check.returncode == 0 and hits["redirect"] == 1, (
                "Test-only redirect-source exception did not admit traffic")
            hits["redirect"] = 0
            rc = lychee(f"http://lychee-egress-redirect.sandbox-runner.net:{redirect_port}/go")
            print(f"REDIRECT_INPUT_EXIT_CODE={rc}", flush=True)
            assert hits["redirect"] == 1, "Test redirect source was not fetched"
            assert hits["target"] == 1, "Firewall followed redirect into loopback"
            print("KERNEL_BLOCK_REDIRECT_TARGET=PASS", flush=True)

            # Verify ordinary public outbound HTTPS remains permitted.
            result = subprocess.run(
                ["curl", "-fsSI", "--connect-timeout", "5", "--max-time", "12",
                 "https://github.com/"],
                capture_output=True, text=True, timeout=15)
            assert result.returncode == 0, "Public HTTPS was unexpectedly blocked"
            print("PUBLIC_HTTPS_STILL_WORKS=PASS", flush=True)

            v6 = sudo("ip6tables", "-w", "-S", "LC_PRIVATE_V6").stdout
            assert "-d ::1/128" in v6 and "-d fc00::/7" in v6
            assert "-d ::ffff:0.0.0.0/96" in v6 or "-d ::ffff:0:0/96" in v6
            print("IPV6_PRIVATE_FILTER_INSTALLED=PASS", flush=True)
        finally:
            sudo("bash", script, "remove")
    finally:
        redirect.shutdown()
        target.shutdown()


if __name__ == "__main__":
    main()
