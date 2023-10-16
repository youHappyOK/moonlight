#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: MainProcess.py
Author: 吉姆哥
Date: 2023/8/27
Description: 用于控制并开启游戏的主流程
"""
from common.CustomerThread import *
from common.OpTool import OpTool


class MainProcess:

    def __init__(self):
        self.threadGroup = Container.get('ThreadGroup')
        self.log = Container.get('Log')
        Container.set('MainProcess', self)

    def runMainProcess(self):
        runProcessMainThread = threading.Thread(target=self.runThread, name='runMainProcess')
        # 启动线程组，每个窗口一个线程负责
        runProcessMainThread.start()

    # 启动threadNum个子线程线程
    def runThread(self):
        subProcess = Container.get("SubProcess")
        # 多开数量
        threadNum = 1
        # 启动延迟(默认10秒)
        self.threadGroup.delaySecond = 10
        self.log.info('启动 %s 个线程...' % threadNum)
        unbindHwnds = self.findUnbindWindows()
        for i in range(threadNum):
            threadObj = CustomThread(subProcess.runProcess, args=(i, unbindHwnds[i]), name='runSubProcess')
            threadDict = {'threadObj': threadObj}
            # 加入线程组
            self.threadGroup.addThread(threadDict)
        # 启动线程组
        self.threadGroup.startAll()

    def findUnbindWindows(self):
        # unbindHwnds = []
        # log = Container.get('Log')
        # OpTool.initOp()
        # op = OpTool.getOpObj()
        # hwnd0 = op.EnumWindow(0, '', 'VMPlayerFrame', 2)
        # if hwnd0 != '':
        #     for hwnd1 in hwnd0.split(','):
        #         hwnd2 = op.EnumWindow(hwnd1, '', 'VMWindow', 2)
        #         hwnd3 = op.EnumWindow(hwnd2, '', 'VMPlayerGuest', 2)
        #         hwnd4 = op.EnumWindow(hwnd3, 'MKSWindow#0', 'MKSEmbedded', 1 + 2)
        #         # 将未绑定的句柄放到unbindHwnds中
        #         log.info('枚举窗口 hwnd: %s 成功' % hwnd4)
        #         unbindHwnds.append(hwnd4)
        # return unbindHwnds


        unbindHwnds = []
        OpTool.initOp()
        op = OpTool.getOpObj()
        hwnd0 = op.EnumWindow(0, 'WPS Office', 'OpusApp', 1+2)
        if hwnd0 != '':
            for hwnd1 in hwnd0.split(','):
                unbindHwnds.append(hwnd1)
        return unbindHwnds