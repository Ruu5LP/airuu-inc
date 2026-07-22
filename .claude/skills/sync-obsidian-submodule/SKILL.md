---
name: sync-obsidian-submodule
description: Sync a merged airuu-inc main commit into ruu-obsidian's airuu-inc git submodule reference. Use this whenever a change to airuu-inc (this repo) has just been merged to main and needs to be reflected in the ruu-obsidian vault repo, which includes airuu-inc as a submodule. Prevents recurring git mistakes (stale branch force-push conflicts, mobile-sync deleting the gitlink, branch name mixups).
---

# ruu-obsidianのairuu-incサブモジュール同期

airuu-inc（このリポジトリ）へのmainへのマージが終わったら、ruu-obsidianリポジトリの`airuu-inc`サブモジュール参照を
最新コミットに更新する定型作業。何度か事故（force-push衝突、モバイル同期による誤削除、ブランチ混線）が起きているので、
毎回この手順に固定する。

## 前提

- ruu-obsidianも同じセッション内にクローン済みであること（`/home/user/ruu-obsidian`など）
- airuu-inc側のmainへのマージが**完了済み**であること（マージ後のコミットSHAが分かっている状態から始める）

## 手順

1. **ruu-obsidianを最新化し、新しいブランチをmainから切る**（既存ローカルブランチの使い回しはしない。stale pushの原因になる）
   ```bash
   cd /home/user/ruu-obsidian
   git fetch origin main
   git checkout -B claude/sync-airuu-<短い説明> origin/main
   git submodule update --init airuu-inc
   ```
2. **サブモジュールを対象コミットにcheckout**
   ```bash
   cd airuu-inc
   git fetch origin main
   git checkout <airuu-incのマージ後コミットSHA>
   cd ..
   ```
3. **差分を確認してからコミット**（`airuu-inc | 1 +-` のような1行差分になるはず）
   ```bash
   git status
   git add airuu-inc
   git commit -m "airuu-incサブモジュール参照を<変更内容>後のmainに更新"
   ```
4. **push**。まず素直にpushし、rejectされたら安全確認してからforce-with-lease
   ```bash
   git push -u origin claude/sync-airuu-<短い説明>
   ```
   rejectされた場合（stale/非fast-forward）：
   ```bash
   git fetch origin claude/sync-airuu-<短い説明>  # 実際の最新tipを取得
   git diff origin/claude/sync-airuu-<短い説明> origin/main -- airuu-inc  # 差分が空 = 内容はmainに既に取り込まれ済み = 安全
   git push --force-with-lease=claude/sync-airuu-<短い説明>:<origin/main上で確認したtipのSHA> -u origin claude/sync-airuu-<短い説明>
   ```
   diffが空でない場合は**force-pushしない**。何か別の変更が乗っている可能性があるので内容を確認する。
5. **PRを作ってmainへマージ**（GitHub連携ツールが使えない場合は、直接 `git checkout main && git merge` → `git push origin main` でもよい）
6. **マージ後、健全性を確認する**（モバイルのObsidian Git同期アプリが、mainへの別コミットとの自動マージで
   サブモジュールのgitlinkを誤って消すことが実際にあった）
   ```bash
   git fetch origin main
   git ls-tree origin/main -- airuu-inc   # 何も出力されなければサブモジュール参照が消えている = 要復旧
   ```
   もし消えていたら、同じ手順（1〜5）でもう一度 `git add airuu-inc` して復旧コミットを作る。

## よくある事故と対処

- **「non-fast-forward」でpushが拒否される**：ローカルブランチをoriginから作り直さず使い回したときに起きやすい。
  手順1で必ず`origin/main`から新しく切ること。過去のブランチ内容が既にmainに取り込まれているか
  （`git diff <古いブランチ> origin/main -- airuu-inc`が空か）を確認してからforce-with-lease。
- **「stale info」でforce-with-leaseが失敗する**：ローカルが把握してるリモートtipが古い。
  `git fetch origin <ブランチ名>`で最新tipを取り直してから、そのSHAを指定してforce-with-leaseし直す。
- **サブモジュールのgitlinkが消える**：モバイル同期アプリの自動マージが原因になることがある。
  上記手順6で定期的に健全性を確認し、消えていたら即座に復旧する。
