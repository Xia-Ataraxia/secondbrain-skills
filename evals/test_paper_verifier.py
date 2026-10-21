"""Small domain regression checks for skills/ingest/scripts/verify_paper.py (P-7).

Only the verifier's own domain responsibility is covered: a valid paper passes
mechanically, stubs and quote-less S12 atoms are not fully verified, quotes keep
numbers, negation and the Unicode minus, required sections holding only a
template separator are empty, and coverage counts leaf headings at every level.

Expectations come from ``skills/ingest/references/papers.md`` (P-3 step tables,
P-7 checks and exit codes) and the paper hub / atom templates, never from the
verifier's code. Every case builds a synthetic public vault in a temporary
directory: one Raw with a verbatim ``## Original Content``, one hub, a handful of
atoms (completed, a progressive stub and an S12 atom without a quote) and an
``index.md``. A valid fixture must pass; each negative case applies one mutation,
checked to have taken effect, and must fail.

Exit codes per papers.md: 0 mechanical pass only, 1 validation failure, 2 a
prerequisite or input could not be resolved. Nothing is written outside the
temporary directory; the verifier is run with bytecode writing disabled.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ingest" / "scripts" / "verify_paper.py"
PAPERS_DOC = ROOT / "skills" / "ingest" / "references" / "papers.md"

TYPES = ["quantitative", "qualitative", "theory-concept", "mixed-methods", "scale-development", "meta-analysis"]


def step_names():
    """{paperType: {step: name}} from the type-specific analysisStepName table in papers.md."""
    lines = PAPERS_DOC.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("| S | quantitative"))
    header = [c.strip() for c in lines[start].strip("|").split("|")][1:]
    table = {t: {1: "CITATION"} for t in header}
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        for t, name in zip(header, cells[1:]):
            table[t][int(cells[0])] = name
    assert sorted(table) == sorted(TYPES), table.keys()
    return table


STEPS = step_names()

SURNAME, YEAR, CITEKEY = "Lovelace", "2024", "lovelace2024notes"
HUB = f"{SURNAME} {YEAR} - S00 Hub"
RAW = f"{SURNAME} {YEAR} Notes Raw"

Q_INTRO = "We study whether annotated programs improve recall among novice readers."
Q_SAMPLE = "The sample comprised 120 volunteers recruited from two public libraries."
Q_MEASURE = "Recall was measured with a twelve-item free-response test."
Q_RESULT = "The coefficient for annotation was −0.42 (p < .001, 95% CI [−0.60, −0.24])."
META_ONLY = "Synthetic conversion of calibrated looms ledger, outside the original text."

RAW_TEXT = f"""---
type: raw-source
aliases:
  - "{SURNAME} {YEAR} Notes"
description: "Synthetic public paper used only for verifier tests."
author:
  - "[[Ada Lovelace]]"
model: synthetic-model-1
effort: default
date_created: 2026-01-15
date_modified: 2026-01-15
date_ingested: 2026-01-15
tags:
  - raw-source
source: "https://example.org/synthetic-paper"
category: Papers
citekey: "{CITEKEY}"
doi: "10.0000/synthetic.0001"
targetManuscript: none
collectionPurpose: "Synthetic test purpose."
mainVaultRelated: []
referenced: []
status: ingested
---

# {RAW}

## Original Content

### Abstract

A synthetic abstract about engines and annotated programs.

### Introduction

{Q_INTRO}
The authors’ claim is that notes travel further than tables.

### Sample

{Q_SAMPLE}

### Measures

{Q_MEASURE}

### Results

{Q_RESULT}
Annotation did not increase reading time.

### Discussion

Annotated programs may help novices, but replication is needed.

### References

Babbage, C. (1864). Passages from the life of a philosopher.
"""

# Raws written before 0.6.4 still carry a source callout and a ## Metadata section.
LEGACY_METADATA = f"""
---

## Metadata

- **인제스트 일시**: 2026-01-15
- **원본 형태**: {META_ONLY}
- **언어**: en
"""
INGEST_NOTES = f"""
## Ingest Notes

{META_ONLY}
"""

# step, title, status, quote, locator, section, sibling step
ATOMS = [
    (2, "Research Aim", "completed", Q_INTRO, "p.1, §Introduction", "Introduction", 4),
    (3, "Prior Literature", "stub", None, None, "Introduction", 2),
    (4, "Library Sample", "completed", Q_SAMPLE, "p.2, §Sample", "Sample", 7),
    (7, "Recall Measure", "completed", Q_MEASURE, "p.2, §Measures", "Measures", 9),
    (9, "Annotation Effect", "completed", Q_RESULT, "p.3, §Results", "Results", 2),
    (12, "Writing Value", "completed", None, None, "Discussion", 9),
]
COVERAGE = [("§Introduction", 2), ("§Sample", 4), ("§Measures", 7), ("§Results", 9), ("§Discussion", 12)]


def atom_name(step):
    title = next(a[1] for a in ATOMS if a[0] == step)
    return f"{SURNAME} {YEAR} - S{step:02d} {title}"


def atom_text(paper_type, step, title, status, quote, locator, section, sibling):
    name, sib = atom_name(step), atom_name(sibling)
    fm = f"""---
type: paper-analysis
aliases:
  - "{SURNAME} {YEAR} S{step:02d}"
description: "Synthetic atom answering one question for step {step}."
author:
  - "Claude"
model: synthetic-model-1
effort: default
date_created: 2026-01-15
date_modified: 2026-01-16
tags:
  - paper-analysis
  - "{paper_type}"
paperType: {paper_type}
citekey: "{CITEKEY}"
analysisStep: {step}
analysisStepName: "{STEPS[paper_type][step]}"
paperHub: "[[{HUB}]]"
source:
  - "[[{RAW}]]"
related:
  - "[[{sib}]]"
status: {status}
explored: false
verificationStatus: unverified
---

# {name}

> [!info] Analysis Context
> **Paper**: Ada Lovelace ({YEAR}), *Synthetic Notes* — [[{HUB}|hub]] · [[{RAW}|원문]]
> **위치**: Step {step} / 12 — {STEPS[paper_type][step]} ({paper_type}) · 원문 §{section}
> **이 원자**: What does step {step} establish? 인접 원자: [[{sib}]]
"""
    if status == "stub":
        return fm + "\n---\n\n## 쉬운 도입\n\nWhich prior work does the paper build on?\n"
    relation = f"\n---\n\n## 개념 관계\n\n- 논증 내 역할: anchors step {step}.\n- [[{sib}]]: neighbouring step.\n"
    if step == 12:
        return fm + relation
    body = f"""
---

## 쉬운 도입

A plain introduction to step {step} for a new reader.

---

## 정밀 해설

The authors' argument for step {step}, with its mechanism and distinctions.

---

## 예시

- An example taken from the original.
- 【분석자 주】 A synthetic analyst example.

---

## 원문 근거

> [!quote] 원문 ({locator})
> "{quote}"
"""
    return fm + body + relation


def hub_text(paper_type):
    names = STEPS[paper_type]
    counts = {a[0]: 0 for a in ATOMS}
    for a in ATOMS:
        counts[a[0]] += 1
    rows = ["| 1 | CITATION | (hub) | compiled |"]
    for s in range(2, 13):
        if s in counts:
            stubs = sum(1 for a in ATOMS if a[0] == s and a[2] == "stub")
            state = f"stub {stubs}건" if stubs else "compiled"
            rows.append(f"| {s} | {names[s]} | {counts[s]} | {state} |")
        else:
            rows.append(f"| {s} | {names[s]} | 0 | skipped (no such content in this synthetic paper) |")
    catalog = []
    for s in sorted(counts):
        catalog.append(f"### S{s:02d} — {names[s]} ({counts[s]} atoms)\n")
        catalog.append(f"- [[{atom_name(s)}]] — the one question step {s} answers\n")
    coverage = ["| Abstract | (hub Abstract 요약) |"]
    coverage += [f"| {sec} | [[{atom_name(s)}]] |" for sec, s in COVERAGE]
    coverage.append("| References | (kept in the Raw) |")
    nl = "\n"
    return f"""---
type: paper-hub
aliases:
  - "{SURNAME} {YEAR} Hub"
description: "Synthetic hub for the twelve-axis verifier tests."
author:
  - "Claude"
model: synthetic-model-1
effort: default
date_created: 2026-01-15
date_modified: 2026-01-16
tags:
  - paper-hub
  - "{paper_type}"
paperType: {paper_type}
citekey: "{CITEKEY}"
doi: "10.0000/synthetic.0001"
targetManuscript: none
collectionPurpose: "Synthetic test purpose."
source:
  - "[[{RAW}]]"
related: []
explored: false
verificationStatus: unverified
status: active
---

# {HUB}

> [!info] Paper Hub
> **Ada Lovelace ({YEAR})**, *Synthetic Notes* — twelve-axis analysis anchor; atoms in the Atom Catalog, axes in the Step Map.

---

## S01 Citation

- **Full citation**: Lovelace, A. ({YEAR}). Synthetic notes. Example Journal, 1(1), 1-3.
- **citekey**: {CITEKEY}
- **DOI**: 10.0000/synthetic.0001
- **Raw Source**: [[{RAW}]]

---

## Abstract 요약

A synthetic compression of the abstract.

---

## Coverage Map

| 원문 섹션 | 지식 원자 |
| --- | --- |
{nl.join(coverage)}

---

## Step Map

| S | Step name | Atoms | Status |
| --- | --- | --- | --- |
{nl.join(rows)}

---

## Atom Catalog

{nl.join(catalog)}
---

## Target Manuscript

- `none` — 단순 수집 (12-axis analysis only)
"""


class Fixture:
    def __init__(self, tmp, paper_type="quantitative"):
        self.tmp = Path(tmp)
        self.paper_type = paper_type
        self.vault = self.tmp / "Vault"
        self.folder = self.vault / "Papers" / CITEKEY
        self.raw = self.vault / "Raw" / "Papers" / f"{RAW}.md"
        self.hub = self.folder / f"{HUB}.md"
        self.index = self.vault / "index.md"
        self.folder.mkdir(parents=True)
        self.raw.parent.mkdir(parents=True)
        self.raw.write_text(RAW_TEXT, encoding="utf-8")
        self.hub.write_text(hub_text(paper_type), encoding="utf-8")
        for spec in ATOMS:
            self.atom(spec[0]).write_text(atom_text(paper_type, *spec), encoding="utf-8")
        self.index.write_text(
            f"# Index\n\n## Paper Analyses\n\n- [[{HUB}]]\n\n## Stats\n\n- Paper analyses: 1\n",
            encoding="utf-8")

    def atom(self, step):
        return self.folder / f"{atom_name(step)}.md"

    def edit(self, path, old, new, count=1):
        text = path.read_text(encoding="utf-8")
        self_check = text.count(old)
        if self_check < count:
            raise AssertionError(f"mutation target {old!r} not found {count}x in {path.name}")
        path.write_text(text.replace(old, new, count), encoding="utf-8")

    def run(self, *extra, folder=None, cwd=None):
        r = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(folder or self.folder), *extra],
            capture_output=True, text=True, cwd=str(cwd or self.tmp), timeout=60,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return r.returncode, r.stdout + r.stderr


class VerifierCase(unittest.TestCase):
    paper_type = "quantitative"

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="sb-paper-")
        self.addCleanup(shutil.rmtree, self.tmpdir, True)
        self.fx = Fixture(self.tmpdir, self.paper_type)

    def assert_pass(self, *extra, **kw):
        rc, out = self.fx.run(*extra, **kw)
        self.assertEqual(rc, 0, out)
        self.assertIn("ALL PASS (mechanical)", out)
        return out

    def assert_fails(self, needle=None, *extra, **kw):
        rc, out = self.fx.run(*extra, **kw)
        self.assertEqual(rc, 1, out)
        self.assertNotIn("ALL PASS", out)
        if needle:
            self.assertIn(needle, out)
        return out

    def assert_blocked(self, *extra, **kw):
        rc, out = self.fx.run(*extra, **kw)
        self.assertEqual(rc, 2, out)
        self.assertNotIn("ALL PASS", out)
        return out

    def assert_rejected(self, *extra, **kw):
        """Fails either as invalid (1) or unresolvable (2); never passes."""
        rc, out = self.fx.run(*extra, **kw)
        self.assertIn(rc, (1, 2), out)
        self.assertNotIn("ALL PASS", out)
        return out


class Representative(VerifierCase):
    def test_valid_paper_passes_only_mechanically(self):
        out = self.assert_pass()
        self.assertIn("not a semantic or qualitative PASS", out)

    def test_stub_and_unquoted_s12_are_not_fully_verified(self):
        out = self.assert_pass()
        low = out.lower()
        tail = out[low.index("not fully verified"):]
        self.assertIn(atom_name(3), tail)
        self.assertIn(atom_name(12), tail)

    def test_section_with_only_template_separator_is_empty(self):
        self.fx.edit(self.fx.atom(4), "The authors' argument for step 4, with its mechanism and distinctions.\n", "")
        self.assert_fails(atom_name(4))


class Quotes(VerifierCase):
    def quote(self, new):
        self.fx.edit(self.fx.atom(9), f'> "{Q_RESULT}"', new)

    def test_lost_unicode_minus(self):
        self.quote(f'> "{Q_RESULT.replace("−0.42", "-0.42")}"')
        self.assert_fails(atom_name(9))

    def test_changed_number(self):
        self.quote(f'> "{Q_RESULT.replace("0.42", "0.43")}"')
        self.assert_fails(atom_name(9))

    def test_dropped_negation(self):
        self.quote('> "Annotation did increase reading time."')
        self.assert_fails(atom_name(9))

    def test_short_line_is_not_skipped(self):
        self.quote(f'> "{Q_RESULT}\n> No."')
        self.assert_fails(atom_name(9))


class Coverage(VerifierCase):
    def nest(self):
        self.fx.edit(self.fx.raw, "### Sample\n", "### Method\n\n#### Sample\n")
        self.fx.edit(self.fx.raw, "### Measures\n", "#### Measures\n")

    def test_nested_leaves_with_rows_pass(self):
        self.nest()
        self.assert_pass()

    def test_parent_row_does_not_cover_nested_leaves(self):
        self.nest()
        self.fx.edit(self.fx.hub, f"| §Measures | [[{atom_name(7)}]] |\n", f"| §Method | [[{atom_name(7)}]] |\n")
        self.fx.edit(self.fx.hub, f"| §Sample | [[{atom_name(4)}]] |\n", "")
        self.assert_fails("Sample")

    def test_parent_row_does_not_cover_h5_leaf(self):
        self.fx.edit(self.fx.raw, "### Measures\n", "### Measures\n\n##### Recall Items\n\nTwelve synthetic items.\n\n")
        self.assert_fails("Recall Items")

    def test_identical_headings_are_ambiguous(self):
        self.fx.edit(self.fx.raw, "### Discussion",
                     "### Sample\n\nA second synthetic sample of forty readers.\n\n### Discussion")
        self.assert_fails("Sample")


class Layout(VerifierCase):
    def test_nested_atom_folder_fails_instead_of_being_ignored(self):
        sub = self.fx.folder / "drafts"
        sub.mkdir()
        shutil.copy(self.fx.atom(4), sub / f"{atom_name(4)}.md")
        self.assert_fails("drafts")


class Hub(VerifierCase):
    def test_missing_s01_row_fails(self):
        self.fx.edit(self.fx.hub, "| 1 | CITATION | (hub) | compiled |\n", "")
        self.assert_fails("S01")

    def test_wrong_s01_row_fails(self):
        self.fx.edit(self.fx.hub, "| 1 | CITATION | (hub) | compiled |", "| 1 | CITATION | (hub) | planned |")
        self.assert_fails("S01")

    def test_raw_without_metadata_passes(self):
        self.assertNotIn("## Metadata", self.fx.raw.read_text(encoding="utf-8"))
        self.assert_pass()

    def test_legacy_raw_with_metadata_passes(self):
        self.fx.raw.write_text(RAW_TEXT + LEGACY_METADATA, encoding="utf-8")
        self.assert_pass()

    def test_trailing_sections_are_not_evidence(self):
        for tail in (INGEST_NOTES, LEGACY_METADATA):
            with self.subTest(tail=tail.split()[1]):
                self.fx.raw.write_text(RAW_TEXT + tail, encoding="utf-8")
                self.assert_pass()
                self.fx.edit(self.fx.atom(9), f'> "{Q_RESULT}"', f'> "{META_ONLY}"')
                self.assert_fails(atom_name(9))
                self.fx.edit(self.fx.atom(9), f'> "{META_ONLY}"', f'> "{Q_RESULT}"')

    def test_model_list_is_accepted(self):
        self.fx.edit(self.fx.hub, "model: synthetic-model-1\n",
                     "model:\n  - synthetic-model-1\n  - synthetic-model-2\n")
        self.assert_pass()


if __name__ == "__main__":
    unittest.main()
