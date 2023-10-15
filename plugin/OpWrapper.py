#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： MyOp.py
    @date：2023/10/7 14:13
    @desc: 
"""
import time
import random

from plugin.Point import Point


class OpWrapper:

    def __init__(self, op):
        self.op = op

    def bindWindow(self, *args):
        return self.op.BindWindow(*args)

    def run(self, actionList):
        while True:
            for action in actionList:
                # todo 支持找图
                findPicRet = self.op.FindPic(*action.argsArr, 0, 0)
                # self.op.Capture(0,0,2000,2000,'2k缩放175不设置兼容性.bmp')
                # 如果找图找到了
                if not findPicRet[0] == -1 and not findPicRet[1] == -1 and not findPicRet[2] == -1:
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
                                self.op.MoveTo(action.point.x, action.point.y)
                                self.op.LeftClick()
                            if methodName == 'sleep':
                                # 这里要加*的原因是methodArgs是一个元组，而time.sleep的参数是一个参数
                                # 所以，要通过*将元组的所有元素作为可变参数传进去
                                time.sleep(*methodArgs)
                            if methodName == 'offset':
                                offset = method[0]
                                offsetType = method[1]
                                if offsetType == 0:
                                    # 点击偏移
                                    randOffset = random.randint(-offset, offset)
                                    action.point.x += randOffset
                                    action.point.y += randOffset
                                if offsetType == 1:
                                    # 滑动偏移
                                    pass
                            if methodName == '退出':
                                break
                        else:
                            # 执行lambda函数
                            method[0](*method[1], **method[2])
                time.sleep(10)



