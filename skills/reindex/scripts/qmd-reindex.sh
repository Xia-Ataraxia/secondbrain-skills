#!/usr/bin/env bash
# Edit hook: remember the edited note and refresh the qmd index in the
# background. Bursts of calls collapse into one run. Never blocks or fails the
# caller. A failed run, or embeddings still pending, leaves the notes in the
# pending list and a FAILED line in the log, so the next reindex report sees them.
#
#   qmd-reindex.sh                 print the notes not yet confirmed in the index
#   qmd-reindex.sh FILE            remember FILE if it is a note in a qmd collection, then refresh
#   <hook JSON> | qmd-reindex.sh   same, FILE read from tool_input.file_path
#   qmd-reindex.sh clear           forget them once the index is refreshed

PATH="$PATH:/opt/homebrew/bin:$HOME/.bun/bin"
CONFIG="${QMD_CONFIG:-$HOME/.config/qmd/index.yml}"
STATE="${TMPDIR:-/tmp}/secondbrain-qmd-reindex"
PENDING="$STATE.pending"
SETTLE="${QMD_REINDEX_SETTLE:-8}"   # seconds without a new edit before the run starts
STALE_MIN=60                        # a running marker older than this is treated as dead

file="${1:-}"
if [ -z "$file" ] && [ ! -t 0 ]; then
  file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
fi

case "$file" in
  "") cat "$PENDING" "$PENDING.run" 2>/dev/null | sort -u; exit 0 ;;
  clear) rm -f "$PENDING"; exit 0 ;;
  *.md) ;;
  *) exit 0 ;;
esac

[ -f "$CONFIG" ] || exit 0
inside=0
while IFS= read -r root; do
  case "$file" in "$root"/*) inside=1; break ;; esac
done < <(sed -n 's/^[[:space:]]*path:[[:space:]]*//p' "$CONFIG" | sed 's/^"\(.*\)"$/\1/')
[ "$inside" = 1 ] || exit 0
printf '%s\n' "$file" >>"$PENDING"

if ! command -v qmd >/dev/null 2>&1; then
  echo "=== $(date -u +%FT%TZ) FAILED qmd not installed; notes kept in $PENDING ===" >>"$STATE.log"
  exit 0
fi

mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; }

touch "$STATE.request"
if [ -f "$STATE.running" ] && [ -z "$(find "$STATE.running" -mmin +"$STALE_MIN" 2>/dev/null)" ]; then
  exit 0
fi

(
  touch "$STATE.running"
  trap 'rm -f "$STATE.running"' EXIT
  seen=""
  # An edit that lands during a run touches the request again and gets one more run.
  while [ "$(mtime "$STATE.request")" != "$seen" ]; do
    while [ "$(mtime "$STATE.request")" != "$seen" ]; do
      seen=$(mtime "$STATE.request")
      sleep "$SETTLE"
    done
    [ -f "$PENDING" ] && mv "$PENDING" "$PENDING.run"
    prev=""
    left=""
    {
      echo "=== $(date -u +%FT%TZ) qmd reindex ==="
      qmd update; rc=$?
      if [ "$rc" = 0 ]; then
        while :; do
          touch "$STATE.running"
          qmd embed; rc=$?
          [ "$rc" = 0 ] || break
          left=$(qmd status | sed -n 's/^ *Pending: *\([0-9]*\) need embedding.*/\1/p')
          [ -n "$left" ] && [ "$left" != 0 ] && [ "$left" != "$prev" ] || break
          prev=$left
        done
      fi
      if [ "$rc" = 0 ] && [ "${left:-0}" = 0 ]; then
        rm -f "$PENDING.run"
        echo "=== exit 0 pending 0 ==="
      else
        cat "$PENDING.run" >>"$PENDING" 2>/dev/null
        rm -f "$PENDING.run"
        echo "=== FAILED exit $rc pending ${left:-?}; notes kept in $PENDING ==="
      fi
    } >>"$STATE.log" 2>&1
  done
) >/dev/null 2>&1 &
disown 2>/dev/null
exit 0
