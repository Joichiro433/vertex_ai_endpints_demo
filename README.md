

# Vertex AI Endpoints DEMO

### 特徴

- 利用側は、払い出されたエンドポイントに対して HTTPS リクエストを送ることで推論結果レスポンスを得ることができる
- Vertex AI Pipelines の一部として[推論APIのリリースを組み込むことができる](https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html)

- 他サービスでこのリリースフローを実現するためには、そのための機能を開発する必要がある

- [利用パターン](https://cloud.google.com/vertex-ai/docs/model-registry/import-model#container-type)は、1) Google Cloud が用意したビルド済みコンテナ, 2) カスタムコンテナ の 2 種類がある

  - カスタムコンテナは[実装要件を満足する必要](https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements)がある

  - [FastAPI](https://fastapi.tiangolo.com/ja/) を利用して実装することになりそう

  - 一般的な使い方は以下の流れになる

  1. Artifact Registry に要件を満たしたコンテナをアップロード
  2. そのコンテナを Vertex AI Model Registry にモデルとしてインポート
  3. インポートしたモデルを、Vertex AI Endpointsにエンドポイントとしてデプロイ

- GPU 利用可能
- API が動作する Node はオートスケール可能
- [Vertex AI Monitoring](https://cloud.google.com/vertex-ai/docs/model-monitoring/overview?hl=ja) による監視が可能

### Refs.

- [Vertex AIでカスタムモデルをサービングする](https://zenn.dev/dhirooka/articles/5e53361fb08f9e#エンドポイントの作成とモデルのデプロイ)
- [【MLOps実践】GCPで始めるエンドツーエンドなMLOps基盤（Vertex AI,etc）](https://qiita.com/nokoxxx1212/items/1c55261f08ce7e95b255)
- [Tech Blog 機械学習導入初期フェーズにおける Vertex AI Models / Endpoints を用いたオンライン推論](https://anymindgroup.com/ja/tech-blog/online-inference-using-vertex-ai/)
- [サービングを楽にできる？？ Vertex AIを利用した推論APIの作成検討](https://qiita.com/okmtz/items/f8bf3725eeb0c83f9ffa)
- [Vertexで3ヶ月で作る運用可能なML API基盤](https://caddi.tech/archives/4123)



```sh
$ gcloud builds submit --config cloudbuild.yaml
```