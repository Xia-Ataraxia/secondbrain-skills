#!/usr/bin/env python3
"""Archive agent CLI sessions (Claude Code, Codex, OpenCode, Cursor, GJC, OmO, Grok) as one chat Raw per session.

usage: agent-sessions.py --vault ROOT --out REL --purpose TEXT --model NAME [--attachments REL]
                         [--host NAME[=ROOT]]... [--tool claude,codex,opencode,cursor,gjc,omo,grok] [--dry]
       agent-sessions.py --check

--out and --attachments are relative to the vault root. Notes go to <out>/<runtime>/; every original
session file goes gzip-compressed to <attachments>/<host>/<runtime>/ and is named in the note's
source_attachment. --host without a root is this machine; a root is a copy of a remote home (rsync)
with the same layout. A rerun skips sessions whose source_identity a note already carries.
"""
import argparse, datetime as dt, glob, gzip, json, pathlib, re, shutil, socket, sqlite3, sys, tempfile, urllib.parse

try:
    from compression import zstd  # Python 3.14+; Codex rewrites archived sessions as .jsonl.zst
except ImportError:
    zstd = None

VAULT = OUT = ATT = None  # set by main()/check()
ATT_REL = LOCAL = PURPOSE = MODEL = ""
TODAY = dt.date.today().isoformat()
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
LABEL = {"claude": "Claude Code", "codex": "Codex", "opencode": "OpenCode", "cursor": "Cursor", "gjc": "GJC", "omo": "OmO", "grok": "Grok"}
FOLDER = {"claude": "claude-code"}
HARNESS = re.compile(r"^\s*(<(command-message|local-command-stdout|local-command-caveat|system-reminder|task-notification|environment_context|user_instructions|permissions instructions|turn_aborted|app_context|collaboration_mode|skills|apps)\b|# AGENTS\.md instructions|Caveat: The messages below|This session is being continued from|Another Claude session|Base directory for this skill|Stop hook feedback:|A session-scoped Stop hook|Goal check-in:)")
SLASH = re.compile(r"<command-name>(.*?)</command-name>.*?<command-args>(.*?)</command-args>", re.S)
GROK_WRAP = re.compile(r"<(user_info|rules)>.*?</\1>\s*", re.S)  # Grok prepends these blocks to the owner's prompt
SNAP = None


def user_text(t):
    """Drop harness injections; turn slash-command records into `/cmd args`."""
    m = SLASH.search(t or "")
    if m:
        return f"{m.group(1).strip()} {m.group(2).strip()}".strip() if m.group(2).strip() else ""
    if t and (t.lstrip().startswith("<command-name>") or HARNESS.match(t)):
        return ""
    return t or ""


def ts(x):
    if x in (None, ""):
        return None
    if isinstance(x, (int, float)):
        return dt.datetime.fromtimestamp(x / 1000 if x > 1e11 else x).astimezone()
    try:
        return dt.datetime.fromisoformat(str(x).replace("Z", "+00:00")).astimezone()
    except ValueError:
        return None


class S:  # one session
    def __init__(self, tool, host, sid, cwd, locator):
        self.tool, self.host, self.id, self.cwd, self.locator = tool, host, sid, cwd or "", locator
        self.title = self.model = self.url = self.resume = self.remote = ""
        self.turns, self.limits = [], []
        self.omitted = {"thinking": 0, "tool_call": 0, "tool_result": 0}
        self.rows = None  # db-backed sessions: callable yielding the raw rows as JSON lines

    def add(self, role, text, when):
        text = (text or "").strip()
        if not text:
            return
        if self.turns and self.turns[-1]["role"] == role:
            self.turns[-1]["text"] += "\n\n" + text
        else:
            self.turns.append({"role": role, "text": text, "ts": when})

    def tool_call(self, name, args, when):
        self.omitted["tool_call"] += 1  # the note is the owner's record; the original attachment holds every call

    def ok(self):
        roles = {t["role"] for t in self.turns}
        return "user" in roles and "assistant" in roles

    def first_user(self):
        return next((t["text"] for t in self.turns if t["role"] == "user"), "")


# ---------- readers ----------
def read_claude(path, host):
    s = S("claude", host, pathlib.Path(path).stem, "", path)
    for line in open(path, errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t = d.get("type")
        if t in ("ai-title", "custom-title"):
            s.title = d.get("aiTitle") or d.get("customTitle") or s.title
        elif t == "summary" and not s.title:
            s.title = d.get("summary") or ""
        if t not in ("user", "assistant") or d.get("isSidechain") or d.get("isMeta") or d.get("isCompactSummary"):
            continue
        s.cwd = s.cwd or d.get("cwd", "")
        s.id = d.get("sessionId") or s.id
        m = d.get("message") or {}
        when = ts(d.get("timestamp"))
        c = m.get("content")
        if t == "user":
            parts = [c] if isinstance(c, str) else [b.get("text", "") for b in c or [] if isinstance(b, dict) and b.get("type") == "text"]
            s.omitted["tool_result"] += sum(1 for b in (c if isinstance(c, list) else []) if isinstance(b, dict) and b.get("type") == "tool_result")
            s.add("user", "\n\n".join(filter(None, map(user_text, parts))), when)
        else:
            s.model = m.get("model") or s.model
            for b in c or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text":
                    s.add("assistant", b.get("text"), when)
                elif b.get("type") == "tool_use":
                    s.tool_call(b.get("name"), b.get("input"), when)
                elif b.get("type") == "thinking":
                    s.omitted["thinking"] += 1
    if host == LOCAL and s.cwd:
        s.url = "claude-cli://open?cwd=" + urllib.parse.quote(s.cwd, safe="")  # the app's own link: project only
    s.resume = f"cd '{s.cwd}' && claude --resume {s.id}"
    return s


def open_text(path):
    if path.endswith(".zst"):
        if not zstd:
            raise RuntimeError("reading .jsonl.zst needs Python 3.14+ (compression.zstd)")
        return zstd.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, errors="replace")


def read_codex(path, host):
    s = S("codex", host, pathlib.Path(path).name.split("-", 1)[-1][20:].split(".")[0], "", path)
    for line in open_text(path):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t, p, when = d.get("type"), d.get("payload") or {}, ts(d.get("timestamp"))
        if t == "session_meta":
            if p.get("thread_source") == "subagent":
                return None
            s.id, s.cwd = p.get("id") or s.id, p.get("cwd", "")
            if p.get("originator"):
                s.limits.append(f"originator: {p['originator']} {p.get('cli_version', '')}".strip())
        elif t == "turn_context":
            s.model = p.get("model") or s.model
        elif t == "response_item":
            k = p.get("type")
            if k == "message" and p.get("role") in ("user", "assistant"):
                text = "\n\n".join(b.get("text", "") for b in p.get("content") or [] if isinstance(b, dict) and b.get("type") in ("input_text", "output_text"))
                s.add(p["role"], user_text(text) if p["role"] == "user" else text, when)
            elif k in ("function_call", "custom_tool_call"):
                s.tool_call(p.get("name"), p.get("arguments") or p.get("input") or "", when)
            elif k in ("function_call_output", "custom_tool_call_output"):
                s.omitted["tool_result"] += 1
            elif k == "reasoning":
                s.omitted["thinking"] += 1
    s.url = f"codex://threads/{s.id}"
    s.resume = f"codex resume {s.id}"
    if "archived_sessions" in path:
        s.limits.append("Archived in Codex.")
    return s


def snapshot(db):
    """Consistent read-only copy (handles WAL while the app runs)."""
    global SNAP
    SNAP = SNAP or pathlib.Path(tempfile.mkdtemp(prefix="agent-sessions-"))
    dst = SNAP / (pathlib.Path(db).name + ".snap")
    src = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    out = sqlite3.connect(dst)
    src.backup(out)
    src.close()
    out.close()
    return dst


def read_opencode(db, host):
    con = sqlite3.connect(f"file:{snapshot(db)}?mode=ro", uri=True)
    for sid, directory, title, share, t0 in con.execute("select id, directory, title, share_url, time_created from session where parent_id is null order by time_created"):
        s = S("opencode", host, sid, directory, f"{db}#session={sid}")
        s.title = title or ""
        s.rows = lambda sid=sid: db_lines(con, sid, (("session", "id"), ("message", "session_id"), ("part", "session_id"), ("session_message", "session_id")))
        rows = con.execute("select m.data, p.data from message m join part p on p.message_id=m.id where m.session_id=? order by m.time_created, p.time_created", (sid,))
        for mdata, pdata in rows:
            try:
                m, p = json.loads(mdata), json.loads(pdata)
            except ValueError:
                continue
            role, when = m.get("role"), ts((m.get("time") or {}).get("created"))
            s.model = m.get("modelID") or s.model
            if p.get("type") == "text" and role in ("user", "assistant"):
                s.add(role, p.get("text"), when)
            elif p.get("type") == "tool":
                st = p.get("state") or {}
                s.tool_call(p.get("tool"), st.get("title") or st.get("input") or "", when)
                s.omitted["tool_result"] += 1
            elif p.get("type") == "reasoning":
                s.omitted["thinking"] += 1
        s.url = share or ""
        s.resume = f"cd '{directory}' && opencode -s {sid}"
        yield s
    con.close()


def read_cursor(db, host):
    con = sqlite3.connect(f"file:{snapshot(db)}?mode=ro", uri=True)
    for key, val in con.execute("select key, value from cursorDiskKV where key like 'composerData:%'"):
        try:
            c = json.loads(val)
        except ValueError:
            continue
        if (c.get("subagentInfo") or {}).get("parentComposerId") or c.get("isBestOfNSubcomposer"):
            continue
        cid = c.get("composerId") or key.split(":", 1)[1]
        uri = (c.get("workspaceIdentifier") or {}).get("uri") or {}
        cwd = uri.get("fsPath", "")
        s = S("cursor", host, cid, cwd, f"{db}#composerData:{cid}")
        if uri.get("scheme") == "vscode-remote" and str(uri.get("authority", "")).startswith("ssh-remote+"):
            s.remote = uri["authority"].split("+", 1)[1]  # the chat is local, the workspace folder is on this SSH host
            s.limits.append(f"The workspace is an SSH remote folder on {s.remote}; the deep link opens that remote window first.")
        s.title = c.get("name") or ""
        s.rows = lambda cid=cid: (jl({"key": k, "value": v}) for k, v in con.execute("select key, value from cursorDiskKV where key=? or key like ?", (f"composerData:{cid}", f"bubbleId:{cid}:%")))
        s.model = (c.get("modelConfig") or {}).get("modelName") or ""
        heads = c.get("fullConversationHeadersOnly") or [{"bubbleId": b.get("bubbleId"), "type": b.get("type")} for b in c.get("conversation") or []]
        for h in heads:
            row = con.execute("select value from cursorDiskKV where key=?", (f"bubbleId:{cid}:{h.get('bubbleId')}",)).fetchone()
            b = c.get("conversation") and next((x for x in c["conversation"] if x.get("bubbleId") == h.get("bubbleId")), None)
            if row:
                try:
                    b = json.loads(row[0])
                except ValueError:
                    b = None
            if not b:
                continue
            when = ts(b.get("createdAt"))
            role = "user" if b.get("type") == 1 else "assistant"
            if role == "assistant":
                s.model = (b.get("modelInfo") or {}).get("modelName") or s.model
            if b.get("text"):
                s.add(role, b["text"], when)
            tf = b.get("toolFormerData") or {}
            if tf.get("name"):
                s.tool_call(tf["name"], tf.get("params") or "", when)
                s.omitted["tool_result"] += 1
            if b.get("thinking"):
                s.omitted["thinking"] += 1
        s.url = ("cursor://file" + urllib.parse.quote(cwd)) if cwd else ""  # the app's own link: workspace only
        s.limits.append("Cursor has no per-chat link; the deep link carries the workspace and composer id for the owner's handler. Without one, find the chat by title in Cursor's history.")
        s.resume = f"open '{cwd}' in Cursor, then pick '{s.title}' in the chat history"
        s.ts0 = ts(c.get("createdAt"))
        yield s
    con.close()


def read_pi(tool, path, host):
    """GJC and OmO share the pi session format (type: session / message / model_change)."""
    s = S(tool, host, pathlib.Path(path).stem.split("_", 1)[-1], "", path)
    for line in open(path, errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t, when = d.get("type"), ts(d.get("timestamp"))
        if t == "session":
            s.id, s.cwd, s.title = d.get("id") or s.id, d.get("cwd", ""), d.get("title") or ""
        elif t == "model_change":
            s.model = d.get("model") or (f"{d.get('provider')}/{d['modelId']}" if d.get("modelId") else s.model)
        elif t == "message":
            m = d.get("message") or {}
            role = m.get("role")
            for b in m.get("content") or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and role in ("user", "assistant"):
                    s.add(role, user_text(b.get("text")) if role == "user" else b.get("text"), when)
                elif b.get("type") == "toolCall":
                    s.tool_call(b.get("name"), b.get("arguments"), when)
                elif b.get("type") == "thinking":
                    s.omitted["thinking"] += 1
                elif role == "toolResult":
                    s.omitted["tool_result"] += 1
    if tool == "gjc":
        s.resume = f"cd '{s.cwd}' && gjc --resume {s.id}"
    else:  # omo --session <id> searches only the current store; sessions in the older ~/.omo/sessions store resume by path
        s.resume = f"cd '{s.cwd}' && omo --session " + (f"'{path}'" if "/.omo/sessions/" in path else s.id)
    return s

def read_grok(path, host):
    """Grok Build: one directory per session; chat_history.jsonl carries no timestamps, summary.json carries the span."""
    d = pathlib.Path(path).parent
    try:
        meta = json.load(open(d / "summary.json"))
    except (OSError, ValueError):
        meta = {}
    info = meta.get("info") or {}
    s = S("grok", host, info.get("id") or d.name, info.get("cwd") or urllib.parse.unquote(d.parent.name), path)
    s.title, s.model = meta.get("session_summary") or "", meta.get("current_model_id") or ""
    s.ts0, s.ts1 = ts(meta.get("created_at")), ts(meta.get("updated_at"))
    for line in open(path, errors="replace"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        t, c = r.get("type"), r.get("content")
        if t == "user" and r.get("synthetic_reason") != "system_reminder":
            text = "".join(b.get("text", "") for b in c if isinstance(b, dict)) if isinstance(c, list) else c or ""
            m = re.search(r"<user_query>(.*?)</user_query>", text, re.S)
            s.add("user", user_text(m.group(1) if m else GROK_WRAP.sub("", text)), None)
        elif t == "assistant":
            s.add("assistant", c if isinstance(c, str) else "", None)
            s.model = r.get("model_id") or s.model
            for call in r.get("tool_calls") or []:
                s.tool_call(call.get("name"), call.get("arguments"), None)
        elif t == "reasoning":
            s.omitted["thinking"] += 1
        elif t == "tool_result":
            s.omitted["tool_result"] += 1
    s.rows = lambda: (l.rstrip("\n") for l in open(path, errors="replace"))  # every session file is chat_history.jsonl; keep it as <id>.jsonl.gz
    s.limits.append("Grok records carry no timestamps; the span is the session's created and updated time, and turns are unstamped.")
    s.resume = f"cd '{s.cwd}' && grok --resume {s.id}"
    return s


# ---------- writer ----------
def jl(obj):
    return json.dumps(obj, ensure_ascii=False, default=lambda b: b.decode("utf-8", "replace") if isinstance(b, bytes) else str(b))


def db_lines(con, sid, tables):
    cur = con.cursor()
    cur.row_factory = sqlite3.Row
    for t, col in tables:
        try:
            for r in cur.execute(f"select * from {t} where {col}=?", (sid,)):
                yield jl({"table": t, **dict(r)})
        except sqlite3.OperationalError:  # older schema without this table
            pass


def raw_rel(s):
    name = f"{s.id}.jsonl" if s.rows else pathlib.Path(s.locator).name
    return f"{ATT_REL}/{s.host}/{s.tool}/{name}" + ("" if name.endswith(".zst") else ".gz")


def keep_raw(s):
    """Copy the original session file (or its db rows as JSON lines) next to the notes, gzip-compressed."""
    dst = ATT / pathlib.Path(raw_rel(s)).relative_to(ATT_REL)
    if dst.exists():
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    if dst.suffix == ".zst":  # already compressed by Codex
        shutil.copyfile(s.locator, tmp)
    else:
        with gzip.open(tmp, "wb", 6) as g:
            if s.rows:
                for line in s.rows():
                    g.write(line.encode("utf-8", "replace") + b"\n")
            else:
                with open(s.locator, "rb") as f:
                    shutil.copyfileobj(f, g)
    tmp.rename(dst)
    return dst


def deep_link(s):
    """agent-session://open?… — the contract for the owner's scheme handler; the note body also carries the resume command."""
    q = {"tool": s.tool, "id": s.id, "cwd": s.cwd, "host": s.remote or ("" if s.host == LOCAL else s.host)}
    return "agent-session://open?" + urllib.parse.urlencode({k: v for k, v in q.items() if v})


def q(x):
    return json.dumps(str(x), ensure_ascii=False)


def safe_name(t):
    t = re.sub(r'[\\/:*?"<>|#^\[\]]+', " ", t)
    return re.sub(r"\s+", " ", t).strip()[:80].rstrip(". ")


def note(s):
    label = LABEL[s.tool]
    title = s.title or s.first_user().strip().splitlines()[0][:60]
    t0 = getattr(s, "ts0", None) or next((t["ts"] for t in s.turns if t["ts"]), None) or dt.datetime.now().astimezone()
    t1 = getattr(s, "ts1", None) or next((t["ts"] for t in reversed(s.turns) if t["ts"]), t0)
    desc = re.sub(r"\s+", " ", s.first_user())[:160]
    speaker = {"user": "You said:", "assistant": f"{label} said:"}
    link = deep_link(s)
    body = [f"# {label} - {title}", "", f"- Runtime: {label}", f"- Host: {s.host}", f"- Working directory: `{s.cwd}`" if s.cwd else "- Working directory: (none)",
            f"- Session id: `{s.id}`", f"- Model: {s.model or '(not recorded)'}", f"- Span: {t0:%Y-%m-%d %H:%M} ~ {t1:%Y-%m-%d %H:%M}",
            f"- Resume: `{s.resume}`" if s.host == LOCAL else f"- Resume: on `{s.host}`, `{s.resume}`", f"- Deep link: [{link}]({link})"]
    if s.url:
        body.append(f"- App link: [{s.url}]({s.url})")
    body += ["", "## Original Content", ""]
    for i, t in enumerate(s.turns, 1):
        when = f" | {t['ts']:%Y-%m-%d %H:%M}" if t["ts"] else ""
        body += [f"### Turn {i} | {speaker[t['role']]}{when}", "", t["text"], ""]
    body += ["## Ingest Notes", "", f"- Extracted from `{s.locator}` on {s.host} by agent-sessions.py.",
             "- Kept: user and assistant text verbatim; tool calls, thinking and tool results are in the original attachment.",
             f"- Omitted: {s.omitted['tool_call']} tool calls, {s.omitted['thinking']} thinking blocks, {s.omitted['tool_result']} tool results."]
    body += [f"- {x}" for x in s.limits]
    fm = f"""---
type: chat
tags: [reference/chat]
date_created: {TODAY}
date_modified: {TODAY}
created_by: agent
authorship: agent
model: {q(MODEL)}
effort: default
aliases: []
description: {q(desc)}
author: []
source_url: {q(link)}
source_locator: {q(f"{s.host}:{s.locator}")}
source_identity: {q(f"urn:{s.tool}:session:{s.id}")}
source_input: file
source_kind: conversation
source_extraction: agent-sessions.py
source_obtained_at: {q(NOW)}
source_attachment: {q(raw_rel(s))}
date_published: {t0:%Y-%m-%d}
purpose: {q(PURPOSE)}
purpose_origin: stated
referenced: []
session_id: {q(s.id)}
---

"""
    return f"{t0:%Y-%m-%d} {label} - {safe_name(title) or s.id[:8]}", f"urn:{s.tool}:session:{s.id}", fm + "\n".join(body) + "\n"


def existing_ids(folder):
    ids = {}
    for p in folder.glob("*.md"):
        with open(p, errors="replace") as f:
            for _ in range(40):
                line = f.readline()
                if line.startswith("source_identity:"):
                    ids[line.split(":", 1)[1].strip().strip('"')] = p
                    break
    return ids


def sources(tools, hosts):
    """(tool, host, store path) for every store under each host root; a root has the layout of a home directory."""
    for host, root in hosts.items():
        r = pathlib.Path(root).expanduser()

        def g(*pats):
            return sorted(p for pat in pats for p in glob.glob(str(r / pat), recursive=True))

        if "claude" in tools:
            for p in g(".claude/projects/*/*.jsonl"):
                if not pathlib.Path(p).stem.startswith("agent-"):  # subagent transcripts belong to their parent session
                    yield "claude", host, p
        if "codex" in tools:
            for p in g(".codex/sessions/**/*.jsonl", ".codex/archived_sessions/**/*.jsonl*"):
                yield "codex", host, p
        if "gjc" in tools:
            for p in g(".gjc/agent/sessions/*/*.jsonl"):
                yield "gjc", host, p
        if "omo" in tools:
            for p in g(".omo/sessions/*/*.jsonl", ".omo/agent/sessions/*/*.jsonl"):
                yield "omo", host, p
        if "grok" in tools:
            for p in g(".grok/sessions/*/*/chat_history.jsonl"):
                yield "grok", host, p
        if "opencode" in tools:
            for p in g(".local/share/opencode/opencode.db"):
                yield "opencode", host, p
        if "cursor" in tools:
            for p in g("Library/Application Support/Cursor/User/globalStorage/state.vscdb", ".config/Cursor/User/globalStorage/state.vscdb"):
                yield "cursor", host, p


def iter_sessions(tool, host, path):
    if tool == "claude":
        yield read_claude(path, host)
    elif tool == "codex":
        yield read_codex(path, host)
    elif tool in ("gjc", "omo"):
        yield read_pi(tool, path, host)
    elif tool == "grok":
        yield read_grok(path, host)
    elif tool == "opencode":
        yield from read_opencode(path, host)
    elif tool == "cursor":
        yield from read_cursor(path, host)


def main():
    global VAULT, OUT, ATT, ATT_REL, LOCAL, PURPOSE, MODEL
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", help="vault root")
    ap.add_argument("--out", help="Raw folder for the notes, relative to the vault")
    ap.add_argument("--attachments", help="folder for the original session files, relative to the vault (default: <out>/_attachments)")
    ap.add_argument("--purpose", help="the owner's purpose for this archive, verbatim")
    ap.add_argument("--model", help="the runtime-reported model of the agent running this")
    ap.add_argument("--host", action="append", metavar="NAME[=ROOT]", help="a host and the root holding its stores; no root means this machine (default: this machine's hostname)")
    ap.add_argument("--tool", default=",".join(LABEL))
    ap.add_argument("--dry", action="store_true", help="count only, write nothing")
    ap.add_argument("--check", action="store_true", help="self-check on synthetic fixtures")
    a = ap.parse_args()
    if a.check:
        return check()
    if not (a.vault and a.out and a.purpose and a.model):
        ap.error("--vault, --out, --purpose and --model are required")
    VAULT, PURPOSE, MODEL = pathlib.Path(a.vault).expanduser(), a.purpose, a.model
    OUT, ATT_REL = VAULT / a.out, a.attachments or f"{a.out}/_attachments"
    ATT = VAULT / ATT_REL
    hosts = {}
    for h in a.host or [socket.gethostname().split(".")[0]]:
        name, _, root = h.partition("=")
        hosts[name] = root or "~"
        LOCAL = LOCAL or ("" if root else name)
    tools = a.tool.split(",")
    stats = {}
    seen = {t: existing_ids(OUT / FOLDER.get(t, t)) | existing_ids(OUT) for t in tools if OUT.exists()}
    for tool, host, path in sources(tools, hosts):
        st = stats.setdefault((tool, host), {"new": 0, "exists": 0, "empty": 0, "error": 0})
        try:
            for s in iter_sessions(tool, host, path):
                if s is None or not s.ok():
                    st["empty"] += 1
                    continue
                name, ident, text = note(s)
                if ident in seen.setdefault(tool, {}):
                    st["exists"] += 1
                    continue
                folder = OUT / FOLDER.get(tool, tool)
                dest = folder / f"{name}.md"
                if dest.exists():
                    dest = folder / f"{name} ({s.id}).md"  # same title and minute: keep the full id
                if not a.dry:
                    folder.mkdir(parents=True, exist_ok=True)
                    keep_raw(s)
                    dest.write_text(text, encoding="utf-8", errors="replace")  # lone surrogates from source JSON
                seen[tool][ident] = dest
                st["new"] += 1
        except Exception as e:  # keep going; report at the end
            st["error"] += 1
            print(f"ERROR {tool} {host} {path}: {e!r}", file=sys.stderr)
    for (tool, host), st in sorted(stats.items()):
        print(f"{tool:9} {host:16} new={st['new']:5} exists={st['exists']:5} empty={st['empty']:5} error={st['error']}")


def check():
    """Self-check on synthetic transcripts: turns, title, harness filtering, deep link, attachment round-trip."""
    global VAULT, OUT, ATT, ATT_REL, LOCAL, PURPOSE, MODEL
    d = pathlib.Path(tempfile.mkdtemp())
    VAULT, ATT_REL, LOCAL, PURPOSE, MODEL = d, "Raw/_attachments", "laptop", "find old sessions again", "model-x"
    OUT, ATT = VAULT / "Raw", VAULT / ATT_REL
    c = d / "11111111-2222-3333-4444-555555555555.jsonl"
    c.write_text("\n".join(json.dumps(x) for x in [
        {"type": "user", "cwd": "/tmp/x", "sessionId": "11111111-2222-3333-4444-555555555555", "timestamp": "2026-01-02T03:04:05Z", "message": {"role": "user", "content": "hello"}},
        {"type": "user", "isMeta": True, "message": {"role": "user", "content": "<command-name>/x</command-name>"}},
        {"type": "user", "timestamp": "2026-01-02T03:04:05Z", "message": {"role": "user", "content": [{"type": "text", "text": "<command-name>/goal</command-name><command-message>goal</command-message><command-args>do it</command-args>"}, {"type": "text", "text": "<system-reminder>x</system-reminder>"}]}},
        {"type": "user", "timestamp": "2026-01-02T03:04:05Z", "message": {"role": "user", "content": "Stop hook feedback:\n[x]"}},
        {"type": "assistant", "timestamp": "2026-01-02T03:04:06Z", "message": {"role": "assistant", "model": "m1", "content": [{"type": "thinking", "thinking": "t"}, {"type": "text", "text": "hi"}, {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}]}},
        {"type": "user", "timestamp": "2026-01-02T03:04:07Z", "message": {"role": "user", "content": [{"type": "tool_result", "content": "a"}]}},
        {"type": "assistant", "timestamp": "2026-01-02T03:04:08Z", "message": {"role": "assistant", "content": [{"type": "text", "text": "done"}]}},
        {"type": "ai-title", "aiTitle": "Say hi"}]))
    s = read_claude(str(c), LOCAL)
    assert s.ok() and s.title == "Say hi" and s.cwd == "/tmp/x" and s.model == "m1", vars(s)
    assert [t["role"] for t in s.turns] == ["user", "assistant"], s.turns
    assert s.turns[0]["text"] == "hello\n\n/goal do it", s.turns[0]["text"]
    assert s.turns[1]["text"] == 'hi\n\ndone', s.turns[1]["text"]
    assert s.omitted == {"thinking": 1, "tool_call": 1, "tool_result": 1}
    name, ident, text = note(s)
    assert name == "2026-01-02 Claude Code - Say hi" and ident == "urn:claude:session:11111111-2222-3333-4444-555555555555"
    assert 'source_url: "agent-session://open?tool=claude&id=11111111-2222-3333-4444-555555555555&cwd=%2Ftmp%2Fx"' in text, text[:900]
    assert 'purpose_origin: stated\nreferenced: []\nsession_id: "11111111-2222-3333-4444-555555555555"\n---' in text and 'model: "model-x"' in text
    assert "- App link: [claude-cli://open?cwd=%2Ftmp%2Fx]" in text and "### Turn 2 | Claude Code said: | 2026-01-02" in text
    assert "- Omitted: 1 tool calls, 1 thinking blocks, 1 tool results." in text and "🔧" not in text
    g = d / "2026-06-16T07-24-39-319Z_019ecf51-6817-7000-a85d-1c96c1d0bb9a.jsonl"
    g.write_text("\n".join(json.dumps(x) for x in [
        {"type": "session", "id": "019ecf51-6817-7000-a85d-1c96c1d0bb9a", "cwd": "/w", "title": "T", "timestamp": "2026-06-16T07:24:39Z"},
        {"type": "message", "timestamp": "2026-06-16T07:24:40Z", "message": {"role": "user", "content": [{"type": "text", "text": "q"}]}},
        {"type": "message", "timestamp": "2026-06-16T07:24:41Z", "message": {"role": "assistant", "content": [{"type": "text", "text": "a"}]}}]))
    s = read_pi("gjc", str(g), "office")
    assert s.ok() and s.title == "T" and not s.url and s.resume.endswith("gjc --resume 019ecf51-6817-7000-a85d-1c96c1d0bb9a")
    assert deep_link(s) == "agent-session://open?tool=gjc&id=019ecf51-6817-7000-a85d-1c96c1d0bb9a&cwd=%2Fw&host=office", deep_link(s)
    assert raw_rel(s) == f"Raw/_attachments/office/gjc/{g.name}.gz" and f'source_attachment: "{raw_rel(s)}"' in note(s)[2]
    assert gzip.open(keep_raw(s)).read() == g.read_bytes()
    o = d / ".omo/sessions/--w--/2026-06-16T07-24-39-319Z_019ecf51-6817-7000-a85d-1c96c1d0bb9a.jsonl"
    o.parent.mkdir(parents=True)
    o.write_text(g.read_text().replace('"title": "T"', '"x": 1') + "\n" + json.dumps({"type": "model_change", "provider": "openai-codex", "modelId": "gpt-5.6-sol"}))
    s = read_pi("omo", str(o), LOCAL)
    assert s.ok() and s.model == "openai-codex/gpt-5.6-sol" and s.resume == f"cd '/w' && omo --session '{o}'", vars(s)
    assert deep_link(s) == "agent-session://open?tool=omo&id=019ecf51-6817-7000-a85d-1c96c1d0bb9a&cwd=%2Fw" and note(s)[0] == "2026-06-16 OmO - q"
    s.remote = "office"
    assert deep_link(s).endswith("&cwd=%2Fw&host=office")
    s.rows, s.id = (lambda: iter(['{"a":1}'])), "sid1"
    assert raw_rel(s).endswith("/sid1.jsonl.gz") and gzip.open(keep_raw(s)).read() == b'{"a":1}\n'
    assert safe_name('a/b: "c"? [d]#') == "a b c d"
    k = d / ".grok/sessions/%2Fg/0f0f0f0f-1111-2222-3333-444444444444"
    k.mkdir(parents=True)
    (k / "summary.json").write_text(json.dumps({"info": {"id": "0f0f0f0f-1111-2222-3333-444444444444", "cwd": "/g"}, "created_at": "2026-07-01T10:00:00Z", "updated_at": "2026-07-01T10:30:00Z", "current_model_id": "grok-x"}))
    (k / "chat_history.jsonl").write_text("\n".join(json.dumps(x) for x in [
        {"type": "system", "content": "sys"},
        {"type": "user", "content": [{"type": "text", "text": "<system-reminder>x</system-reminder>"}], "synthetic_reason": "system_reminder"},
        {"type": "user", "content": [{"type": "text", "text": "<user_info>\nOS: x\n</user_info>\n\n<rules>\nr\n</rules>\n\n<user_query>q</user_query>"}], "prompt_index": 0},
        {"type": "reasoning", "id": "rs_1", "summary": [], "encrypted_content": "e", "status": "completed"},
        {"type": "assistant", "content": "a", "tool_calls": [{"id": "c1", "name": "read_file", "arguments": "{\"target_file\":\"f\"}"}], "model_id": "grok-x-build"},
        {"type": "tool_result", "tool_call_id": "c1", "content": "1→x"},
        {"type": "user", "content": [{"type": "text", "text": "<user_info>\nOS: x\n</user_info>\n\n<rules>\nr\n</rules>\n\nplain"}], "prompt_index": 1},
        {"type": "assistant", "content": "done", "model_id": "grok-x-build"}]))
    s = read_grok(str(k / "chat_history.jsonl"), LOCAL)
    assert s.ok() and s.id == "0f0f0f0f-1111-2222-3333-444444444444" and s.cwd == "/g" and s.model == "grok-x-build", vars(s)
    assert [t["text"] for t in s.turns] == ["q", "a", "plain", "done"] and s.omitted == {"thinking": 1, "tool_call": 1, "tool_result": 1}, s.turns
    name, ident, text = note(s)
    assert name == f"{ts('2026-07-01T10:00:00Z'):%Y-%m-%d} Grok - q" and ident == "urn:grok:session:0f0f0f0f-1111-2222-3333-444444444444"
    assert f"- Span: {ts('2026-07-01T10:00:00Z'):%Y-%m-%d %H:%M} ~ {ts('2026-07-01T10:30:00Z'):%Y-%m-%d %H:%M}" in text and "### Turn 1 | You said:\n" in text, text[:1200]
    assert s.resume == "cd '/g' && grok --resume 0f0f0f0f-1111-2222-3333-444444444444" and deep_link(s) == "agent-session://open?tool=grok&id=0f0f0f0f-1111-2222-3333-444444444444&cwd=%2Fg"
    assert raw_rel(s) == "Raw/_attachments/laptop/grok/0f0f0f0f-1111-2222-3333-444444444444.jsonl.gz" and gzip.open(keep_raw(s)).read() == (k / "chat_history.jsonl").read_bytes() + b"\n"
    assert len(list(sources(["grok"], {"laptop": str(d)}))) == 1
    assert len(list(sources(["gjc", "omo"], {"laptop": str(d)}))) == 1 and list(sources(["claude"], {"laptop": str(d)})) == []
    if zstd:
        z = d / "rollout-2026-06-07T22-44-15-019ea253-b6ea-75c0-bad3-b1b8448c9da9.jsonl.zst"
        with zstd.open(z, "wt") as f:
            f.write("\n".join(json.dumps(x) for x in [
                {"type": "session_meta", "timestamp": "2026-06-07T22:44:15Z", "payload": {"id": "019ea253-b6ea-75c0-bad3-b1b8448c9da9", "cwd": "/c"}},
                {"type": "response_item", "timestamp": "2026-06-07T22:44:16Z", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "q"}]}},
                {"type": "response_item", "timestamp": "2026-06-07T22:44:17Z", "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "a"}]}}]))
        s = read_codex(str(z), LOCAL)
        assert s.ok() and s.id == "019ea253-b6ea-75c0-bad3-b1b8448c9da9" and s.cwd == "/c" and len(s.turns) == 2, vars(s)
        assert raw_rel(s) == f"Raw/_attachments/laptop/codex/{z.name}" and keep_raw(s).read_bytes() == z.read_bytes()
    shutil.rmtree(d)
    print("check ok")


if __name__ == "__main__":
    main()
