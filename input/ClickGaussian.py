#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author：吉姆哥儿
    @file： ClickPoisson.py
    @date：2023/11/20 14:16
    @desc: 
"""

import cv2
import numpy as np


class ClickGaussian:

    @staticmethod
    def generatePointInCircle(centerX, centerY, radius):
        while True:
            x = np.random.normal(centerX, radius / 3)
            y = np.random.normal(centerY, radius / 3)
            if (x - centerX) ** 2 + (y - centerY) ** 2 <= radius ** 2:
                return int(x), int(y)


if __name__ == '__main__':
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    for i in range(1000):
        centerX, centerY = 200, 200  # 圆心坐标
        radius = 150  # 圆半径
        x, y = ClickGaussian.generatePointInCircle(centerX, centerY, radius)
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
        cv2.imshow('Gaussian Distribution', img)
        cv2.waitKey(1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
