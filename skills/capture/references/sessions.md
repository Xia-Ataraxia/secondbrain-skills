# Agent sessions (owner extension)

Not in 구요한's `/capture-tabs`; added by the owner. It uses the same note shape, fields and routes as the main procedure.

## Unit: the topic

Several selected sessions that worked on one subject become one research-bundle note. Unlike a multi-platform bundle, each member had its own task: record that task as its role; do not line members up as rival answers.

## Building a bundle

1. The owner names the topic and the sessions, or a bounded way to find them ("today's sessions about the inbox redesign"). Read only through an available read-only runtime interface or an owner-selected export. Never sweep every session, schedule exports or archive whole sessions.
2. One Source Manifest row per session: runtime as platform, session title, session id and selected range as URL/locator, the task given as role, and capture status.
3. `captureMode` per member by density:
   - `curated-excerpts` — default for a working session: the owner's own turns verbatim and the agent's conclusions, with tool output named as an omission;
   - `transcript` — a short session, or one whose reasoning is itself the point;
   - `manifest-only` — a session that could not be read.
4. Write at the dated path in the destination's agent-session lane when its live policy defines one, else the AI Research lane. A later session on the same topic is a new note listing the earlier one in `referenced`.

In Agent Capture Notes, "disagreements between platforms" becomes where members differ in task, result or real disagreement; add the owner's concerns and decisions with the member each came from.

## Honesty limits

- Say a session was read only when a real tool read it. If no interface or export is available, write a manifest-only note or report unsupported; never claim capture.
- Never claim the whole session or bundle was captured when only part was. Report partial members as `partial` with the obtained range.
- A runtime report, a transcript and a machine ledger are different records; a report's sections do not prove a transcript was acquired.
- A line range in an export is not a turn range unless the exporter says so.
- Never fill missing messages from a summary; reconstruction belongs in Agent Capture Notes.
