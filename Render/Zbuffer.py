# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 10:45
# @Author  : xinyuan tu
# @File    : render.py
# @Software: PyCharm

import numpy as np
from .cython import render_core

class Zbuffer():
    def __init__(self,verts,triangles,imagesize):
        self.verts = verts
        if self.verts.shape[0]==3:
            self.verts = np.transpose(verts)
        self.verts = np.ascontiguousarray(self.verts).astype(np.float32)

        self.verts_num = self.verts.shape[0]

        self.triangles = np.array(triangles,dtype=np.int32)
        if self.triangles.shape[0]==3:
            self.triangles = np.transpose(triangles)
        self.triangles = np.ascontiguousarray(self.triangles)

        self.triangle_count = self.triangles.shape[0]

        self.imagesize = imagesize

        self.barycentric_coordinates = np.zeros((self.imagesize,self.imagesize,3)).reshape((self.imagesize*self.imagesize,3))
        self.barycentric_coordinates = np.ascontiguousarray(self.barycentric_coordinates).astype(np.float32)

        self.triangle_ids = np.zeros((imagesize,imagesize))-1
        self.triangle_ids = self.triangle_ids.reshape((self.imagesize*self.imagesize))
        self.triangle_ids = np.ascontiguousarray(self.triangle_ids).astype(np.int32)

        self.zbuffer = -np.ones((self.imagesize,self.imagesize,1))*10000000
        self.zbuffer = self.zbuffer.reshape(self.imagesize*self.imagesize)
        self.zbuffer = np.ascontiguousarray(self.zbuffer).astype(np.float32)


    def forward(self):
        '''
        def zbuffer_core(np.ndarray[float,ndim = 3,mode = "c"] verts not None,
                 np.ndarray[int,ndim = 3,mode  = "c"] triangles not None,
                 np.ndarray[float,ndim = 3,mode  = "c"] barycentric not None,
                 np.ndarray[float,ndim = 1,mode  = "c"] zbuffer not None,
                 np.ndarray[int, ndim = 1,mode  = "c"] triangle_ids not None,
                 int triangle_num,
                 int verts_num, int imagesize
                 )
        '''

        render_core.zbuffer_core(self.verts,self.triangles,self.barycentric_coordinates,
                                 self.zbuffer,self.triangle_ids,self.triangle_count,
                                 self.verts_num,self.imagesize
                                 )

        self.barycentric_coordinates = self.barycentric_coordinates.reshape([self.imagesize,self.imagesize,3])
        self.zbuffer = self.zbuffer.reshape([self.imagesize,self.imagesize])
        self.triangle_ids = self.triangle_ids.reshape([self.imagesize,self.imagesize])

        return self.barycentric_coordinates,self.triangle_ids,self.zbuffer


class Zbuffer_uv():
    def __init__(self,verts,triangles,imagesize):
        self.verts = verts
        if self.verts.shape[0]==2:
            self.verts = np.transpose(verts)
        self.verts = np.ascontiguousarray(self.verts).astype(np.float32)

        self.verts_num = self.verts.shape[0]

        self.triangles = np.array(triangles,dtype=np.int32)
        if self.triangles.shape[0]==3:
            self.triangles = np.transpose(triangles)
        self.triangles = np.ascontiguousarray(self.triangles)

        self.triangle_count = self.triangles.shape[0]

        self.imagesize = imagesize

        self.barycentric_coordinates = np.zeros((self.imagesize,self.imagesize,3)).reshape((self.imagesize*self.imagesize,3))
        self.barycentric_coordinates = np.ascontiguousarray(self.barycentric_coordinates).astype(np.float32)

        self.triangle_ids = np.zeros((imagesize,imagesize))-1
        self.triangle_ids = self.triangle_ids.reshape((self.imagesize*self.imagesize))
        self.triangle_ids = np.ascontiguousarray(self.triangle_ids).astype(np.int32)




    def forward(self):
        '''
        def zbuffer_core(np.ndarray[float,ndim = 3,mode = "c"] verts not None,
                 np.ndarray[int,ndim = 3,mode  = "c"] triangles not None,
                 np.ndarray[float,ndim = 3,mode  = "c"] barycentric not None,
                 np.ndarray[int, ndim = 1,mode  = "c"] triangle_ids not None,
                 int triangle_num,
                 int verts_num, int imagesize
                 )
        '''

        render_core.zbuffer_uv_core(self.verts,self.triangles,self.barycentric_coordinates,
                                    self.triangle_ids,self.triangle_count,
                                 self.verts_num,self.imagesize
                                 )

        self.barycentric_coordinates = self.barycentric_coordinates.reshape([self.imagesize,self.imagesize,3])

        self.triangle_ids = self.triangle_ids.reshape([self.imagesize,self.imagesize])

        return self.barycentric_coordinates,self.triangle_ids


