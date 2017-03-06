#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Tkinter import *
import os, sys, re

def search(path, string):
    result_list = []
    if os.path.isdir(path):
        if not string:
            return "关键字不能为空！"
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path) as data:
                    for line_num, line in enumerate(data):
                        m = re.search(r'%s'%string, line)
                        if m:
                            result_list.append("%s --> [line:%s]" % (file_path, line_num+1))
        return result_list
    else:
        return path + "目录不存在！"

def result():
    dira = d.get()
    key = k.get()
    rst = search(dira, key)
    t.delete(0.0, END)  #每次执行就清空文本框
    if len(rst) == 0:
        t.insert(END, "没有你要搜索的结果...")
    if isinstance(rst, list):
        for i in rst:
            t.insert(END, "%s\n"%i)  #最后插入执行结果
    else:
        t.insert(END, rst)

root = Tk()
root.title('递归搜索目录包含关键字的文件')
root.geometry("600x500")
# w, h = root.maxsize()   #根据分辨率放大窗口
# root.geometry("{}x{}".format(w, h))

l = Label(root, text="目录：")
# sticky设置对齐方式：N（上中）,E（右中），S（底中）,W（左中）
# NE(右上角)，SE（右下角），SW（左下角），NW（左上角）
l.grid(row=0, column=0, sticky=W)   

d = Entry(root,  font=('宋体,16'), bd="2", width="30")
d.grid(row=0, column=0)

l2 = Label(root, text="关键字：")
l2.grid(row=1, column=0, sticky=W)

k = Entry(root, font=('宋体,16'), bd="2", width="30")
k.grid(row=1, column=0)

b = Button(root, text='执行', font=('宋体,12'), bd="5", command=result)  #绑定函数
b.grid(row=2, column=0)

t = Text(root, height="1000", width="80", fg="black", bg="white", font=('宋体,16'))
t.grid()

root.mainloop()