#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： Action.py
    @date：2023/10/7 9:50
    @desc: 
"""
from functools import partial
from plugin.Point import Point


class Action:

    def __init__(self, argsArr):
        self.argsArr = argsArr
        self.methods = []
        self.point = None

    # 自定义函数
    def func(self, method, *args, **kwargs):
        # 使用 functools.partial 传递参数
        self.methods.append((method, args, kwargs))
        return self

    # 调用op的左键
    def click(self, *args):
        self.methods.append(('LeftClick', args, None))
        return self

    # 操作间sleep
    def sleep(self, *args):
        self.methods.append(('sleep', args, None))
        return self

    # 点击和移动偏移量像素
    # 传参
    # offset int 偏移像素(是一个范围[-offset, offset])
    # type int 0：点击偏移，1：滑动偏移
    def offset(self, *args):
        self.methods.append(('offset', args, None))
        return self

        

