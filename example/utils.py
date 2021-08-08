# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 14:15
# @Author  : xinyuan tu
# @File    : utils.py
# @Software: PyCharm

import scipy.io as sio
import numpy as np
import os
import imageio
import glob
from PIL import Image


class ModelConfig():
    def __init__(self):
        self.imagesize = 256
        self.BATCH_SIZE = 1

        self.base_bfm = './data/BFM_model_front'
        self.LightMU = './data/LshMu.npy'
        self.Lightcov = './data/LshCov.npy'
        self.uvmap_path ='./data/UVmap.mat'
        self.image_path ='./data/image/'
        self.pcl_path = './pcl.txt'
        self.flow_gt_path = './flow_gt/train_small'
        self.RT_path = './RT/train_small'
        self.visi_map = './visi_map/train_small'
        self.visi_map_colo = './visi_map_colo/train_small'
        self.landmark = 1
        self.landmark_path = './landmark/train_small'

def Load3dmmPara(para_path):
    data=sio.loadmat(para_path)
    print('load 3dmm paramaters')
    shapePC=data['idBase']#n*80
    expPC=data['exBase']#n*64
    texPC=data['texBase']#n*80
    ###n=3*vertexNUM###
    shapeMU=data['meanshape']#1*n
    texMU=data['meantex']#1*n

    LandmarksCorrespondence=data['keypoints']#1*68
    LandmarksCorrespondence=LandmarksCorrespondence.T#convert matlab to python need -1s,already start from 0

    skinmask_idx=data['frontmask2_idx']#皮肤上点的序号
    skinmask_idx=skinmask_idx-1
    Tri=data['tri']#三角面片包含点的序号
    Tri=Tri-1#convert matlab to python need -1
    VertexTri=data['point_buf']  #每一个点属于的面片序号
    VertexTri=VertexTri-1#convert matlab to python need -1
    point_one_ring=data['point_one_ring']
    point_one_ring=point_one_ring-1#convert matlab to python need -1
    return shapePC,expPC,texPC,shapeMU,texMU,\
    LandmarksCorrespondence,Tri,VertexTri,skinmask_idx,point_one_ring



def write_gif(data_path):
    outfilename = os.path.join(data_path,'result.gif')  # 转化的GIF图片名称
    filenames = sorted(glob.glob(os.path.join(data_path,'*.jpg')) )# 存储所需要读取的图片名称
    frames = []
    for image_name in filenames:  # 索引各自目录
        frames.append(imageio.imread(image_name))  # 批量化
    imageio.mimsave(outfilename, frames,'GIF', duration=0.2)


