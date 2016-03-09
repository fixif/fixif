# coding: utf8

"""
This file contains Object and methods for a structure
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Chevrel Philippe"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import os
from glob import glob
import imp

class Structure(object):
	"""
	- name: name of the structure
	"""

	options = None
	parameters = None


	def initStructure(self, name):
		"""
		Plays the same role of the constructor, BUT it's nicer to call, and now there is no way to build a Structure (only object of derived class)
		"""
		self._name = name


	def __str__(self):
		"""
		Return string describing the structured SIF
		"""
		return "Structured realization (" + self._name + ")\n" + str(self.SIF)


	@property
	def name(self):
		return self._name


	@staticmethod
	def iterStructures(lti):
		for cls in Structure.__subclasses__():
			yield cls(lti)






#
#
# # auto-discovery
# # find here to find existing structures and to import them
# if __name__ != '__main__':	# because __file__ does not exist in that case, but this should never happen
# 	# get the path of this file
# 	structures_path = os.path.dirname( __file__ )
# 	# iterate on each subfolder (each one should contains a structure class)
# 	#try:
# 	for f in glob(structures_path+'/*/'):
# 		f = os.path.normpath(f)
# 		module = f.split(os.sep)[-1]
# 		imp.load_source( module, f+os.sep+module+'.py')
# 	#except Exception as e:
# 		#raise e
# 		#raise ValueError("Structure: failed to import structure in folder '%s' "%f)