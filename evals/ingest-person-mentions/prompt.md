---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

You are running the `ingest` skill from the secondbrain-skills plugin on an article. Load that skill before answering.

Situation during Step 3: the article is by Dana Reyes, and the analysis found her significant, so you create a person Entity `Dana Reyes` with alias `D. Reyes`. The destination's live policy registers an Entities folder with a People folder inside it; the owner's personal vault also has a `People` folder. Searching this vault's Wiki finds:

- Concept `Field Notes Method`: "Dana Reyes, the ethnographer who wrote this article, coined the term." Plain prose; no other Entity is named Dana.
- Concept `Team Rituals`: "Dana suggested a weekly retro." No surname or other context.
- Concept `Interview Craft`: a block quote `> Dana Reyes: "Ask twice."` and a URL `https://example.org/dana-reyes`.
- Concept `Ethnography Basics`: its first paragraph already has a resolving `[[Dana Reyes]]` link; a later paragraph says "Dana Reyes revised the method in 2024." in plain prose.
- The Raw you just saved contains "Dana Reyes" in `## Original Content`.

Answer in a few sentences, exactly per the skill:
1. Which folder does the new Entity go into?
2. Which of the five mentions do you link, and what exactly does the edited text look like?
3. What happens to the others?
4. What lint run follows, on what scope, and may it apply fixes?
