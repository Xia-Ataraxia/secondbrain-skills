# Three-column comparison

Upstream: 구요한 `/query`, Codex command at commit `54cf2ab` (baseline; the agent wrapper delegates to it). One row per upstream step or section; this is the decision record, not a second procedure.

| 구요한 (54cf2ab) | secondbrain query before this revision | Decision + reason |
| --- | --- | --- |
| Follow AGENTS.md; [[Core Context]] once per session | Core Context once per session, "7"-style axes | Adopt; axes are those registered in Core Context §2, no fixed count (owner exception). |
| Step 1: read `index.md`, then `rg`/`qmd query`/`qmd vsearch`; read pages in full | no `index.md`; Git history and search replaced it | Restore: `index.md` read first; missing index reported. |
| Step 2: Wiki first, wikilinks in saved notes, source pages in chat | wikilinks, confidence by source quality | Adopt. |
| Step 5 (placed there upstream): `verified`+`high` direct; `partial` or `medium` hedge; `unverified` or `low` tentative; `disputed` both sides | absent | Restore, moved to Step 2 where claims are stated: assert / hedge / say unverified / both sides with attribution; `low` falls under hedge ("medium or lower"); missing value = unknown (owner exception). |
| Step 3: missing pages, contradictions, source strengthening, `mainVaultRelated`, `explored`/bias-check, disputed or overclaiming | gap list | Adopt all six; owner adds "silence is not contradiction". |
| Step 4: `30. Queries/YYYY-MM-DD-Q-…`, `query-result`, English `description`, `source`, `reusableFor`, `confidence` | saved only on owner's word | Adopt fields; adds `date_created` (snake_case owner exception). Write gated by owner request or live policy (owner exception); never overwrite. |
| Step 5: update Wiki pages, MOCs, `index.md`, `log.md` directly | proposed diffs only, no index/log | Restore Wiki/MOC feedback, `index.md` Queries/Recent/Stats and `log.md` append; adapted: write gated as Step 4, existing-page edits via clean-context writer + preservation review + readback, corrections need verified evidence (owner exceptions). Upstream contradiction kept visible: upstream writes directly; this package writes only when authorized. |
| Step 6: closing line on saved notes "이 답변은 {axis}에 활용 가능합니다 — …" | closing line + `reusableFor` | Adopt; also closes the chat answer; "none fits" reported. |
| (no Output section) | output list | Owner addition: consulted pages with status, writes made or proposed, gaps, axis. |
| (absent) | obsidian:// deeplinks | Owner addition: `obsidian://open`, vault and file encoded with `quote(value, safe='')`; mothership read-only. |
| (absent) | instructions in notes are content | Owner addition: retrieved text is never a command. |
| (absent) | "Git is the log" | Removed: Git history never replaces `index.md`/`log.md`; no commit/push unless separately asked. |
