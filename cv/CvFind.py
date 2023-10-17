#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： CvFind.py
    @date：2023/10/16 15:46
    @desc: 
"""
import os
import sys
from ctypes import windll

import cv2
import numpy as np
import win32gui
import win32ui
from PIL import ImageGrab

from common.Container import Container


class CvFind:

    def __init__(self):
        # 这里修改为资源文件的路径
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        self.path = baseDir + '\\resources'
        Container.set('CvFind', self)

    # 前端截图
    def capWinFront(self, hwnd):
        # 获取窗口位置信息
        rect = win32gui.GetWindowRect(hwnd)
        window_rect = (rect[0], rect[1], rect[2], rect[3])
        # 捕获窗口图像
        image = ImageGrab.grab(window_rect)

        npImg = np.array(image)

        # 因为pillow的图像是rgb的，所以要转成cv2需要的bgr
        bgrArray = cv2.cvtColor(npImg, cv2.COLOR_RGB2BGR)

        return bgrArray

    # 后台截图
    def capWinBackend(self, hwnd):
        # 获取窗口的位置和大小
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # 创建设备上下文对象
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # 创建位图对象并将其与设备上下文关联
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # 将窗口内容绘制到位图中
        windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)

        # 将位图转换为数组
        bitmap_bits = save_bitmap.GetBitmapBits(True)
        image_np = np.frombuffer(bitmap_bits, dtype=np.uint8)
        image_np = image_np.reshape((height, width, -1))

        # 清理资源
        save_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return image_np

    # x1: 区城的左上X坐标
    # y1: 区域的左上Y坐标
    # x2: 区城的右下X坐标
    # y2: 区城的右下Y坐标
    # pic_nane: 图片名，只能单个图片
    # sim: 相似度，和算法相关
    # method: 算法，总共有6总(默认是5，参考opencv的模版匹配算法)
    # draw: 是否在找到的位置画图并显录，默认不画
    def findPicByTemplate(self, hwnd, x1, y1, x2, y2, picName, sim, draw, isFront: bool):
        windowShotImage = None
        # 从截图读取要查找范围的图片
        if isFront:
            windowShotImage = self.capWinFront(hwnd)
        else:
            windowShotImage = self.capWinBackend(hwnd)
        imgSource = windowShotImage[y1:y2, x1:x2]
        # 读取要查找的图
        imgTarget = self.readImageWithChinesePath(self.path + os.path.sep + picName)

        # 将通道转成3通道，不然matchTemplate会报错
        sh, sw, sc = imgSource.shape
        if sc == 4:
            # 将 4 通道图像转换为 3 通道图像
            imgSource = cv2.cvtColor(imgSource, cv2.COLOR_RGBA2RGB)
        th, tw, tc = imgTarget.shape
        if tc == 4:
            # 将 4 通道图像转换为 3 通道图像
            imgTarget = cv2.cvtColor(imgTarget, cv2.COLOR_RGBA2RGB)


        # 计算匹配位置
        # result是一个二维的浮点型 Numpy 数组。该数组表示了在源图像中搜索到的所有可能匹配的位置。每个元素的值表示了模板与源图像的对应位置之间的匹配程度。
        result = cv2.matchTemplate(imgSource, imgTarget, 5)
        # 当调用 cv2.minMaxLoc(result) 时，它会返回矩阵中的最小值、最大值以及对应的位置信息。
        # 具体返回值：
        # minVal：矩阵中的最小值。
        # maxVal：矩阵中的最大值。
        # minLoc：最小值对应的位置（坐标）。
        # maxLoc：最大值对应的位置（坐标）。
        # TM_CCOEFF_NORMED即5最佳匹配位置在maxLoc计算得到的最小值位置处
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        # 过滤相似度
        if maxVal < sim:
            return False, -1, -1
        # loc 是一个包含两个数组的元组，其中第一个数组表示找到的匹配位置的行索引，第二个数组表示找到的匹配位置的列索引。
        # 在使用模板匹配时，loc 表示的是匹配位置矩形框的左上角坐标
        else:
            if draw:
                #  注意计算右下角坐标时x坐标要加模板图像shape[1]表示的宽度，y坐标加高度
                leftTop = (x1 + maxLoc[0], y1 + maxLoc[1])
                rightBottom = (leftTop[0] + imgTarget.shape[1], leftTop[1] + imgTarget.shape[0])
                cv2.rectangle(windowShotImage, leftTop, rightBottom, (0, 255, 0), 5, 8, 0)
                cv2.imshow('match', windowShotImage)
                cv2.waitKey(0)
            # 返回匹配中心位置
            return True, x1 + maxLoc[0] + imgTarget.shape[1]/2, y1 + maxLoc[1] + imgTarget.shape[0]/2

    def readImageWithChinesePath(self, path):
        return cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)

if __name__ == '__main__':
    cvFind = CvFind()
    cvFind2 = Container.get('CvFind')
    isMatch, x, y = cvFind2.findPicByTemplate(855716, 34, 163, 501, 487, '最近.bmp', 0.9, False, False)
    print(str(isMatch) + ' ' + str(x) + ' ' + str(y))

    # cvFind = CvFind()
    # img = cvFind.capWinBackend(855716)
    # cv2.imshow('123', img)
    # cv2.waitKey(0)