#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： MyOp.py
    @date：2023/10/7 14:13
    @desc: 
"""
import time

from plugin.Point import Point


class OpWrapper:

    def __init__(self, op):
        self.op = op

    def bindWindow(self, *args):
        return self.op.BindWindow(*args)

    def run(self, actionList):
        while True:
            for action in actionList:
                findPicRet = self.op.FindPic(*action.argsArr, 0, 0)
                # self.op.Capture(0,0,2000,2000,'2k缩放175不设置兼容性.bmp')
                # 如果找图找到了
                if not findPicRet[0] == -1 and not findPicRet[1] == -1 and not findPicRet[2] == -1:
                    action.point = Point(findPicRet[1], findPicRet[2])
                    # 按顺序执行里面的每个方法
                    for method in action.methods:
                        if type(method[0]) == str:
                            # 判断method传的是否为字符串，如果为字符串，说明是op的方法
                            if method[0] == 'LeftClick':
                                self.op.MoveTo(action.point.x, action.point.y)
                                self.op.LeftClick()
                            if method[0] == '退出':
                                break
                        else:
                            # 执行lambda函数
                            method[0](*method[1], **method[2])
                time.sleep(10)



