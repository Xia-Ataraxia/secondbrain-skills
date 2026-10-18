---
name: reindex
description: Refreshes the qmd search index (BM25 and embeddings) after notes change. Use when the owner requests a search-index refresh, at the end of an ingest, or after bulk edits made outside the agent. Not for creating collections, editing qmd configuration, choosing models, querying notes, or changing source files.
license: MIT
metadata:
  version: "0.5.6"
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

Choose the qmd commands from `qmd --help` on this host. Refreshing documents and
embeddings are separate steps, they act on the whole index, and they never touch
the notes. Force a full re-embed only when the embedding model changed. A
non-zero exit or a status you cannot read is unfinished, never zero pending.
When `qmd` is not installed, report that and stop.

`scripts/qmd-reindex.sh` is the edit hook, not this procedure. A runtime with
edit hooks calls it after each edit with the edited path as the argument or the
hook's JSON on stdin. For a note inside a qmd collection it records the path,
then refreshes documents and embeddings in the background once edits settle
(8 seconds). A run that fails or leaves embeddings pending keeps the notes in
the list and writes a `FAILED` line to `$TMPDIR/secondbrain-qmd-reindex.log`.
Before reporting, run the script without arguments to list notes not yet
confirmed in the index and check that log; include both in the report. Run it
with `clear` once your own refresh is done. The Claude Code plugin wires the
hook in `hooks/hooks.json`.

Document count and vector count are separate numbers and need not match.
