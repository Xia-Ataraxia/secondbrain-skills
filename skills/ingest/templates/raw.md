---
type: raw-source
aliases:
  - "{{short_name}}"
description: "{{english_one_or_two_sentences}}"
author:
  - "[[{{original_author}}]]"
model: {{runtime_model}}
effort: {{runtime_effort_or_default}}
date_created: {{today}}
date_modified: {{today}}
date_ingested: {{acquisition_date}}
date_published: {{publication_date_when_known}}
date_clipped: {{capture_date_when_carried_over}}
tags:
  - raw-source
  - {{topic_tag}}
source: "{{canonical_url_or_reference}}"
category: {{Articles|Papers|Books|Transcripts|Clippings|AI Research|live_policy_registered_category}}
collectionPurpose: "{{owner_answer_verbatim_or_stated_inference_with_reason}}"
source-vault: "{{mothership_vault_name}}"
mainVaultRelated: []
mainVaultCmds: {{registered_mothership_category_or_command_reference_in_live_policy_form_or_empty}}
referenced: []
status: ingested
# Omit date_published, date_clipped and source-vault when inapplicable.
# Converted document: add source-attachment, source-format, conversion-tool, conversion_date, conversion-fidelity.
# Fill slots as YAML-serialized values: one author item per person; a name containing " or \ is escaped by YAML double-quoted rules inside "[[...]]".
# mainVaultRelated entries: "[label](obsidian://open?vault=<encoded vault>&file=<encoded path>)".
---

# {{title}}

> [!info] Source
> 원본 출처: {{source}}

---

## Original Content

{{verbatim_source_content}}

---

## Metadata

- **인제스트 일시**: {{ingest_datetime}}
- **원본 형태**: {{original_form}}
- **언어**: {{language}}
- **분량**: {{length}}

## Ingest Notes

{{deduplicated_clipper_artifacts_conversion_limits_batched_inbox_files_or_delete_this_section}}
