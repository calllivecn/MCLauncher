#!/usr/bin/env py3
#coding=utf-8
# date 2018-09-01 20:36:29
# author calllivecn <c-all@qq.com>


import os
from os import path
import tkinter as tk
from tkinter import ttk

def get_win_location(win):#,H=200, W=400):
    width = win.winfo_screenwidth()
    height = win.winfo_screenheight()

    win.update()

    x = win.winfo_width()
    y = win.winfo_height()

    x_real = (width - x )//2
    y_real = (height -y )//2
    #print( x, y, "+" + str(x_real) + "+" + str(y_real))
    return "+" + str(x_real) + "+" + str(y_real)


def getuserinfo():
    global version

    print("username:",entry1.get())
    print("password:",entry2.get())
    print("select versioin:",version.get())
    

def getversion(listbox,window):
    global version
    version.set(listbox.get(listbox.curselection()))
    
    window.destroy()


def getversions(PATH="."):
    global win
    if path.exists(path.join(PATH)):
        return os.listdir(PATH)

def select_version():
    global win
    select_win = tk.Toplevel(win)
    select_win.update()
    select_win.geometry(get_win_location(select_win))

    select_win.title("请选择版本")

    #versions=['1.13.1',"1.13","1.10","1.10.2","1.12.2","1.11.2"]

    versions = getversions()

    versions.sort(reverse=True)

    version = tk.StringVar(value=versions)

    scrollbar3 = ttk.Scrollbar(select_win)
    scrollbar3.pack(side=tk.RIGHT,fill=tk.Y)

    listbox = tk.Listbox(select_win,height=5,listvariable=version,selectmode=tk.BROWSE,yscrollcommand=scrollbar3.set)
    listbox.pack(side="left",fill="x",expand="yes")
    listbox.select_set(0)

    scrollbar3.config(command=listbox.yview)

    button = ttk.Button(select_win,text="确定",command=lambda : getversion(listbox, select_win))
    button.pack(anchor="se")
    button.bind("<Return>",func=lambda event: getversion(listbox, select_win))


win = tk.Tk()
win.geometry(get_win_location(win))#("400x200")

win.title("MCL v1.0")

frame1 = ttk.Frame(win)
frame1.pack(side="top",fill="x")

label1 = ttk.Label(frame1,text="用户名:")
label1.pack(side="left")


username = tk.StringVar(value="天天MC")
entry1 = ttk.Entry(frame1,textvariable=username)
entry1.pack(side="left",fill="x",expand="yes")

frame2 = ttk.Frame(win)
frame2.pack(side="top",fill="x")

label2 = ttk.Label(frame2,text="密  码:")
label2.pack(side="left")

entry2 = ttk.Entry(frame2,show="*")
entry2.pack(side="left",fill="x",expand="yes")

frame3 = ttk.Frame(win)
frame3.pack(side="top",fill="x")

label3 = ttk.Label(frame3,text="版本:")
label3.pack(side="left")

version = tk.StringVar(value="默认")
label4 = ttk.Label(frame3,textvariable=version)
label4.pack(side="left")

button2 = ttk.Button(frame3, text="选择版本", command=select_version)
button2.bind("<Return>",func=lambda event: select_version())
button2.pack(side="right")


# select game version



# for i in range(14):
#     listbox3.insert(tk.END,i)
frame4 = ttk.Frame(win)
frame4.pack(side="bottom",fill="x")

label5 = ttk.Label(frame4, text="Author: calllivecn")
label5.pack(side="left")

button1 = ttk.Button(frame4,text="启动",command=getuserinfo)
button1.bind("<Return>",func=lambda event: getuserinfo())
button1.pack(side="right")

win.mainloop()
