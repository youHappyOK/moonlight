import numpy as np
import random

# 根据起点和终点坐标生成贝塞尔曲线
class BezireMouse:

    @staticmethod
    def generateBezierCurve(start_point, end_point):
        # Generate a random control point within certain constraints
        control_point_x = (start_point[0] + end_point[0]) / 2
        control_point_y = random.uniform(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]))
        control_point = (control_point_x, control_point_y)

        t = np.linspace(0, 1, 100)
        bezier_curve = []
        for i in t:
            x = (1-i)**2 * start_point[0] + 2*i*(1-i) * control_point[0] + i**2 * end_point[0]
            y = (1-i)**2 * start_point[1] + 2*i*(1-i) * control_point[1] + i**2 * end_point[1]
            bezier_curve.append((x, y))
        return bezier_curve

    @staticmethod
    def calculateSpeedFactor(startPoint, endPoint):
        distance = ((endPoint[0] - startPoint[0]) ** 2 + (endPoint[1] - startPoint[1]) ** 2) ** 0.5
        if distance < 100:
            return 4
        elif distance >= 100 and distance < 500:
            return 5
        elif distance >= 500 and distance < 1000:
            return 6
        elif distance >= 1000 and distance < 2000:
            return 8
        elif distance >= 2000:
            return 10

    @staticmethod
    def customEase(p):
        a = 0
        if p < 3 / 4:
            p = (p * 1.5)  # Scale to [0, 1]
            a = 0.01 * (100 - 90 * p)  # Decrease sleep time for acceleration
        else:
            p = ((p - 2 / 3) * 3)  # Scale to [0, 1]
            a = 0.01 * (1 + 90 * p)  # Increase sleep time for deceleration
        # print(a)
        return a

