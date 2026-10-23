# Frontmatter — single source

Schema of 구요한's cmds-llm-wiki at commit `54cf2ab150f866bbfcf1aa2c7e03514d14febe20`: `CLAUDE.md` Frontmatter Standards, `90. Settings/Templates/Template_Raw Source.md`, `90. Settings/Templates/Template_Wiki Page.md` and the Claude/Codex `ingest.md` Step 2–3 blocks. Two owner exceptions only: date keys are snake_case, and `referenced` lists originals and earlier captures. The destination's live policy wins wherever it defines a field, value or placement; this schema fills the rest. One meaning has one field.

## Writing rules

- YAML frontmatter is indented with 2 spaces; the Markdown body with tabs.
- Wikilinks inside YAML are double-quoted: `"[[Name]]"`. Body wikilinks are bare.
- `description` is English, one or two sentences, always double-quoted (`description: ""` when empty).
- Dates are ISO 8601 (`YYYY-MM-DD`, time optional). An existing value keeps its form.
- New keys are camelCase, except the snake_case date keys below and the upstream kebab-case keys kept as named (`source-vault`, `source-attachment`, `source-format`, `conversion-tool`, `conversion-fidelity`, `superseded-by`). The owner's snake_case date keys are exactly `date_created`, `date_modified`, `date_ingested`, `date_published` and `conversion_date`; upstream's verification-field timestamps `exploredDate` and `verifiedAt` keep their upstream names.
- Unknown applicable metadata stays unknown, never invented. An inapplicable optional key is omitted.
- Fill every slot as a value serialized by YAML's own rules, never by pasting raw text. A person name containing `"` or `\` inside a double-quoted `"[[Name]]"` follows YAML double-quoted escaping (`\"`, `\\`). Emit lists as YAML lists, one item per existing value; never collapse several existing items into one string.
- A Persona's `source` keeps every existing item as a separate list item and appends this Raw.

## Required on every note (7) plus provenance

| Key | Value |
| --- | --- |
| `type` | role value from the table below |
| `aliases` | list of alternative names |
| `description` | English, double-quoted |
| `author` | list. People are quoted wikilinks `"[[Name]]"` whether or not that note exists; a missing target is not a reason to create an Entity. Raw: the original author(s). Wiki and other agent-written pages: the author the live policy names, otherwise the writing agent's role name (`Claude`, `Codex`, …) as upstream. |
| `date_created` | creation date of this note |
| `date_modified` | last modification date of this note |
| `tags` | list |
| `model`, `effort` | directly after `author` on every agent-written content page: the runtime-reported model id (a list when several contributed) and reasoning effort, `default` when unreported. Never fabricate a model. |

No `created_by` or `authorship` default. A vault whose live policy defines its own provenance keys (for example `created_by`) gets exactly those values from that policy; never infer them.

## Roles

| Role | type | layer | status | Template |
| --- | --- | --- | --- | --- |
| Raw Source | `raw-source` | — | `ingested` | raw.md |
| Book Index (Raw) | `raw-source` | — | `ingested` | book-index.md |
| Book chapter (Raw) | `raw-source` | — | `stub` → `reading` → `completed` | book-chapter.md |
| Concept | `wiki-page` | `concepts`; Paper promotions `theory`, `method` or `scale` | `active` | concept.md |
| Entity | `wiki-page` | `entities` | `active` | entity.md |
| Guide | `wiki-page` | `guides` | `active` | guide.md |
| Map | `moc` | — | `active` | live Map template |
| Persona | `persona` | — | — | persona.md |
| Paper hub | `paper-hub` | — | `active` | paper-hub.md |
| Paper atom | `paper-analysis` | — | `completed` or `stub` | paper-atom.md |

`category` names the Raw kind: `Articles`, `Papers`, `Books`, `Transcripts`, `Clippings` or `AI Research`, plus any value the destination's live policy registers for its own Raw lanes (for example a personal `Mail` lane). It selects the Raw folder of the same kind in the destination. Never invent a value the live policy does not list.

## Raw Source keys

| Meaning | Key | Notes |
| --- | --- | --- |
| Original address or reference | `source` | Canonical URL or reference. A capture bundle with several member URLs keeps them as a list. |
| Kind | `category` | One of the six values above or a value the live policy registers. |
| Processing state | `status` | `ingested`; chapter stubs per the Roles table. |
| Acquisition date | `date_ingested` | When the source was taken into the vault; for a chapter stub, the scaffold date. |
| Publication date | `date_published` | The original's own date when known (Web Clipper `published`). |
| Language | `language` | The source's language code, such as `en` or `ko`. |
| Length | `length` | The source's size as stated or counted, such as `12 pages` or `3,400 words`. |
| Collection purpose | `collectionPurpose` | The owner's answer verbatim, or the stated inference and its reason when the owner delegated it. |
| Mothership vault | `source-vault` | Only when a mothership is configured. |
| Mothership notes | `mainVaultRelated` | Stat-verified `"[label](obsidian://open?vault=<encoded vault>&file=<encoded path>)"` list, both components encoded with `urllib.parse.quote(value, safe='')`; `[]` when none. |
| Mothership category | `mainVaultCmds` | A category or command reference the Core Context or mothership actually registers, copied exactly in its registered form and with the cardinality the live policy defines; empty when none fits. Never invented. |
| Originals and earlier captures | `referenced` | List. A wikilink when the original or earlier capture is already a Raw or Book Index in the vault, otherwise its canonical URL. It records where a claim came from; it never proves the original was read and never authorizes fetching it. |
| Retained document | `source-attachment` | `"[[original-filename]]"` of the binary moved into the attachments folder. |
| Converted format | `source-format` | `pdf`, `pptx`, `docx`, `hwp`, `hwpx`, … |
| Converter | `conversion-tool` | `markitdown`, `pandoc`, `hwp5txt`, `defuddle`, `hwpx-xml`, … |
| Conversion date | `conversion_date` | Date of the conversion. |
| Conversion fidelity | `conversion-fidelity` | `high`, `medium` or `low`. |
| Newer version | `supersedes` / `superseded-by` | Source Update, major change: new `-v2` Raw points back with `supersedes`; the earlier Raw gains `superseded-by`. |
| Paper | `citekey`, `doi`, `targetManuscript` | Paper Mode Raw; same values as the hub. |
| Book chapter | `bookIndex`, `chapterNumber`, `chapterPart`, `chapterPrev`, `chapterNext` | Chapter stubs only: quoted wikilink, integer, original-language part name, quoted wikilinks or `null` at the ends. |

## Wiki page keys

| Meaning | Key | Notes |
| --- | --- | --- |
| Evidence | `source` | Quoted wikilink list of Raw Sources. Add the new Raw on every update; keep earlier entries. |
| Related knowledge | `related` | Quoted wikilink list. |
| Confidence | `confidence` | `high` (well-sourced), `medium` (partial), `low` (speculative). A page resting only on secondary claims is not well-sourced. |
| Reuse unit | `layer` | Per the Roles table. |
| Exploration gate | `explored` | `false` on every new page; `true` only after a human read it or a source-backed review loop verified it, with optional `exploredBy`, `exploredDate`. |
| Verification state | `verificationStatus` | `unverified` on every new page; `verify` sets `verified`, `partial`, `unverified` or `disputed` with `verifiedAt`, `verifiedBy`. |
| Claim classification | `claimType`, `evidenceScope` | Optional at ingest; record only when the classification is clear. `claimType`: `definition`, `empirical`, `theoretical`, `historical`, `prescriptive`, `interpretive` or `mixed`. `evidenceScope`: `single-source`, `multi-source-primary`, `multi-source-mixed`, `synthesis-only` or `user-original`. |
| Conflict | `disputed` | Set only by `verify`; `audit` only queues it, ingest never sets it. |
| Page state | `status` | `active`. |
| Mothership links | `mainVaultRelated`, `mainVaultCmds` | Optional, same form as on the Raw. |
| Persona | `personaOf`, `personaMaturity`, `personaDomains` | Persona only; ingest never changes `personaMaturity`. |
| Paper | `paperType`, `citekey`, `doi`, `targetManuscript`; atoms add `analysisStep` (integer 2–12), `analysisStepName`, `paperHub` | Paper Mode only. |
| Map | `topic`, `related` | Map only. |

## Existing notes and migration

New notes use the schema above. A run that touches an existing note preserves what it already holds.

- Keep every existing key and value, including unknown keys and earlier identity, location and history values. Ordinary ingest changes only the keys its update names (`source`, `related`, `date_modified` and additions the preservation review accepted); it renames, re-forms, copies or removes nothing else, date keys and `author` values included. The one exception is ingest Step 4's Entity reference resolution, which changes only a confirmed reference's link form or target, never its key, role or meaning.
- Identity matching reads `source` first, and any other source address or locator the existing note already records; titles never prove sameness. Ingest requires no identity key beyond this schema.
- Key migration runs only when the owner explicitly authorizes it for named notes. Record each note's before-image first; map a value only when its meaning is verified equivalent to the target key (`source_obtained_at` is not `date_ingested` without proof that both record the same acquisition); stop on any conflict, such as a target key already holding a different value or an ambiguous meaning, and report it. A completed migration leaves one key per meaning, with no permanent dual keys. A value still needed for identity, location or history is never dropped merely as legacy.
