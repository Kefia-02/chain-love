# Proposed PR title

data: fix Algorand Nansen link and add Fuse AI API

# PR body

## Submission hold

**This combined change is not ready for upstream submission.** Fuse is absent from `references/providers/providers.csv`, and its provider logo is not registered in upstream main. Official JSON generation fails with:

```text
ValueError: Provider 'Fuse' is missing in references/providers/providers.csv.
```

Provider/logo work is already open in upstream #5005 and #5034; #5291 also proposes a Fuse provider for native RPC listings. Do not duplicate that registration. After a compatible provider and logo merge, rebase this combined branch and rerun full generation and schema validation.

## Summary

Prepare two independently scoped data changes in one patch:

1. **Algorand / Nansen:** remove the listing-specific Token God Mode URL that selects `chain=hyperliquid` for ALGO. The existing `!offer:nansen` reference inherits the canonical `https://app.nansen.ai` dashboard.
2. **Fuse AI API:** add the official pay-per-request REST API as a canonical offer plus a Fuse-mainnet listing. The data and on-chain-action network is Fuse mainnet (122); observed x402 settlement is USDC on Base mainnet (8453).

## Type of change

- [x] Add data rows
- [x] Update data rows
- [ ] Remove data rows
- [ ] Schema change
- [ ] Documentation/metadata only

## Scope

Exactly three CSV files:

- `listings/specific-networks/algorand/analytics.csv`: one `actionButtons` cell cleared.
- `references/offers/apis.csv`: one `fuse-ai-pay-per-request` row added.
- `listings/specific-networks/fuse/apis.csv`: one `fuse-ai-pay-per-request-mainnet` row added, inheriting the canonical offer.

No provider or logo duplication, and no unrelated dataset changes.

The Fuse offer follows the API column definitions: `apiType=Custom`, `technology=REST`, `historicalData=Pruned`, `planType=Pay-As-You-Go`, and two official action buttons. The owner-claim `address` cell remains empty.

## Primary sources and URL checks

Verified by automated tooling on 2026-11-17 JST:

- [Nansen supported chains](https://docs.nansen.ai/reference/chains): Algorand and Hyperliquid have different identifiers. The page also schedules Algorand API retirement for 2026-11-25.
- [Canonical Nansen dashboard](https://app.nansen.ai): direct GET returned HTTP 200. The old deep link also returned application HTML; the bug is its network selection, not an HTTP-error claim.
- [Fuse official source](https://github.com/fuseio/ai/blob/ad066a041bb25f783c7cd0aa40421df854a00267/README.md), including the same revision's API routing, discovery, and configuration.
- [Fuse live OpenAPI](https://ai.fuse.io/openapi.json): HTTP 200, OpenAPI 3.1.0, six paid operations.
- [Fuse health](https://ai.fuse.io/health): HTTP 200 with `status=ok`.
- Unpaid GET `https://ai.fuse.io/api/fuse/stats`: HTTP 402, with an x402 Base-mainnet USDC challenge for $0.01.

| Method | Path | USD per request |
| --- | --- | --- |
| GET | `/api/fuse/stats` | $0.01 |
| GET | `/api/fuse/wallet/{address}` | $0.05 |
| GET | `/api/fuse/defi/opportunities` | $0.10 |
| POST | `/api/fuse/loyalty/create` | $5.00 |
| POST | `/api/fuse/loyalty/mint` | $0.50 |
| GET | `/api/fuse/loyalty/balance/{token}/{address}` | $0.02 |

No payments, signed authorizations, deployments, or minting were performed. MPP discovery was observed, but successful paid execution of its rails is not asserted by the listing.

[Official URL-check log](https://github.com/Kefia-02/chain-love/actions/runs/43965667902)

## Validation

Combined source commit: `ae813326d80733b13c8605f199861ab4954f4a44`
Checked upstream main: `bf96e27932ae13600aeb68e07ab2fceb902df03d`
Unmodified official json-tools: `4e979403c3eef6fdfcd7f5d6cf4ae25f6254aa2b`

- `python validate_csv.py`: **passed**.
- Strict CSV shape/order/unique-slug checks: **passed**. Algorand analytics: 46 rows / 14 columns. API offers: 402 rows / 25 columns. Fuse API listings: 3 rows / 26 columns.
- Official offer resolution and normalization for both changed listings: **passed**.
- Both isolated hydrated rows validated against their official category JSON schemas: **passed**.
- Nansen inherits `["[Dashboard](https://app.nansen.ai)"]`; the Hyperliquid override is absent.
- `python test_action_buttons_max.py`: **all 10 existing tests passed**.
- `python csv_to_json.py`: **failed**, missing Fuse provider.
- Full generated-JSON `python validate.py`: **not run**, since generation failed.
- Independent provider-resolution check reproduces the same missing-Fuse-provider blocker.
- GitHub comparison confirms exactly three changed files, one commit ahead of checked upstream main and zero behind.

[Combined validation run](https://github.com/Kefia-02/chain-love/actions/runs/43971253346)

The Nansen-only source was also tested separately through the full generation/schema pipeline and passed. Combining it with the pending Fuse addition makes the **whole combined submission wait** for the Fuse provider dependency.

## Duplicate check and contributor disclosure

The earlier preparation checked current main, open-PR metadata, and related patches. No equivalent Nansen listing-cell fix or Fuse AI offer was found. Fuse MCP/native RPC registrations are separate products; provider/logo registrations are dependencies.

Prepared with AI assistance. Checks above were automated. No personal verification, repository-star status, wallet ownership, or payment success is claimed on behalf of the account holder.

## Preparation state

Source branch: `Kefia-02:prep/nansen-fuse-ai-api-20261117`.
Intended eventual base: `Chain-Love/chain-love:main`.

**Branch and PR text only. No combined PR or Draft PR exists, and no upstream submission was made.** Existing individual fork-only drafts remain separate reference material. Choose the combined submission instead of submitting the same changes individually when the dependency is resolved.
