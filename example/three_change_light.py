# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 20:17
# @Author  : xinyuan tu
# @File    : three_change_light.py
# @Software: PyCharm


import numpy as np
import os
import tqdm
from PIL import Image
from example.utils import *
from Render.Render import *
from Render.Zbuffer import *
from Render.Projection import *
from Render.light import *


def main(state = "diffuse"):
    modelconfig = ModelConfig()
    shapePC, expPC, texPC, shapeMU, texMU, \
    LandmarksCorrespondence, Tri, VertexTri, skinmask_idx, point_one_ring = Load3dmmPara(modelconfig.base_bfm)
    lightMU = np.load(modelconfig.LightMU)
    lightconv = np.load(modelconfig.Lightcov)
    modelconfig.image_path = os.path.join(modelconfig.image_path,'light')

    if not os.path.isdir(modelconfig.image_path):
        os.makedirs(modelconfig.image_path)


    ########生成3DMM SHAPE########
    shape_para = np.random.rand(1, shapePC.shape[1])
    Shape = shapeMU + np.dot(shape_para, shapePC.T)
    exp_para = 2 * np.random.rand(1, expPC.shape[1]) - 1
    Shape = Shape + np.dot(exp_para, expPC.T)
    Shape = Shape.reshape(int(Shape.shape[1] / 3), 3)
    Shape = Shape-np.mean(Shape,axis=0,keepdims=True)
    Shape = Shape.T

    ########生成3DMM TEXTURE########
    texture_para = 4 * np.random.rand(1, texPC.shape[1]) - 2
    texture = texMU + np.dot(texture_para, texPC.T)
    texture = texture.reshape(int(texture.shape[1] / 3), 3)


    ########生成3DMM LIGHT########
    normal = compute_normal(Shape, Tri, VertexTri)
    '''I = albedo * (sh(n) x sh_coeff)'''
    if state =="SphericalHarmonize":
        light_para = 5 * np.random.rand(9, 1) - 2
        light = (np.expand_dims(lightMU, -1) + np.dot(lightconv, light_para)) / 5
        texture = texture * np.dot(SphericalHarmonize(normal), light).repeat(3, axis=1)
        image_path = os.path.join(modelconfig.image_path,  'SphericalHarmonize.png')

        ########PROJECTION########
        angle = np.zeros((1, 3))
        T = np.expand_dims([0, 0, 10], 1)
        Shape_2d = projection(Shape, modelconfig.imagesize, angle, T)

        ######Zbuffer#######
        tranfer = Zbuffer(np.transpose(Shape_2d), Tri, modelconfig.imagesize)
        barycentric_coordinates, triangle_ids, zbuffer = tranfer.forward()

        ######render color#######
        rander = Render_color(barycentric_coordinates, triangle_ids, texture, Tri, modelconfig.imagesize)
        image = rander.forward()

        img = Image.fromarray(np.uint8(image))
        img.show()

        img.save(image_path)

    '''I = (ambient+diffuse+specular)*texture'''
    if state == "diffuse":
        for i in range(10):
            p_x = -10+20/10*i
            light_positions = np.array([[p_x, 0, -30]])
            light_intensities = np.array([[1,1,1]])
            texture_temp = Basic_light(texture, normal, np.transpose(Shape), light_positions, light_intensities)
            image_path = os.path.join(modelconfig.image_path, 'diffuse_'+str(i)+'.jpg')

            ########PROJECTION########
            angle = np.zeros((1, 3))
            T = np.expand_dims([0, 0, 10], 1)
            Shape_2d = projection(Shape, modelconfig.imagesize, angle, T)

            ######Zbuffer#######
            tranfer = Zbuffer(np.transpose(Shape_2d), Tri, modelconfig.imagesize)
            barycentric_coordinates, triangle_ids, zbuffer = tranfer.forward()

            ######render color#######
            rander = Render_color(barycentric_coordinates, triangle_ids, texture_temp, Tri, modelconfig.imagesize)
            image = rander.forward()

            img = Image.fromarray(np.uint8(image))
            #img.show()

            img.save(image_path)




if __name__=="__main__":
    main(state = "SphericalHarmonize")
    main(state = "diffuse")
    modelconfig = ModelConfig()
    write_gif(os.path.join(modelconfig.image_path, 'light'))