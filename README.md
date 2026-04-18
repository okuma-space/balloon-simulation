# balloon-simulation
learning project for balloon engineering

自学習用のリポジトリです.

プロダクトではなく学習リポジトリのため効率重視でREAD ME、コメントともに日本語にて書いています.

同様に計算部分もC++エンジン化せずにPythonにて試作しています.

作業ログのためにPRは作っていますが,コードレビューは基本的にVsCode上でAIレビューを使っています.

# 結果サマリ
[結果サマリ](https://okuma-space.github.io/balloon-simulation/report.html)

# 学習文献
- 宇宙工学シリーズ6 気球工学
- 宇宙システム入門　ロケット・人工衛星の運動

# ci/workflow
以下の4ステージで構成.

deployステージでdocs/report.mdをhtmlとしてリリースする.
- build-and-push
- lint
- test
- deploy

# Directory Structure
## docs
シミュレーション結果サマリ

## src
コア実装コード

### physics
物理法則・基礎モデル（力学・流体・熱など）

### dynamics
時間発展・数値積分・状態更新アルゴリズム

### environment
外部環境モデル（大気・風・重力場など）

### systems
統合システムモデル（気球・ロケットなどのドメインモデル）

## scripts
シミュレーション実行・解析スクリプト

## tests
テストコード

## tools
ビルド・Docker・CI・補助スクリプト

# commandシート
## dockerコマンド
```bash
docker build -t balloon-sim -f .\tools\Dockerfile .

docker run -it --rm -v ${PWD}:/balloon-simulation balloon-sim bash
```

## python format & style check(ruff)
```bash
ruff format src scripts tests
ruff check src scripts tests --fix
```

## test
test
```bash
pytest tests
```

coverage report
```bash
pytest tests --cov=src --cov-report=term --cov-report=xml
```