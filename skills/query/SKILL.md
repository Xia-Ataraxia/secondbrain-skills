---
name: query
description: Search Wiki pages, synthesize a cited answer, optionally save to 30. Queries/, and feed gaps/contradictions back into the Wiki.
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__qmd__query
# Antigravity equivalents: view_file, write_to_file, replace_file_content, list_dir, grep_search, run_command
license: MIT
metadata:
  version: "0.5.5"
---

# /query — LLM Wiki Query

Answer a question by searching the wiki, synthesizing information, and optionally saving the result.

> **🧭 Prerequisite**: [[Core Context]] once per session. Tailor answers to the owner's reuse axes listed in [[Core Context]] §2 — a good answer connects to at least one axis. The axes are the owner's own; do not assume a fixed list or count.

## Input

`$ARGUMENTS`

## Process

### Step 1: Search

Read `index.md` to identify relevant pages. Then read those pages in full.
If the question spans multiple topics, read pages from each relevant area.

### Step 2: Synthesize

Compose a comprehensive answer based on wiki content:
- Cite sources with `[[wikilinks]]` to specific wiki pages
- If information is from raw sources, reference via the wiki page that compiled it
- Note confidence level based on source quality

### Step 3: Identify Gaps

While answering, note:
- Questions the wiki **cannot** answer → flag as knowledge gaps
- Contradictions discovered between pages → add `> [!warning]` callouts
- Missing pages that would help → suggest for future ingest
- Missing `mainVaultRelated`, `explored`, or Bias Check coverage → flag as quality-control gaps

### Step 4: Save (if substantial)

If the answer is substantial (comparison, analysis, multi-source synthesis), save it:
- File: `30. Queries/YYYY-MM-DD-Q-{question-summary}.md`
- Type: `query-result`
- Include referenced pages in `source` property

If it's a simple factual answer, just reply without saving.

### Step 5: Feedback

Update wiki pages if the query revealed:
- Missing cross-references → add them
- Outdated information → flag with `> [!note] Update`
- New connections between concepts → add to `related` properties
- High-confidence synthesis without a counter-argument or data-gap note → add `> [!note] Bias Check`

### Step 6: Connect to User's Reuse Axes

Before finalizing, ask which of the owner's reuse axes the answer feeds — see [[Core Context]] §2. If none fits, say so.

Add a closing line to the answer: **"이 답변은 ${axis}에 활용 가능합니다 — ${one-sentence why}."**

If saving as Query Result, set `reusableFor` frontmatter to the matched axis.

## Output

Answer the question, then briefly note:
- Pages consulted
- Whether result was saved
- Any gaps or contradictions found
- Reuse axis the answer connects to
