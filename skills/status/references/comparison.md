# Three-column comparison

Upstream: 구요한 `/status`, Codex command at commit `54cf2ab` (baseline; the agent wrapper delegates to it). One row per upstream step or section; this is the decision record, not a second procedure.

| 구요한 (54cf2ab) | secondbrain status before this revision | Decision + reason |
| --- | --- | --- |
| 1. Read `index.md` stats | no index; counts were the stats | Restore; missing `index.md` reported missing. |
| 2. Last 5 relevant entries from `log.md` | `git log -5` as proxy | Restore: `log.md` only; Git is not a proxy; missing `log.md` reported. |
| 3. Count Raw Sources, Wiki subfolders, Maps, Queries, Paper Analyses (citekey folders), Inbox | per-area counts, hubs vs files, Inbox >30 days | Adopt; owner keeps hubs vs files and Inbox age. Questions/Paper Analyses the vault lacks reported `absent` with reason, empty = 0, untaken = `unknown`. Upstream does not count Questions (RQ cards) separately; this package lists them under Wiki subfolders. |
| 4. `collectionPurpose` coverage in Raw | coverage + inferred/unknown | Adopt; delegated inferences counted from `collectionPurpose`; an existing `purpose_origin` is read as it is, never written. |
| 5. `mainVaultRelated` coverage | coverage, "not applicable" without mothership | Adopt. |
| 6. `explored` coverage | presence + false backlog, Bias Check count | Adopt; adds true ratio over Concepts/Entities/Guides. |
| 7. `verificationStatus` coverage | absent | Restore coverage; adds breakdown verified/partial/unverified/disputed/invalid and `confidence` breakdown per frozen schema (upstream gives coverage only). |
| 8. Core Context `snapshot_date` | snapshot age with git fallback | Adopt; git fallback removed (missing = `unknown`). |
| 9. Index drift vs actual counts | no index drift | Restore, plus stale Recent entries. |
| Output block (no Recent Activity, Issues `...`) | block with "last 5 commits" | Adapt: upstream fields plus MOCs, Papers, breakdowns; Recent Activity from `log.md` (step 2 output, which upstream's block omits); Issues routed to owning skills. Removed filed-back ratio (not upstream). |
| (implicit) read-only | read-only | Adopt explicitly: writes nothing, including no `log.md` entry. |
