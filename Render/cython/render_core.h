#pragma once
#ifndef RENDER_CORE_HPP_
#define RENDER_CORE_HPP_

#include <stdio.h>
#include <cmath>
#include <algorithm>
#include <string>
#include <iostream>
#include <fstream>

using namespace std;
float get_max(float x1, float x2, float x3);
float get_min(float x1, float x2, float x3);
bool PixelIsInsideTriangle(float p0_x, float p0_y, float p1_x, float p1_y, float p2_x, float p2_y, float x, float y);
bool IsCCW(float x1,float y1,float x2,float y2,float x,float y);
bool PixelIsInsideTriangle_uv(float p0_x, float p0_y, float p1_x, float p1_y, float p2_x, float p2_y, float x, float y);
void zbuffer_core_cpp(float* verts, int* triangles, float* barycentric, float* zbuffer, int* triangle_ids, int triangle_num, int verts_num, int imagesize);
void render_colour_core_cpp(int* triangle_ids, int* triangles, float* texture, float* barycentric_coordinates, int* colorimage, int imagesize);
void zbuffer_uv_core_cpp(float* uv_coord, int* triangles,float* barycentric,int* triangle_ids , int triangle_num, int verts_num, int imagesize);
#endif // RENDER_CORE_HPP_

