#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： OpWrapper.py
    @date：2023/10/7 14:13
    @desc: 
"""
import time
import random

from common.Container import Container
from input.BezierMouse import BezireMouse
from input.OpInputHidKeyCode import OpInputHidKeyCode
from plugin.Point import Point


class OpWrapper:

    def __init__(self, op):
        self.op = op
        self.yjsInput = None
        self.config = Container.get('ApplicationProperties')
        self.bindWin = 0

    def setYjsInput(self, yjsInput):
        self.yjsInput = yjsInput

    def bindWindow(self, *args):
        self.bindWin = args[0]
        return self.op.BindWindow(*args)

    def unbindWindow(self):
        self.op.UnBindWindow()

    def rebindWindow(self, *args):
        self.bindWin = args[0]
        return self.op.BindWindow(*args)

    def enumWindow(self, title, className, filter):
        unbindHwnds = []
        hwnd0 = self.op.EnumWindow(0, title, className, filter)
        if hwnd0 != '':
            for hwnd1 in hwnd0.split(','):
                unbindHwnds.append(hwnd1)
        return unbindHwnds

    def activeWindow(self, bindWin):
        self.op.SetWindowState(bindWin, 1)

    def miniWindow(self, bindWin):
        self.op.SetWindowState(bindWin, 2)

    # 循环执行
    def run(self, actionList, times=0):
        breakFlag = {'exit': False}
        runTime = 0
        while True:
            if breakFlag['exit']:
                break
            if times != 0 and runTime >= times:
                return
            self.runOnce(actionList, breakFlag)
            if times:
                runTime += 1

    # 只执行一次
    def runOnce(self, actionList, breakFlag):

        actionhasOrder = False

        for action in actionList:
            order = action.orderNum
            if order == 0:
                continue
            else:
                actionhasOrder = True
                break

        # 如果有顺序对actionList排序
        if actionhasOrder:
            actionList = sorted(actionList, key=lambda x: x.orderNum)

        runOrder = 1
        while runOrder <= len(actionList):

            action = actionList[runOrder - 1]
            print(*action.argsArr)
            findPicRet = None
            if action.argsArr:
                findPicRet = self.findPic(action)
            # 没有传argsArr或者找图找到了
            if not action.argsArr or (not findPicRet[0] == -1 and not findPicRet[1] == -1 and not findPicRet[2] == -1):
                action.point = Point(findPicRet[1], findPicRet[2])
                # 按顺序执行里面的每个方法
                for method in action.methods:
                    methodName = method[0]
                    # 这里接受到的是一个元组tuple
                    methodArgs = method[1]
                    # 这里接收到的是一个dict
                    methodKw = method[2]
                    if type(methodName) == str:
                        # 判断method传的是否为字符串，如果为字符串，说明是op的方法
                        if methodName == 'LeftClick':
                            if not methodArgs:
                                self.moveTo(action.point.x, action.point.y)
                            else:
                                self.moveTo(methodArgs[0], methodArgs[1])
                            self.leftClick()
                        if methodName == 'LeftDoubleClick':
                            self.moveTo(action.point.x, action.point.y)
                            self.leftDoubleClick()
                        if methodName == 'KeyPressStr':
                            self.KeyPressStr(*methodArgs)
                        if methodName == 'sleep':
                            # 这里要加*的原因是methodArgs是一个元组，而time.sleep的参数是一个参数
                            # 所以，要通过*将元组的所有元素作为可变参数传进去
                            time.sleep(*methodArgs)
                        if methodName == 'offset':
                            offset = methodArgs[0]
                            offsetType = methodArgs[1]
                            if offsetType == 0:
                                # 点击偏移
                                randOffset = random.randint(-offset, offset)
                                action.point.x += randOffset
                                action.point.y += randOffset
                            if offsetType == 1:
                                # 滑动偏移
                                pass
                        if methodName == '退出':
                            breakFlag['exit'] = True
                            break
                    else:
                        # 执行lambda函数
                        method[0](*method[1], **method[2])
                    # 同一个action中两个method的间隔时间，默认0.3s
                    time.sleep(action.intervalTime)
                if breakFlag['exit']:
                    runOrder += 1
                    break
            else:
                if actionhasOrder:
                    time.sleep(1)
                    # 如果没找到图且有顺序，就重复循环找
                    continue

            runOrder += 1
            time.sleep(1)

    def moveTo(self, x, y):
        # 易键鼠鼠标移动自带轨迹
        if self.config.useYjs:
            self.yjsInput.moveTo(x, y)
        else:
            if self.config.useFrontMouseCurve:
                self.moveToWithCurve(x, y)
            else:
                self.op.MoveTo(x, y)

    # 带轨迹移动
    def moveToWithCurve(self, x, y):
        # 当前坐标
        ret = self.op.GetCursorPos()
        startPoint = (ret[1], ret[2])
        endPoint = (x, y)
        # print("current point %s" % str(startPoint))
        # print("moveTo x: %s, y:%s" % (x, y))
        bezierCurve = BezireMouse.generateBezierCurve(startPoint, endPoint)
        totalPoints = len(bezierCurve)
        speedFactor = BezireMouse.calculateSpeedFactor(startPoint, endPoint)
        # print(speedFactor)
        for i in range(0, len(bezierCurve), speedFactor):
            point = bezierCurve[i]
            self.op.moveTo(point[0], point[1])
            progress = i / totalPoints
            delay = BezireMouse.customEase(progress) * 0.01
            time.sleep(delay)
        self.op.moveTo(x, y)

    def leftClick(self):
        if self.config.useYjs:
            self.yjsInput.leftClick()
        else:
            self.op.LeftClick()

    def leftDoubleClick(self):
        if self.config.useYjs:
            self.yjsInput.leftDoubleClick()
        else:
            self.op.LeftDoubleClick()

    def KeyPressStr(self, *args):
        if self.config.useYjs:
            self.yjsInput.KeyPressStr(*args)
        else:
            for arg in args[0]:
                self.KeyPressChar(arg)
                time.sleep(random.uniform(0.1, 0.3))

    def KeyPressChar(self, *args):
        if self.config.useYjs:
            self.yjsInput.keyPressChar(*args)
        else:
            if args[0] == '@':
                self.op.KeyDownChar('shift')
                self.op.KeyDownChar('2')
                self.op.KeyUpChar('2')
                self.op.KeyUpChar('shift')
            if args[0] == '*':
                self.op.KeyDownChar('shift')
                self.op.KeyDownChar('8')
                self.op.KeyUpChar('8')
                self.op.KeyUpChar('shift')
            if args[0] == '.':
                self.op.KeyPress(OpInputHidKeyCode['.'])
            else:
                self.op.KeyPressChar(*args)


    # 找图方法
    def findPic(self, action):
        if self.config.findPicMethod == 'op':
            return self.op.FindPic(*action.argsArr, 0, 0)
        if self.config.findPicMethod == 'opencv':
            # 使用opencv截图时，窗口不能提前被op绑定
            isFind, x, y = self.cvFind.findPicByTemplate(self.bindWin,
                                                    action.argsArr[0],
                                                    action.argsArr[1],
                                                    action.argsArr[2],
                                                    action.argsArr[3],
                                                    action.argsArr[4],
                                                    action.argsArr[6],
                                                    False,
                                                    self.config.useFrontShot)
            if isFind:
                return 1, x, y
            else:
                return -1, -1, -1

    def unbind(self):
        self.op.UnBindWindow()