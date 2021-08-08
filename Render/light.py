# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 14:13
# @Author  : xinyuan tu
# @File    : light.py
# @Software: PyCharm
import numpy as np

def compute_normal(vertex,tri,Vertex_tri):
    tri = np.array(tri, dtype=np.int32)
    Vertex_tri = np.array(Vertex_tri,dtype = np.int32)
    vertex = vertex.T #n*3
    vertex_normal = np.zeros((Vertex_tri.shape[0],3))
    vt1_indices = tri[:, 0]
    vt2_indices = tri[:, 1]
    vt3_indices = tri[:, 2]
    vt1 = vertex[vt1_indices,:]
    vt2 = vertex[vt2_indices,:]
    vt3 = vertex[vt3_indices,:]
    #print(vt1.shape)

    normalf = np.cross(vt2-vt1,vt3-vt1)
    Nmax = np.expand_dims(normalf.max(axis=1),1).repeat(3,axis=1)
    Nmin = np.expand_dims(normalf.min(axis=1),1).repeat(3,axis = 1)
    normalf = (normalf-Nmin)/(Nmax-Nmin)#所有面片的法向量，而点的法向量是8个相关面片法向量加和

    for i in range(8):
        vertex_normal =normalf[Vertex_tri[:,i]-1,:]+vertex_normal
    VNmax = np.expand_dims(vertex_normal.max(axis=1),1).repeat(3,axis=1)
    VNmin = np.expand_dims(vertex_normal.min(axis=1),1).repeat(3,axis=1)
    vertex_normal = (vertex_normal-VNmin)/(VNmax-VNmin)

    v = vertex-vertex.mean(axis= 0)
    s = (v*vertex_normal).sum(axis = 0)
    count_s_greater_0 = (s>0).sum()
    count_s_less_0 = (s<0).sum()
    sign = 2*(count_s_greater_0>count_s_less_0) - 1
    vertex_normal = vertex_normal*sign
    return vertex_normal


def SphericalHarmonize(normal):
    '''
    :param normal:
    :return:
    In 3d face, usually assume:
    1. The surface of face is Lambertian(reflect only the low frequencies of lighting)
    2. Lighting can be an arbitrary combination of point sources
    --> can be expressed in terms of spherical harmonics(omit the lighting coefficients)
    I = albedo * (sh(n) x sh_coeff)
    sh_coeff: 9 x 1
    Y(n) = (1, n_x, n_y, n_z, n_xn_y, n_xn_z, n_yn_z, n_x^2 - n_y^2, 3n_z^2 - 1)': n x 9
    '''
    #normal N*3
    Nx=normal[:,0]
    Ny=normal[:,1]
    Nz=normal[:,2]
    #[Nx,Ny,Nz]= tf.split(axis=-1, num_or_size_splits=3, value=normal)
    c1 = 0.429043
    c2 = 0.511664
    c3 = 0.743125
    c4 = 0.886227
    c5 = 0.247708
    Hn0=np.ones_like(Nx)*c4
    Hn1=2*c2*Ny
    Hn2=2*c2*Nz
    Hn3=2*c2*Nx
    Hn4=2*c1*Nx*Ny
    Hn5=2*c1*Ny*Nz
    Hn6=c3*Nz*Nz-c5
    Hn7=2*c1*Nz*Nx
    Hn8=c1*(Nx*Nx-Ny*Ny)
    Hn = np.stack( [Hn0,Hn1,Hn2,Hn3,Hn4,Hn5,Hn6,Hn7,Hn8], axis=-1)#VerticNum*9
    return Hn


def Basic_light(colors,normals,vertices,light_positions,light_intensities):
    '''
    :param normal:
    :return:
    https://learnopengl-cn.readthedocs.io/zh/latest/02%20Lighting/02%20Basic%20Lighting/
    I =  (ambient+diffuse+specular)*texture
    we don’t consider specular here
    '''
    '''diffuse'''
    direction_to_lights = vertices[np.newaxis, :, :] - light_positions[:, np.newaxis, :]  # [nlight, nver, 3]
    direction_to_lights_n = np.sqrt(np.sum(direction_to_lights ** 2, axis=2))  # [nlight, nver]
    direction_to_lights = direction_to_lights / direction_to_lights_n[:, :, np.newaxis]
    normals_dot_lights = normals[np.newaxis, :, :] * direction_to_lights  # [nlight, nver, 3]
    normals_dot_lights = np.sum(normals_dot_lights, axis=2)  # [nlight, nver]
    diffuse_output = colors[np.newaxis, :, :] * (normals_dot_lights[:, :, np.newaxis] * light_intensities[:, np.newaxis,:]+1e-4)
    diffuse_output = np.sum(diffuse_output, axis=0)  # [nver, 3]

    return diffuse_output