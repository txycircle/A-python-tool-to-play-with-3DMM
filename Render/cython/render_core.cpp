#include "render_core.h"
#include <algorithm>
#include <cmath>

float get_max(float x1, float x2, float x3)
{
	float max = x1 > x2 ? x1 : x2;
	return max > x3 ? max : x3;
}

float get_min(float x1, float x2, float x3)
{
	float min = x1 < x2 ? x1 : x2;
	return min < x3 ? min : x3;
}


bool IsCCW(float x1,float y1,float x2,float y2,float x,float y)
{
    float a1 = x2-x1;
    float a2 = y2-y1;
    float a3 = x-x1;
    float a4 = y-y1;
    return a1*a4>=a2*a3?1:0;
}
bool PixelIsInsideTriangle_uv(float p0_x, float p0_y, float p1_x, float p1_y, float p2_x, float p2_y, float x, float y)
{
    return (IsCCW(p0_x,p0_y,p1_x,p1_y,x,y) && IsCCW(p1_x,p1_y,p2_x,p2_y,x,y) &&IsCCW(p2_x,p2_y,p0_x,p0_y,x,y) )||
    (IsCCW(p1_x,p1_y,p0_x,p0_y,x,y) && IsCCW(p2_x,p2_y,p1_x,p1_y,x,y) && IsCCW(p0_x,p0_y,p2_x,p2_y,x,y));
}



bool PixelIsInsideTriangle(float p0_x, float p0_y, float p1_x, float p1_y, float p2_x, float p2_y, float x, float y)
{

	/* Judge whether the point is in the triangle
	Method:
		http://blackpawn.com/texts/pointinpoly/
	*/
	float v0_x = p1_x - p0_x;
	float v0_y = p1_y - p0_y;
	float v1_x = p2_x - p0_x;
	float v1_y = p2_y - p0_y;
	float v2_x = x - p0_x;
	float v2_y = y - p0_y;

	float dot00 = v0_x * v0_x + v0_y * v0_y;
	float dot01 = v0_x * v1_x + v0_y * v1_y;
	float dot02 = v0_x * v2_x + v0_y * v2_y;
	float dot11 = v1_x * v1_x + v1_y * v1_y;
	float dot12 = v1_x * v2_x + v1_y * v2_y;

	float invDenom = 1 / (dot00 * dot11 - dot01 * dot01);
	float u = (dot11 * dot02 - dot01 * dot12) * invDenom;
	float v = (dot00 * dot12 - dot01 * dot02) * invDenom;

	return (u >= 0) && (v >= 0) && (u + v <= 1);
}



void zbuffer_core_cpp(float* verts, int* triangles,float* barycentric,float* zbuffer,int* triangle_ids , int triangle_num, int verts_num, int imagesize)
{

	for (int i = 0; i < triangle_num; ++i)
	{

		int v0_t_id = triangles[3 * i + 0];
		int v1_t_id = triangles[3 * i + 1];
		int v2_t_id = triangles[3 * i + 2];


		float v0_x = verts[3 * v0_t_id];
		float v0_y = verts[3 * v0_t_id + 1];
		float v1_x = verts[3 * v1_t_id ];
		float v1_y = verts[3 * v1_t_id + 1];
		float v2_x = verts[3 * v2_t_id];
		float v2_y = verts[3 * v2_t_id + 1];



		int left = std::max((int)floor(get_min(v0_x, v1_x, v2_x)), 0);
		int bottom = std::max((int)floor(get_min(v0_y, v1_y, v2_y)), 0);
		int right = std::min((int)ceil(get_max(v0_x, v1_x, v2_x)), imagesize-1);
		int top = std::min((int)ceil(get_max(v0_y, v1_y, v2_y)), imagesize-1);


		
		for (int x = left; x <= right; ++x)
		{
			for (int y = bottom; y <= top; ++y)
			{
				if (PixelIsInsideTriangle(v0_x, v0_y, v1_x, v1_y, v2_x, v2_y, x, y))
				{

					float v0_z = verts[3 * v0_t_id+2];
					float v1_z = verts[3 * v1_t_id+2];
					float v2_z = verts[3 * v2_t_id+2];

					float twice_triangle_area = abs((v2_x - v0_x) * (v1_y - v0_y) - (v2_y - v0_y) * (v1_x - v0_x));
					float b0 = abs((x - v1_x) * (y - v2_y) - (y - v1_y) * (x - v2_x))/ twice_triangle_area;
					float b1 = abs((x - v0_x) * (y - v2_y) - (y - v0_y) * (x - v2_x))/ twice_triangle_area;


					float b2 = 1.0 - b0 - b1;

					float z = b0 * v0_z + b1 * v1_z + b2 * v2_z;

					if (z >= zbuffer[y * imagesize + x])
					{
						triangle_ids[y * imagesize + x] = i;
						zbuffer[y * imagesize + x] = z;
						barycentric[3*(y * imagesize + x) + 0] = b0;
						barycentric[3*(y * imagesize + x) + 1] = b1;
						barycentric[3*(y * imagesize + x) + 2] = b2;
					}
				}
			}
		}
	}

}

void zbuffer_uv_core_cpp(float* uv_coord, int* triangles,float* barycentric,int* triangle_ids , int triangle_num, int verts_num, int imagesize)
{

	for (int i = 0; i < triangle_num; ++i)
	{

		int v0_t_id = triangles[3 * i + 0];
		int v1_t_id = triangles[3 * i + 1];
		int v2_t_id = triangles[3 * i + 2];


		float v0_x = uv_coord[2 * v0_t_id];
		float v0_y = uv_coord[2 * v0_t_id + 1];
		float v1_x = uv_coord[2 * v1_t_id ];
		float v1_y = uv_coord[2 * v1_t_id + 1];
		float v2_x = uv_coord[2 * v2_t_id];
		float v2_y = uv_coord[2 * v2_t_id + 1];



		int left = std::max((int)floor(get_min(v0_x, v1_x, v2_x)), 0);
		int bottom = std::max((int)floor(get_min(v0_y, v1_y, v2_y)), 0);
		int right = std::min((int)ceil(get_max(v0_x, v1_x, v2_x)), imagesize-1);
		int top = std::min((int)ceil(get_max(v0_y, v1_y, v2_y)), imagesize-1);



		for (int x = left; x <= right; ++x)
		{
			for (int y = bottom; y <= top; ++y)
			{

				if (PixelIsInsideTriangle_uv(v0_x, v0_y, v1_x, v1_y, v2_x, v2_y, x, y))
				{
					float twice_triangle_area = abs((v2_x - v0_x) * (v1_y - v0_y) - (v2_y - v0_y) * (v1_x - v0_x));
					float b0 = abs((x - v1_x) * (y - v2_y) - (y - v1_y) * (x - v2_x))/ twice_triangle_area;
					float b1 = abs((x - v0_x) * (y - v2_y) - (y - v0_y) * (x - v2_x))/ twice_triangle_area;


					float b2 = 1.0 - b0 - b1;

                    triangle_ids[y * imagesize + x] = i;
                    barycentric[3*(y * imagesize + x) + 0] = b0;
                    barycentric[3*(y * imagesize + x) + 1] = b1;
                    barycentric[3*(y * imagesize + x) + 2] = b2;


				}
			}
		}
	}

}



void render_colour_core_cpp(int* triangle_ids, int* triangles, float* texture, float* barycentric_coordinates, int* colorimage, int imagesize)
{
	for (int i = 0; i < imagesize; ++i)
	{
		for (int j = 0; j < imagesize; ++j)
		{
			if (triangle_ids[i * imagesize + j] != -1)
			{
				int triangle_id = triangle_ids[i * imagesize + j];
				int v0_id = triangles[3 * triangle_id + 0];
				int v1_id = triangles[3 * triangle_id + 1];
				int v2_id = triangles[3 * triangle_id + 2];

				float b0 = barycentric_coordinates[3*(i * imagesize + j)];
				float b1 = barycentric_coordinates[3*(i * imagesize + j) + 1];
				float b2 = barycentric_coordinates[3*(i * imagesize + j) + 2];
				colorimage[3*(i * imagesize + j) + 0] = std::max(std::min((int)floor(texture[3 * v0_id + 0] * b0 +
				                                                                     texture[3 * v1_id + 0] * b1 +
				                                                                     texture[3 * v2_id + 0] * b2),255),0);
				colorimage[3*(i * imagesize + j) + 1] = std::max(std::min((int)floor(texture[3 * v0_id + 1] * b0 +
		                                                                             texture[3 * v1_id + 1] * b1 +
		                                                                             texture[3 * v2_id + 1] * b2), 255), 0);
				colorimage[3*(i * imagesize + j) + 2] = std::max(std::min((int)floor(texture[3 * v0_id + 2] * b0 +
				                                                                     texture[3 * v1_id + 2] * b1 +
				                                                                     texture[3 * v2_id + 2] * b2), 255), 0);

			}
		}
	}

}


