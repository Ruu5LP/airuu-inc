---
title: CEOの名前を「Alex」にする
tags:
  - 決定ログ
  - AiRuu
  - CEO
date: 2026-07-21
aliases:
  - CEO改名
  - Alexという名前
---

# 2026-07-21 CEOの名前を「Alex」にする

## 決めたこと

CEOの人格名を「Ai」から **Alex** に変更した。社名「AiRuu」は創業時の由来としてそのまま残す。

## 背景 / 選択肢

CEOの名前は発足時から「Ai」（AI + 愛のダブルミーニング）だったが、Ruu から「もっと固有の名前にしたい／外国の名前がいい」という要望があった。

検討の軸は2つ。

1. **社名との整合性** — 「AiRuu」は Ai + Ruu の融合として名付けられているため、CEOの名前を変えると由来の扱いが必要になる。
   → 社名は創業時の由来としてそのまま残し、CEOは「Aiという名前で始まり、育つ中で自分の名前を持った」という成長の物語として扱うことにした。
2. **名前の方向性** — 外国の名前・性別を感じさせないユニセックスな名前、という希望を受け、候補として Sage（賢者・助言者の意）/ Quinn（知恵・助言者の意）/ Robin（相棒のニュアンス）を提示。
   最終的に Ruu が選んだのは、この3案とは別に出た **Alex**。

## やったこと

- `team/ai-ceo.md` → `team/alex-ceo.md` にリネーム。`title`/`aliases` を更新し、旧名「Ai」もaliasとして残す（既存の `[[Ai — CEO]]` wikilinkが壊れないように）。
- `CLAUDE.md` / `AGENTS.md` / `README.md` / `company-overview.md` / `relationships/founder-ceo-charter.md` / `team/ruu-founder.md` の CEO名表記を Alex に更新。
- `company-overview.md` に「CEOの名前について」の注記を追加し、社名の由来とCEO個人名の変更を切り分けて説明。

## 次の一歩

- 過去の決定ログ（`2026-07-21-agent-ready-repo.md` など）は当時の記録として書き換えない。wikilinkは alias 経由でそのまま生きる。
- 続けて [[Obsidian連携]] の方針を決める。
