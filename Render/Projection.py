# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 14:11
# @Author  : xinyuan tu
# @File    : Projection.py
# @Software: PyCharm
import numpy as np
import math

def projection(Shape,imagesize,angle,TT):
    '''旋转'''

    angle[0, 0] = 2.0 / 360.0 * math.pi * angle[0, 0] - 1.0 / 360.0 * math.pi
    angle[0, 1] = 2.0 / 4.0 * math.pi * angle[0, 1]# + 1.0 / 6.0 * math.pi
    angle[0, 2] = 2.0 / 360.0 * math.pi * angle[0, 2] - 1.0 / 360.0 * math.pi
    R_x = np.array([[1, 0, 0], [0, math.cos(angle[0, 0]), math.sin(angle[0, 0])],
           [0, -math.sin(angle[0, 0]), math.cos(angle[0, 0])]])
    R_y = np.array([[math.cos(angle[0, 1]), 0, -math.sin(angle[0, 1])], [0, 1, 0],
           [math.sin(angle[0, 1]), 0, math.cos(angle[0, 1])]])
    R_z = np.array([[math.cos(angle[0, 2]), math.sin(angle[0, 2]), 0], [-math.sin(angle[0, 2]), math.cos(angle[0, 2]), 0],
           [0, 0, 1]])
    R = np.dot(np.dot(R_x, R_y), R_z)

    '''平移'''
    Shape = np.dot(R,Shape)+TT
    scale = 180/(np.max(Shape[1,:]/Shape[2,:])-np.min(Shape[1,:]/Shape[2,:]))
    Shape[0,:] = scale*Shape[0,:]/(Shape[2,:])+imagesize/2
    Shape[1,:] = scale*Shape[1,:]/(Shape[2,:])+imagesize/2
    Shape[2,:] = Shape[2,:]
    Shape[1,:] = imagesize*1.0-Shape[1,:]

    return Shape