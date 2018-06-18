# coding: utf8

"""
This file contains the class MatlabHelper, able to connect to matlab
"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



class MatlabHelper(object):
	"""
	Class to help to connect to matlab
	A unique engine is created
	"""
	_engine = None

	def __init__(self, raiseError=False):
		"""
		Connect to the matlab engine
		:param raiseError: True if an error is raise when matlab and the engine are not installed
		"""
		# try to import the matlab engine
		try:
			from matlab.engine import start_matlab, MatlabExecutionError
			from matlab import double as matlab_double
			self._engine = start_matlab()
		except ImportError:
			if raiseError:
				raise ValueError("Matlab and the matlab python engine are not working correctly (may be not installed")

	# TODO: useful ??
	@property
	def engine(self):
		return self._engine


	def __getattr__(self, name):
		if self._engine is None:
			raise ValueError("Matlab and the matlab engine are not installed")
		else:
			return getattr(self._engine, name)

	def double(self):
		return matlab_double

	def MatlabExecutionError(self):
		return MatlabExecutionError


def isMatlabInstalled():
	"""Returns True is the matlab engine is installed (ie accessible with import)"""
	try:
		from matlab import engine
		return True
	except:
		return False




# TODO: log the results, convert the datas, etc.