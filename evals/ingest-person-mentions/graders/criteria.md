---
type: llm
weight: 1
---

Score the response against the `ingest` skill's Step 3 Entity placement, Step 4 person-mention linking and Step 6 bounded lint rules. All seven must hold for a pass:

1. The new Entity goes into the People folder the live policy registers under Entities, not the owner's personal `People` folder and not an invented folder.
2. Only the `Field Notes Method` mention is linked, by wrapping the existing text in brackets (`[[Dana Reyes]]`, or `[[Dana Reyes|Dana Reyes]]`), with the rest of the sentence unchanged.
3. The `Team Rituals` mention ("Dana" alone) is not linked and is reported as an ambiguous or unconfirmed candidate.
4. Nothing inside the Raw, the block quote or the URL is linked or edited.
5. The repeated `Ethnography Basics` mention is neither linked nor reported as a candidate, because that page already holds a resolving link to `Dana Reyes`.
6. One `lint` run follows in report mode only, scoped to exactly the files this ingest created or changed; the rest of the vault is used only as a read-only source for inbound-link lookup, and pages that link in are not added to the lint scope.
7. The response does not have that lint run apply fixes or call ingest again, and does not present it as a replacement for the Raw fidelity checks or `verify`.

Pass only if all seven hold. Linking `Team Rituals` or the repeated `Ethnography Basics` mention, moving or creating a note in the personal `People` folder, linting inbound-link pages or the whole vault, or running lint in fix mode is a fail.
