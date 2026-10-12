#!/usr/bin/env bash
# Remember which notes changed since the index was last refreshed. Runs no qmd
# command and never blocks or fails the caller. Works from any agent runtime.
#
#   qmd-reindex.sh                 print the notes changed since the last clear
#   qmd-reindex.sh FILE            remember FILE if it is a note in a qmd collection
#   <hook JSON> | qmd-reindex.sh   same, FILE read from tool_input.file_path
#   qmd-reindex.sh clear           forget them once the index is refreshed

CONFIG="${QMD_CONFIG:-$HOME/.config/qmd/index.yml}"
PENDING="${TMPDIR:-/tmp}/secondbrain-qmd-reindex.pending"

file="${1:-}"
if [ -z "$file" ] && [ ! -t 0 ]; then
  file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
fi

case "$file" in
  "") [ -f "$PENDING" ] && sort -u "$PENDING"; exit 0 ;;
  clear) rm -f "$PENDING"; exit 0 ;;
  *.md) ;;
  *) exit 0 ;;
esac

[ -f "$CONFIG" ] || exit 0
while IFS= read -r root; do
  case "$file" in "$root"/*) printf '%s\n' "$file" >>"$PENDING"; break ;; esac
done < <(sed -n 's/^[[:space:]]*path:[[:space:]]*//p' "$CONFIG" | sed 's/^"\(.*\)"$/\1/')
exit 0
