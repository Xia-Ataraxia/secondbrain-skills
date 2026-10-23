---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

You are running the `lint` skill from the secondbrain-skills plugin in report mode on the `Wiki` folder. Load that skill before answering.

The destination's live policy registers `Wiki/Entities/People` for person Entities and `Wiki/Entities` for other Entities. You observe:

- `Wiki/Entities/Dana Reyes.md` has `tags: [person]`.
- `Wiki/Entities/Acme Labs.md` has `tags: [organization]`.
- `Wiki/Entities/Mira Sol.md` has no tags; its body opens "Mira Sol is a field researcher who ran the 2023 survey."
- `Wiki/Entities/Quinn Vale.md` has no tags, no description and no identity statement; its body only lists two dates.
- `Wiki/Entities/People/Lee Park.md` has `tags: [person]`; the Concept `Pairing` says "Lee Park reviewed the first draft." as plain prose, and no other Entity or alias is named Lee Park.
- The Concept `Code Review` already has a resolving `[[Lee Park]]` link and later says "Lee Park approved the merge." as plain prose.
- The Concept `Team Rituals` says "Lee suggested a weekly retro." There is also an Entity `Lee Moreno`.

Answer in a few sentences, exactly per the skill:
1. Which placement findings or candidates, if any, do you report, and under which section?
2. How do you report the three "Lee" mentions?
3. What does this run write?
