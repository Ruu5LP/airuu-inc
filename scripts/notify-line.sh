#!/usr/bin/env bash
# 決定ログ・振り返りなどの更新をRuuのLINEにpushする。
# 必須の環境変数: LINE_CHANNEL_ACCESS_TOKEN, LINE_USER_ID
#
# 使い方:
#   scripts/notify-line.sh "メッセージ本文"
#   scripts/notify-line.sh -f path/to/file.md   # ファイルの中身をそのまま送る
#
# LINE Messaging API の1通あたり上限(5000文字)を超える分は切り詰める。

set -euo pipefail

if [[ -z "${LINE_CHANNEL_ACCESS_TOKEN:-}" || -z "${LINE_USER_ID:-}" ]]; then
  echo "notify-line.sh: LINE_CHANNEL_ACCESS_TOKEN / LINE_USER_ID が未設定。通知をスキップする。" >&2
  exit 0
fi

if [[ "${1:-}" == "-f" ]]; then
  text=$(cat "$2")
else
  text="${1:?メッセージ本文か -f <file> を渡して}"
fi

text="${text:0:4900}"

payload=$(jq -n --arg to "$LINE_USER_ID" --arg text "$text" \
  '{to: $to, messages: [{type: "text", text: $text}]}')

curl -sS -X POST https://api.line.me/v2/bot/message/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${LINE_CHANNEL_ACCESS_TOKEN}" \
  -d "$payload" \
  -o /tmp/notify-line-response.json \
  -w "notify-line.sh: HTTP %{http_code}\n"

cat /tmp/notify-line-response.json >&2 || true
