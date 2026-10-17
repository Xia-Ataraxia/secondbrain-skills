---
type: llm
weight: 1
---

Score the response against the `ingest` skill's Step 1 rule for secondary claims. All five must hold for a pass:

1. The paper's canonical URL (https://doi.org/10.1098/rsbl.2021.0158) is placed in the article Raw's `referenced` list.
2. The response states that the paper is NOT fetched, downloaded, ingested or made into its own Raw during this run. Any plan to fetch it, run Paper mode on it, or create a Raw or Inbox candidate for it is a fail.
3. The claim is attributed to the article's author as a secondary claim, not to Lindenfors as a primary claim in the vault.
4. A Concept resting only on this secondary claim is capped at `confidence: medium` (not high).
5. If the paper were already in the vault as a Raw, `referenced` would hold a wikilink to that Raw instead of the URL.

Pass only if all five hold. A response that hedges between fetching and linking fails item 2.
