# balloon-simulation
learning project for balloon engineering

自学習用のリポジトリです

プロダクトではなく学習リポジトリのため効率重視でREAD ME、コメントともに日本語にて書いています

同様に計算部分もC++エンジン化せずにPythonにて試作しています

作業ログのためにPRは作っていますが、コードレビューは基本的にVsCode上でAIレビューを使っています。

# レポート
[簡易レポート](https://okuma-space.github.io/balloon-simulation/report.html)

# 学習文献
- 宇宙工学シリーズ6 気球工学
- 宇宙システム入門　ロケット・人工衛星の運動

# ci/workflow
以下の4ステージで構成
deployステージでdocs/report.mdをhtmlとしてリリースする
- build-and-push
- lint
- test
- deploy

# commandシート
## dockerコマンド
```bash
docker build -t balloon-sim -f .\tool\Dockerfile .

docker run -it --rm -v ${PWD}:/balloon-simulation balloon-sim bash
```

## python format & style check(ruff)
```bash
ruff ruff format py scripts tests
ruff check py scripts tests --fix
```

## test
test
```bash
pytest tests
```

coverage report
```bash
pytest tests --cov=py --cov-report=term --cov-report=xml
```