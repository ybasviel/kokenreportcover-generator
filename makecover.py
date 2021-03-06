#!/bin/python3

from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pathlib import Path
import sys
from unicodedata import east_asian_width

def get_east_asian_width(text):     #文字数を英数字1, 日本語2文字でカウント
    count = 0
    for c in text:
        if east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


def split_text(length, content):    #文字列を指定の文字数で分割する
    splited_text = []

    t = 0
    while get_east_asian_width(content[t:]) >= length:
        x = 1
        while(get_east_asian_width(content[t:-x]) >= length):
            x = x + 1
        
        splited_text.append(content[t:-x])
        t = len(content) - x
    
    splited_text.append(content[t:])

    return splited_text

def futidori(font_color, edge_color, content, font, font_size, draw, position ):   #フチつきで文字を書くらしい
    w, h = draw.textsize(content, font)
    stroke_width = int(font_size*0.1)
    draw.multiline_text(position, content, font=font, fill=font_color, stroke_width=stroke_width, stroke_fill=edge_color)


def textincover(src, dest, content_list, font_size, font_path, maxline, rx, ry, font_color, edge_color):

    image = Image.open(src)     #なんかファイル開く
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(font_path),font_size)

    x, y = image.size

    x = int(x*rx)
    y = int(y*ry)

    content_index = len(content_list)   #目次数

    for content in content_list:
        content = str(content_index) + ". " + content
        content_index -= 1
        if len(content) == 0:
            pass
        elif get_east_asian_width(content) >= maxline:
            splited_text = split_text(maxline, content)
            splited_text.reverse()

            for i in range(0, len(splited_text) - 1):
                splited_text[i] = "　" + splited_text[i]
             
            for content in splited_text:
                futidori(font_color, edge_color, content, font, font_size, draw, (x,y) )
                y = y - ( font_size*1.3 )
        else:
            futidori(font_color, edge_color, content, font, font_size, draw, (x,y) )
            y = y - ( font_size*1.3 )

    content = "もくじ"
    x = x - font_size
    futidori(font_color, edge_color, content, font, font_size, draw, (x,y) )

    image.save(dest)


def str_to_rgb(rgb_str):
    return tuple(map(int, rgb_str.split(",")[:3]))


if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--output", type=Path, required=True, help="出力ファイル指定")
    parser.add_argument("-i", "--input", type=Path, required=True, help="入力ファイル指定")
    parser.add_argument("-x", type=float, default=0.1, help="開始位置指定 (横幅に対する比率)")
    parser.add_argument("-y", type=float, default=0.9, help="終了位置指定 (縦幅に対する比率)")
    parser.add_argument("-m", type=int, default=20, help="改行位置指定 (英数1文字幅)")
    parser.add_argument("-s", type=int, default=100, metavar="FONT_SIZE", help="フォントサイズ指定")
    parser.add_argument("-f", "--font", type=Path, required=True, help="フォントパス指定")
    parser.add_argument("--fontcolor", type=str_to_rgb, default=(255,255,255), metavar="FONT_COLOR", help="フォント色RGB指定")
    parser.add_argument("--edgecolor", type=str_to_rgb, default=(0,0,0), metavar="EDGE_COLOR", help="縁取りの色RGB指定")
    parser.add_argument("index", nargs="?", type=FileType("r"), default=sys.stdin)

    args = parser.parse_args()

    maxline = args.m + 4
    content_list = []
    if args.index.isatty():  # interactive keyboard input
        print("目次を入力（ctrl-dで終了）")
        try:
            while True:
                content_list.append( input(" > ") )
                print(content_list[-1])
        except EOFError:
            pass
    else:
        content_list = list(map(lambda line: line.rstrip(), args.index))

    while ( "" in content_list ):   #空文字列があったら削除
        content_list.remove("")

    content_list.reverse()

    textincover(args.input, args.output, content_list, args.s, args.font, maxline, args.x, args.y, args.fontcolor, args.edgecolor)

