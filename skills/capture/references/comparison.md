# Three-column comparison

Upstream: 구요한 cmds-llm-wiki `/capture-tabs`, commit `54cf2ab150f866bbfcf1aa2c7e03514d14febe20` (Codex command as baseline; agent skill wrapper, `CLAUDE.md` capture rules, `Template_AI Research Capture.md`). One row per upstream section; this is the decision record, not a second procedure. No upstream file is copied.

| 구요한 (54cf2ab) | secondbrain capture | Decision + reason |
| --- | --- | --- |
| Header: pre-ingest capture layer; read Core Context once per session | same | Adopt; one runtime-neutral package instead of Claude/Codex mirrors. |
| Purpose: `00. Inbox/05. AI Research/YYYY-MM-DD-ai-research-{topic-slug}.md`; `04. Clippings/` for short/manifest-only | same dated path and Clippings exception | Adopt; adapt only when the destination's live policy names other lanes (same dated naming, no invented lane). |
| Capture Principles 1–6 | 1–6 kept, plus selection-only and in-place omission markers | Adopt all six; owner additions: preserve selected range/speakers/turn order with explicit omission markers, record a method only when a tool actually used it, capture only the selection. |
| Tool Choice: Computer Use / Chrome automation, Browser plugin, paste/export fallback | aside browser, `defuddle`, `yt-dlp`, paste/export fallback | Adapt tool names to this collection's tools; keep least-lossy order and fallback. |
| Step 0 Scope: topic, platforms, captureMode, nextStep, collectionPurpose (7 reuse axes) | same fields | Adopt fields and one ambiguity question. Owner exception: purpose asked once only when not already stated; delegation → inference + reason from Core Context §2 registered axes, not a fixed 7. |
| Step 1 Read Tab Metadata | same manifest | Adopt. |
| Step 2 Extract Conversation Or Page Text | same four sub-steps | Adopt; owner order across members kept. |
| Step 3 Create Inbox Note: template frontmatter (type inbox, category, clip_type, source_url, platforms, capture_method, capture_status, captureMode, collectionPurpose, author, model, effort, dates, tags) | same fields | Adopt all fields and body sections (Capture Summary, Source Manifest, Original Content, Agent Capture Notes, Ingest Notes). Owner exceptions: snake_case `date_created`/`date_modified`/`date_clipped`; `referenced` added; never overwrite an existing candidate. |
| Step 4 Add Capture Notes | same list | Adopt; ingest places Source Manifest and Agent Capture Notes after `## Metadata`. |
| Step 5 Route: inbox-only / run-inbox / ingest-now after purpose gate and mothership search | same | Adopt; inbox-only default; routing only when the owner chose it; no commit. |
| Verification 1–5, incl. "ingest preserved raw before deleting any Inbox original"; template "Delete Inbox original only after Raw Source preservation passes" | 1–6 | Adopt checks 1–5 plus purpose set. Deletion branch kept but unsettled: the Inbox original stays unless the owner separately authorizes deletion; no automatic cleanup. |
| — (no agent-session capture) | `sessions.md` | Owner extension: same shape and routes; never claims a session or whole source was read when it was not; partial/unsupported reported. |
