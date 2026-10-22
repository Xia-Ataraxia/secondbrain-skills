---
name: ingest
description: Turn one selected URL, file, text or Inbox candidate into a preserved Raw source plus 10–15 created or updated Wiki pages, updated Maps, index.md and log.md, in a single run. Use for ingest, paper analysis (12-axis), book notes (책 노트, 독서 노트, 목차 넣어줘), chapter promotion and attributed Persona updates. Not automatic collection, personal profiles or undesignated research questions.
---

# Ingest

Built on 구요한's `/ingest` (cmds-llm-wiki `54cf2ab`). The baseline is the Codex flow his agent skill `agents/skills/ingest/SKILL.md` delegates to, `codex/commands/ingest.md`: its step order and names are kept. Detail the Codex command leaves to the Claude command (Step 0 wording, Step 3.5, Book Mode) comes from `claude/commands/ingest.md`; the two are vendor variants of one procedure. Owner exceptions are stated where they apply. Earlier decisions against his version are in [comparison](references/comparison.md).

Execute every step in order. Asking for ingest authorizes the writes this recipe names in the destination vault — Raw, Wiki pages, Maps, `index.md`, `log.md` — under the vault's live policy. It does not authorize deleting an Inbox original or any other file, committing, pushing, or writing into a mothership. [Frontmatter](references/frontmatter.md) governs every key; YAML uses 2 spaces, the body tabs, YAML wikilinks are quoted.

Read the vault's Core Context once per session before the first ingest. Use the reuse axes actually registered in its §2 (normally 5–9), never a fixed list.

## Input

- URL: fetch the content, then process.
- File path or name: read it from the vault, checking the Inbox and its lanes first.
- Blank or `all`: delegate selection to `inbox`.
- Raw text: the argument is the source.
- Academic paper (DOI, arXiv or journal URL, a document with Abstract and References, a file from the papers lane): Paper Mode.
- Multi-page book or docs site (5+ chapters in its sidebar or TOC): Book Mode.
- Binary or non-Markdown file: Step 0.5 after Steps 0 and 0-a.

Per-material acquisition detail: [articles](references/articles.md), [videos](references/videos.md), [repositories](references/repositories.md), [mail](references/mail.md), [conversations](references/conversations.md).

## Category detection

Pick the Raw `category` in this order: the Inbox lane the file sits in; a `category` in Web Clipper frontmatter; inference from the content; default `Articles`. Save into the destination's Raw folder for that category (upstream layout `10. Raw Sources/11. Articles` … `16. AI Research`).

## Step 0 — Collection purpose (미래의 나에게 보내는 편지)

Ask exactly one collection-purpose question before ingest, and nothing else:

> 미래의 내가 이 자료를 다시 볼 때 — 왜 수집했고, 어디에 쓸 예정인지 한 줄 남겨주세요.
> 재활용 축 참고: {Core Context §2 에 등록된 축}

- Save the answer verbatim as `collectionPurpose`.
- Do not ask when the task already states a valid purpose, or the capture candidate carries `collectionPurpose`; use it.
- When the owner says "알아서 판단해줘" or "자동으로", infer the most likely axis from the source and Core Context §2, state the inference and its reason, and record that in `collectionPurpose`.
- Batch: ask once up front — "오늘 들어온 {N}개 소스, 전체를 하나의 목적으로 묶으시겠어요, 아니면 개별로 물을까요?" — and follow the choice.

## Step 0-a — Mothership connections

Skip when Core Context registers no mothership. Otherwise search it read-only with the source's key concepts and the purpose (`qmd`, keyword fallback), keep the 2–5 most relevant notes (essays, MOC or hub notes, category pages, recent teaching or consulting notes when the purpose is teaching or consulting), and for each:

1. use the exact path the search returned;
2. confirm the file exists before using it, dropping any that does not;
3. percent-encode both URI components separately: the vault name with `urllib.parse.quote(vault, safe='')` and the path with `urllib.parse.quote(path, safe='')`;
4. write `"[<filename without .md>](obsidian://open?vault=<encoded vault>&file=<encoded path>)"`.

Notes the owner names in the task or explicitly confirms go through the same four checks and join the list. Fill `mainVaultCmds` only with a category or command reference the Core Context or mothership actually registers, copied exactly in its registered form and with the cardinality the live policy defines; leave it empty when none fits. Never invent or impose a classification. Record the stat-verified list in `mainVaultRelated` on the Raw and the relevant Wiki pages, and list it in the report. Ask no further question here. Never write into the mothership.

Use `obsidian://open`, the form the Codex command and its link check use, unless the live policy names another form such as `obsidian://advanced-uri`.

## Step 0.5 — Format conversion

Skip for `.md`, `.markdown`, `.txt`. Transcribe audio (`.mp3`, `.wav`, `.m4a`) with a transcription tool; leave the audio file where it is and report it. Convert any other document (`.pdf`, `.pptx`, `.docx`, `.hwp`, `.epub`, `.html`, images, …) with an available converter (`markitdown`, `pandoc`, `hwp5txt`, `defuddle`). Move the original binary into the vault's attachments folder under its original filename, place the converted `.md` beside where the binary was, and carry `source-attachment`, `source-format`, `conversion-tool`, `conversion_date` and `conversion-fidelity` into the Raw. `## Original Content` then holds the converted Markdown; the binary stays preserved as the attachment. When conversion fails, leave the binary where it is, name the missing tool or ask the owner to convert, and stop this input; other inputs in the run continue.

## Step 1 — Analyze

Read the whole source. Extract:

- key concepts (3–8) worth a Concept page — candidates that may land on existing pages; an abstract or sentence-style title is a legitimate Concept;
- entities (1–5): people, organizations, products, models;
- practical guidance (0–3) worth a Guide;
- key claims to track;
- connections to existing Wiki pages.

Read `index.md` and search the vault (`qmd`) for existing pages first; updating an existing page beats creating a new one. Match a source by `source` URL or reference before title. This lookup establishes identity and targets from titles, aliases, paths, `source` and index lines; existing page prose stays out of Step 3's writer.

When a claim reports another creator's work, attribute it to this source's author as a secondary claim and put the original in the Raw's `referenced`: its Raw or Book Index wikilink when already in the vault, otherwise its canonical URL. Never fetch or ingest the original for this; record provenance unknown in `## Ingest Notes` when it cannot be located. A Concept resting only on secondary claims is at most `confidence: medium`. Each claim stays with its creator and the source it arrived through; never merge claims from different creators into one unattributed statement.

## Step 2 — Save Raw Source

Use [raw](templates/raw.md), filename `{Title}.md` (`{Title} (YYYY-MM-DD).md` when that name is taken); an Inbox candidate keeps its existing name so links to it resolve. The Raw keeps the source's own order and structure; nothing is reordered, regrouped or normalized.

The Raw body is `# {Title}`, `## Original Content`, and `## Ingest Notes` only when there is something to record.

- Preserve the original verbatim under `## Original Content` — no summaries, no "redacted for brevity", however long. Keep image lines `![alt](url)`, video and media URLs, quote blocks, citation lists and code blocks.
- Keep each image as its original `![alt](url)`; do not download it.
- OCR every image that contains text and put the text, as Markdown with spelling unchanged, in a `>` blockquote directly below the image. Record the OCR method and any uncertain reading in `## Ingest Notes`.
- A clipper body already wrapped in `## Original Content` is copied verbatim. A fetched URL keeps the fetched content.
- Remove only obvious clipper artifacts (a block repeated by a clipper bug) and say so in `## Ingest Notes`.
- From a Web Clipper or capture candidate carry over `source_url` → `source`, `author` → `author` as `"[[Name]]"`, `published` → `date_published`, `collectionPurpose` and `referenced`. A capture's Source Manifest and Agent Capture Notes go under `## Ingest Notes`, unchanged; they guide Step 3 and never enter Original Content.
- Never rewrite an existing Raw body. When an already-ingested source changed, ask the owner first: a minor change keeps the Raw; a major change becomes `{Title}-v2.md` with `supersedes`, the earlier Raw gains `superseded-by`, and both stay. See [source update and reprocessing](references/reingest.md).

Pre-flight before moving on:

- `## Original Content` is present;
- its body matches the obtained source: for an Inbox source at least 80% of the Inbox body's lines, a short clipping in full;
- images, media URLs, quotes, citations and code blocks survived;
- the 7 required properties are present.

Inbox cleanup: upstream finishes this step as a move by deleting the Inbox original. Delete it only when the owner's request or the vault's live policy authorizes removing it, and only after the pre-flight passes; when several Inbox files went into one Raw, the same applies to each and `## Ingest Notes` lists them. Without that authorization leave the original in place and report it as awaiting cleanup. A URL, an external file or raw text leaves nothing to delete.

## Step 3 — Compile Wiki pages

For each extracted concept, entity and guide, update the existing page or create one: Concepts with [concept](templates/concept.md), Entities with [entity](templates/entity.md), Guides with [guide](templates/guide.md). Keep the levels distinct: Raw holds evidence, Wiki pages hold one concept, entity or guide each and cite their Raws, Maps group pages.

- New writing comes only from this source and is attributed to it.
- An existing page is updated in three separate contexts, in this order:
	1. Writer — a fresh context given only the vault's approved policy, this run's extraction and the Raw's `## Original Content`. It never sees the existing page's prose or examples; the page's path, title, aliases, `type`, `layer` and `source` list may be passed to fix identity and target. It drafts only source-grounded additions for that page.
	2. Preservation reviewer — a separate context given the page's before-image and the writer's proposal. It first checks that every valid existing statement, link and frontmatter value survives, then reduces the proposal to the minimal patch: additions under the relevant sections, the Raw appended to `source`, `date_modified` updated. It drops anything the source does not support and never regenerates the page.
	3. Apply the reviewed patch, read the page back and compare it with the before-image. Links to and from the page are added only after this validation (Step 4).
- When the runtime cannot provide separate contexts, stop the update of that existing page and report it; new pages and the rest of the run continue.
- The existing Wiki is not ground truth, and neither is one source. An existing statement changes only when the correction rests on verified evidence (a `verify` result or the owner's confirmation) and the reviewer accepted it. When this source explicitly conflicts with an existing claim, keep both, attributed, with `> [!warning] Contradiction` and the uncertainty stated. A source that is silent on a claim does not contradict it.
- An Entity exists because the analysis found it significant, never only to resolve an author link.
- New pages start `explored: false` and `verificationStatus: unverified`; `explored: true` only after a human or agent completed the Exploration Gate check and documented it in the page body. `confidence: high` or synthesis-heavy pages carry the Bias Check callout.
- When the classification is clear, set `claimType` and `evidenceScope` for later `verify`.

Target: 10–15 Wiki pages touched per ingest when the source is substantial, created or updated. It is not a creation quota; a thin source reports the shortfall instead of padding.

## Step 3.5 — Persona accumulation

When the source's author or primary speaker matches an existing Persona card, append with [persona](templates/persona.md): 1–3 verbatim quotes that grep-match the Raw's `## Original Content`, as `> [!quote] {topic} ({date}, [[raw source]])`; one dated Position Timeline row when a position is stated or shifts, keeping a contradicted earlier position with `> [!warning] Contradiction`; one Accumulation Log line; the Raw in `source` and a new `date_modified`. Never change `personaMaturity` and never create a Persona during ingest.

For a GitHub file, `## Original Content` comes from the raw file at a pinned commit (`raw.githubusercontent.com/{owner}/{repo}/{sha}/…`), never a rendered-page scrape.

## Step 4 — Connect

After Step 3's readback, add `[[wikilinks]]` between all related pages, create or update the relevant Map (MOC), and leave no orphan: every new page is linked from at least one other page.

## Step 5 — Update index and log

Update `index.md`, completing all four:

- each new Wiki page under its section (Concepts, Entities, Guides, Maps) as `- [[Page Name]] — one-line description`;
- the Stats table recounted from the folders (Raw Sources, Wiki Pages, Concepts, Entities, Guides, MOCs, Queries), never incremented by guess;
- one Recent Ingests row at the top: date, Raw link, pages touched;
- the index's modification date.

Re-read `index.md` and confirm every new page appears. When the vault has no `index.md`, create it with those sections and say so in the report.

Append to `log.md`, never editing earlier entries:

```markdown
## [YYYY-MM-DD] ingest | {source title}

- Source: [[{raw source filename}]]
- **Purpose**: {collectionPurpose verbatim}
- Mothership links: {mainVaultRelated count} — {top 1-2 paths}
- Pages created: [[page1]], [[page2]], ...
- Pages updated: [[page3]], [[page4]], ...
```

Git history does not replace `index.md` or `log.md`. Ingest never commits or pushes; when the owner separately asks for a commit, its subject is `ingest: {source title}`.

## Step 6 — Review

Check every item and fix failures:

- the Raw has `## Original Content` with a substantive verbatim body (compared against the Inbox body before any deletion);
- the Inbox original is deleted when deletion was authorized, otherwise reported as awaiting cleanup;
- every new `source`, `related` and body wikilink resolves, except intentional person wikilinks in `author`, which may have no note; no Entity or author note was created only to make a link resolve; no duplicate page was created;
- every updated existing page still holds every valid statement, link and frontmatter value of its before-image, apart from reviewed corrections;
- every new Wiki page has `explored: false`; every `confidence: high` page has a Bias Check with `Counter-argument:` and `Data gap:` lines;
- every `mainVaultRelated` link resolves on the mothership filesystem with both `vault` and `file` percent-encoded, no literal placeholder remains, `mainVaultCmds` holds only a reference the mothership actually registers, copied exactly, and no bare `[[…]]` to a mothership note appears in a body;
- every new page appears in `index.md` and the Stats counts match the folders;
- the `log.md` entry is appended;
- the qmd index status is known: when `reindex` reports pending or failed work, run it and report the result.

## Output

Report: the source (title, URL); where the Raw was saved; pages created, each with one line; pages updated and what changed; key connections added; the touched count against 10–15; originals in `referenced` or provenance unknown; Inbox and binary originals left in place; any branch stopped by an upstream conflict, with the exact conflict; open questions, gaps and contradictions.

## Paper Mode

Follow [papers](references/papers.md) with [paper hub](templates/paper-hub.md) and [paper atom](templates/paper-atom.md): P-0 purpose and target RQ, P-1 paper type, P-2 Raw, P-3 hub and knowledge atoms across the twelve axes, P-4 Wiki promotion, P-5 RQ sync for an owner-designated RQ only, P-6 `index.md` (hub only) and `log.md` (`ingest-paper`), P-7 verification with `scripts/verify_paper.py` plus a read-back (a PASS is necessary, not proof of fidelity). The question budget is exactly two, P-0 and P-1: P-0 carries the Step 0 purpose question, a purpose the task already states is used without asking, and Step 0-a runs without a question, recording stat-verified and owner-confirmed links only. Promote only what the paper supports, updating existing pages before creating; a shortfall against P-4's target is reported, never padded. There is no blanket Scale, RQ or Persona promotion.

## Book Mode

Follow [books](references/books.md): Steps 0 and 0-a once for the whole book, B-1 TOC and chapter URL pattern, B-2 Book Index, B-3 chapter stubs, B-4 a small set of book-level pages, B-5 `index.md` and one `log.md` entry; on Promotion append `## [YYYY-MM-DD] promote | {book} ch{NN}`. Never compile unread chapter content.

Upstream contradiction on this branch only: Book Mode saves the Index and stubs in the Articles folder with `category: Articles`, while the schema reserves the Books folder for books. When the live policy or the owner's task names the folder and `category` for books, follow it. Otherwise run Steps 0, 0-a and B-1, then stop before the B-2 and B-3 writes and report the conflict with the TOC found.

## Tools

Pages: `defuddle`; transcripts: `defuddle`, `yt-dlp`; pages behind login or JavaScript: the aside browser; search: `qmd`; app operations: `obsidian-cli`.
