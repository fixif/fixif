# coding: utf8

"""
This file contains the class MatlabHelper, able to connect to matlab
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"






class MatlabHelper(object):
	"""
	Singleton class (so that a unique engine is started)
	"""
	_engine = []
	def __init__(self):
		try:
			from matlab.engine import start_matlab
			if not self._engine:
				self._engine.append(start_matlab())
		except:
			self._engine = None

	@property
	def engine(self):
		if self._engine:
			return self._engine[0]
		else:
			return None


# TODO: ne pas crasher qd matlabengine n'est pas installé
# TODO: logger les résultats, convertir les données, etc.