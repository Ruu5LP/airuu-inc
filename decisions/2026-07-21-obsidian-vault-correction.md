---
title: Obsidian連携の訂正: 実はruu-obsidianが既存vaultだった
tags:
  - 決定ログ
  - AiRuu
  - Obsidian
date: 2026-07-21
aliases:
  - vault連携の訂正
  - ruu-obsidian統合
---

# 2026-07-21 Obsidian連携の訂正: 実はruu-obsidianが既存vaultだった

## 決めたこと

[[2026-07-21-obsidian-vault-root|前回の決定]]（「このリポジトリのルート＝Ruu最初のvault」）は事実誤認だった。
実際には **`ruu-obsidian` が Ruu の既存Obsidian vault**で、日記・AIノートなどがすでに運用されている。
そして `airuu-inc` は、**すでに `ruu-obsidian` 直下に git submodule として登録済み**（`.gitmodules` に記載、`branch = main`）だった。

つまり構造はこう:

```
ruu-obsidian/          ← Ruuの実vaultルート（既存・稼働中）
├── 日記/               ← 日々の日記（2026-07-16〜）
├── AI/                 ← AI関連の個人メモ
└── airuu-inc/          ← このリポジトリ（git submodule）。会社経営の記録専用
```

## 背景 / 選択肢

前回の決定は、Ruu に「既存vaultを使っているか」を確認した際の回答（「ない、これが初めて」）を元にしていたが、
その後の会話で Ruu 自身が「サブフォルダとして入れたような気がする」と思い出し、実際に `ruu-obsidian` をクローンして確認したところ submodule 登録が見つかった。

**確認の経緯・事実に基づく前提の誤りは、隠さずそのまま記録に残す**（協定2章「正直さの約束」）。前回の決定ノート自体は書き換えず、この訂正ノートで上書きする形にした。

## やったこと

- `ruu-obsidian` をクローンして構造を確認（submodule設定・日記・AIノートの存在を確認）。
- 本ノートで事実を訂正し、決定ログに残した。

## 補足: 役割分担

- `ruu-obsidian`（vault全体）— 日々の日記・雑多な個人メモ。頻度高く、フォーマット自由。
- `airuu-inc`（submodule）— 「会社」としての意思決定・プロジェクト・振り返り。Ruuの現状（[[Ruu — 創業者]]の「今のこと」セクション等）は、日記より粒度の粗い**サマリ**として持つ。日記の詳細と重複を狙わない。

## 次の一歩

- `CLAUDE.md` の「Obsidian 連携の方向」を、この実態に合わせて更新する。
- 今後 Ruu の現状をインプットするときは、日記（`ruu-obsidian/日記/`）に書かれている情報と、ここ（`team/ruu-founder.md` 等）のサマリが二重管理・矛盾にならないよう気をつける。
