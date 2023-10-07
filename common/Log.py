#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from common.Container import *


class Log:

    def __init__(self):
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))
        # 获取日志文件的目录路径
        parentPath = baseDir
        logDir = os.path.join(parentPath, 'logs')

        os.makedirs(logDir, exist_ok=True)  # 创建日志目录，如果目录已经存在则不会报错

        # 创建日志记录器
        logger = logging.getLogger('fishJumpLogger')
        # 设置所有日志控制器的下限
        logger.setLevel(logging.DEBUG)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 创建按天滚动的文件处理器
        # TimedRotatingFileHandler的参数when用于设置日志滚动的时间间隔。你可以通过以下值来指定滚动的间隔：
        #
        # 'S'：秒级滚动
        # 'M'：分钟级滚动
        # 'H'：小时级滚动
        # 'D'：天级滚动
        # 'W0' - 'W6'：每周滚动，其中'W0'代表星期一，'W1'代表星期二，以此类推
        # 'midnight'：每天午夜滚动

        # 按天滚动的日志文件名通常包含日期信息，格式为<base_filename>-YYYY-MM-DD.log。其中，<base_filename>是日志文件的基础名称，可以自定义。
        #
        # 例如，如果你指定的日志文件基础名称为my_log.log，那么生成的按天滚动的日志文件名格式将是my_log-YYYY-MM-DD.log，其中YYYY代表四位数的年份，MM代表两位数的月份，DD代表两位数的日期。
        #
        # 每天的日志消息将被追加到对应日期的日志文件中，而不会覆盖之前的日志内容。
        file_handler = TimedRotatingFileHandler(logDir + '/moonlight.log', when='midnight', backupCount=7, encoding='utf-8')
        # 设置历史文件后缀
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setLevel(logging.INFO)

        # 定义日志格式
        formatter = logging.Formatter('%(asctime)s - %(filename)-16s - %(levelname)-5s - %(message)s')

        # 设置处理器的格式和添加到日志记录器
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.info('日志路径: ' + logDir)

        Container.set("Log", logger)

if __name__ == '__main__':

    log = Log()
