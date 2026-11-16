# ChainLove link-check SSRF: verified isolated GitHub Actions behavior (2026-11-16)

## Result

The GitHub-hosted Ubuntu runner executed the actual pinned lychee v0.24.2 binary.
All HTTP requests were to disposable 127.0.0.1 Python HTTP servers on that runner.
Input was a CSV file and `--extensions csv .`, mirroring the production link-check.
The job was run only in the personal fork; no upstream PR or third-party target was contacted.

Successful test run: https://github.com/Kefia-02/chain-love/actions/runs/43836985762
Commit: bf3d716dbea663068ba837fd8b2135cbcf9e9c25

The job log confirms:

- `lychee 0.24.2`
- `BASELINE_GET=PASS`
- `LITERAL_LOOPBACK_BLOCK=PASS`
- `DNS_ALIAS_BYPASS=CONFIRMED_IN_ISOLATED_TEST`
- `REDIRECT_TO_LOOPBACK_BYPASS=CONFIRMED_IN_ISOLATED_TEST`
- `AUTHORIZATION_HEADER_TO_ARBITRARY_LOCAL_TARGET=NOT_OBSERVED`

The DNS aliases were pinned to 127.0.0.1 via the disposable runner's /etc/hosts
and checked before contacting them. The redirected target was another disposable
loopback server. No real internal/cloud metadata endpoints, secrets, or credentials
were read, logged or exfiltrated.

## Scope / interpretation

The current upstream ChainLove workflow invokes lychee v0.24.2 without the
`--exclude-all-private` flag, so its exposed URL surface is broader than the
partially hardened fork branch.

The isolated test demonstrates actual URL-filter bypass on a GitHub-hosted
runner *even with* `--exclude-all-private` for DNS aliases and redirects.
It does **not** demonstrate access to any pre-existing internal service,
cloud metadata service, authenticated API, or secret of ChainLove.

The Lychee action passes the job token to Lychee for GitHub API calls, but
the loopback servers did not observe an Authorization HTTP header.
The production report renders URL and status/error counts; it does not render
HTTP response bodies. The job uses `contents: read`, does not explicitly pass
secrets, and has checkout `persist-credentials: false`.

Conclusions: SSRF primitive / internal GET reachability is confirmed in a
controlled environment. Material information leakage, privilege escalation,
or unauthorized operations on ChainLove infrastructure remain **unproven**.

## Practical decision

Do not claim credential theft, data disclosure or major impact without further
evidence. Do not submit an upstream security PR as a complete fix based on the
existing `--exclude-all-private` single-line mitigation: it does not cover
the confirmed DNS/redirect bypass paths. No upstream PR was created.

Earlier attempted runs used direct-URL input (not matching production) and
reserved `.test` domains (excluded as example domains by Lychee) and were
superseded by the successful CSV-based isolated test above.
