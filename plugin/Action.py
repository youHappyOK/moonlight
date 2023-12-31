#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： Action.py
    @date：2023/10/7 9:50
    @desc: 
"""


class Action:

    def __init__(self, argsArr):
        self.argsArr = argsArr
        self.methods = []
        self.point = None
        self.intervalTime = 0.3
        self.isFindPic = False

    # 自定义函数
    def func(self, method, *args, **kwargs):
        # 使用 functools.partial 传递参数
        self.methods.append((method, args, kwargs))
        return self

    # 左键单击
    def click(self, *args):
        self.methods.append(('LeftClick', args, None))
        return self

    def leftDoubleClick(self, *args):
        self.methods.append(('LeftDoubleClick', args, None))
        return self

    # 操作间sleep
    def sleep(self, *args):
        self.methods.append(('sleep', args, None))
        return self

    def interval(self, time):
        self.intervalTime = time
        return self

    # 点击和移动偏移量像素
    # 传参
    # offset int 偏移像素(是一个范围[-offset, offset])
    # type int 0：点击偏移，1：滑动偏移
    def offset(self, *args):
        self.methods.append(('offset', args, None))
        return self

    def keyPressStr(self, *args):
        self.methods.append(('KeyPressStr', args, None))
        return self

    # 按单个字符
    def keyPressC(self, *args):
        self.methods.append(('KeyPressChar', args, None))
        return self

    def exit(self):
        self.methods.append(('退出', None, None))
        return self



        

