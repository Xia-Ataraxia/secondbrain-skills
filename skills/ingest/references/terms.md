# Terms

A Term page explains a name a field uses. This file owns what becomes a Term, its title and its sections; `lint` checks existing pages against it.

## What is a Term

- A Term is a name an established field uses independently of this source: self-contained jargon with one meaning (`ReplicaSet`) and a shared word whose meaning varies by field (`AI Agent`) are both Terms.
- One page per name when its senses are related, that is when one definition can state what they share (AI Agent: anything that perceives its environment and acts on it, which covers both the reinforcement learning agent and the LLM-based agent).
- Unrelated meanings under one name are separate Terms (`Transformer (Machine Learning)` and `Transformer (Electrical Engineering)`).
- A named individual thing (a product, service, model, dataset or organization such as `OpenClaw` or `Claude Code`) is an Entity. The Term links to it as an example.
- A name only one author uses is a Concept until an independent source uses it.

## Title

Apply in order:

1. The full name in its original language. A Korean title only when the term originates in Korean.
2. `Full Name (ACRONYM)` when the field uses an acronym.
3. A parenthetical qualifier only when two unrelated Terms would otherwise share a title.
4. Everything else goes to `aliases`: translations, other scripts, spelling variants, years, former and incorrect forms.

The title uses the correct current form; an incorrect or former expansion stays in `aliases` and is named as such in `## Origin`. No space inside the parentheses.

## Sections

Follow [term](../templates/term.md):

- **Definition:** the definition the field shares, with its status: `consensus`, `contested` or `emerging`. Claim `consensus` only when the sources show it.
- **Origin:** the word's etymology, its first documented use (who, where, when, cited from the primary source) and when each later sense appeared. An unknown point is written as unknown.
- **Senses:** only when the meaning varies by field. One `### {field}` section per sense, with that field's definition, since when it is used that way, and examples. List those fields in `domain`; self-contained jargon needs no `domain`.
- **Literature Review:** one entry per source, attributed, walked up to the source that establishes the claim.
- **Personal Insights:** the owner's own notes. Ingest leaves this section as it finds it.
- **Related Terms:** typed as broader, narrower, related or confused-with. A Term is never both broader and related to the same page. A relation that holds for one sense goes in that sense section.

When a sense's definition shifts, keep the earlier definition with its date and source and add the new one; never overwrite.

Link a Term as a whole page, never a heading inside it (`[[Term#Section]]`).
