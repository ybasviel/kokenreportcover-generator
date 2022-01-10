# 工研部報目次生成ツール

## 簡単な使い方

多分最低限これで動く
```
./makecover.py < 目次ファイル -i 入力ファイル -o 出力ファイル -s フォントサイズ -x xの開始位置 -y yの終了位置 -f フォントのパス
```

色指定付き、英数6文字で改行の例
```
./makecover.py < report69 -i report69.png -o report69out.png -s 30 -x 0.1 -y 0.9 -m 6 -f /usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc --fontcolor=255,0,0 --edgecolor=0,0,0
```

## ./makecover.py --help
```
usage: makecover.py [-h] -o OUTPUT -i INPUT [-x X] [-y Y] [-m M] [-s FONT_SIZE] -f FONT [--fontcolor FONT_COLOR] [--edgecolor EDGE_COLOR] [index]

positional arguments:
  index

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        出力ファイル指定
  -i INPUT, --input INPUT
                        入力ファイル指定
  -x X                  開始位置指定 (横幅に対する比率)
  -y Y                  終了位置指定 (縦幅に対する比率)
  -m M                  改行位置指定 (英数1文字幅)
  -s FONT_SIZE          フォントサイズ指定
  -f FONT, --font FONT  フォントパス指定
  --fontcolor FONT_COLOR
                        フォント色RGB指定
  --edgecolor EDGE_COLOR
                        縁取りの色RGB指定
```