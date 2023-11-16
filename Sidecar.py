import logging
import os
import random
import sys
import time
from ctypes import windll

from flask import Flask, request, json
from win32com.client import Dispatch
from input.BezierMouse import BezireMouse


class Sidecar:
    def __init__(self):
        # 使用op来做虚拟机内部的前台键鼠
        self.initOp()
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(__file__)
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
            baseDir = os.path.dirname(__file__)
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

# 鼠标移动
# todo 正太分布
@app.route('/moveTo', methods=['POST'])
def moveTo():
    # 接收处理json数据请求
    data = json.loads(request.data)  # 将json字符串转为dict
    x = data['x']
    y = data['y']
    useCurve = data['useCurve']
    if useCurve:
        # 当前坐标
        ret = sidecar.op.GetCursorPos()
        startPoint = (ret[1], ret[2])
        endPoint = (x, y)
        # print("current point %s" % str(startPoint))
        # print("moveTo x: %s, y:%s" % (x, y))
        bezierCurve = BezireMouse.generateBezierCurve(startPoint, endPoint)
        totalPoints = len(bezierCurve)
        speedFactor = calculateSpeedFactor(startPoint, endPoint)
        print(speedFactor)
        for i in range(0, len(bezierCurve), speedFactor):
            point = bezierCurve[i]
            sidecar.op.moveTo(point[0], point[1])
            progress = i / totalPoints
            delay = customEase(progress) * 0.01
            time.sleep(delay)
    else:
        sidecar.op.moveTo(x, y)
    return 'ok'

# 鼠标点击
@app.route('/click', methods=['POST'])
def click():
    # 接收处理json数据请求
    data = json.loads(request.data)
    times = int(data['times'])
    clickType = data['type']
    if times == 1:
        if clickType == 'left':
            sidecar.op.LeftClick()
        elif clickType == 'right':
            sidecar.op.RightClick()
    elif times >= 2:
        if clickType == 'left':
            sidecar.op.LeftDoubleClick()
        elif clickType == 'right':
            sidecar.op.RightDoubleClick()
    return 'ok'

# 键盘输入
@app.route('/keyPress', methods=['POST'])
def keyPress():
    # 将json字符串转为dict
    data = json.loads(request.data)
    key = data['key']
    type = data['type']
    if type == 'char':
        sidecar.op.KeyPressChar(key)
    elif type == 'str':
        for c in key:
            # 生成0.1到0.4之间的随机数
            randomSleepTime = random.uniform(0.1, 0.3)
            # 休眠相应的时间
            time.sleep(randomSleepTime)
            sidecar.op.KeyPressChar(c)
    else:
        raise ValueError('Invalid type value: must be "char" or "str"')
    return 'ok'

def calculateSpeedFactor(startPoint, endPoint):
    distance = ((endPoint[0] - startPoint[0]) ** 2 + (endPoint[1] - startPoint[1]) ** 2) ** 0.5
    if distance < 100:
        return 4
    elif distance >= 100 and distance < 500:
        return 5
    elif distance >= 500 and distance < 1000:
        return 6
    elif distance >= 1000 and distance < 2000:
        return 8
    elif distance >= 2000:
        return 10

def customEase(p):
    a = 0
    if p < 3 / 4:
        p = (p * 1.5)  # Scale to [0, 1]
        a = 0.01 * (100 - 90 * p)  # Decrease sleep time for acceleration
    else:
        p = ((p - 2 / 3) * 3)  # Scale to [0, 1]
        a = 0.01 * (1 + 90 * p)  # Increase sleep time for deceleration
    # print(a)
    return a


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=8080)
