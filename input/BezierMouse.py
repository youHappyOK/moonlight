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

