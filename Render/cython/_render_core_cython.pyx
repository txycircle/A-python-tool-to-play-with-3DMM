import numpy as np
cimport numpy as np


# use the Numpy-C-API from Cython
np.import_array()

cdef extern from "render_core.h":
    void zbuffer_core_cpp(float * verts, int * triangles, float * barycentric, float * zbuffer, int * triangle_ids, int triangle_num, int verts_num, int imagesize)
    void render_colour_core_cpp(int* triangle_ids,int* triangles, float* texture, float* barycentric_coordinates, int* colorimage, int imagesize)
    void zbuffer_uv_core_cpp(float* uv_coord, int* triangles,float* barycentric,int* triangle_ids , int triangle_num, int verts_num, int imagesize)

def zbuffer_core(np.ndarray[float,ndim = 2,mode = "c"] verts not None,
                 np.ndarray[int,ndim = 2,mode  = "c"] triangles not None,
                 np.ndarray[float,ndim = 2,mode  = "c"] barycentric not None,
                 np.ndarray[float,ndim = 1,mode  = "c"] zbuffer not None,
                 np.ndarray[int, ndim = 1,mode  = "c"] triangle_ids not None,
                 int triangle_num,
                 int verts_num, int imagesize
                 ):
    zbuffer_core_cpp(
        <float *> np.PyArray_DATA(verts),
        <int *> np.PyArray_DATA(triangles),
        <float *> np.PyArray_DATA(barycentric),
        <float *> np.PyArray_DATA(zbuffer),
        <int *> np.PyArray_DATA(triangle_ids),
        triangle_num,verts_num,imagesize
    )


def zbuffer_uv_core(np.ndarray[float,ndim = 2,mode = "c"] verts not None,
                 np.ndarray[int,ndim = 2,mode  = "c"] triangles not None,
                 np.ndarray[float,ndim = 2,mode  = "c"] barycentric not None,
                 np.ndarray[int, ndim = 1,mode  = "c"] triangle_ids not None,
                 int triangle_num,
                 int verts_num, int imagesize
                 ):
    zbuffer_uv_core_cpp(
        <float *> np.PyArray_DATA(verts),
        <int *> np.PyArray_DATA(triangles),
        <float *> np.PyArray_DATA(barycentric),
        <int *> np.PyArray_DATA(triangle_ids),
        triangle_num,verts_num,imagesize
    )

def render_colour_core(np.ndarray[int,ndim = 1,mode = "c"] triangle_ids not None,
                       np.ndarray[int,ndim = 2,mode = "c"] triangles not None,
                       np.ndarray[float,ndim = 2,mode = "c"] texture not None,
                       np.ndarray[float,ndim = 2,mode = "c"] barycentric_coordinates not None,
                       np.ndarray[int,ndim = 2,mode = "c"] colorimage not None,
                       int imagesize
                       ):
    render_colour_core_cpp(
        <int*> np.PyArray_DATA(triangle_ids),
        <int*> np.PyArray_DATA(triangles),
        <float*> np.PyArray_DATA(texture),
        <float*> np.PyArray_DATA(barycentric_coordinates),
        <int*> np.PyArray_DATA(colorimage),
        imagesize
    )