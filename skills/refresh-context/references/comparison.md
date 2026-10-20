# Three-column comparison

Upstream: 구요한 `/refresh-context`, commit `54cf2ab` (Codex command; Claude variant for Step 6 entry fields). One row per upstream step or section; this is the decision record, not a second procedure.

| 구요한 (54cf2ab) | secondbrain refresh-context before this revision | Decision + reason |
| --- | --- | --- |
| Intro: Core Context is a 시점 snapshot | dated snapshot of the owner | Adopt his term and §1–§5 section map; owner adds "sources stay the truth" and the derived-file location from AGENTS. |
| When to Run: lint/status 30 days or drift; mothership major version; new essay → §4; axes change; §1 continuity | when to run list | Adopt all five triggers; owner adds staleness against a listed source change and "old but unchanged → date check only". |
| Step 1 Load Current Core Context | load snapshot | Adopt; also read `version` and `source`. |
| Step 2 Re-read mothership system files (Codex lists 9 fixed paths) | mothership re-read + git log | Adapt (owner exception): read only the files the Core Context registers, no fixed count; Claude variant's four captures adopted; owner adds `git -C … log --since`, read-only, missing mothership reported and run continues. |
| Step 3 (옵션) Re-Read Personal Essays; new essays last 60 days via `find … -mtime -60 \| head -10` | re-read sources + new essays as candidates | Adopt; drop `head -10` cap; owner adds candidates-not-sources and no guessing from folder names. |
| Codex step 4: "Scan recent Permanent Notes for major philosophy drift" (Claude variant has no such step) | essays in `source` only | Restore from Codex: Step 3-b scans the Permanent Notes folder Core Context registers (upstream `30. Permanent Notes/`), window 60 days taken from the Claude essay scan since Codex says only "recent"; evidence for the diff, not new `source` entries. |
| (absent in both) Raw frontmatter rules | §6 Raw keys incl. `reusableFor`, keep `purpose_origin` | Remove: neither upstream refresh-context says anything about Raw frontmatter; that belongs to `ingest`. |
| Step 4 Diff & Propose: side by side, new essays one line, "전체 / 부분 / 거부" | section diff with source line | Adopt the three-way ask verbatim; 거부 writes nothing, not even log; axes = those registered in §2 (owner exception, not a fixed 7); stack traceability, keep owner wording, axes owner-defined with downstream-shift warning. |
| Step 5 Apply: update sections, `snapshot_date`, `date modified`, version minor/major, `source` | apply on OK, byte-for-byte rest | Adopt; `date modified` → `date_modified`; owner adds untouched sections byte-for-byte and read-back. |
| Step 6 Log: append to `log.md` (`update \| Core Context refreshed`, drift, essays, sections, why) | git commit message | Restore: append-only `log.md` entry with his fields when writes were approved; Git never replaces it; no commit/push unless the owner asks separately. |
| Output: age, changes, essays, version | report 1–5 | Adopt + mothership drift line. |
| allowed-tools incl. qmd | rg, qmd, git | Adapt: tools in one line. |
| (absent) | boundaries | Owner addition: never edit Me, AGENTS, policy, mothership, qmd config or runtime profiles; never publish. |
