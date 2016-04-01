# coding: utf8

"""
This file contains Object and methods for a structure


To Build a structure, we should
- build a class derived from Structure class
- set the name (_name)
- set the options (dictionary _possibleOptions)
- if the structure cannot handle some filters (MIMO filters, for example), override the canAcceptFilter method
- in the constructor:
	- run manageOptions (that check if the options are correct, and store the options of the instance)
	- set the SIF (_SIF)

"""

__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Chevrel Philippe"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from itertools import izip, product
from fipogen.SIF import Realization


class Structure(object):
	"""
	- _name: name of the structure
	- _options: dictionary discribing the possible options (name of the option -> tuple of possible values for the option; 1st value is the DEFAULT value for this option)
	- _make: "factory" function to call to make/build a realization
	- _accept: function indicating if the structure can accept a filter
	"""



	def __init__(self, name, make, accept, options=None):
		self._name = name
		self._options = options
		self._make = make
		self._accept = accept

		# store it in the list of possible structures



	@property
	def name(self):
		return self._name



	def makeRealization(self, filter, **options):
		"""
		Factory function
		Return the structured realization of a given filter
		the options passed should correspond to the possible options of the structure
		if no value is passed for a given option, the DEFAULT value for is option (1st value in the tuple of possible values) is chosen
		"""
		if self._options:
			Ropt = { k:v[0] for k,v in self._options.items() }
		else:
			Ropt = {}
		# check the options
		for opt, val in options.items():
			if self._options is None:
				raise ValueError( self._name + ": the option " + opt + "=" + str(val) + " is not correct")
			if opt not in self._options:
				raise ValueError( self._name + ": the input argument " + opt + " doesn't exist")
			if val not in self._options[opt]:
				raise ValueError( self._name + ": the option " + opt + "=" + str(val) + " is not correct")
			# fill the dictionary of option's value with the options given
			Ropt[opt] = val

		# call the "factory" function
		d = self._make( filter, **Ropt)
		structName = self._name + " (" + ", ".join( '%s:%s'%(key,str(val)) for key,val in Ropt.items() ) + ")"

		# build the realization
		return Realization( filter, structureName = structName, **d)





	# def manageOptions(self, **options):
	# 	"""
	# 	Check the options and store them
	# 	"""
	# 	self._options = options
	# 	for opt,val in options.items():
	# 		if self._possibleOptions is None:
	# 			raise ValueError( self.__class__.__name__ + ": the option " + opt + "=" + str(val) + " is not correct")
	# 		if opt not in self._possibleOptions:
	# 			raise ValueError( self.__class__.__name__ + ": the input argument " + opt + " doesn't exist")
	# 		if val not in self._possibleOptions[opt]:
	# 			raise ValueError( self.__class__.__name__ + ": the option " + opt + "=" + str(val) + " is not correct")





def iterStructures(filter):
	"""
	Iterate over all the possible structures, to build (and return through a generator) all the possible realization
	of a given Filter filter (lti)
	Parameters
	----------
	- lti: the filter (Filter object) we want to implement

	Returns
	-------
	a generator

	>>>> f = Filter( num=[1, 2, 3, 4], den=[5.0,6.0,7.0, 8.0])
	>>>> for R in Structure.iterStructures(f):
	>>>>    print(R)

	print the filter f implemeted in all the existing structures wih all the possible options
	(ie Direct Form I (with nbSum=1 and also nbSum=2), State-Space (balanced, canonical observable form, canonical controlable, etc.), etc.)

	"""
	for cls in Structure.__subclasses__():
		if cls._possibleOptions:
			# list of all the possible values for dictionnary
			# see http://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
			vl = ( dict(izip(cls._possibleOptions, x)) for x in product(*cls._possibleOptions.itervalues()) )
			for options in vl:
				if cls.canAcceptFilter(filter, **options):
					yield cls(filter, **options)
		else:
			if cls.canAcceptFilter(filter):
				yield cls(filter)