# Provenance

Where every part of this repository came from, what rights apply to it, and which
feature owns each implementation in this local candidate.

Two records work together and must agree:

| record | what it holds |
|---|---|
| `NOTICE` | the third-party notices, verbatim, plus the file-by-file import map |
| this file | the readable lineage: which source, which revision, which rights, which relationship |

Per-change detail lives in each package's Git history; skill bodies may summarize attribution.

## The nine features

Each `skills/obsidian-*` package owns exactly one feature. There is no root skill,
no dispatcher, and no shared runtime.

| id | feature | package | origin | relationship |
|---|---|---|---|---|
| F01 | markdown | `skills/obsidian-markdown` | `obsidian-skills` `skills/obsidian-markdown/` (MIT) | imported, then extended |
| F02 | bases | `skills/obsidian-bases` | `obsidian-skills` `skills/obsidian-bases/` (MIT) | imported, then extended |
| F03 | canvas | `skills/obsidian-canvas` | `obsidian-skills` `skills/json-canvas/` (MIT) | imported, renamed, then extended |
| F04 | mermaid (Pele) | `skills/obsidian-visualize/references/pele*.md` (was `skills/obsidian-mermaid`) | authored here from public Mermaid, Pele and Obsidian documentation; merged into F05 as its Pele branch | original |
| F05 | visualize | `skills/obsidian-visualize` | original deterministic plugin drawing workflow, extended with MIT pi-extension inspection/layout source | original and adapted |
| F06 | cli | `skills/obsidian-cli` | `obsidian-skills` `skills/obsidian-cli/` (MIT) | imported, then substantially extended |
| F07 | clipper | `skills/obsidian-clipper` | authored here from the official Web Clipper documentation, with schema, enumerations, and import-validation facts checked against the MIT-licensed `obsidianmd/obsidian-clipper` source at `6d56d618b00bd970aa738d6a7a61edee27783e81`; nothing vendored | original |
| F08 | doctor | `skills/obsidian-doctor` | authored here from the requirement that plugin diagnosis be a bounded, evidence-gated pipeline | original |
| F09 | sync | `skills/obsidian-sync` | authored here from the requirement that every sync change be staged, evidenced, and reversible | original |

`imported` means upstream files are present in this repository, modified, and
still covered by the upstream notice. `original` means no upstream file is
present; the package was written here.

## Sources

### obsidian-skills — MIT, imported

- Repository: <https://github.com/kepano/obsidian-skills>
- Revision: `3ccff5338ea700537839b21900aa5358a0402c98`
- Licence evidence: repository-root `LICENSE` at that revision carries the full
  MIT text — copyright line, permission grant, notice-retention condition, and
  warranty disclaimer — with SHA-256
  `64c64d48361edfe8610016441bf593256ea9b67f133b00f47c55aa29ee878567`.
  `.claude-plugin/plugin.json` independently declares `"license": "MIT"`.
- Rights exercised: copy and modify, with the notice retained. `Copyright (c) 2026
  Steph Ango (@kepano)` appears in this repository's root `LICENSE`, in `NOTICE`
  with the full permission text, and in the README attribution.
- Files imported: nine, listed one by one in `NOTICE` section 1.1.
- Read but not imported: its `README.md` and two plugin manifests, consulted for
  installation and manifest convention only (`mit-reference`; no text copied), and
  its `skills/defuddle/` and `skills/knap/` packages, which are outside these nine
  features and over which no rights are exercised here.

### craft-skills — no licence notice, requirements evidence only

- Repository: <https://github.com/Xia-Ataraxia/craft-skills>
- Revision: `836eb8778134d68f3ea675cd30ee5f9ae692f9e3`, read-only.
- Licence evidence: **no** `LICENSE`, `COPYING`, or `NOTICE` file exists at that
  revision, and no inventoried file carries a licence header. The only licence
  statement is the string `MIT` in `.claude-plugin/plugin.json` and
  `.codex-plugin/plugin.json`, and that repository's own README states MIT is
  declared in the plugin manifest with no licence file present. A declaration
  without the copyright line and permission text is not a notice this repository
  can honour or pass on.
- Consequence, applied without exception: **no code, prose, table, checklist,
  example, asset, or corpus prompt/response from that source is copied into or
  redistributed by this repository.** Every behaviour adopted from it was
  re-expressed from the underlying requirement and grounded in public vendor
  documentation, cited per package in that package's Git history.
  Source paths, stable unit identifiers, and digests are retained for inventory
  and attribution, not as a redistributed evaluation corpus.
- What was taken: the *requirements*. That source is a single thick Obsidian
  package; reading it answered which problems these nine features must solve, in
  what order, and with what failure behaviour. It did not supply the answers.
- Rule: nothing from that source may be copied; it stays evidence only.
- Downstream lineage claim: that source's own changelog claims a further
  third-party lineage for material predating it, also without a licence notice.
  Because no expression from it is reproduced here, no rights over that
  third-party material are claimed, granted, or implied.

## What the inventory covers

The authenticated native inventory below is preserved. The plugin-first F05
addition is an additive owner-local source map in
`skills/obsidian-visualize/references/source-map.json`, with exact revision, complete package
tree/digests, retained MIT notice, exclusions and verification paths. It is not
represented as newly authenticated native rows or as part of an earlier release
seal. Git history records the source-only
implementation revision 0.2.0; collection metadata became 0.2.0 on 2026-10-07.

Complete, digest-pinned, and audited:

| source | inventoried files | units | coverage rule |
|---|---|---|---|
| craft-skills | 37 | 121 | every file under `skills/obsidian/` and `tests/obsidian/` is inventoried, plus the root policy and distribution files that shaped this repository's own contract, installer, and manifests |
| obsidian-skills | 13 | 14 | every file of the four imported packages, plus the licence, readme, and manifests |
| total | 50 | 135 | 95 functional units with exactly one owner each, 40 shared supporting units |

Functional units per owner: F01 11, F02 7, F03 6, F04 6, F05 15, F06 19, F07 14,
F08 7, F09 10.

Unit granularity follows the shape of the source file. A file serving one feature
is one whole-path unit. A file serving several is split: the thick package's
`SKILL.md` by route row and by section, its changelog by dated record, and the
eval corpus by case and by trigger. A mixed file is never reduced to a single
record, and a shared requirement is never given an invented single owner — it
becomes a supporting unit instead. Both sources declare `partition: true`, so with
a checkout supplied the audit fails if any file in it is neither inventoried nor
covered by a stated exclusion.

## Deliberately not adopted

Six units record behaviour this repository refuses, so the refusal is auditable
rather than invisible:

- mandatory discovery of four external format and CLI packages through the host
  loader, and the two references that deferred Markdown, embed, and canvas
  answers to those packages — here each package owns its own format outright;
- the rule against holding a format or command catalogue locally — inverted here
  by design, keeping only the narrower rule that a package reports a capability
  gap instead of inventing a surface it does not own;
- selective sub-recipe loading — a property of one thick package, meaningless when
  the host loads one small package per task;
- the consolidation of eight packages into one thick package — this repository
  takes the opposite shape on purpose.

## Public sources consulted for facts

Several packages ground a format, command, or schema fact in a public third-party
project. Those readings produced facts, not text: no file from any of them is
vendored here, so none of them imposes a notice obligation and none of them
endorses this repository. Each package cites its own list with exact URLs, and
usually exact revisions, in its Git history and attribution section; `NOTICE`
section 2.1 carries the consolidated list.

## Knowledge operation set — built on cmds-llm-wiki

The eleven knowledge packages (`capture`, `inbox`, `ingest`, `query`, `verify`,
`audit`, `lint`, `status`, `reindex`, `refresh-context`, `onboard`) follow the
operation set and LLM-wiki workflow of Yohan Koo (구요한)'s
[cmds-llm-wiki](https://github.com/johnfkoo951/cmds-llm-wiki), read at commit
`863ca43778e639d96a31f71fb388ee000336d0ff` (2026-09-21), re-read at
`54cf2ab150f866bbfcf1aa2c7e03514d14febe20` for the restoration recorded below. That repository ships
eleven commands of the same names (its `capture-tabs` corresponds to `capture`)
and itself credits Andrej Karpathy's LLM Wiki pattern.

- Relationship: each package is built on the matching upstream command. Its step
  skeleton, section names and terms (for example 지식요건해당성 / 정합성 /
  확증가능성, 미래의 나에게 보내는 편지) are kept, and the owner's own judgment is
  stacked on top. Each package records every upstream step as Adopt, Adapt or
  Reject in its `references/comparison.md`, and credits 구요한 at the top of its
  `SKILL.md`.
- Text: the explanatory prose was written here, but some short phrases and rule
  sentences match the upstream (an 8-gram comparison finds shared runs, most in
  `verify`, `capture` and `query`).
- Rights: the upstream repository publishes no licence, so this repository's MIT
  licence grants nothing over that material. Its author's permission for the
  adopted wording has not been recorded here.
- No endorsement by, or affiliation with, the upstream author is claimed.

## Helpers transferred from bstack, now removed

Two ingest helpers (`web-source-validate.py`, `youtube-transcript-extract.py`, bstack `290cb51`) and two book fetchers (`fetch_yes24.py`, `fetch_aladin_toc.py`, bstack `2b38de8`) were copied byte-identical into `skills/ingest/scripts/` without a confirmed origin licence. They were removed in 0.4.0; ingest now names the tools (`defuddle`, `yt-dlp`, the aside browser) instead. Their records remain in Git history.

## Native obligation restoration — Unreleased

These additive restorations keep the candidate at `0.1.0`. Requirement lineage
is public `Xia-Ataraxia/craft-skills@836eb8778134d68f3ea675cd30ee5f9ae692f9e3`:
native maintenance and operating requirements, Korean discovery intent, explicit
vault-registry resolution, and append-only plugin evidence. The requirements were
re-expressed, not copied as prose or evaluation-corpus examples. No new source
permission grant is claimed; existing MIT copyright and permission notices and
the local ingest transfer's unresolved origin-rights and redistribution hold
remain unchanged.

- `AGENTS.md` restores native-only official-documentation-first checking,
  installed-version evidence, conflict disclosure and unknown facts; per-change
  source/version records and affected evaluations when either moves; and the
  prospective runtime-change order of documentation, evaluations, recipe,
  version. It preserves relied-on description triggers, including
  non-English intent, and the seven native operating steps: exact artifact and
  effect, read first, preserve unrelated content, least destructive supported
  selected surface, exact readback, evidence and prerequisites, unknown runtime
  facts. This adds no shared runtime, dependency or write authority.
- `skills/obsidian-markdown/SKILL.md` restores Korean note-cleanup discovery in
  the description only; the existing English scope and body are unchanged.
- `skills/obsidian-cli/SKILL.md` restores Korean backlinks discovery without
  changing the existing description scope or body.
  `skills/obsidian-cli/references/operations.md` adds supported read-only registry
  lookup, task-selected name-to-root mapping and root cross-checking; missing,
  stale or ambiguous registration stops before effects, without default changes
  or fallback surfaces.
- `skills/obsidian-doctor/references/plugins.yaml` changes only the header:
  retired or renamed APIs retain version-scoped evidence and retirement is
  appended, never deletes history. The whole parsed registry data is unchanged.

The new CLI source is <https://help.obsidian.md/cli>, consulted through the
publisher's raw document
<https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Extending%20Obsidian/Obsidian%20CLI.md>:
32,586 bytes, SHA-256
`884d3f36a30ad2dc08bcdc84c1243e17e255677a2bd4a7a1aa0d8f77939fc012`.
Lines 137-148 document explicit vault name/id first; lines 1208-1225 document
`vault info=path` and `vaults verbose`. These are documentation facts, not proof
that an installed build supports or executed them.

Verification established static description/body preservation and whole-registry
parsed-data equality; six existing frontmatter checks passed independently.
Bundle metadata `1.12.7` is not a live CLI version or help response: the current
help/version probes timed out. No current registry execution, live routing or
runtime behavior is proved. Earlier version-specific tests remain historical;
no unchanged suite is rerun for these prose records.

## Ingest and capture workflow adoption — Unreleased

Source read: [cmds-llm-wiki](https://github.com/johnfkoo951/cmds-llm-wiki) at
`863ca43778e639d96a31f71fb388ee000336d0ff` — its `/ingest`, paper-ingest and
`/capture-tabs` command documents and the twelve-step analysis scheme. That
repository still carries no license, so the relationship stays design inspiration:
the single-run ingest, the page target, update-or-create, Map updates, the
twelve-axis paper pipeline and topic bundles were adopted as procedures and
rewritten here. No file, template, script or passage was copied; its verifier
script is replaced by a checklist. `skills/ingest/references/comparison.md`
records each decision. The `references/interface.md` named for `skills/ingest`
in the section below no longer exists.

## Knowledge registration and resource corrections — Unreleased

Source baseline: existing local revision
`25f484a63e7278e1864f08b372eea3d96e809289`. These corrections keep version
`0.1.0` and record existing packages and code, not new runtime behavior.

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` now list the
  eleven canonical knowledge names in their existing `knowledgePackages` arrays.
  Native registration, collection identity and all other metadata are unchanged.
- The existing `references/interface.md` in `skills/ingest`, `skills/audit`,
  `skills/lint` and `skills/verify` now declares ten existing package-local helper
  paths and their roles. Git history records the details; no helper,
  callable role, protocol, dispatcher or shared runtime was added.

No code or asset was imported, copied, modified or relicensed by these corrections.
Existing source attribution and MIT notices remain intact. The local ingest
transfer's unconfirmed origin rights and public-redistribution hold remain in
force; this registration/documentation change supplies no new permission grant.
No installation, native app execution or model/runtime proof is established.

## Collection release 0.2.0 — 2026-10-07

The collection release identity moved from `0.1.0` to `0.2.0` in every manifest,
in `install.sh` and in each package `metadata.version` that carries it, so native
plugin hosts see the knowledge packages and fixes added since `0.1.0` as an
upgrade. Plugin identity `obsidian-skills@obsidian-skills` is unchanged. Only
version metadata, manifest prose, inventory target digests of the changed
`SKILL.md` files and documentation changed; no code or asset was imported,
copied or relicensed. The immutable `v0.1.0` tag and the historical Claude Code
and Hermes results stay bound to their original revisions.

## Collection release 0.2.1 — 2026-10-07

Observed evidence: a Hermes Agent v0.21.5 install of `0.2.0`, run with
`hermes skills tap add Xia-Ataraxia/secondbrain-skills` and then
`hermes skills install Xia-Ataraxia/secondbrain-skills/<name> --yes`, installed
16 of 20 packages. Hermes `tools/skills_guard.py` blocked four with a
community-source CAUTION verdict:

- HIGH `inline_shell_exec` (regex ``!`[^`\s][^`\n]*` ``) in
  `obsidian-markdown/references/EMBEDS.md`, `obsidian-bases/SKILL.md` and
  `obsidian-clipper/references/template-language.md`, each from an exclamation
  mark written as a one-backtick code span.
- HIGH `python_os_environ` in `reindex/scripts/reindex.py`, from an environment
  copy that set `PYTHONIOENCODING` for qmd.

All four were false positives. The three documents were reworded with the same
meaning, and `reindex` stopped copying the environment; see Git history. The
same v0.21.5 `scan_skill` was rerun locally over every `skills/<name>` directory
of this tree. That is a scanner verdict, not a host install or fresh-load. No
code or asset was imported, copied or relicensed. The `0.2.0` results and every
earlier pin stay bound to their original revisions.

## Status and limits

The new plugin-first visualization source absorbs inspection/layout/skeleton
material from `Jonghakseo/pi-extension` at
`a4a8107885d2e944d03d8ebc7d9b1cdcf8b7521f`, under the complete MIT grant
`Copyright (c) 2026 Jonghak Seo` retained in `NOTICE` and the owner package.
`scripts/inspect.mjs` and `references/style.md` / `references/skeleton.md` are
adapted; the full-scene adapter and guarded native workbench helper are original.
No standalone app/server/dist, dependency/font bundle or plugin artifact is
redistributed. Official plugin API/loader facts were inspected at
`f30b4c5d3dcb66ac76ced8f05d9e95409ee94c79` (source manifest 2.28.1), not
inferred as an installed version. Source tests do not establish a current
Obsidian plugin load/render; fresh exact-tree release and privacy revalidation
remain necessary before later publication or deployment.

- The local release candidate holds twenty packages: the nine native features
  above and the eleven knowledge packages.
  Its documentation adds no source, code or asset. The local ingest transfer's
  two helpers and three tests keep their unconfirmed origin rights and
  public-redistribution hold; a local release candidate is not a new grant or a
  publication approval.
- This repository is a public prerelease at version `0.2.1`. Nothing recorded
  here installs it on a host, publishes it to a marketplace, or retires, replaces,
  or supersedes any other project — both sources above remain their owners' to
  maintain. `docs/cutover.md` states what a change of ownership would require.
- Provenance records authorship and rights. It is not runtime evidence: what has
  and has not been exercised against a running Obsidian app, CLI, plugin, or sync
  service is recorded in `docs/verification-matrix.md` and in each package's
  Git history, and unverified claims stay marked unverified there.
- Only synthetic, public examples appear in shipped files. No credential, account
  identifier, workstation path, private note, or internal planning document is
  reproduced in this repository, including in this record.

## Installer removed — 2026-10-10

`install.sh`, `scripts/install_packages.py` and `docs/install-matrix.md` were
removed. Packages are installed and updated only through each runtime's own
plugin or skill registry, listed in the README. A directory copy made by the
script alongside a plugin install had shadowed the plugin, so plugin updates
were not used (#25). Earlier records above that cite these files remain as
history. No code, asset or licence changed.

## Upstream semantic restoration of the knowledge packages — Unreleased, UNVERIFIED

Source re-read: [cmds-llm-wiki](https://github.com/johnfkoo951/cmds-llm-wiki) at
`54cf2ab150f866bbfcf1aa2c7e03514d14febe20` (2026-10-10). Files consulted:
`CLAUDE.md` (Frontmatter Standards, folder and naming tables, verification
section), `90. Settings/Templates/Template_Raw Source.md`,
`90. Settings/Templates/Template_Wiki Page.md` and the paper templates,
`90. Settings/Skills/paper-ingest.md`, `90. Settings/Sharing/Paper Ingest Guide.md`,
`90. Settings/94. Agent Settings/codex/commands/*.md`, the matching
`agents/skills/*/SKILL.md` wrappers, `claude/commands/ingest.md`,
`claude/commands/onboard.md` and `codex/hooks/qmd-reindex.sh`. The earlier pin
`863ca43…` above stays as history.

- Baseline: each agent wrapper delegates to its Codex command, so the Codex
  command is the port baseline; Claude-only detail fills gaps, and Claude/Codex
  step ordering is treated as a vendor variant, not a contradiction.
- Restored upstream semantics: Codex ingest order (0 → 0-a → 0.5 → 1 → 2 → 3/3.5
  → 4 → 5 → 6), `index.md` catalog/Stats/Recent sections and append-only
  `log.md` across the operations that keep them upstream, the original
  role/`type`/`layer`/`category` schema, the claim taxonomy and verification
  fields, Paper Mode's twelve axes and hub/atom shapes, Book Mode scaffolding
  and promotion, capture-tabs fields, the audit phases and scores, lint checks.
- Owner exceptions kept on top: snake_case date keys (including
  `conversion_date`); `referenced` for originals and earlier captures; author
  wikilinks allowed without target notes; purpose gate with explicit delegation
  recorded with its reason; Core Context read once per session with its actually
  registered axes; mothership links with both URI components percent-encoded and
  `mainVaultCmds` limited to registered references; clean-context writer plus a
  separate preservation reviewer for existing Wiki pages; no incidental metadata
  migration; no automatic commit, push or deletion; principles and
  `secondbrain-mode` stay optional, never a runtime gate.
- Genuine upstream contradictions kept visible and scoped: Book Mode's Articles
  placement versus the schema's Books folder; Paper Mode's P-4 lower bound;
  verify's `Disputed Claim` versus ingest's `Contradiction` callout name; audit
  saving by default versus the owner's approval rule.
- Rights: unchanged. The upstream still publishes no licence; procedures and
  terms were re-expressed here, and no upstream file, script or template is
  shipped (see the P-7 verifier note below). The
  native packages, their MIT notices and their records are unchanged.
- `reindex` hook status parsing is grounded in the published `@tobilu/qmd`
  2.8.3 package (`dist/cli/qmd.js`, the `status` command): it prints a
  `QMD Status` header, `Total: N files indexed` and `Vectors: N embedded`, and a
  `Pending: N need embedding` line only when N is above 0. That is a source
  reading of one version, not a run against an index.
- `skills/ingest/references/reingest.md` was rewritten to separate a source
  update from reprocessing, with `log.md` as the record instead of a Git trailer.
- Independent QA round on this candidate: 58 tests, 8 failed (reindex hook
  behaviour and template serialization; recorded in
  `docs/verification-matrix.md`). Repairs after that run: the hook's bookkeeping
  moved to `skills/reindex/scripts/qmd_reindex.py` (structured JSON queue, `fcntl`
  locks, qmd 2.8.3 config resolution read from `dist/collections.js` and the CLI:
  project-local `.qmd/index.yaml|yml`, then `QMD_CONFIG_DIR`, `XDG_CONFIG_HOME/qmd`,
  `HOME/.config/qmd`; one queue and one worker per selected config plus
  `HOME`/`XDG_*`/`QMD_CONFIG_DIR`/`INDEX_PATH`, list and `clear` per target, no
  age- or PID-based reclamation, `qmd` taken only from the caller's `PATH`;
  PyYAML required, never installed); persona `source` keeps
  several existing items; verify's confidence matrix restored from
  `claude/commands/verify.md` with its overlaps reported as uncertainty; Paper Mode
  step names, guiding questions, conditional Scale page and P-7 checks restored.
- P-7 verifier: an interim unpublished candidate copied and adapted the
  upstream `90. Settings/Scripts/p7_verify.py`; it was never released and has been
  removed. `skills/ingest/scripts/verify_paper.py` replaces it: a separate
  implementation written from the P-7 functional requirements in
  `skills/ingest/references/papers.md`, by an author who did not read the upstream
  script or the interim copy. It is this repository's own MIT-covered code. It
  shares only public interface facts with the upstream workflow (field names, the
  twelve-axis step names, section titles); it fails ambiguous Coverage Map rows
  and Markdown in subfolders instead of passing them. A mechanical PASS is not a
  semantic or qualitative PASS.
- Paper hub `status: active` follows upstream
  `90. Settings/Templates/Template_Paper Hub.md:27`; the first QA draft of
  `evals/test_templates.py` wrongly expected no status, and only that expectation
  was corrected.
- Verify's confidence matrix: the `low` row's "created < 7 days" reads
  `date_created`; the `high` row's "age > 30 days" names no field upstream, so it
  is reported as unknown and never used to promote.
- Later QA round: 166 tests, 7 failed, run against the candidate as it stood
  then (historical; not rerun). After it the owner judged the reindex queue and
  the test suites over-engineered, and they were removed: the
  `skills/reindex/scripts/qmd_reindex.py` queue/lock/state helper above, the
  `evals/test_reindex.py` suite that exercised it against a fake qmd, and the
  `evals/test_templates.py` template renderer (templates are model instructions,
  not a program). `skills/reindex/scripts/qmd-reindex.sh` is back to the shape it
  had at `11fbde9`, which follows upstream `codex/hooks/qmd-reindex.sh`: a debounce
  hook kept only because qmd 2.8.3 has no file watcher or edit trigger (its help
  lists `update`, `embed`, `status` and no watch command). Changes from `11fbde9`:
  no host `PATH` append; a failed or header-less `qmd status` keeps the notes
  pending instead of reading as zero; only a line-leading `Pending:` counts. The
  `reindex` procedure itself calls the qmd CLI directly.
- After 0.6.0 the owner directed that wrapper scripts are not attached to
  packaged CLIs at all. `skills/reindex/scripts/qmd-reindex.sh` and its only
  registration, `hooks/hooks.json` (a `PostToolUse` Write/Edit hook), were
  removed, so automatic edit-hook indexing is retired; nothing replaces it.
  Explicit reindex stays the direct `qmd update`, `qmd embed`, `qmd status`
  sequence at the end of a workflow. `AGENTS.md` and `principle-skill-creating`
  now state the anti-pattern. The hook entries above are history.
- `verify_paper.py` stays: it checks this package's paper artifacts (structure,
  located quotes, coverage), which neither qmd nor Obsidian provides and P-7
  requires. Fixes after the 166-test round: leaf/parent headings are judged at
  every level H1-H6, so a parent row never covers nested leaves; a required
  section holding only a `---` separator is empty. `evals/test_paper_verifier.py`
  was narrowed to a few domain regressions (pass is mechanical only, stub/S12,
  separator-only section, quote numbers/negation/minus/short lines, nested
  coverage, identical headings, nested atom folders).
- Review fixes after the narrowed suite: the verifier requires the Step Map S01
  row as `CITATION | (hub) | compiled` and accepts `model` as a list when several
  models contributed, as the frontmatter schema allows; the schema now lists the
  owner's snake_case date keys exactly, and upstream `exploredDate`/`verifiedAt`
  keep their upstream names.
- Evidence for the current state is recorded in `docs/verification-matrix.md`
  (focused verifier eval, `claude plugin validate . --strict`, one native
  fresh-load of `ingest`). The earlier failing rounds above stay historical.

## Raw note shape — 0.6.4

- Owner exception to 구요한's `Template_Raw Source.md` at `54cf2ab`: no `[!info] Source` callout, no `## Metadata` (language and length move to frontmatter), filename `{Title}.md` without a date prefix, no `date_clipped` in the Raw; URL images stay as links and text-bearing images get an OCR blockquote.
- `evals/` was removed at the owner's direction; the repository keeps no tests and `verify_paper.py` stays as ingest's runtime check.

## Pele branch of obsidian-visualize — 2026-10-23

- Owner direction: `skills/obsidian-mermaid/` merged into `skills/obsidian-visualize/`, which now owns three branches: Canvas, Excalidraw and Pele. Moved with history: `SKILL.md` → `references/pele.md`, `references/diagram-catalog.md` → `references/pele-catalog.md`, `references/compatibility.md` → `references/pele-compatibility.md`. The collection is now 25 packages, 8 native.
- Sources: Obsidian 1.15.0 desktop changelog (early access, 2026-10-22) <https://obsidian.md/changelog/2026-10-22-desktop-v1.15.0/>; <https://github.com/obsidianmd/pele> (MIT); <https://pele.run/compatibility>; <https://pele.run/security>. Pele targets Mermaid 12.1.0 syntax and has no CLI; the fence stays `mermaid`.
- Observed: Obsidian 1.15.0, installer 1.13.4, desktop macOS. `window.pele` present after `loadMermaid()`. Every block in `pele-catalog.md` rendered through `pele.render()` called by `obsidian eval` (level B). No note was written; rendered-note QA (level D), `internal-link` navigation and the Excalidraw `addMermaid` path under Pele stay unverified.
- CLI rule check: no visualize script shells out to a packaged CLI; `plugin-workbench.js` is an in-app payload sent by `obsidian eval`. No wrapper was added.
