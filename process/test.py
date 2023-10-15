from ctypes import windll

import numpy
import numpy as np
import pyautogui
import win32api
import win32con
import win32gui
import win32ui
import cv2
from PIL import ImageGrab
import pygetwindow as gw


def captureWindow(hwnd, filename, x1, y1, x2, y2):
    # 获取窗口的位置和大小
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    left += x1
    top += y1
    right = left + x2 - x1
    bottom = top + y2 - y1
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

    # 保存位图到文件
    save_bitmap.SaveBitmapFile(save_dc, filename)

    # 清理资源
    save_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

def capture(hwnd, xLeftTop, yLeftTop, xRightBottom, yRightBottom):
    x, y, x2, y2 = win32gui.GetWindowRect(hwnd)
    width = x2 - x
    height = y2 - y
    # 故图
    hWndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDc = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDc.SelectObject(saveBitMap)
    saveDc.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # 保存图片转cV图物
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)
    img = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
    cv2.imshow('orgin', img)
    cv2.waitKey(0)

    # 截取感兴趣区域
    roi = img[yLeftTop:yRightBottom, xLeftTop:xRightBottom]
    # 释放内存
    saveDc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)
    return roi

def capture_window(hwnd, x1, y1, x2, y2):
    # 获取窗口位置信息
    rect = win32gui.GetWindowRect(hwnd)
    window_rect = (rect[0], rect[1], rect[2], rect[3])

    # 捕获窗口图像
    image = ImageGrab.grab(window_rect)
    cv2.imshow('123', image)
    cv2.waitKey(0)

    # 裁剪图像
    cropped_image = image.crop((x1, y1, x2, y2))

    return cropped_image

def capture_vmware_window(hwnd):
    # 获取窗口位置和大小
    window = gw.win32wrapper.Win32Window(hwnd)
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    width = right - left
    height = bottom - top

    # 创建设备上下文
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # 使用 Virtual Screen 设备上下文截取窗口图像
    virtual_screen_size = (win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN),
                           win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN))
    virtual_screen_dc = win32gui.CreateDC("MKSWindow#0", None, None, None)
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(virtual_screen_dc, width, height)
    save_dc.SelectObject(bitmap)

    # 使用 BitBlt 函数截图
    save_dc.BitBlt((0, 0), (width, height), virtual_screen_dc, (left, top), win32con.SRCCOPY)

    # 将位图数据转换为 PIL 图像对象
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    image = np.frombuffer(bmpstr, dtype='uint8')
    image = image.reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))
    image = image[..., :3]  # 去除 Alpha 通道
    image = np.flipud(image)  # 翻转图像

    # 释放资源
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    virtual_screen_dc.DeleteDC()

    return image

if __name__ == '__main__':
    image = capture_vmware_window(135316)
    pyautogui.imshow(image)  # 显示截图结果