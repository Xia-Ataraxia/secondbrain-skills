---
type: persona
aliases: {{existing_aliases}}
description: "{{existing_description}}"
author: {{existing_author_list}}
model: {{existing_model_plus_runtime_model}}
effort: {{runtime_effort_or_default}}
date_created: {{existing_date_created}}
date_modified: {{today}}
tags: {{existing_tags}}
personaOf: "[[{{existing_entity}}]]"
personaMaturity: {{existing_value_unchanged}}
personaDomains: {{existing_domains}}
source: [{{existing_raw_sources}}, "[[{{this_raw_source}}]]"]
related: {{existing_related}}
# Only date_modified changes and this Raw is appended to source. Never change personaMaturity (verify- or owner-gated).
# existing_raw_sources: every item already in source, in order, each kept as its own YAML item ("[[A]]", "[[B]]"); never merged into one string.
# Fill each slot with a YAML-serialized value: list slots as lists, a name containing " or \ escaped by YAML double-quoted rules.
---

# {{existing_persona_title}}

<!-- Append recipe for an EXISTING Persona card only (Step 3.5). Never create a Persona during ingest; creation is owner-nominated. Keep every existing key, value and section; change only what is listed here. -->

## Quote Bank

<!-- Append 1–3 quotes; each must grep-match this Raw's ## Original Content verbatim. -->
> [!quote] {{topic}} ({{YYYY-MM-DD}}, [[{{this_raw_source}}]])
> {{verbatim_quote}}

## Position Timeline

<!-- Append one dated row only when the source states or shifts a position. -->
| Date | Position | Source |
| --- | --- | --- |
| {{YYYY-MM-DD}} | {{attributed_position}} | [[{{this_raw_source}}]] |

<!-- Only when this source explicitly conflicts with an earlier position; keep both rows. Silence is not a contradiction. -->
> [!warning] Contradiction
> {{earlier_position_with_source}} / {{new_position_with_source}}

## Accumulation Log

- {{YYYY-MM-DD}} · [[{{this_raw_source}}]] → {{what_was_added}}
