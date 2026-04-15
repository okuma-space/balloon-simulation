# balloon-simulation
learning project for balloon engineering

自学習用のリポジトリ

学習のため効率のためREAD ME、コメントともに日本語にて書いております

# 学習文献
-宇宙工学シリーズ6 気球工学

# コマンドシート
- dockerコマンド
```bash
docker build -t balloon-sim -f .\tool\Dockerfile .

docker run -it --rm -v ${PWD}:/app balloon-sim
```

- pythonフォーマット&スタイルチェック(ruff)
```bash
ruff check py
```