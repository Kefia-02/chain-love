#!/usr/bin/env python3
"""Reject global EVM JSON-RPC listings that would be copied to unsupported networks.

Provider and offer definitions remain canonical. Scope EVM RPC offers through
listings/specific-networks/<network>/apis.csv instead of all-networks/apis.csv.
"""
from __future__ import annotations

import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, strict=True))


def find_unscoped_evm_rpc(root: Path) -> list[str]:
    offers_path = root / "references/offers/apis.csv"
    listings_path = root / "listings/all-networks/apis.csv"
    offers = {row["slug"]: row for row in read_csv(offers_path)}
    errors = []
    for index, row in enumerate(read_csv(listings_path), start=2):
        ref = (row.get("offer") or "").strip()
        canonical = offers.get(ref[len("!offer:"):], {}) if ref.startswith("!offer:") else {}
        api_type = (row.get("apiType") or "").strip() or canonical.get("apiType", "")
        technology = (row.get("technology") or "").strip() or canonical.get("technology", "")
        if api_type == "RPC" and technology == "EVM JSON-RPC":
            errors.append(
                f"{listings_path}: row {index}, slug '{row.get('slug')}': "
                f"EVM JSON-RPC must be scoped to verified specific networks "
                f"(offer '{ref or 'inline'}')"
            )
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    errors = find_unscoped_evm_rpc(root)
    if errors:
        print("\n".join(errors))
        return 1
    print("Global API scope check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
