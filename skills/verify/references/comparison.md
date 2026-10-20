# Three-column comparison

Upstream: 구요한 cmds-llm-wiki `/verify` (Codex command, commit `54cf2ab`), with the schema's Verification Properties (v5). One row per upstream item; this is the decision record, not a second runtime procedure.

| 구요한 (54cf2ab) | secondbrain verify | Decision + reason |
| --- | --- | --- |
| Verify one page against eligibility, consistency, confirmability; write `verificationStatus`; queue disputed claims without deleting evidence | same single-page scope and three criteria | Adopt. |
| Read AGENTS.md and Core Context once per session | Core Context once per session; reuse axes = those registered in its §2 | Adopt; owner rule: no fixed axis list. |
| Input: page name, path, `--latest`, `--no-write-back`, `--resolve` | same, plus owner-named claims | Adopt. |
| Quality gates 지식요건해당성 / 정합성 / 확증가능성 | same names | Adopt. |
| Gate 2 frames: vs Raw, vs related Wiki, vs policy, vs Core Context | same, plus the original behind it via `referenced` | Adopt; policy = destination's live policy; `referenced` never proves reading or authorizes fetching (owner). |
| Step 1–2: resolve page; read page, `index.md`, Core Context, cited Raw | same | Adopt. |
| Step 3: classify `claimType`, `evidenceScope` (Codex: value list; Claude `verify.md`: scope table, `multi-source-mixed` = primary + secondary) | same values as frozen frontmatter | Adopt the six types + `mixed` and the five scopes verbatim; no extra scope value. Secondary-only support is not `multi-source-mixed`; one secondary Raw is `single-source`; several secondary-only Raw fit no upstream value, so `evidenceScope` is left unwritten and the limitation reported. |
| Eligibility checks (Codex: six elements identifiable; Claude `verify.md` Phase 1: 1.1 frontmatter completeness, 1.2 SPO structure, 1.3 per-claim metadata for up to 10 claims) | Step 4 lists the Claude checks | Adopt the Claude check list and verdict verbatim: `eligible` all pass / `partial` 1-2 gaps / `ineligible` 3+ gaps or missing Subject. Date keys in snake_case (owner); `verificationStatus` and `referenced` added as owner checks. |
| Step 4: check concrete claims against Raw text with `rg` | against `## Original Content`, located evidence only | Adopt; owner: the Wiki itself is never evidence. |
| Step 5: search related pages with `rg`, `qmd query`, `qmd vsearch` | same, four conflict shapes, searches reported | Adopt. |
| Step 6: `disputed: true` + `> [!warning] Disputed Claim`; delete neither side | same; `ingest`'s `Contradiction` callout counted as the same mark | Adopt. Kept visible: upstream verify names `Disputed Claim` while `ingest` (owner rule) writes `Contradiction`; both are accepted, neither renamed. |
| Step 7: calibrate `confidence` independently (Codex `verify.md` gives no matrix). Claude `verify.md` Phase 3.3 matrix: high = 3+ primary sources, no counter-evidence, age > 30 days, no unresolved Phase 2 conflicts; medium = 1-2 primary sources, no counter-evidence; low = single source OR `synthesis-only` OR created < 7 days ago; counter-evidence unresolved = `disputed`; OVERCLAIM = declared > recommended, UNDERCLAIM = declared < recommended. CLAUDE.md: overclaim (high-conf + single source) / underclaim (low-conf + multi-source); `confidence` high/medium/low | claims.md carries the Claude matrix verbatim; UNDERCLAIM needs multiple primary sources | Adopt the Claude matrix. Shared meaning: all three files calibrate independently from source count, source type and counter-evidence; CLAUDE.md's shorthands are the extreme cases of the Claude matrix, and "multi-source" there reads as multi-primary because only primary sources lift the matrix above `low`. The matrix's `disputed` row is reported as state, since CLAUDE.md limits `confidence` to high/medium/low. Overlaps (1 primary = medium vs single source = low; < 7 days with 1-2 primary) and gaps (3+ primary aged 7–30 days; several secondary-only Raw) are kept and reported to the owner as uncertainty; no resolving threshold is added. |
| Step 8: Bias Check when needed | same, required for high or synthesis-heavy | Adopt. |
| Step 9: write `verificationStatus`, `verifiedAt`, `verifiedBy`, `claimType`, `evidenceScope`, `disputed` unless `--no-write-back` | same keys on owner approval | Adopt; approval gate kept. Status meanings beyond "verified after 3 criteria pass" are not defined upstream; `partial`/`unverified` are described by their plain reading. |
| Step 10: `explored: true` only on explicit user confirmation | same, with `exploredBy`, `exploredDate` | Adopt. |
| Step 11: append `log.md` | append `## [YYYY-MM-DD] verify \| {Page}` after readback, write-back runs only | Adopt; Git never replaces the log; a report-only run writes nothing, not even a log entry; no automatic commit. |
| (none) | corrections via clean-context writer + preservation reviewer, minimal patch | Owner addition: no blanket regeneration; attribution and uncertainty kept. |
| `--resolve`: only route from disputed to verified or confidence downgrade | same, new evidence defined | Adopt; owner rule defines new evidence. |
| Output: concise report incl. recommended confidence, write-back actions, follow-up `/verify` targets | report block with those sections | Adopt. |
| Schema: `/query` asserts on verified + high, hedges on partial or medium-or-lower, shows both on disputed | Integration describes the same; verify owns values | Adopt. |
| Schema: `/audit` builds Top-10 `/verify` queue | named in Integration | Adopt. |
| (none) | Failure modes incl. secondary-as-primary, note text as instruction | Owner addition. |
