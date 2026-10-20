# Three-column comparison

Upstream: 구요한 `/audit`, commit `54cf2ab` (Codex command as baseline; Claude mirror for formulas and report layout). The row labels identify every upstream section and Phase; this is the decision record, not a second runtime procedure. The procedure is written in this package's own words; no upstream file is copied.

| 구요한 (54cf2ab) | secondbrain audit before this revision | Decision + reason |
| --- | --- | --- |
| Prerequisite: read Core Context once per session | live policy only | Restore: read Core Context once per session plus live placement policy; reuse axes are whatever its §2 registers (owner exception: no fixed 7 list). |
| Relation to /verify: planner vs worker | planner vs worker | Adopt verbatim framing. |
| Input: `--full`, `--moc`, `--recent`, `--confidence high`, `--no-save`, `--compare` | Step 0 scope in prose | Restore all flags; `--recent` reads `date_modified` (owner snake_case exception). Saving without `--no-save` still asks first (owner exception: save on approval). Never widen scope unasked. |
| Conceptual Framework: 지식요건해당성 / 정합성 / 확증가능성, Claim Type taxonomy, Evidence Scope levels | criteria paraphrased as eligibility gaps, disagreement, confidence | Adopt his three names, Korean included; the taxonomy and levels stay owned by `verify`, named not restated. |
| Scaling Strategy table | absent | Adopt; the Confirmability row adds disputed pages, matching his Phase C. |
| Phase 0 — Inventory: Wiki pages, MOCs, Raw, Queries, membership, audit-orphan pages | Step 1 Inventory | Restore; MOC becomes Map, folders from live policy; Map-as-parent-context stated inline. |
| Phase A.1 — Frontmatter coverage: claimType, evidenceScope, confidence, explored, mainVaultRelated, verificationStatus | Step 2 sweep | Restore the six keys plus `source`/`related`; Raw `collectionPurpose` presence; dropped the non-upstream `purpose_origin`/`source_locator` checks. |
| Phase A.2 — SPO structure: H1, Sources, Related | Step 2 | Adopt; Bias Check on high-confidence pages added here. |
| Phase A.3 — Source citation density, synthesis-only must declare `evidenceScope` | synthesis pages noted | Restore: an undeclared synthesis-only page is a finding. |
| Phase A.4 — Policy violations (YAML/body indent, quoted wikilinks, Mermaid labels, layer mismatch) | absent | Restore the list as counted from the live policy; intentional `author` wikilinks exempt (owner exception); repair routed to `lint`. |
| Phase A output: coverage table, top-20 paths, Eligibility score | n/total plus 20 paths | Restore including the score, scoped to the examined pages. |
| Phase B — Consistency Clusters steps 1–4 and the four drift kinds | Step 3 | Restore; hallucination suspects reported in Phase B output as upstream; primary-vs-secondary independence stated inline. |
| Phase B conflict default: `disputed: true` + `> [!warning] Disputed Claim` via `/verify --resolve` | Contradiction callout via verify | Restore `disputed: true`, set only by `verify --resolve` with owner authorization; callout is `> [!warning] Contradiction` (owner exception). Audit queues, never writes. |
| Phase B concurrency: one sub-task per MOC | parallel subagents | Adopt, with ingest's delegation rule: paths in, one line per finding out, lighter model. |
| Phase B audit-orphan handling: per-tag pseudo-cluster (top-3 tags) or uncluster-able | same | Restore. |
| Phase B output incl. Consistency score formula | per-cluster findings | Restore lists and `100 − 5×conflicts − 10×hallucination − 2×policy`, floored at 0. |
| Phase C — Confirmability Sampling: all high, stale explored:false (>30d by date modified), disputed, random 10% stratified | Step 4 same four groups | Restore in his order; age from `date_modified`; disputed = `disputed: true` or `verificationStatus: disputed`. |
| Phase C abbreviated /verify Phase 3: source counts, counter-evidence (Grep + qmd), recommended confidence, over/underclaim, Bias Check | Step 4 | Restore; audit proposes confidence, never writes it or `verificationStatus`. |
| Phase C concurrency: batches of ~20 in parallel | absent | Adopt. |
| Phase C output: calibration table, over/underclaim, Bias Check %, Confirmability score | report table | Restore including the score. |
| Phase D — Synthesis: three 0–100 scores + composite Vault Health | Step 5 ranking, no score | Restore the three scores and composite; each stated as covering only the examined scope. |
| Phase D Top 10 actions and priority signals | Step 5 | Restore his four signals, STALE FLAG first (his Failure Mode 4); each `verify [[Page]] — reason`. |
| Phase E — Save report to `30. Queries/…-Q-vault-audit.md` with query-result frontmatter unless `--no-save` | save on approval | Restore filename and query-result note; owner exception: save only on approval, at the live policy's query location, snake_case date keys, vault template. |
| Phase E body sections incl. `## Vault Health` and `## Drift Since Last Audit` | report.md | Restore all sections incl. Vault Health and Drift. |
| Phase E append to `log.md` | no log | Restore the append-only entry, written only when the save is approved; a no-save run writes nothing. Git history never replaces it; no automatic commit. |
| Output: terminal summary with Vault Health and three scored criteria | report in conversation | Restore Vault Health, scored criteria, Top 10, report path, drift; emoji decoration omitted. |
| Failure Mode 1 — MOC out of sync | same | Adopt; route to `lint` Map sync. |
| Failure Mode 2 — Oversized cluster (50+) | 40+ split | Restore the 50+ threshold; tiny-cluster merging dropped. |
| Failure Mode 3 — Sample bias | same | Adopt. |
| Failure Mode 4 — Audit storm, `STALE FLAG` | repeat flag | Adopt his name and escalation. |
| Failure Mode 5 — Concurrency safety | writing during audit | Restore; the only writes are the approved report and log entry, in Phase E. |
| Failure Mode 6 — Confirmability vs source ground truth | same | Adopt. |
| Failure Mode 7 — Action list explosion | cap at ten | Adopt. |
| (none) | silent coverage loss | Keep as Failure Mode 8: unread = not examined; scores cover only the examined scope. |
| Integration: consumes v5 keys; lint vs audit; Top 10 feeds /verify; `--moc` after ingest | Neighbours | Adopt the division and incremental audit; v5 keys only when the vault uses them. |
| Scheduling Suggestion: lint weekly, audit monthly | absent | Not adopted as a rule; the owner sets the cadence. |
