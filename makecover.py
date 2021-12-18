#!/bin/python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import getopt, sys
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

def futidori(font_color, edge_color, content, font, draw, position ):   #フチつきで文字を書くらしい
    w, h = draw.textsize(content, font)
    stroke_width = int(font_size*0.1)
    draw.multiline_text(position, content, font=font, fill=font_color, stroke_width=stroke_width, stroke_fill=edge_color)


def textincover(src, dest, content_list, font_size, font_path, maxline, rx, ry, font_color, edge_color):

    image = Image.open(src)     #なんかファイル開く
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path,font_size)

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
                futidori(font_color, edge_color, content, font, draw, (x,y) )
                y = y - ( font_size*1.3 )
        else:
            futidori(font_color, edge_color, content, font, draw, (x,y) )
            y = y - ( font_size*1.3 )

    content = "もくじ"
    x = x - font_size
    futidori(font_color, edge_color, content, font, draw, (x,y) )

    image.save(dest)



if __name__ == '__main__':

    srcflag = False
    outflag = False
    font_pathflag = False

    font_size = 100 
    maxline = 24
    font_color = (255, 255, 255)
    edge_color = (0, 0, 0)
    rx = 0.1
    ry = 0.9

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:i:o:x:y:s:m:", ["font", "help", "output=", "input=", "fontcolor=", "edgecolor="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    
    verbose = False
    for o, arg in opts:
        if o in ("-h", "--help"):
            print("-o --output=\t\t:出力ファイル指定")
            print("-i --input=\t\t:入力ファイル指定")
            print("-x float\t\t:x開始位置指定 (横幅に対する比率)\tdefault > 0.1")
            print("-y float\t\t:y終了位置指定 (縦幅に対する比率)\tdefault > 0.9")
            print("-m int\t\t\t:改行位置指定 (英数1文字幅)\t\tdefault > 20")
            print("-s int\t\t\t:フォントサイズ指定\t\t\tdefault > 100")
            print("-f --font=\t\t:フォントパス指定")
            print("--fontcolor=int,int,int\t:フォント色RGB指定\t\t\tdefault > 255,255,255")
            print("--edgecolor=int,int,int\t:縁取りの色RGB指定\t\t\tdefault > 0,0,0")
            sys.exit()
        elif o in ("-o", "--output"):
            outflag = True
            output  = repr(str(arg))[1:-1]
        elif o in ("-f"):
            font_pathflag = True
            font_path = str(arg)
        elif o in ("--fontcolor="):
            font_color = arg.split(",")
            for i in range(0,3):
                font_color[i] = int(font_color[i])
            font_color = tuple(font_color)
        elif o in ("--edgecolor="):
            edge_color = arg.split(",")
            for i in range(0,3):
                edge_color[i] = int(edge_color[i])
            edge_color = tuple(edge_color)
        elif o in ("-i", "--input"):
            srcflag = True
            src     = repr(str(arg))[1:-1]
        elif o in ("-m"):
            maxline = int(arg) + 4
        elif o in ("-x"):
            rx = float(arg)
        elif o in ("-y"):
            ry = float(arg)
        elif o in ("-s"):
            font_size = int(arg)
        else:
            assert False, "unhandled option"

    if(not srcflag):
        print("No Source File")
        sys.exit()
    if(not outflag):
        print("No Out File")
        sys.exit()
    if(not font_pathflag):
        print("No Font File")
        sys.exit()


    content_list = []
    print("目次を入力")
    try:
        while True:
            print(" > ", end="")
            content_list.append( input() )
            print(content_list[-1])
    except EOFError:
        pass


    while ( "" in content_list ):   #空文字列があったら削除
        content_list.remove("") 

    content_list.reverse()

    textincover(src, output, content_list, font_size, font_path, maxline, rx, ry, font_color, edge_color)

