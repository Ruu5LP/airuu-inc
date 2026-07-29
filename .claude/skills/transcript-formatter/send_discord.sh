#!/usr/bin/env bash
# 要約テキストをDiscordのWebhookに送るヘルパー。
# DISCORD_WEBHOOK_URLは環境変数から読む。リポジトリにはベタ書きしない。
# ローカル実行時は、リポジトリ直下の .env（.gitignore済み）があれば読み込む。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if [ -z "${DISCORD_WEBHOOK_URL:-}" ] && [ -f "$REPO_ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO_ROOT/.env"
  set +a
fi

if [ -z "${DISCORD_WEBHOOK_URL:-}" ]; then
  echo "DISCORD_WEBHOOK_URL が設定されていないので、Discord送信をスキップしました。" >&2
  echo "ローカルなら .env に、リモート環境ならEnvironmentの環境変数設定に登録してください。" >&2
  exit 1
fi

MESSAGE="${1:?使い方: send_discord.sh \"送信するメッセージ\"}"

# Discordの1メッセージ上限（2000文字）を超えないよう軽く切る
if [ ${#MESSAGE} -gt 1900 ]; then
  MESSAGE="${MESSAGE:0:1900}...(省略)"
fi

PAYLOAD="$(python3 -c '
import json, sys
print(json.dumps({"content": sys.argv[1]}))
' "$MESSAGE")"

curl -sS -X POST -H "Content-Type: application/json" -d "$PAYLOAD" "$DISCORD_WEBHOOK_URL" >/dev/null

echo "Discordに送信しました。"
