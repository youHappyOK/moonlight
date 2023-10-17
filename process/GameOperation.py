#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: GameOpration.py
Author: 吉姆哥
Date: 2023/8/27
Description: 游戏操作
"""

from common.Container import Container
from plugin.Action import Action
from resources.Desc import desc


# 这个文件加密后运行始终有问题，怀疑是lamdba表达式被cython编译有问题

class GameOperation:

    def __init__(self):
        self.log = Container.get('Log')
        Container.set('GameOperation', self)

    def gameOpration(self, threadDict, threadIndex):
        opWapper = threadDict['op']
        self.log.info('窗口句柄: %s 游戏中...' % threadDict['bindHwnd'])
        task = [
            # Action(desc['文本图标']).func(lambda: print('找到文本图标')).offset(3, 0).leftDoubleClick()
            # .keyPressStr('so nvidia fuck you\n').interval(1),
            # Action(None).click(729, 14),
            # Action(None).click(661, 378),
            # Action(desc['文本图标关闭']).func(lambda: print('找到文本图标关闭')).click().exit(),
            Action(desc['最近']).click().exit(),
        ]
        opWapper.run(task, times=0)

