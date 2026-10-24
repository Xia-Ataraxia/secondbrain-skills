# Three-column comparison

Upstream: 구요한 `/onboard`, commit `54cf2ab`. At that commit it exists only as `claude/commands/onboard.md`; there is no Codex command or agent wrapper, so the Claude command is the counterpart. The kit ships `Core Context.md`, `index.md` and `log.md` as placeholder files that onboarding fills. One row per upstream step or section; this is the decision record, not a second procedure.

| 구요한 (54cf2ab) | secondbrain onboard | Decision + reason |
| --- | --- | --- |
| Intro: freshly-cloned kit → your wiki in ~10 min; driver for `Setup Guide.md` | starting template folder, no Setup Guide dependency | Adapt: starting template instead of a cloned kit. |
| Philosophy 1–4: Context-first, Answer-1-of-many, Agent-does-the-typing, Resume-safe | same four | Adopt verbatim names. |
| Pre-flight: pwd, placeholder grep count, Core Context status | `rg` pre-flight with branches | Adopt; owner adds: empty target scaffolded only with explicit authorization, copying only missing files and preserving existing ones byte-for-byte; existing vault with owner notes gets read-only diagnosis and proposal. |
| Kit ships `Core Context.md`, `index.md`, `log.md` | scaffold includes all three; missing ones created from the template shape on a fresh target | Adopt: index and log are restored; Git never replaces them. Existing vault: missing index/log are proposed, not created (`ingest` creates `index.md` on first run). |
| Interview 필수 5 + 옵션 2; voice 1 / text batch; confirm 1–2 sentences | same | Adopt. |
| Q1 위치 & 이름 | same | Adopt. |
| Q2 운영 모드 Mode A / Mode B | same; mothership read-only always | Adopt. |
| Q3 (Mode B) 모선 경로·이름 | same plus existence and `obsidian-cli` registration check | Adopt with checks. |
| Q4 §1 정체성 + 연속성 선언 | same | Adopt. |
| Q5 §2 재활용 축 5–9 (7 권장) | 5–9 owner-defined axes; examples only as prompts | Adopt range; never a fixed list. These registered axes feed `ingest` Step 1. |
| 옵션 §3 프레임워크 / §4 철학 3–5 | same | Adopt. |
| Failure mode: passive 모드 | same; nothing invented | Adopt. |
| Fill F1 placeholder sed (Mode A / B) | same token lists, fresh targets only | Adapt: never replaces tokens in an existing vault's files. |
| Fill F2 Core Context: draft, confirm, template→active, snapshot_date, version 1.0, Mode A delete §5 | same | Adopt. |
| Fill F3 verification grep | re-run pre-flight `rg -l` | Adopt. |
| (absent) | settings for an existing vault: proposal of exact keys, never written | Owner addition: no mutation of existing notes, JSON, config or settings. |
| Resume logic: placeholders → F1; template → F2 | same; existing vault stays read-only | Adopt. |
| Pre-flight grep counts `{your-name}`, `{PATH_TO_YOUR_LLM_WIKI}`, `{your-mothership-vault-name}` together; F3 says mothership tokens are harmless in Mode A | separate Mode A and Mode B token checks | Adapt: upstream's F1 split (Mode A tokens vs Mode B mothership tokens) and F3 note applied to completion detection, so a Mode A vault with only mothership tokens left counts as complete and a missing Mode A value never does. Upstream does not say how to tell the mode afterwards; this package takes Mode B only from the owner's Q2 choice or a concrete registered mothership (real path and name), never from the template's §5 heading. |
| Wrap-up 1–5: /status, /ingest with axis answer (미래의 나에게 보내는 편지), /query, Research Question / Synthesis cards, qmd + Web Clipper via Setup Guide | same; item 5 → `capture`/`inbox`/`reindex` | Adopt items 1–4; item 5 adapted; owner adds read-back. |
| Pointer to mothership kit `cmds-onboarding` | absent | Reject: external kit not part of this repo. |
| allowed-tools incl. AskUserQuestion | `rg`, `sed`, `cp`, `obsidian-cli` | Adapt: plain-text questions. |
| (absent) | no install, sync, migration, ingest, deletion or commit as side effect | Owner addition: commit only when the owner separately asks. |
