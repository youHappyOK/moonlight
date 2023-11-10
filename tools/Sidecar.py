import ctypes
import logging
import os
import sys
from ctypes import windll
from flask import Flask, request, json
from win32com.client import Dispatch

class Sidecar:
    def __init__(self):
        # 使用op来做虚拟机内部的前台键鼠
        self.initOp()
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        # 创建对象
        self.op = Dispatch("op.opsoft")
        # 设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径. 比如图片,字库等.
        self.op.SetPath(baseDir + "\\" + 'resources')

    @staticmethod
    def initOp():
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        # 初始化全局op对象
        # 加载免注册dll
        dll = windll.LoadLibrary(baseDir + "\\" + 'tools_64.dll')
        # 调用setupW函数
        result = dll.setupW(baseDir + "\\" + 'op_x64.dll')
        # 如果result不等于1,则执行失败
        if result != 1:
            exit(0)

app = Flask(__name__)
# 关闭flask终端输出的请求/响应记录日志
log = logging.getLogger('werkzeug')
log.disabled = True

sidecar = Sidecar()

@app.route('/moveTo', methods=['POST'])
def moveTo():
    # 接收处理json数据请求
    data = json.loads(request.data)  # 将json字符串转为dict
    x = data['x']
    y = data['y']
    # 创建两个整型指针
    ret = sidecar.op.GetCursorPos()
    print(ret)

    # print("current cx: %s, cy:%s" % (current_x, current_y))
    print("moveTo x: %s, y:%s" % (x, y))
    sidecar.op.moveTo(x, y)
    return 'hello world'


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=8080)
