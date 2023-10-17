#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： ConfigLoader.py
    @date：2023/10/16 9:20
    @desc: 
"""
import os
import sys

from common.Container import Container
from repository.ApplicationProperties import ApplicationProperties


class ConfigLoader:

    def __init__(self):
        Container.set('ConfigLoader', self)

    def loadConfig(self, configFilePath: str, configObj: object):

        with open(configFilePath, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # 去掉注释和空行
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 分离出key和value
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if value == 'True':
                    value = True
                if value == 'False':
                    value = False

                # 如果key对应的属性存在于configObj中，则将value赋给这个属性
                if hasattr(configObj, self.snakeToCamel(key)):
                    setattr(configObj, self.snakeToCamel(key), value)

    def loadAllConfig(self):
        baseDir = ''
        if getattr(sys, 'frozen', None):
            baseDir = sys._MEIPASS
        else:
            baseDir = os.path.dirname(os.path.dirname(__file__))

        applicationProperties = ApplicationProperties()
        self.loadConfig(baseDir + '\\resources\\' + 'application.properties', applicationProperties)
        Container.set('ApplicationProperties', applicationProperties)

    def snakeToCamel(self, snakeCaseString):
        words = snakeCaseString.split('_')
        result = words[0].lower()
        for word in words[1:]:
            result += word.capitalize()
        return result


if __name__ == '__main__':
    configLoader = ConfigLoader()
    configLoader.loadAllConfig()