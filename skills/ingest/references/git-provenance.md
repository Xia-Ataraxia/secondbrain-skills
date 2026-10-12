# Git provenance

One ingest, including every Raw, Wiki, Map and atom it touched and the removed Inbox original, is exactly one local commit. No `index.md` or `log.md`: sync carries content, git carries history. Track attachments without LFS; ignore only workspace, cache, trash and sync-lock artifacts according to live policy.

The commit is done when:

- it holds exactly the paths this ingest touched, matched as exact filenames, never a glob - nothing extra, nothing missing;
- its subject is `ingest: {title}` and it carries the trailers `Ingest-Source: <source identity or canonical locator>` and `Ingest-Purpose: <purpose>`;
- nothing that was staged or dirty before the ingest is in it. Check the index before writing; entries already staged belong to someone else, so stop.

Unrelated dirty files stay unstaged and byte-unchanged. A page a human changed during the run is re-read and merged, never overwritten. Never hard reset, check out to settle content, amend an earlier ingest, or force push.

Publication is not part of ingest unless live vault policy says ingest pushes. When it does and the remote has moved on, do not rewrite history to land it: stop and report the local SHA and how the remote differs. Never create or delete a remote. A vault that is not a git repository skips this step and says so in the report.

Undoing an ingest is reverting its commit, which also restores the Inbox original.
