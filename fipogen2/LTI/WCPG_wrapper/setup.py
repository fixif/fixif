#coding=utf8
#package using distutils
from distutils.core import setup, Extension
import numpy.distutils.misc_util

#module1 = Extension('_pyWCPG', sources = ['_pyWCPG.c'])

#setup (name='myWCPG',
       #version = '0.0.9',
       #description = 'WCPG calculation package',
       #ext-modules = [module1])

setup(
    ext_modules=[ Extension("_pyWCPG", 
	          sources=["_pyWCPG.c"], 
	          extra_compile_args=[],
#	          extra_link_args=['-rdynamic', '-Wl,/usr/local/lib/libwcpg.so /usr/lib/liblapacke.so'])], #'-l', 'libwcpg.so.0.0.9', '-rdynamic', '' '-Wl,-rpath /usr/local/lib/'
	          extra_link_args=['-rdynamic', '-Wl,./libwcpg.so /usr/lib/liblapacke.so'])], #'-l', 'libwcpg.so.0.0.9', '-rdynamic', '' '-Wl,-rpath /usr/local/lib/'
# RPATH does not work
    
    include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs())

