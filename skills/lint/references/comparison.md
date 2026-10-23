# Three-column comparison

Upstream: 구요한 (Yohan Koo) `cmds-llm-wiki` `/lint`, commit `54cf2ab` (Codex command is the baseline; the agent skill is its companion spec). The row labels identify every upstream check and section; this is the decision record, not a second runtime procedure. The procedure is written in this package's own words; no upstream file is copied.

| 구요한 (54cf2ab) | secondbrain lint | Decision + reason |
| --- | --- | --- |
| Prerequisite: read Core Context once per session | read once, plus live policy | Adopt; live policy wins where it defines a field, value or placement. |
| 1: Inventory Raw, Wiki, Queries, index.md, log.md | Step 1 | Adopt. |
| 2: Compare actual counts with index.md | Step 1 + Step 6 | Adopt; Stats recounted from folders. |
| 3: Orphan Wiki pages | Step 2 | Adopt; owner additions: whole vault as link source, uncompiled Raw reported apart, unlinked Entity-mention candidates. |
| 4: Broken wikilinks — create or remove | Step 3 | Adopt; add rename option and Inbox-candidate exception. Owner exception: quoted `author` wikilinks may stay unresolved and are not reported; no author note is created. |
| 5: Contradiction callouts, resolved by newer sources | Step 4 | Adopt; lint never removes a callout, possible resolution routed to `verify`. |
| 6: Low-confidence pages not updated 30+ days (date modified) | Step 5 | Adopt on `date_modified` (owner snake_case key); git age only as a marked fallback; `explored: false` shown as backlog. |
| Skill Step 6: Index Sync — missing/deleted entries, Stats | Step 6 Index Sync | Adopt the checks, plus Recent sections and `log.md` presence/recency. Adapt: reported, applied only as an owner-picked fix; git history does not replace index or log. |
| 7: MOC coverage | Step 7 | Adopt; hierarchy and collection-description judgments kept inline. |
| 8: Raw `collectionPurpose`, `mainVaultRelated`, `mainVaultCmds` | Step 8 | Adopt, with the "pre-v2 — consider backfill" label; add `referenced` on secondary Raw (owner exception: never proof the original was read). |
| 9: Wiki `mainVaultRelated`, `mainVaultCmds` | Step 8 | Adopt where live policy expects them. |
| 10: `explored` coverage; `exploredBy`/`exploredDate` completeness | Step 8 Exploration Gate | Adopt all three. |
| 11: v5 `claimType`, `evidenceScope`, `verificationStatus`, `verifiedAt`, `verifiedBy`, `disputed` | Step 8 verification fields | Adopt; value set checked; disputed → high-priority `verify` queue. |
| 12: Bias coverage — high confidence and synthesis guides, Counter-argument + Data gap | Step 8 Bias Check | Adopt. |
| 13: Cross-vault `mainVaultRelated` URLs and `mainVaultCmds` format | Step 10 | Adopt; owner rule: both URI components encoded with `quote(value, safe='')`, stat on mothership; `mainVaultCmds` must match a registered reference exactly. |
| Skill 10.3: candidates, read-only by default; `--fix-crossvault` | Step 10 + cross-vault fix mode | Adapt: fix mode only with explicit opt-in, patches only this vault's Raw/Wiki references, diff and OK per batch of at most ten; never writes the mothership. |
| 14: Attachment paths | Step 8 | Adopt; location from live policy. |
| 15: Core Context `snapshot_date` vs mothership system files | Step 9 | Adopt; the file set is the one Core Context was built from, not a fixed list. |
| 16: Persona health (v6.3) | Step 8 Persona health | Adopt all items; owner addition: no Persona leak into shared pages. |
| — (no policy-drift check) | Step 11 Live Policy Conformance + policy conformance fixes | Owner addition: notes written under an older policy or by a writer still on it are reported against the live policy (placement incl. Entity subtype folders, Entity identity, kind values, retired keys, duplicate spellings, kept old values) and grouped by recorded provenance; fixes only as owner-picked batches with outside-vault copies, a changed-note check, no overwrite or merge, unchanged bodies, and link updates after moves. |
| Output: Stats … Recommended fixes by impact and effort | Output 1–13 | Adopt; add Not checked (a skipped step is a limit). Owner rule: full report preserved; display truncation states the count and where the full list is. |
| (implicit) Index Sync edits during lint | report-first | Keep owner rule: a lint run writes nothing (no log entry); owner-picked fixes with diff per ten, read-back, one `log.md` entry after applied fixes; no automatic commit. |
