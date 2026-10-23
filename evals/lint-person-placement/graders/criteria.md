---
type: llm
weight: 1
---

Score the response against the `lint` skill's Step 11 placement rule and Step 2 person-mention candidates. All seven must hold for a pass:

1. `Dana Reyes` (by its `person` tag) and `Mira Sol` (by its identity statement) are reported as placement findings under Policy Conformance (Step 11), naming `Wiki/Entities/People` as the registered folder; neither needs a new person field.
2. `Quinn Vale` is reported as a placement candidate only, because nothing recorded settles its kind; it is not called a person from its name and gets no definite finding.
3. `Acme Labs` and `Lee Park` get no placement finding.
4. The `Pairing` mention is reported as an unlinked person-mention candidate for `Lee Park`, not as a definite error or proof of identity.
5. The repeated `Code Review` mention is not reported, because that page already holds a resolving link to `Lee Park`.
6. The `Team Rituals` "Lee" mention is reported as ambiguous (shared by `Lee Park` and `Lee Moreno`, or first name only), not attributed to one person.
7. The run writes nothing: no move, no link added, no `log.md` entry.

Pass only if all seven hold. Moving any Entity, classifying `Quinn Vale` as a person, linking any mention, flagging the `Code Review` mention, or calling a mention a confirmed missing link is a fail.
