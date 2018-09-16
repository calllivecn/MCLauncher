#!/usr/bin/env py3
#coding=utf-8
# date 2018-09-01 20:36:29
# author calllivecn <c-all@qq.com>



import tkinter as tk


def getuserinfo():

    print("username:",entry1.get())
    print("password:",entry2.get())
    print("select versioin:",listbox3.get(listbox3.curselection()))
    
    

win = tk.Tk()

win.title("MCL v1.0 author zx")
#win.geometry("400x200")

frame1 = tk.Frame(win)
frame1.pack(side="top",fill="x")

label1 = tk.Label(frame1,text="用户名:")
label1.pack(side="left")


username = tk.StringVar(value="天天MC")
entry1 = tk.Entry(frame1,textvariable=username)
entry1.pack(side="left",fill="x",expand="yes")

frame2 = tk.Frame(win)
frame2.pack(side="top",fill="x")

label2 = tk.Label(frame2,text="密码:")
label2.pack(side="left")

entry2 = tk.Entry(frame2,show="*")
entry2.pack(side="left",fill="x",expand="yes")

frame3 = tk.Frame(win)
frame3.pack(side="top",fill="x")

label3 = tk.Label(frame3,text="版本")
label3.pack(side="left")


scrollbar3 = tk.Scrollbar(frame3)
scrollbar3.pack(side=tk.RIGHT,fill=tk.Y)


versions=['1.13.1',"1.13","1.10","1.10.2","1.12.2","1.11.2"]
versions.sort(reverse=True)

version = tk.StringVar(value=versions)
listbox3 = tk.Listbox(frame3,height=3,listvariable=version,selectmode=tk.BROWSE,yscrollcommand=scrollbar3.set)
listbox3.pack(side="left",fill="x",expand="yes")
listbox3.select_set(0)
scrollbar3.config(command=listbox3.yview)

# for i in range(14):
#     listbox3.insert(tk.END,i)

button1 = tk.Button(win,text="启动",command=getuserinfo)
button1.pack(anchor="ne")
button1.bind("<Return>",func=lambda event: getuserinfo())

win.mainloop()
