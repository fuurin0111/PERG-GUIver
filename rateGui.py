import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import random
import time
import csv

# アプリの作成
root = tk.Tk()

# 諸設定
root.geometry("1024x720")
root.title("擬似為替レートアプリ")
root.configure(bg="white")

#csvからセーブデータを取得
url = 'url'
data = [[-1,-1,-1]]
money = 0
pre_money = 0

EMPTY = 0
def read():
    # CSVファイルの読み込み
    with open(url, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data[EMPTY] = list(map(int, row))

def write():
    data[EMPTY][0] = money
    data[EMPTY][1] = rate_all[len(rate_all)-1]
    data[EMPTY][2] = pre_money
    with open(url, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

read()

if data[EMPTY] == [-1,-1,-1] or data[EMPTY] == [ 0, 0, 0]:
    data[EMPTY][0] = 1000
    data[EMPTY][1] = random.randint(100,200)
    data[EMPTY][2] = 0

BUYMONEY = 100

#買うボタン押した時
def buy():
    global money,pre_money
    if BUYMONEY <= money and BUYMONEY >= 0:
            money -= BUYMONEY
            pre_money += round((100/rate_all[len(rate_all)-1])*BUYMONEY)
            text1.set(f"現在のレートは{rate_all[len(rate_all)-1]}円=100プレ,手持ち金額{money}円,{pre_money}プレ")
            text2.set(f"{BUYMONEY}円分買いました。残り{money}円")
            write()
    else:
        text2.set("買えませんでした")

#買うボタン押した時
def sell():
    global money,pre_money
    if BUYMONEY <= pre_money and BUYMONEY >= 0:
            money += round((rate_all[len(rate_all)-1]/100)*BUYMONEY)
            pre_money -= BUYMONEY
            text1.set(f"現在のレートは{rate_all[len(rate_all)-1]}円=100プレ,手持ち金額{money}円,{pre_money}プレ")
            text2.set(f"{BUYMONEY}プレ分売りました。残り{pre_money}プレ")
            write()
    else:
        text2.set("売れませんでした")

def ender():
    text2.set("終わります")
    write()
    time.sleep(1)
    root.destroy()

#ボタンサイズと場所設定
btn_buy = tk.Button(text="buy",fg="tomato",width=6, height=2,font=("",96),command=buy).place(x=75,y=475)
btn_sell = tk.Button(text="sell",fg="deepskyblue",width=6, height=2,font=("",96),command=sell).place(x=550,y=475)
btn_end = tk.Button(text="end",fg="black",width=6, height=2,font=("",20),command=ender).place(x=900,y=400)

#canvaサイズ
canva = tk.Canvas(root, width=1000, height=350)
canva.pack()

#グラフの元
RATESUM = 30
rate_all = [0]*(RATESUM-1)

money = data[EMPTY][0]
rate_all.append(data[EMPTY][1])
pre_money = data[EMPTY][2]

#グラフデータ
x = np.array(range(len(rate_all)))
y = np.array(rate_all)

#グラフ用オブジェクト生成
fig = Figure(figsize=(20,4), dpi=100)   #Figure
ax = fig.add_subplot(1, 1, 1)           #Axes
line, = ax.plot(x, y)                   #2DLine
point, = ax.plot(x, y,".",markersize=15)

#Figureを埋め込み
canvas = FigureCanvasTkAgg(fig, canva)
canvas.get_tk_widget().pack()

#文字ラベル
text1 = tk.StringVar()
text1.set(f"現在のレートは{rate_all[len(rate_all)-1]}円=100プレ,手持ち金額{money}円,{pre_money}プレ")
text_label = tk.Label(root, textvariable=text1,font=("",28)).place(x=100,y=390)

text2 = tk.StringVar()
text2.set(f"")
text_label = tk.Label(root, textvariable=text2,font=("",28)).place(x=100,y=425)

TIME = 4000

def repeat():
    for i in range(len(rate_all)):
        if i >= len(rate_all)-1:
            rate_all[i] += random.randrange(-1*round(rate_all[len(rate_all)-1]/2),round(rate_all[len(rate_all)-1]/2))
            text2.set("")
        else:
            rate_all[i] = rate_all[i+1]

    choice = random.randrange(0,99)
    if rate_all[len(rate_all)-1] <= 5:
        text2.set("レート急上昇")
        rate_all[len(rate_all)-1] = random.randint(100,300)
        write()
    if choice <= 5:
        text2.set("レート急上昇")
        rate_all[len(rate_all)-1] += random.randint(rate_all[len(rate_all)-1],round(rate_all[len(rate_all)-1]*1.5))
        write()
    elif choice >= 94:
        text2.set("レート急降下")
        rate_all[len(rate_all)-1] += random.randint(-1*rate_all[len(rate_all)-1]+10,-1*round(rate_all[len(rate_all)-1]/2)+10)
        write()

    #グラフデータ
    y = np.array(rate_all)
    ax.set_ylim(0,max(rate_all))
    line.set_ydata(y)
    point.set_ydata(y)
    canvas.draw()
    text1.set(f"現在のレートは{rate_all[len(rate_all)-1]}円=100プレ,手持ち金額{money}円,{pre_money}プレ")
    root.after(TIME, repeat)

#スタート
root.after(TIME, repeat)
root.mainloop()
