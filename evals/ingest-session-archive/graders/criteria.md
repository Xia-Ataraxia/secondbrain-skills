---
type: llm
weight: 1
---

Score the response against the `ingest` skill's Session archive mode (SKILL.md and references/conversations.md). All five must hold for a pass:

1. `ingest` owns the request as its session archive mode (not `capture`), and the Wiki compile steps (Steps 1, 3, 3.5 and 4: analyze, compile pages, Persona, Maps) do not run, so each session becomes one `type: chat` Raw and nothing else.
2. The run uses the package's `scripts/agent-sessions.py` over the whole store, with the build server copy passed as a host root, not a note written by hand per session. A rerun skips sessions whose `source_identity` already exists in the Raw folder.
3. `source_url` is `agent-session://open?tool=codex&id=019ea253-b6ea-75c0-bad3-b1b8448c9da9&cwd=%2Fsrc%2Fapp&host=build-server` (cwd URL-encoded, a host parameter because the session is not local); `source_identity` is `urn:codex:session:019ea253-b6ea-75c0-bad3-b1b8448c9da9`; `purpose_origin` is `stated`.
4. `source_attachment` names the original session file kept under the attachments folder by host and runtime, gzip-compressed or a `.jsonl.zst` kept as-is.
5. Thinking blocks and tool results are not archived; their counts are recorded in `## Ingest Notes` and nothing is reconstructed.

Pass only if all five hold. A response that compiles Wiki pages, proposes a capture topic bundle, or writes the notes one by one fails.
