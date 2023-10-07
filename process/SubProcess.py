#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: SubThread.py
Author: 吉姆哥
Date: 2023/8/27
Description: 每个线程的运行流程
"""
import os
import sys
import threading

from common.Container import *
from common.OpTool import OpTool
from plugin.OpWrapper import OpWrapper
from process.GameOperation import GameOperation


class SubProcess:

    def __init__(self):
        self.gameOpration = Container.get('GameOperation')
        Container.set('SubProcess', self)

    def runProcess(self, threadIndex: int, bindHwnd: int):
        log = Container.get('Log')
        log.info('初始化线程op对象')
        op = OpTool.getOpObj()
        opWrapper = OpWrapper(op)
        threadDict = Container.get('ThreadGroup').getThread(threadIndex)
        threadDict['op'] = opWrapper
        threadDict['bindHwnd'] = bindHwnd
        gameOperation = Container.get('GameOperation')
        threadDict['process'] = '绑定窗口'
        while True:
            log.info('线程: %s 运行中...' % threading.currentThread().ident)
            if threadDict['process'] == '绑定窗口':
                if bindHwnd:
                    # 绑定窗口，不知道为啥，虚拟机只能用前台模式绑定
                    bindRet = opWrapper.bindWindow(bindHwnd, 'gdi', 'windows', 'windows', 1)
                    # bindRet = opWrapper.bindWindow(bindHwnd, 'normal', 'normal', 'normal', 1)
                    if bindRet:
                        log.info('绑定成功')
                        threadDict['process'] = '游戏操作'
                    else:
                        log.error('绑定失败')
            if threadDict['process'] == '游戏操作':
                gameOperation.gameOpration(threadDict, threadIndex)






