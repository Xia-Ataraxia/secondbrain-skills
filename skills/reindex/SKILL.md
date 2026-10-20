---
name: reindex
description: Refreshes the qmd search index (BM25 and embeddings) after notes change. Use when the owner requests a search-index refresh, at the end of an ingest, or after bulk edits made outside the agent. Not for creating collections, editing qmd configuration, choosing models, querying notes, or changing source files.
license: MIT
metadata:
  version: "0.6.0"
---

# Reindex

Refresh the configured qmd index so new and changed notes are searchable. The
index and its collections are whatever qmd is already configured with; this
skill does not create, rename, or edit them.

Done means:

- the changed notes are in the index and a search finds them;
- no embedding the index needs is left pending, or the pending count is
  reported as unfinished;
- the report names the collections refreshed, the document and vector counts
  from qmd's own status, and anything qmd reported as failed.

Upstream runs `qmd update`, `qmd embed`, `qmd status` over the registered
`wiki`, `raw_sources` and `queries` collections (Inbox excluded until ingest).
Refresh only the collections the live qmd configuration already registers; confirm
command names with `qmd --help` on this host. Do not change qmd models, the
embedding model or its environment variable, network access, or the collections
config without the owner's approval; live policy wins and anything unknown is
reported as unknown. Force a full re-embed (`qmd embed -f`) only after an
approved embedding-model change. A non-zero exit or a status you cannot read is
unfinished, never zero pending. When `qmd` is not installed, report that and stop.

This procedure is the qmd CLI itself: run `qmd update`, then `qmd embed`, then
`qmd status`, and read the counts and any `Pending: N need embedding` line from
that status (qmd 2.8.3 prints the line only when N is above 0; vectors count
embedded chunks, not files). A failed command or an empty or unrecognized status
is unfinished.

`scripts/qmd-reindex.sh` is an optional edit hook, not this procedure. It exists
only because qmd has no file watcher or edit trigger: after each edit it remembers
the note if its path lies under a `path:` in the qmd config
(`$QMD_CONFIG`, default `~/.config/qmd/index.yml`) and, once edits settle for 8
seconds, runs the same three commands in the background. It never blocks the
caller and adds no other job semantics. A failed `qmd update`, `qmd embed` or
`qmd status`, a status without its `QMD Status` header, or embeddings stuck
pending keeps the notes in the list and writes a `FAILED` line to
`$TMPDIR/secondbrain-qmd-reindex.log`; a missing `qmd` on `PATH` is logged the
same way. Its limits are those of a debounce script: config paths are read
line by line (no project-local `.qmd/` config), the settle check uses
one-second file times, and a run marker older than 60 minutes is treated as dead.
Before reporting, run the script without arguments to list notes not yet
confirmed in the index and check that log; include both in the report. Run it
with `clear` once your own refresh is done. The Claude Code plugin wires the
hook in `hooks/hooks.json`.
