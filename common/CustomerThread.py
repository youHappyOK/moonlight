#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: CustomerThread.py
Author: 吉姆哥
Date: 2023/8/27
Description: 自定义线程，提供开启、暂停、恢复、结束功能
"""

import threading
import ctypes
import time

from common.Container import Container


class CustomThread(threading.Thread):

    def __init__(self, target=None, args=(), kwargs=None, name=''):
        threading.Thread.__init__(self, target=target, args=args, kwargs=kwargs, name=name)
        self.kernel32 = ctypes.windll.kernel32
        self.thread_flag = 0
        self.log = Container.get('Log')

    # ctypes.pythonapi.PyThreadstate_SetAsyncExc(self.ident, ctypes.py_object(SystemExit)): 这行代码使用 ctypes 库来调用 Python
    # 解释器的 C API 函数 PyThreadstate_SetAsyncExc()。 这个函数的作用是向指定标识符对应的线程发送一个异步异常，试图中断线程的执行。在这里，self.ident
    # 可能是线程的标识符，ctypes.py_object(SystemExit) 则是要发送的异常对象，这里是 SystemExit 异常，意味着试图优雅地中止线程。
    #
    # self.thread_flag = 0: 这行代码将类中的 thread_flag 属性设置为 0，这可能是一个标志，用于指示线程是否应该继续执行或停止。
    #
    # return self.thread_flag: 这行代码将更新后的 self.thread_flag 返回，作为方法的返回值。
    def stop(self):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, ctypes.py_object(SystemExit))
        # 标志位
        # 0：运行或结束，1 暂停
        self.thread_flag = 0
        return self.thread_flag

    def start(self):
        threading.Thread.start(self)
        return

    # 通过 self.kernel32.OpenThread(0x0002, False, self.ident) 打开一个线程句柄（self.ident 可能是线程的标识符），使用的标志是 0x0002，它代表
    # THREAD_SUSPEND_RESUME，即允许暂停和恢复线程。
    #
    # 使用 self.kernel32.SuspendThread(handle) 暂停线程，这会阻止线程继续执行。
    #
    # 使用 self.kernel32.CloseHandle(handle) 关闭线程句柄，这告诉操作系统不再需要该句柄。
    #
    # self.thread_flag 的值递增，表示线程已经被暂停并且标志已被更新。
    #
    # 最后，返回更新后的 self.thread_flag。
    def pause(self):
        handle = self.kernel32.OpenThread(0x0002, False, self.ident)
        self.kernel32.SuspendThread(handle)
        self.kernel32.CloseHandle(handle)
        self.thread_flag += 1
        return self.thread_flag

    def resume(self):
        handle = self.kernel32.OpenThread(0x0092, False, self.ident)
        self.kernel32.ResumeThread(handle)
        self.kernel32.CloseHandle(handle)
        self.thread_flag -= 1
        return self.thread_flag


if __name__ == '__main__':
    def thread_function(count: int):
        while True:
            print("Thread is running... count: %s" % str(count))
            time.sleep(1)
            count += 1


    myThread = CustomThread(target=thread_function, args=(2,), name='myThread')

    print('开启线程5s...')
    myThread.start()
    time.sleep(5)

    print('暂停线程5s')
    myThread.pause()
    time.sleep(5)

    print('恢复线程5s')
    myThread.resume()
    time.sleep(5)

    print('结束线程')
    myThread.stop()

    time.sleep(1)

    # 注意，stop后不是马上结束的，可能有一点延迟，所以上面sleep了1秒
    if not myThread.is_alive():
        print('线程结束了')

