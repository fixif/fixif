from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

setup(
	cmdclass = {'build_ext': build_ext},
	ext_modules = [Extension("runC",
					sources=["runCython.pyx", "runC.c"],
					extra_compile_args=['-Wno-unused-function'],
					include_dirs=[numpy.get_include()])],
)