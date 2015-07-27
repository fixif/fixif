#coding=utf8
#package using distutils
from distutils.core import setup, extension
import numpy.distutils.misc_util

setup(
    ext_modules=[Extension("_pyWCPG",["_pyWCPG.c", "chi2.c"])],
    include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs(),
  
)
