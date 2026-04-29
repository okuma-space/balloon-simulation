# balloon-simulation
A learning project for balloon engineering simulation

本リポジトリは学習用途を目的としており，READMEおよびコードコメントは日本語で記述している．

同様に計算部分もC++エンジン化せずにPythonにて試作している.

作業ログのためにPRは作っているが,コードレビューは主にローカル環境で自主的に実施している．

# 結果サマリ

気球の飛翔ダイナミクスシミュレーションを実施した.

実行結果の3D軌跡のグラフは以下となる.

![trajectry](https://okuma-space.github.io/balloon-simulation/images/generated/v1/balloon_3D_trajectory_2.0.png)
[trajectry](https://okuma-space.github.io/balloon-simulation/html/v1/balloon_3D_trajectory_2.0.html)

実行条件や実装されたダイナミクスについてのサマリは以下にまとめた.

- [結果サマリ:latest 3D飛翔シミュレーション](https://github.com/okuma-space/balloon-simulation/blob/main/docs/report.md)
- [結果サマリ:v1.0 上昇下降運動シミュレーション](https://github.com/okuma-space/balloon-simulation/blob/main/docs/reports/report_v1.0.md)
- [ノート](https://github.com/okuma-space/balloon-simulation/blob/main/docs/note.md)


# シミュレーション実行手順
## 飛翔ダイナミクスシミュレーション
気球モデルの初期値および計算条件は `config.json` に定義している．

実行は以下のコマンドからできる.
```bash
python scripts/run_trajectory_simulation.py <気球コンフィグファイル名>
```

# 学習文献
- 宇宙工学シリーズ6 気球工学
- 宇宙システム入門　ロケット・人工衛星の運動
- 数値計算[新訂版]

# issues
現時点での改善アイディアなどはissuesに記載.

[GitHub Issues](https://github.com/okuma-space/balloon-simulation/issues)

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

スタイルチェックが厳格すぎるため導入を検討中であるが以下でpylintの実行も可能
```bash
pylint src scripts tests
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