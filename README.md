# balloon-simulation
A learning project for balloon engineering simulation

本リポジトリは学習用途を目的としており，READMEおよびコードコメントは日本語で記述している．

同様に計算部分もC++エンジン化せずにPythonにて試作している.

作業ログのためにPRは作っているが,コードレビューは主にローカル環境で自主的に実施している．

# 結果サマリ
[結果サマリ](https://okuma-space.github.io/balloon-simulation/report.html)

# シミュレーション実行手順
## 上下運動ダイナミクスシミュレーション
気球モデルの初期値および計算条件は `config.json` に定義している．

実行は以下のコマンド.
```bash
python scripts/plot_vertical_propagate.py 
```

# 学習文献
- 宇宙工学シリーズ6 気球工学
- 宇宙システム入門　ロケット・人工衛星の運動
- 数値計算[新訂版]

# issues
現時点での改善アイディアなどはissuesに記載.

https://github.com/okuma-space/balloon-simulation/issues

# ci/workflow
以下の4ステージで構成.

PRがmergeされる際にdeployステージが実行され、docs/report.mdをhtmlとしてリリースする.
- build-and-push
- lint
- test
- deploy

# Directory Structure
## docs
シミュレーション結果およびレポート

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

# Commands
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