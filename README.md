# balloon-simulation
learning project for balloon engineering

自学習用のリポジトリです

プロダクトではなく学習リポジトリのため効率重視でREAD ME、コメントともに日本語にて書いています

同様に計算部分もC++エンジン化せずにPythonにて試作しています

# 学習文献
- 宇宙工学シリーズ6 気球工学
- 宇宙システム入門　ロケット・人工衛星の運動

# コマンドシート
- dockerコマンド
```bash
docker build -t balloon-sim -f .\tool\Dockerfile .

docker run -it --rm -v ${PWD}:/app balloon-sim
```

- pythonフォーマット&スタイルチェック(ruff)
```bash
ruff format py
ruff check py --fix
```

- テスト
```bash
pytest tests
```

- テスト(カバレッジ付)
```bash
pytest tests --cov=py --cov-report=term --cov-report=xml
```