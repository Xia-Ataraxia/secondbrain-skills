---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

You are running the `ingest` skill from the secondbrain-skills plugin on an article. Load that skill before answering.

Situation during Step 1 (Analyze): the article says "A 2021 Biology Letters paper by Lindenfors and colleagues found that the 95% confidence interval for the cognitive limit on group size spans 2 to 520 people." You located the paper's canonical address, https://doi.org/10.1098/rsbl.2021.0158, and searched the vault: no Raw, Book Index or Inbox candidate for that paper exists.

Answer in a few sentences, exactly per the skill:
1. What goes into the article Raw's `referenced` frontmatter for this claim, and do you fetch the paper?
2. Who is the claim attributed to?
3. If a new Concept page rests only on this claim, what is the highest `confidence` it may carry?
4. What would change if the paper were already in the vault as a Raw?
