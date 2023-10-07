#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: ThreadGroup.py
Author: 吉姆哥
Date: 2023/8/27
Description: 线程组
"""
import time

from common.Container import *


class ThreadGroup:

    def __init__(self, delaySecond = 10):
        self.threadGroup = []
        self.delaySecond = delaySecond
        self.log = Container.get('Log')
        Container.set('ThreadGroup', self)

    def getThread(self, index):
        return self.threadGroup[index]

    # 加入线程
    def addThread(self, thread):
        self.threadGroup.append(thread)

    # 开启所有线程
    def startAll(self):
        for threadDict in self.threadGroup:
            threadDict['threadObj'].start()
            time.sleep(self.delaySecond)

    # 暂停所有线程
    def pauseAll(self):
        for threadDict in self.threadGroup:
            if threadDict['threadObj'].is_alive():
                threadDict['threadObj'].pause()

    # 恢复所有线程
    def resumeAll(self):
        for threadDict in self.threadGroup:
            if threadDict['threadObj'].is_alive() and threadDict['threadObj'].thread_flag == 1:
                threadDict['threadObj'].resume()

    # 结束所有线程
    def stopAll(self):
        for threadDict in self.threadGroup:
            if threadDict['threadObj'].is_alive():
                threadDict['threadObj'].stop()


    def joinAll(self):
        for threadDict in self.threadGroup:
            threadDict['threadObj'].join()

    def clear(self):
        self.threadGroup.clear()

    def delAll(self):
        self.clear()

    def unbindThread(self):
        # 多开数量
        for threadDict in self.threadGroup:
            if 'op' in threadDict:
                self.log.info('解绑并停止线程: %s 成功' % (threadDict['threadIdent']))
                threadDict['op'].UnBindWindow()