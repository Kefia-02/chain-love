"""Focused regressions for global API EVM JSON-RPC scope."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/check-global-api-scope.py"
spec = importlib.util.spec_from_file_location("check_global_api_scope", MODULE_PATH)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class GlobalAPIScopeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "references/offers").mkdir(parents=True)
        (self.root / "listings/all-networks").mkdir(parents=True)
        (self.root / "references/offers/apis.csv").write_text(
            "slug,apiType,technology\n"
            "evm-rpc,RPC,EVM JSON-RPC\n"
            "indexed-data,Data,REST\n",
            encoding="utf-8",
        )

    def set_global(self, data):
        (self.root / "listings/all-networks/apis.csv").write_text(
            "slug,offer,apiType,technology\n" + data, encoding="utf-8"
        )

    def test_rejects_canonical_evm_rpc(self):
        self.set_global("bad,!offer:evm-rpc,,\n")
        errors = guard.find_unscoped_evm_rpc(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("bad", errors[0])

    def test_rejects_inline_evm_rpc(self):
        self.set_global("bad,,RPC,EVM JSON-RPC\n")
        self.assertEqual(len(guard.find_unscoped_evm_rpc(self.root)), 1)

    def test_permits_other_network_agnostic_apis(self):
        self.set_global("good,!offer:indexed-data,,\n")
        self.assertEqual(guard.find_unscoped_evm_rpc(self.root), [])

    def test_permits_empty_global_list_with_specific_rpc(self):
        self.set_global("")
        network = self.root / "listings/specific-networks/ethereum"
        network.mkdir(parents=True)
        (network / "apis.csv").write_text(
            "slug,offer,chain\nrpc-mainnet,!offer:evm-rpc,mainnet\n",
            encoding="utf-8",
        )
        self.assertEqual(guard.find_unscoped_evm_rpc(self.root), [])


if __name__ == "__main__":
    unittest.main()
