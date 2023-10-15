#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： InputTool.py
    @date：2023/10/15 1:10
    @desc: 
"""
import ctypes
import os
import sys
import time
from ctypes import windll, wintypes

from common import YjsInputHidKeyCode
from common.Container import Container

# 一个线程持有一个YjsInputTool
class YjsInputTool:

    # 初始化易建鼠dll
    def __init__(self, vid, pid, width, high):
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        # log = Container.get('Log')
        # 加载免注册dll
        self.objDll = windll.LoadLibrary(baseDir + "\\resources\\" + 'msdk.dll')
        self.objDll.M_Open_VidPid.restype = wintypes.LPHANDLE
        # 打开易键鼠盒子
        self.hdl = self.objDll.M_Open_VidPid(vid, pid)
        # 输入被控机的屏幕分辨率
        self.objDll.M_ResolutionUsed(self.hdl, width, high)

    def KeyPressStr(self, str: str):
        bt_str = str.encode(encoding="gbk")
        len_ = len(bt_str)
        p_str = ctypes.c_char_p(bt_str)
        self.objDll.M_KeyInputStringGBK(self.hdl, p_str, len_)

    def keyPressChar(self, str):
        self.objDll.M_KeyPress(self.hdl, YjsInputHidKeyCode.yjsInputHidKeyCode[str], 1)

    def moveTo(self, x, y):
        self.objDll.M_MoveTo3(self.hdl, x, y)

    def leftClick(self):
        self.objDll.M_LeftClick(self.hdl, 1)

    def leftDoubleClick(self):
        self.objDll.M_LeftDoubleClick(self.hdl, 1)

    def rightClick(self):
        self.objDll.M_RightClick(self.hdl, 1)




if __name__ == '__main__':
    time.sleep(1)
    yjsInputTool = YjsInputTool(int('A001', 16), int('0001', 16))
    yjsInputTool.moveTo(114, 343)
    yjsInputTool.leftDoubleClick()
    yjsInputTool.KeyPressStr('so nvidia fuck you')
    yjsInputTool.keyPressChar('!')




