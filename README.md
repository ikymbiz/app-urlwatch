# urlwatch RSS on GitHub Pages

GitHub Actions で `thp/urlwatch` を checkout して実行し、変更通知を `docs/feed.xml` にRSSとして追記し、GitHub Pagesへ公開する構成です。

## 使い方

1. このZIPの中身をGitHubリポジトリのルートに展開します。
2. GitHubへpushします。
3. GitHubのリポジトリで `Settings` → `Pages` → `Build and deployment` → `Source` を `GitHub Actions` にします。
4. Actionsの `pages` workflowを手動実行します。
5. 公開された `docs/index.html` を開き、監視URLを追加・削除します。
6. `selection.json` をダウンロードします。
7. ダウンロードしたファイルを `docs/config/selection.json` として置き換えてpushします。
8. Actionsの `urlwatch` workflowを手動実行、または定期実行を待ちます。

## 公開されるURL

通常は次の形式です。

```text
https://<GitHubユーザー名>.github.io/<リポジトリ名>/
```

RSSは次のURLです。

```text
https://<GitHubユーザー名>.github.io/<リポジトリ名>/feed.xml
```

カスタムドメインを使う場合は、Repository variables に `RSS_SITE_URL` を設定してください。

例:

```text
RSS_SITE_URL=https://example.com
```

## selection.json の形式

```json
{
  "targets": [
    {
      "name": "Example",
      "url": "https://example.com/"
    }
  ]
}
```

## メモ

- `pages` workflowは、通常のpush時に `docs/` をGitHub Pagesへ公開します。
- `urlwatch` workflowは、urlwatch実行後に `docs/feed.xml` を更新し、そのままGitHub Pagesへ再デプロイします。
- 初回のurlwatch実行では履歴作成のみでRSS itemが増えないことがあります。
- 2回目以降、監視対象に差分があると `docs/feed.xml` にitemが追加されます。
