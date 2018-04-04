#coding=UTF8

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

from glob import glob
from os.path import dirname, join, basename
from imp import find_module, load_module
from inspect import getfile


def dynMethodAdder(t_class):
	"""
	This decorator adds (dynamically) some methods to the class t_class, when:
	- function modules are contained in same location as target class module
	- function module name start with the class name
	- the __all__ variable in each function module, is used as list of functions to be added to target class

	How to use it: decorate the class declaration, and that's all
	>>> @dynMethodAdder
	>>> class toto(object):
	>>>     pass

	"""

	# look at all the .py files in the same directory as t_class and starting with its name plus '_'
	path_mod = dirname(getfile(t_class))
	file_pattern = join( path_mod, t_class.__name__ + "_*.py" )
	for f_name in glob( file_pattern ):

		submod_name = basename(f_name)[:-3]   # basename without the extension .py
		f, tmp_filename, description = find_module( submod_name, [dirname(f_name)])

		try:
			mod_mod = load_module( submod_name, f, tmp_filename, description)

			# iter over all the method listed in __all__
			for func_name in mod_mod.__all__:
				setattr( t_class, func_name, mod_mod.__dict__[func_name])

		except ImportError as err:
			print('ImportError:', err)

		finally:
			f.close()

	return t_class