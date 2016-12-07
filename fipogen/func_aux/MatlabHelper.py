# coding: utf8

"""
This file contains the class MatlabHelper, able to connect to matlab
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



from matlab.engine import start_matlab


class MatlabHelper(object):
	"""
	Singleton class (so that a unique engine is started)
	"""
	_engine = []
	def __init__(self):
		if not self._engine:
			self._engine.append( start_matlab() )

	@property
	def engine(self):
		return self._engine[0]


# TODO: ne pas crasher qd matlabengine n'est pas installé
# TODO: logger les résultats, convertir les données, etc.