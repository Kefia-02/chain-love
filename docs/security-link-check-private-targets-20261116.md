# Link-check private target hardening — assessment (2026-11-16)

Scope: `.github/workflows/link-check-analysis.yaml` on upstream `main` at
`bf96e27932ae13600aeb68e07ab2fceb902df03d`, with Lychee v0.24.2.
No pull request was opened.

## Confirmed exposure and limits

- A PR author can add HTTP(S) URLs in CSV content. The analysis job checks additions
  only when a maintainer applies `check-links`; authorized users can also run it manually.
- Before this change, the job did not set any of Lychee's private/loopback/link-local
  exclusions. The v0.24.2 source defaults those filters to false.
- A direct request to a reachable non-public HTTP endpoint can be induced if its URL
  is included in a checked PR. Reachability and disclosure of any sensitive content
  on GitHub-hosted runners have **not** been demonstrated.
- The analysis job has `contents: read`, uses checkout with
  `persist-credentials: false`, and does not explicitly inject repository secrets.
  The Lychee action defaults its token input to the job's GitHub token;
  this is not proof of token disclosure. Reports expose results, not response bodies.

## Implemented partial mitigation

- Added `--exclude-all-private` to the existing v0.24.2 invocation, retaining
  public-link options and the default redirect behavior. This excludes ordinary
  literal RFC1918, localhost/loopback and link-local targets, including the literal
  cloud metadata address `169.254.169.254`.
- Added configuration regression tests, plus an optional live-binary test that only
  contacts a disposable local loopback HTTP server.

## Residual attack paths — DO NOT claim complete SSRF protection

Lychee v0.24.2 applies those filters to the supplied URL host before requesting,
not to DNS-resolved connection addresses. Its redirect policy follows redirects
without reapplying private-IP filtering to each hop. Its v0.24.2 source tests also
document a limitation for IPv4-mapped IPv6 addresses. Therefore, DNS aliases,
DNS rebinding, redirects to internal services, and unusual address encodings
are **not** covered by this change. An enforced outbound policy at connect time,
or an equivalently verified hardened client, is needed for a complete defense.

## Testing and coordination

- Locally, the configuration regression failed before the flag and passed after it.
  Public-link option checks passed in both cases.
- The runtime Lychee loopback test is skipped where the pinned binary is not
  installed; hosted CI and real Lychee behavior have not been verified for this branch.
- Upstream PR #5285 is open and edits the same workflow for an unrelated header
  parsing bug, so the branch must be rebased/reconciled before a future PR.
- PR #5276, #5292 and #5293 address report/artifact safety, comment permissions
  and display; no matching private-address protection was identified.
- Decision: **Hold submission.** This is useful defense-in-depth, not a
  demonstrated end-to-end SSRF fix or proven high-impact vulnerability.
