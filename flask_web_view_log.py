#!/usr/bin/env python
#coding:utf-8
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    f = open("log")    #log是当前目录下文件名，里面是日志绝对路径
    for log in f.readlines():
        cmd = 'tail -n100 %s'%(log)
        result_list = os.popen(cmd).readlines()
        result = '<br/>'.join(result_list)
    return result
if __name__ == '__main__':
        app.run(host="0.0.0.0", port=9000, debug="Ture")