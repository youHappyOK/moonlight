#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.Container import Container
from common.Log import Log
from common.ThreadGroup import ThreadGroup
from process.GameOperation import GameOperation
from process.MainProcess import MainProcess
from process.SubProcess import SubProcess
from repository.ConfigLoader import ConfigLoader


class App:

    def __init__(self):
        # 放到 ioc 容器中
        Log()
        ThreadGroup()
        GameOperation()
        SubProcess()
        MainProcess()
        ConfigLoader()


if __name__ == '__main__':
    app = App()
    configLoader = Container.get('ConfigLoader')
    configLoader.loadAllConfig()
    mainProcess = Container.get('MainProcess')
    mainProcess.runMainProcess()