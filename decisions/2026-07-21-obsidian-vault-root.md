---
title: リポジトリのルートをObsidian vaultにする
tags:
  - 決定ログ
  - AiRuu
  - Obsidian
date: 2026-07-21
aliases:
  - Obsidian連携
  - vault連携方針
---

# 2026-07-21 リポジトリのルートをObsidian vaultにする

## 決めたこと

このリポジトリのルートを、**そのまま Ruu の Obsidian vault** として開く。一部フォルダだけを既存vaultに同期する形は取らない。

## 背景 / 選択肢

`CLAUDE.md` には「vaultの全体または一部として開けることを想定する」と曖昧に書かれたままだったため、方針を確定させた。

- Ruu はこれまで別のObsidian vault（日常メモなど）を使っておらず、**これが最初のvault**。
- 既存vaultとの合流・移行作業が発生しないため、選択肢は単純だった: このリポジトリをそのままvaultルートにする一択で、他の案（部分同期・既存vaultとの合流）を検討する必要がなかった。

## やったこと

- `CLAUDE.md` の「Obsidian 連携の方向」を更新し、「リポジトリのルート = vaultルート」と明記。

## 次の一歩

- Ruu 側で、このリポジトリのローカルクローンを Obsidian で「フォルダをvaultとして開く」。
- 個人の作業状態（`.obsidian/workspace*` 等）は `.gitignore` で除外済み。プラグイン・テーマなどvault設定を将来共有したくなったら、そのとき `.gitignore` を見直す。
