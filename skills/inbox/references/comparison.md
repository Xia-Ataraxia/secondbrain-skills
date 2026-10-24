# Three-column comparison

Upstream: 구요한 `codex/commands/inbox.md` with its `agents/skills/inbox` wrapper, commit `54cf2ab`. One row per upstream step or rule; this is the decision record, not a second runtime procedure. The procedure is written in this package's own words; no upstream file is copied.

| 구요한 (54cf2ab) | secondbrain inbox | Decision + reason |
| --- | --- | --- |
| Header: follow AGENTS.md, read Core Context once per session | Core Context read once; §2 axes offered for purpose | Adopt. Axes are those registered in its §2, never a fixed list. |
| Wrapper: scan all subfolders unless narrowed | Input: all / lane / `count`/`status` / named notes | Adopt; named notes and count-only added. |
| 1. Scan `00. Inbox/` recursively, skip `.gitkeep` | same; unreadable notes reported as problems; "Inbox is empty" stop | Adopt. |
| 2. Group by Articles, Papers, Transcripts, Clippings, AI Research, root | live lanes, including agent and dated lanes; root = uncategorized | Adapt: read the destination's actual lanes; capture's `type: inbox` notes with `capture_status`/`captureMode` are normal candidates. |
| 3. Preview title, source URL, author, category, language, length, 2–3 topics | same plus fidelity, recorded `collectionPurpose`, duplicate column | Adopt his fields; owner adds fidelity (manifest-only is not text), topics from Original Content, and a source-backed duplicate check: source URL/reference first, then content; titles never prove sameness; `referenced` never proves an original was read. |
| Wrapper: present counts and a compact preview | counts per lane, then one table, problems below | Adopt. |
| 4. Ask scope (all / category / selected) and purpose mode (shared / per-file / auto-infer) in one turn | same, one turn | Adopt. Owner rule: a purpose the candidate carries in `collectionPurpose` or the task states is reused, not re-asked; auto-infer records inference and reason in `collectionPurpose`. No answer selects nothing. |
| 5. Route each selected file through `ingest` | compose `ingest` per note, sequential `[3/7] Ingesting:` progress | Adopt. Ingest owns Raw, Wiki, Maps, index and log. |
| 6. Delete Inbox originals only after raw-source verbatim preservation passes | ask "Inbox에서 처리된 파일 삭제할까요?"; delete only on explicit yes and only verbatim-passed candidates | Adopt with the owner's no-automatic-deletion rule: the ask is kept; no answer leaves originals in place as awaiting cleanup; failed or partial ingests and unselected files are never deleted. |
| 7. Update `index.md`, `log.md`, qmd indexes | performed by each ingest's Step 9 and Step 10; inbox checks them on disk | Adopt: index and log are restored and owned by `ingest`; Git history never replaces them. No automatic commit or push; commit only when the owner separately asks. |
| Output: pending counts, scope, completed Raw, Wiki pages, files left in Inbox | same plus files deleted | Adopt. |
