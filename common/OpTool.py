#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from ctypes import *
from win32com.client import Dispatch

from common.Container import Container
from common.Log import Log


class OpTool:

    # 初始化全局op对象
    @staticmethod
    def initOp():
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        log = Container.get('Log')
        # 初始化全局op对象
        # 加载免注册dll
        dll = windll.LoadLibrary(baseDir + "\\" + 'tools_64.dll')
        # 调用setupW函数
        result = dll.setupW(baseDir + "\\" + 'op_x64.dll')
        # 如果result不等于1,则执行失败
        if result != 1:
            exit(0)

    @staticmethod
    def getOpObj():
        log = Container.get('Log')
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        # 创建对象
        op = Dispatch("op.opsoft")
        # 设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径. 比如图片,字库等.
        op.SetPath(baseDir + "\\" + 'resources')
        # 打印op插件的版本
        log.info(op.Ver())
        log.info(op.GetPath())
        return op


if __name__ == '__main__':
    Log()
    op = OpTool()
    op.initOp()