#coding=utf8
#package using distutils
from distutils.core import setup, Extension
import numpy.distutils.misc_util

# multiarch example taken from fltk python wrapper
from sys import platform, exit


#module1 = Extension('_pyWCPG', sources = ['_pyWCPG.c'])

#setup (name='myWCPG',
       #version = '0.0.9',
       #description = 'WCPG calculation package',
       #ext-modules = [module1])

if platform.startswith('linux'):
  print('Building for Linux')
  list_extra_links = ['-rdynamic', '-Wl,./libwcpg.so /usr/lib/liblapacke.so']
elif platform == 'darwin':
  print('Building for Darwin')
  list_extra_links = ['-rdynamic', '-Wl,./libwcpg.dylib /usr/lib/liblapacke.a']
else:
  print("platform not supported, please port this software to your platform !")
  exit(0)

setup(
    ext_modules=[ Extension("_pyWCPG", 
	          sources=["_pyWCPG.c"], 
	          extra_compile_args=[],
#	          extra_link_args=['-rdynamic', '-Wl,/usr/local/lib/libwcpg.so /usr/lib/liblapacke.so'])], #'-l', 'libwcpg.so.0.0.9', '-rdynamic', '' '-Wl,-rpath /usr/local/lib/'
	          extra_link_args=list_extra_links)], #'-l', 'libwcpg.so.0.0.9', '-rdynamic', '' '-Wl,-rpath /usr/local/lib/'
# RPATH does not work
    
    include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs())

