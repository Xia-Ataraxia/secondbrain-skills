---
type: paper-analysis
aliases:
  - "{{surname}} {{year}} S{{NN}}"
description: "{{english_one_line_on_the_single_question_this_atom_answers}}"
author:
  - "{{live_policy_author_or_agent_role}}"
model: {{runtime_model}}
effort: {{runtime_effort_or_default}}
date_created: {{today}}
date_modified: {{today}}
tags:
  - paper-analysis
  - "{{paperType}}"
paperType: {{paper_type}}
citekey: "{{citekey}}"
analysisStep: {{integer_2_to_12}}
analysisStepName: "{{step_name_exactly_as_in_papers_md}}"
paperHub: "[[{{surname}} {{year}} - S00 Hub]]"
source:
  - "[[{{raw_source}}]]"
related:
  - "[[{{sibling_atom}}]]"
status: {{completed|stub}}
explored: false
verificationStatus: unverified
---

# {{surname}} {{year}} - S{{NN}} {{atom_title}}

> [!info] Analysis Context
> **Paper**: {{authors}} ({{year}}), *{{paper_title}}* — [[{{surname}} {{year}} - S00 Hub|hub]] · [[{{raw_source}}|원문]]
> **수집 맥락**: "{{collectionPurpose_gist}}" → {{RQ_link_or_단순 수집}}
> **위치**: Step {{N}} / 12 — {{step_name}} ({{paperType}}) · 원문 §{{section}}
> **이 원자**: {{the_one_question}}. 인접 원자: [[{{neighbour}}]]

<!-- A stub (progressive) keeps only the Analysis Context and one line under 쉬운 도입 stating the question. -->

---

## 쉬운 도입

{{one_or_two_paragraphs_for_a_reader_new_to_the_idea}}

---

## 정밀 해설

{{the_authors_definition_and_argument_with_mechanisms_and_distinctions}}

---

## 예시

- {{example_from_the_original}}
- 【분석자 주】 {{analyst_example_marked_as_not_the_authors}}

---

## 원문 근거

<!-- Guidance: two to six quotes per atom, not a quota. Hard: verbatim from the Raw's Original Content and a page-first locator in every header. -->

> [!quote] 원문 (p.{{page}}, §{{section}})
> "{{verbatim_from_raw_original_content}}"

---

## 개념 관계

- 논증 내 역할: {{what_breaks_without_this_atom}}
- [[{{sibling_atom}}]]: {{distinction_or_link}}
- Wiki: [[{{promoted_page}}]]

---

## 내 원고 맥락

{{optional_reading_against_targetManuscript}}

---

## Open Questions

> [!question] Open Question
> {{point_to_recheck_in_the_original}}
