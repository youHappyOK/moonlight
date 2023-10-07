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

    def func(self, method, *args, **kwargs):
        # 使用 functools.partial 传递参数
        self.methods.append((method, args, kwargs))
        return self

    def click(self, *args):
        self.methods.append(('LeftClick', args))
        return self

