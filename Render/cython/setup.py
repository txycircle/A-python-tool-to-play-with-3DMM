# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 17:03
# @Author  : xinyuan tu
# @File    : setup.py
# @Software: PyCharm

from distutils.core import setup,Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy

setup(
    name='render_core',
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension('render_core',
                sources=["_render_core_cython.pyx","render_core.cpp"],
                language="c++",
                include_dirs=[numpy.get_include()])],
)