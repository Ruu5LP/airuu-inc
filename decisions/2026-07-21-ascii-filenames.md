---
title: ファイル名は ASCII、表示名は日本語で持つ
tags:
  - 決定ログ
  - AiRuu
  - リポジトリ
  - 運用ルール
date: 2026-07-21
aliases:
  - ファイル名はASCII、表示名は日本語で持つ
  - ASCIIファイル名ルール
---

# 2026-07-21 ファイル名は ASCII、表示名は日本語で持つ

## 決めたこと

**ファイル名・フォルダ名は ASCII（英数字・ハイフン）に統一**し、日本語の見た目は
frontmatter の `title` と `aliases` で持たせる、というハイブリッド方式を採用した。
本文の wikilink（例: `[[Ai — CEO]]`）は日本語のまま、alias 経由で解決される。

## 背景 / 選択肢

Ruu は Mac と Windows の両方でこのリポジトリ（Obsidian vault）を扱う。日本語ファイル名のままだと、
主に2つが気になっていた。

1. **Unicode 正規化ゆらぎ** — Mac は NFD、Windows / GitHub は NFC でファイル名を持つため、
   濁点を含む語（`決定ログ` など）で「見た目同じなのに別ファイル」の二重化・リンク切れが起きうる。
2. **自動化のしにくさ** — スクリプト・CI・URL で、日本語＋空白＋em-dash はクォート必須になる。

選択肢は3つ挙げた。

- **A. 日本語のまま維持**（＋git 設定 `core.precomposeunicode` 等）— 温かいが、正規化は設定依存で残る。
- **B. フル ASCII 化** — 機械には最強だが、ノートごとに名前を英訳する手間が恒久化し、日本語の本文と見た目がちぐはぐになる。
- **C. ハイブリッド（ファイル名 ASCII ＋ title/aliases 日本語）** — 機械には ASCII、人間には日本語の両取り。

論点が「正規化と自動化」だったため、設定に依存せず**構造で問題を消せる C** を Ruu が選択。

## やったこと

- フォルダをリネーム: `経営陣/`→`team/`、`関係性/`→`relationships/`、`決定ログ/`→`decisions/`、
  `振り返り/`→`retrospectives/`、`プロジェクト/`→`projects/`。
- ノートを ASCII 名にリネーム（例: `Ai — CEO.md`→`team/ai-ceo.md`、`会社概要.md`→`company-overview.md`）。
- 各ノートの `aliases` に**旧ファイル名（日本語）を追加** → 本文の wikilink はそのまま生きる。
- `title` / `tags` は日本語のまま維持（本文扱いで正規化・自動化リスクなし。温かさを残す）。
- `CLAUDE.md` / `AGENTS.md` の記述規約を更新（旧「空白・em-dash は意図的」ルールを差し替え）。
- `README.md` の相対リンクを新パスに更新。

## 効いていること / 補足

- **フォルダ名は wikilink の対象ではない**（リンクはノートに張る）ため、フォルダの ASCII 化はリンク影響ゼロの純粋なプラス。
- Obsidian の同期を**クラウド同期（iCloud / OneDrive 等）ではなく Git に寄せる**と、正規化の一貫性が保てて事故りにくい。
- 保険として git 設定を入れておくと更に堅い:
  - Mac: `git config --global core.precomposeunicode true`
  - 両OS: `git config --global core.quotePath false`（日本語をログ/diff でそのまま表示）
  - Windows: `git config --global core.longpaths true`

## 次の一歩

- Ruu 側の Mac / Windows それぞれで上記 git 設定を入れる。
- 以降の新規ノートは、ファイル名 ASCII・`title` 日本語で作る（[[決定ログ]] / [[振り返り]] / [[プロジェクト]] の書き方に準拠）。
