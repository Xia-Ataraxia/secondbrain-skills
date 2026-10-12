---
name: reindex
description: Refreshes the qmd search index (BM25 and embeddings) after notes change. Use when the owner requests a search-index refresh, at the end of an ingest, or after bulk edits made outside the agent. Not for creating collections, editing qmd configuration, choosing models, querying notes, or changing source files.
license: MIT
metadata:
  version: "0.5.4"
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

`scripts/qmd-reindex.sh` keeps the list of notes edited since the last refresh.
Run it without arguments to see that list, and with `clear` after the refresh is
done. A runtime with edit hooks calls it after each edit with the edited path as
the argument or the hook's JSON on stdin; it records only notes inside a qmd
collection and runs no qmd command. The Claude Code plugin wires this in
`hooks/hooks.json`.

Document count and vector count are separate numbers and need not match.
