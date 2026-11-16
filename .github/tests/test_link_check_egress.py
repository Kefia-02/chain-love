"""Configuration regression for SSRF-hardened link-check analysis."""
from pathlib import Path
import subprocess
import unittest

HERE = Path(__file__).resolve().parent.parent
WORKFLOW = HERE / "workflows" / "link-check-analysis.yaml"
GUARD = HERE / "scripts" / "link-check-egress.sh"


class TestLinkCheckEgress(unittest.TestCase):
    def test_guard_is_valid_shell(self):
        result = subprocess.run(["bash", "-n", str(GUARD)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_ipv4_ipv6_private_ranges_and_bypass_families(self):
        guard = GUARD.read_text(encoding="utf-8")
        for destination in (
            "10.0.0.0/8", "127.0.0.0/8", "169.254.0.0/16",
            "172.16.0.0/12", "192.168.0.0/16",
            "100.64.0.0/10", "::1/128", "::ffff:0:0/96",
            "fc00::/7", "fe80::/10",
        ):
            with self.subTest(destination=destination):
                self.assertIn(destination, guard)
        self.assertIn('sudo -n iptables -w -I OUTPUT 1', guard)
        self.assertIn('sudo -n ip6tables -w -I OUTPUT 1', guard)
        self.assertIn("ESTABLISHED,RELATED", guard)
        self.assertIn('install) install_guard', guard)
        self.assertIn('remove) remove_guard', guard)

    def test_production_stages_guard_before_untrusted_pr_materialization(self):
        yaml = WORKFLOW.read_text(encoding="utf-8")
        self.assertLess(
            yaml.index("Stage link-check network guard"),
            yaml.index("Materialize PR additions only"),
        )
        self.assertIn('git show "origin/$GITHUB_BASE_REF:$guard"', yaml)
        self.assertLess(
            yaml.index("Install private-destination egress guard"),
            yaml.index("Run Lychee on CSV files"),
        )
        self.assertIn('bash "$RUNNER_TEMP/link-check-egress.sh" install', yaml)
        self.assertIn('bash "$RUNNER_TEMP/link-check-egress.sh" remove', yaml)
        self.assertIn("--exclude-all-private", yaml)
        self.assertIn("if: always()", yaml)
        self.assertIn("lycheeVersion: v0.24.2", yaml)
        self.assertIn("fail: false", yaml)

    def test_public_http_link_configuration_is_preserved(self):
        yaml = WORKFLOW.read_text(encoding="utf-8")
        for value in ("--method GET", "--timeout 15", "--extensions csv",
                      "--accept 200,202,204,400,401,403,405,429",
                      "output: lychee/out.json", "lychee-output-v2"):
            with self.subTest(value=value):
                self.assertIn(value, yaml)


if __name__ == "__main__":
    unittest.main()
