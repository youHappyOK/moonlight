#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Container:

    container = dict()

    def __init__(self, **kw):
        super().__init__(**kw)

    @staticmethod
    def get(key):
        try:
            return Container.container[key]
        except KeyError:
            raise AttributeError(r"'container' object has no attribute '%s'" % key)

    @staticmethod
    def set(key, value):
        Container.container[key] = value