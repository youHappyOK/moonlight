#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： snapshot.py
    @date：2023/11/14 14:23
    @desc: 
"""
import os
import sys
import time
from ctypes import windll

import win32gui
from PIL import ImageGrab
from win32com.client import Dispatch


# 截图工具，方便以后使用yolo标注
class Snapshot:
    def __init__(self, hwnd, isFront, savePath, isOnce, intervalSecond):
        self.hwnd = hwnd
        self.savePath = savePath
        self.isOnce = isOnce
        self.intervalSecond = intervalSecond
        # 是否前台截图
        self.isFront = isFront
        if not isFront:
            self.initOp()
            # 创建对象
            self.op = Dispatch("op.opsoft")
            # 设置全局路径,设置了此路径后,所有接口调用中,相关的文件都相对于此路径. 比如图片,字库等.
            self.op.SetPath(savePath)
            # 绑定后台
            bindRet = self.op.bindWindow(hwnd, 'gdi', 'normal', 'normal', 1)
            print('绑定结果 %s' % bindRet)

    def snapAndSave(self):
        # 前台截图
        if self.isFront:
            rect = win32gui.GetWindowRect(self.hwnd)
            index = 1  # 初始化序号
            while True:
                windowRect = (rect[0], rect[1], rect[2], rect[3])
                gameImage = ImageGrab.grab(windowRect)

                # 生成新的文件名
                newFileName = f'{index}.png'
                savePath = os.path.join(self.savePath, newFileName)

                # 保存截图至指定目录
                gameImage.save(savePath)
                print('完成截图：%s' % newFileName)
                if self.isOnce:
                    break
                else:
                    index += 1  # 更新序号
                    time.sleep(self.intervalSecond)
        # 后台截图
        else:
            index = 1  # 初始化序号
            while True:
                # 生成新的文件名
                newFileName = f'{index}.png'
                self.op.Capture(0, 0, 2000, 2000, newFileName)
                print('完成截图：%s' % newFileName)
                if self.isOnce:
                    break
                else:
                    index += 1
                    time.sleep(self.intervalSecond)

    def initOp(self):
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        # 初始化全局op对象
        # 加载免注册dll
        dll = windll.LoadLibrary(baseDir + "\\" + 'tools_64.dll')
        # 调用setupW函数
        result = dll.setupW(baseDir + "\\" + 'op_x64.dll')
        # 如果result不等于1,则执行失败
        if result != 1:
            exit(0)

if __name__ == '__main__':
    s = Snapshot(525816, False, r'D:\截图', False, 1)
    s.snapAndSave()
