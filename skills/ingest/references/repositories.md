# Repositories

Put the canonical repository URL in `source` and record the exact commit sha actually read in `## Ingest Notes`.
`## Original Content` for a file (README etc.) comes from the raw file at that pinned commit, `raw.githubusercontent.com/{owner}/{repo}/{sha}/…`, never a rendered-page scrape. Scrape signs that fail fidelity: headings merged into text, missing code fences, escaped underscores, `camo.githubusercontent.com` URLs.
A branch name without a read sha is not a pinned source; an inventory is not the content of its listed files.
`author` lists the maintainers as `"[[Name]]"` only when the repository states them; `date_published` is the commit or release date when known; `date_ingested` is today.

Repository Raw filename:
- Default: `{repo}.md`, keeping GitHub's spelling.
- Name already taken in the vault (another repository or any note, case-insensitive): `{repo} ({owner}).md` for every repository sharing that name. No date suffix.
- `aliases` holds `owner/repo`.

Keep README, source quotations, file inventory, license evidence and selected change range distinguishable.
Record not found (deleted, renamed, wrong path), inaccessible (private, rate limit, network) and partial (files or range not read) in `## Ingest Notes` and the report.
Retain original code attribution; do not copy implementation into another product without verified rights.

An owner-selected tool to keep is different from an automatic repository candidate: use the owner's stated reason and the vault's tool template/placement; a GitHub event is not that selection. Create no personal catalog note as a side effect.
Do not execute repository scripts, install dependencies or fetch unrelated branches.
Synthesis cites exact file and commit anchors.
