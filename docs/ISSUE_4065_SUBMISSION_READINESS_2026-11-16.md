# Issue #4065 — Submission readiness and release grouping (2026-11-16 JST)

**Decision: HOLD bulk submission.** The candidate data is structurally valid, but not yet independently verified for all provider-specific Enterprise and Archive entitlements. No additional PRs should be opened automatically. This is a review plan, not a claim of reward eligibility.

## Existing submission
- [PR #5364](https://github.com/Chain-Love/chain-love/pull/5364) covers **1RPC only**: 39 network-specific rows (33 network folders), one removed global row. Open and independent from this branch.
- The work branch `work/global-evm-rpc-remaining42-20261116` covers the **other 42 canonical offers** from **28 providers**. It changes **31 network CSVs**, adds **215 scoped rows**, and removes **42 global rows**. It also contains a defensive validation script, four tests, workflow wiring, and evidence/audit notes.
- The 43 figure counts **global CSV listing records**, not separate GitHub Issues or service providers.
- [CI run #43789775418](https://github.com/Kefia-02/chain-love/actions/runs/43789775418) successfully ran CSV validation, CSV-to-JSON generation, four scope tests, and JSON validation for **138 network exports**. Changes after that run were to documentation and checkout configuration; data additions/deletions were unchanged. Rerun CI on the final PR head.

## Confirmed 2026-11-16 bounty rules
- [Official discussion #41](https://github.com/Chain-Love/chain-love/discussions/41) limits the bounty PR size to **100 code lines and/or 200 edited cells**.
- Current named reward-scope networks: **Algorand, Filecoin, and Fuse** (Somnia and Avalanche ended Nov 1). Non-target network PRs are accepted but do not automatically qualify for rewards.
- **None of the 215 added network-specific rows is for Algorand, Filecoin, or Fuse.** Consequently, no reward should be projected for those added data rows under the current listed-network rule. An approved exception or other compensation, if any, must come from maintainers.
- The published quality gateway penalizes invalid links, nonexistent providers, unsupported networks, and unsupported claimed plans. Passing schema/CI does not establish product or paid-plan entitlement.

## Four balanced *data-only* grouping options (not yet separate branches or PRs)

These are possible review batches **only if maintainers want multiple capped contributions**. Group by entire provider, keeping each provider's global removals with its scoped replacements. Each row typically changes the nonempty fields `slug`, `offer`, `chain` on addition and `slug`, `offer` on deletion.

| Candidate batch | Providers | Added scoped rows | Removed global rows | Total diff CSV lines | Estimated nonempty edited cells |
| --- | --- | ---: | ---: | ---: | ---: |
| A | Alchemy, Tatum, BlockPi, Sentio, InfStones, RPCFast | 54 | 9 | 63 | 180 |
| B | Spectrum, Ankr, WatchData, Uniblock, Tenderly, NodeReal, Validation Cloud | 54 | 11 | 65 | 184 |
| C | Dwellir, Nodit, Thirdweb, Omnia, RadiumBlock, Infura, Ginco | 54 | 10 | 64 | 182 |
| D | AllThatNode, Crypto APIs, SpeedyNodes, Blockdaemon, dRPC, BlockEden, BlockVision, OnFinality | 53 | 12 | 65 | 183 |
| **Total** | 28 providers | **215** | **42** | **257** | **729** |

**Edited-cell counts are conservative, nonempty-field estimates rather than the maintainers' confirmed counting method.** Extra code, tests, or documentation cannot be added freely to these batches without rechecking the size cap. Batches are not approved or independently verified just because they fit the numerical cap.

The scope guard **cannot be merged before all legacy global EVM RPC rows have been removed**: otherwise it intentionally fails the existing data. The current guard + tests + workflow additions exceed 100 code lines as one standalone data-bounty PR; reduce and separately review, or request maintainer approval for an exception, before submission. Four data PRs **plus** a guard PR would add five more PRs to the contributor's backlog. With no clear data-bounty eligibility, do not create these merely to increase PR counts.

## Factual source and plan verification still required

All 215 candidate rows resolve an existing canonical `!offer:` reference, match the branch's per-provider scope table, and passed full CSV/JSON CI. **They are not all verified against product-specific commercial terms.** Treat the 42/42 metric as candidate coverage, not proof of provider support on every claimed network/plan.

Priority rechecks before any publication:

1. **Enterprise/Archive scope** — distinguish provider network support from paid-plan/Archive historical-state capability. Especially Alchemy archive, Dwellir archive, Tatum business archive, Sentio enterprise archive, BlockVision archive, and Validation Cloud private archive.
2. **Product mismatch risk** — Crypto APIs docs describe shared and dedicated NaaS rather than the exact canonical Enterprise plan; RPCFast docs confirm self-hosted archive nodes on ETH/BNB but not the exact enterprise catalog offer; AllThatNode's cited MCP docs show networks but do not establish its Business Archive tier.
3. **Insufficient or indirect citation** — InfStones source is a terms page with platform links, NodeReal citation is only an introduction, Sentio supported-network URL redirects beyond available verification; WatchData docs establish supported networks but do not by themselves prove an Enterprise EVM JSON-RPC contract.
4. **Network semantics** — ensure EVM JSON-RPC for each specific chain (e.g. Flow EVM versus native Flow, Hyperliquid EVM versus native API) and do not copy native/Cosmos/Move API support to an EVM offer.

First-party examples reviewed:
- [Alchemy supported chain endpoints](https://www.alchemy.com/docs/reference/node-supported-chains)
- [SpeedyNodes full and archive network matrix](https://docs.speedynodes.com/networks/overview/)
- [Crypto APIs JSON-RPC supported networks](https://developers.cryptoapis.io/v-2.2-176/JSON-RPC/general-information/overview)
- [RPCFast archive nodes](https://docs.rpcfast.com/self-hosted-cluster/archive-nodes)
- [Nodit feature support by chain](https://developer.nodit.io/en/chains/supported-chains/)
- [OnFinality EVM endpoints](https://onfinality.io/en/networks)
- [Official reward, quality, and size policy](https://github.com/Chain-Love/chain-love/discussions/41)

## Recommended next move

**Do not append all 42 provider fixes to PR #5364**; it would exceed the published cap and expand review scope materially. Retain the consolidated patch as a tested draft, keep PR #5364 unchanged and awaiting maintainer response, and seek maintainer guidance on one coordinated non-bounty migration / explicit size exception rather than posting 4–5 additional unsolicited PRs. If maintainers ask for small batches, use the group sizes above, reverify each provider, and rerun CI for each proposed PR. Do not claim or estimate a payout from this batch.

**Nothing in this document authorizes additional PR creation, paid use, or provider registration.**
