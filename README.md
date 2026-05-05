# urlwatch RSS on GitHub Actions

GitHub Actions で `thp/urlwatch` を checkout して実行し、変更通知を `docs/feed.xml` にRSSとして追記する構成です。

## 使い方

1. このZIPの中身をGitHubリポジトリのルートに展開します。
2. `docs/config/targets.json` に監視候補URLを追加します。
3. GitHubへpushします。
4. GitHub Pagesを `main` ブランチの `/docs` から公開します。
5. `docs/index.html` を開き、監視対象を選んで `selection.json` をダウンロードします。
6. ダウンロードしたファイルを `docs/config/selection.json` として置き換えてpushします。
7. Actionsの `urlwatch` workflowを手動実行、または定期実行を待ちます。

## RSS URL

通常は次の形式です。

```text
https://<GitHubユーザー名>.github.io/<リポジトリ名>/feed.xml
```

カスタムドメインを使う場合は、Repository variables に `RSS_SITE_URL` を設定してください。

例:

```text
RSS_SITE_URL=https://example.com
```

## ファイル構成

```text
.github/workflows/urlwatch.yml
docs/index.html
docs/feed.xml
docs/config/targets.json
docs/config/selection.json
scripts/build-urlwatch-config.py
scripts/rss_reporter.py
.gitignore
README.md
```

## メモ

- 初回実行では履歴作成のみでRSS itemが増えないことがあります。
- 2回目以降、監視対象に差分があると `docs/feed.xml` にitemが追加されます。
- `docs/feed.xml` はActionsが自動コミットします。
