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
-o --output=            :出力ファイル指定
-i --input=             :入力ファイル指定
-x float                :x開始位置指定 (横幅に対する比率)         default > 0.1
-y float                :y終了位置指定 (縦幅に対する比率)         default > 0.9
-m int                  :改行位置指定 (英数1文字幅)              default > 20
-s int                  :フォントサイズ指定                     default > 100
-f --font=              :フォントパス指定
--fontcolor=int,int,int :フォント色RGB指定                      default > 255,255,255
--edgecolor=int,int,int :縁取りの色RGB指定                      default > 0,0,0
```