# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 14:04
# @Author  : xinyuan tu
# @File    : Render.py
# @Software: PyCharm
import numpy as np
from .cython import render_core
class Render_color():
    def __init__(self,barycentric_coordinates,triangle_ids,texture,triangles,imagesize):
        self.barycentric_coordinates = barycentric_coordinates
        self.barycentric_coordinates = self.barycentric_coordinates.reshape((imagesize*imagesize,3)).astype(np.float32)
        self.barycentric_coordinates = np.ascontiguousarray(self.barycentric_coordinates)

        self.triangle_ids = np.array(triangle_ids,dtype=np.int32)
        self.triangle_ids = self.triangle_ids.reshape((imagesize*imagesize))
        self.triangle_ids = np.ascontiguousarray(self.triangle_ids)

        self.texture = texture.astype(np.float32)
        if self.texture.shape[0]==3:
            self.texture = np.transpose(self.texture)
        self.texture = np.ascontiguousarray(self.texture)

        self.imagesize = imagesize

        self.triangles = np.array(triangles,dtype=np.int32)
        if self.triangles.shape[0]==3:
            self.triangles = np.transpose(self.triangles)
        self.triangles = np.ascontiguousarray(self.triangles)
            
        self.colorimage = np.zeros((self.imagesize,self.imagesize,3)).reshape((self.imagesize*self.imagesize,3))
        self.colorimage = np.ascontiguousarray(self.colorimage).astype(np.int32)

    def forward(self):
        '''
        void
        render_colour_core_cpp(int * triangle_ids, int * triangles,
        float * texture, float * barycentric_coordinates,
                               int * colorimage, int
        imagesize);
        '''
        render_core.render_colour_core(self.triangle_ids,self.triangles,self.texture,self.barycentric_coordinates,
                                       self.colorimage,self.imagesize)

        return self.colorimage.reshape((self.imagesize,self.imagesize,3))
