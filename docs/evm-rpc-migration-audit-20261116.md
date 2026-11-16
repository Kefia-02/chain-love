# Issue #4065 — Global EVM RPC migration audit

**Status:** candidate work branch only, **not** an approved or submitted full fix. Existing PR #5364 is unchanged.

## Scope and count definitions

- One issue: #4065, concerning indiscriminate inheritance of network-limited EVM JSON-RPC API offers.
- Original audit: 43 global CSV records, across 29 providers. The first provider (1RPC, one record) was submitted separately in PR #5364.
- This batch: the other 42 former global CSV records, across 28 providers.
- Network-specific replacement candidates: **195 rows** for **38 of 42** original records.
- **4 offers** had no defensible network-specific replacement in the candidate; they were removed from global listings but are not reintroduced. Do not merge until this coverage impact is explicitly reviewed.

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
| `crypto-apis-enterprise-full-archive` | Crypto APIs | 0 | [documentation](https://cryptoapis.io/) | Unverified: do not publish |
| `crypto-apis-enterprise-recent-state` | Crypto APIs | 0 | [documentation](https://cryptoapis.io/) | Unverified: do not publish |
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
| `rpcfast-enterprise-full-archive` | RPCFast | 0 | [documentation](https://docs.rpcfast.com/rpc-fast-saas-evm/pricing-and-plans.md) | Unverified: do not publish |
| `sentio-enterprise-full-archive` | Sentio | 0 | [documentation](https://docs.sentio.xyz/docs/readme) | Unverified: do not publish |
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
- Four focused Python unit tests for the newly added global scope guard passed. The guard also protects pull-request and release workflows.
- Full export and schema validation across all network outputs **has not been run**. No claim of complete CI approval or live enterprise verification.

## Handling of unverified offers

- `crypto-apis-enterprise-full-archive` — canonical provider Crypto APIs; source product/chain evidence insufficient.
- `crypto-apis-enterprise-recent-state` — canonical provider Crypto APIs; source product/chain evidence insufficient.
- `rpcfast-enterprise-full-archive` — canonical provider RPCFast; source product/chain evidence insufficient.
- `sentio-enterprise-full-archive` — canonical provider Sentio; source product/chain evidence insufficient.

This document was prepared using AI-assisted code and documentation comparison. Do not treat published vendor chain lists alone as proof of every paid plan or Archive mode. Keep batch separate from PR #5364 until acceptance criteria and a full validator run can be met.
