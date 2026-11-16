# Issue #4065 — Global EVM RPC migration audit

**Status:** candidate work branch only, **not** an approved or submitted full fix. Existing PR #5364 is unchanged.

## Scope and count definitions

- One issue: #4065, concerning indiscriminate inheritance of network-limited EVM JSON-RPC API offers.
- Original audit: 43 global CSV records, across 29 providers. The first provider (1RPC, one record) was submitted separately in PR #5364.
- This batch: the other 42 former global CSV records, across 28 providers.
- Network-specific replacement candidates: **215 rows** for **42 of 42** original records.
- **Four previously unscoped offers were additionally mapped**: two Crypto APIs enterprise plan records, RPCFast archive and Sentio archive. Coverage candidates now exist for all 42 source records. Provider documentation and existing network-specific offer rows support the chains; exact paid plan entitlement remains to be verified.

The evidence table below is a **scope audit, not proof of individual Enterprise / Archive plan entitlement or live endpoint availability**. A network must have vendor evidence plus another pre-existing chain-specific EVM JSON-RPC row from the same provider; a full-archive claim also needs pre-existing Archive metadata. Network folders without evidence were not populated. The whitelist itself requires provider-by-provider human scrutiny before merge.

## Results by original record

| Source record | Provider | Scoped rows | Vendor reference | Status |
| --- | --- | ---: | --- | --- |
| `alchemy-enterprise-full-archive` | Alchemy | 9 | [documentation](https://www.alchemy.com/docs/reference/node-supported-chains) | Candidate; plan review required |
| `alchemy-enterprise-recent-state` | Alchemy | 24 | [documentation](https://www.alchemy.com/docs/reference/node-supported-chains) | Candidate; plan review required |
| `allthatnode-business-full-archive` | AllThatNode | 7 | [documentation](https://docs.allthatnode.com/docs/model-context-protocol) | Candidate; plan review required |
| `allthatnode-business-recent-state` | AllThatNode | 7 | [documentation](https://docs.allthatnode.com/docs/model-context-protocol) | Candidate; plan review required |
| `ankr-enterprise-full-archive` | Ankr | 13 | [documentation](https://www.ankr.com/docs/rpc-service/chains/chains-list/) | Candidate; plan review required |
| `blockdaemon-enterprise-full-archive` | Blockdaemon | 5 | [documentation](https://docs.blockdaemon.com/reference/rpc-api-overview) | Candidate; plan review required |
| `blockeden-enterprise-full-archive` | BlockEden | 1 | [documentation](https://blockeden.xyz/docs/intro/) | Candidate; plan review required |
| `blockeden-enterprise-recent-state` | BlockEden | 1 | [documentation](https://blockeden.xyz/docs/intro/) | Candidate; plan review required |
| `blockpi-enterprise-full-archive` | BlockPi | 2 | [documentation](https://public.blockpi.io/) | Candidate; plan review required |
| `blockpi-enterprise-recent-state` | BlockPi | 3 | [documentation](https://public.blockpi.io/) | Candidate; plan review required |
| `blockvision-enterprise-full-archive` | BlockVision | 2 | [documentation](https://docs.blockvision.org/reference/welcome-to-blockvision) | Candidate; plan review required |
| `crypto-apis-enterprise-full-archive` | Crypto APIs | 7 | [NaaS supported networks](https://developers.cryptoapis.io/v-2.2-176/JSON-RPC/general-information/overview) | Candidate; enterprise archive entitlement review required |
| `crypto-apis-enterprise-recent-state` | Crypto APIs | 7 | [NaaS supported networks](https://developers.cryptoapis.io/v-2.2-176/JSON-RPC/general-information/overview) | Candidate; enterprise plan review required |
| `drpc-enterprise-recent-state` | dRPC | 3 | [documentation](https://drpc.org/docs/pricing/compute-units) | Candidate; plan review required |
| `dwellir-enterprise-full-archive` | Dwellir | 7 | [documentation](https://www.dwellir.com/docs) | Candidate; plan review required |
| `dwellir-enterprise-recent-state` | Dwellir | 10 | [documentation](https://www.dwellir.com/docs) | Candidate; plan review required |
| `ginco-enterprise-recent-state` | Ginco | 1 | [documentation](https://ginco.com/nodes) | Candidate; plan review required |
| `infstones-enterprise-full-archive` | InfStones | 1 | [documentation](https://infstones.com/terms/terms-and-conditions) | Candidate; plan review required |
| `infstones-enterprise-recent-state` | InfStones | 1 | [documentation](https://infstones.com/terms/terms-and-conditions) | Candidate; plan review required |
| `infura-enterprise-full-archive` | Infura | 1 | [documentation](https://docs.infura.io/get-started/endpoints/) | Candidate; plan review required |
| `infura-enterprise-recent-state` | Infura | 1 | [documentation](https://docs.infura.io/get-started/endpoints/) | Candidate; plan review required |
| `node-real-semita-full-archive` | NodeReal | 1 | [documentation](https://docs.nodereal.io/docs/intro-nodereal) | Candidate; plan review required |
| `node-real-semita-recent-state` | NodeReal | 1 | [documentation](https://docs.nodereal.io/docs/intro-nodereal) | Candidate; plan review required |
| `nodit-enterprise-full-archive` | Nodit | 7 | [documentation](https://developer.nodit.io/en/chains/supported-chains/) | Candidate; plan review required |
| `nodit-enterprise-recent-state` | Nodit | 7 | [documentation](https://developer.nodit.io/en/chains/supported-chains/) | Candidate; plan review required |
| `omnia-enterprise-recent-state` | Omnia | 5 | [documentation](https://docs.omniatech.io/rpc-api-docs/chains) | Candidate; plan review required |
| `onfinality-enterprise-full-archive` | OnFinality | 1 | [documentation](https://onfinality.io/en/networks) | Candidate; plan review required |
| `radiumblock-enterprise-recent-state` | RadiumBlock | 3 | [documentation](https://radiumblock.com/pricing.html) | Candidate; plan review required |
| `rpcfast-enterprise-full-archive` | RPCFast | 2 | [Archive nodes (ETH/BNB)](https://docs.rpcfast.com/self-hosted-cluster/archive-nodes) | Candidate; contract entitlement review required |
| `sentio-enterprise-full-archive` | Sentio | 4 | [supported networks](https://docs.sentio.xyz/docs/supported-network) | Candidate; enterprise archive entitlement review required |
| `spectrum-custom-full-archive` | Spectrum | 8 | [documentation](https://spectrumnodes.com/docs/api-reference) | Candidate; plan review required |
| `spectrum-custom-recent-state` | Spectrum | 8 | [documentation](https://spectrumnodes.com/docs/api-reference) | Candidate; plan review required |
| `spectrum-custom-trace` | Spectrum | 8 | [documentation](https://spectrumnodes.com/docs/api-reference) | Candidate; plan review required |
| `speedynodes-enterprise-full-archive` | SpeedyNodes | 4 | [documentation](https://docs.speedynodes.com/networks/overview/) | Candidate; plan review required |
| `speedynodes-enterprise-recent-state` | SpeedyNodes | 8 | [documentation](https://docs.speedynodes.com/networks/overview/) | Candidate; plan review required |
| `tatum-business-full-archive` | Tatum | 8 | [documentation](https://docs.tatum.io/docs/supported-blockchains) | Candidate; plan review required |
| `tenderly-enterprise-recent-state` | Tenderly | 3 | [documentation](https://tenderly.co/products/node) | Candidate; plan review required |
| `thirdweb-pro-recent-state` | Thirdweb | 12 | [documentation](https://thirdweb.com/rpc) | Candidate; plan review required |
| `uniblock-enterprise-custom` | Uniblock | 5 | [documentation](https://uniblock.dev/) | Candidate; plan review required |
| `validation-cloud-private-full-archive` | Validation Cloud | 1 | [documentation](https://www.validationcloud.io/post/archive-nodes-powering-web3-data-access-and-historical-analysis) | Candidate; plan review required |
| `watchdata-custom-full-archive` | WatchData | 3 | [documentation](https://docs.watchdata.io/) | Candidate; plan review required |
| `watchdata-custom-recent-state` | WatchData | 3 | [documentation](https://docs.watchdata.io/) | Candidate; plan review required |

## Regression checks

- Global `all-networks/apis.csv` has no canonical `RPC + EVM JSON-RPC` rows after candidate migration.
- Changed network CSVs were reread (30 files): 26 fields per row, slug-sorted, no duplicate slugs.
- Four focused Python scope-guard unit tests were executed successfully in an isolated local reconstruction. The candidate branch itself has not run GitHub Actions CI; CI has succeeded only for the earlier PR #5364.
- Full export and schema validation across all network outputs **has not been run**. No claim of complete CI approval or live enterprise verification.

## Remaining verification gates

- The 42 source records all have a replacement candidate, but **contract-specific availability of Enterprise and Archive modes is not established** by each provider's public network list. Maintainership review is required.
- Validate full CSV-to-JSON generation and output schema for all networks. It has **not** been run on this work branch.
- Check provider-specific EVM vs native RPC semantics for every added listing; a generic supported blockchain does not prove an EVM JSON-RPC service on that chain.
- GitHub Database Population Program [limits each PR to 100 lines of code and/or 200 edited cells](https://github.com/Chain-Love/chain-love/discussions/41). This batch is over the stated limit as one PR and should **not** be appended blindly to #5364 if pursuing bounty eligibility.
- One unrelated Arbitrum CSV URL quoting change introduced by automated rewriting was restored to the upstream original.

## Sources for the final four

- Crypto APIs: [NaaS supported networks](https://developers.cryptoapis.io/v-2.2-176/JSON-RPC/general-information/overview), plus [its Ethereum nodes and archive explanation](https://cryptoapis.io/blog/99-ethereum-full-nodes-vs-archive-nodes).
- RPCFast: [Archive Nodes on Ethereum and BNB Chain](https://docs.rpcfast.com/self-hosted-cluster/archive-nodes).
- Sentio: [Supported networks](https://docs.sentio.xyz/docs/supported-network) and existing free/pay-as-you-go Archive rows in the repo (provider-side specific Enterprise Archive terms still unverified).

Data and automated candidate generation were AI-assisted. No paid endpoint was accessed, and no new PR was opened. Submit only after full CI plus approval of scope and plan claims.

## Full CI validation (2026-11-16)

The candidate branch was tested with GitHub Actions run [#43789775418](https://github.com/Kefia-02/chain-love/actions/runs/43789775418), commit `54ab3c38663f355783db5b7e80119cd3efd30318`. **Conclusion: success.** The successful job ran:

1. Four Python regression tests for global EVM JSON-RPC scoping (all passed).
2. `check-global-api-scope.py` (passed).
3. `validate_csv.py` (passed).
4. `csv_to_json.py` (passed).
5. `validate.py` over **138 network JSON files** (passed).

The CI-only temporary push trigger was removed from the work branch after the successful run; normal upstream pull-request-triggered validation remains configured. The tool checkout was explicitly set to the upstream `Chain-Love/chain-love` `json-tools` branch, because the contributor fork lacks that branch.

**CI proves structural and schema validity, not factual correctness of each provider's Enterprise/Archive entitlements.**
