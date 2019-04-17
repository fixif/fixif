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
__copyright__ = "Copyright 2015, FiXiF project, LIP6"
__credits__ = ["Thibault Hilaire", "Chevrel Philippe"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.SIF import Realization
from fixif.LTI.Filter import iter_random_Filter


class Structure(object):
	"""
	- _shortName: (short) name of the structure (Ex: 'rhoDFIIt'); used as key to reference the structure
	- _fullName: full name of the structure (Ex: 'rho Direct Form II transposed')
	- _options: dictionary discribing the possible options (name of the option -> tuple of possible values for the option; 1st value is the DEFAULT value for this option)
	- _make: "factory" function to call to make/build a realization
	- _accept: function indicating if the structure can accept a filter
	"""

	_allStructures = {}

	def __init__(self, shortName, fullName, make, accept, options=None):
		self._shortName = shortName
		self._fullName = fullName
		self._options = options
		self._make = make
		self._accept = accept

		# store it in the disctionary of existing structures
		self._allStructures[shortName] = self

	@property
	def name(self):
		return self._fullName

	@property
	def options(self):
		return self._options

	@classmethod
	def iterAllStructures(cls):
		return cls._allStructures.values()

	@classmethod
	def getFromName(cls, name):
		"""Get a structure from its name"""
		if name in cls._allStructures:
			return cls._allStructures[name]
		else:
			raise ValueError("Structure: the realization '%s' doesn't exist (must be in {%s})", name, ", ".join(cls._allStructures.keys()))

	def canAcceptFilter(self, filt, **options):
		"""
		Indicates if the structure is able to implement the filter
		(some structures cannot implement MIMO filters, some are dedicated to butterworth, etc.)
		Returns a boolean
		"""
		return self._accept(filt, **options)

	def makeRealization(self, filt, **options):
		"""
		Factory function
		Return the structured realization of a given filter
		the options passed should correspond to the possible options of the structure
		if no value is passed for a given option, the DEFAULT value for is option (FIRST value in the tuple of possible values) is chosen
		"""
		if self._options:
			Ropt = {k: v[0] for k, v in self._options.items()}
		else:
			Ropt = {}

		# TODO: check correctly the options (should we also add the parameters ? see the rhoDFIIt that can require some extra parameters like the gammas)
		# # check the options
		for opt, val in options.items():
			# 	if self._options is None:
			# 		raise ValueError( self._shortName + ": the option " + opt + "=" + str(val) + " is not correct")
			# 	if opt not in self._options:
			# 		raise ValueError( self._shortName + ": the input argument " + opt + " doesn't exist")
			# 	if val not in self._options[opt]:
			# 		raise ValueError( self._shortName + ": the option " + opt + "=" + str(val) + " is not correct")
			# 	# fill the dictionary of option's value with the options given
			Ropt[opt] = val

		# call the "factory" function
		d = self._make(filt, **Ropt)
		structName = self._fullName + " (" + ", ".join('%s:%s' % (key, str(val)) for key, val in Ropt.items()) + ")"

		# build the realization
		return Realization(filt, structureName=structName, shortName=self._shortName, **d)

	def __call__(self, *args, **kwargs):
		"""
		Call the factory
		StateSpace(filter, ...) is equivalent to StateSpace.makeRealization(filter,...)
		"""
		return self.makeRealization(*args, **kwargs)




# TODO: should we turn this into a method of Filter class ?????????


# TODO: check if this is really unused (if yes, then remove)
# def iterStructuresAndOptions(filt):
# 	"""
# 	Iterate over all the possibles structures
# 	filt is used to determine the options
# 	Returns a 2-tuple (structure,options)
# 	"""
# 	for st in Structure.iterAllStructures():
# 		if st.options:
# 			# list of all the possible values for dictionnary
# 			# see http://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
# 			vl = ( dict(zip(st.options, x)) for x in product(*st.options.values()))
# 			for options in vl:
# 				if st.canAcceptFilter(filt, **options):
# 					yield st, options
# 		else:
# 			if st.canAcceptFilter(filt):
# 				yield st, st.options


def iterAllRealizationsRandomFilter(number, n=(5, 10), p=(1, 5), q=(1, 5), seeded=True, ftype='all'):
	"""
	Iterate over all the possible structures (exactly like iterAllRealizations), except that it does it for `number` random filters
	it just call iterAllRealization for all the random filters
	Parameters are those of iter_random_Filter
	"""
	for F in iter_random_Filter(number, n, p, q, seeded, ftype):
		for R in F.iterAllRealizations():
			yield R


def makeARealization(filt, realizationName, **options):
	"""
	Factory function to make a realization given its name (among 'DirectForms', 'DFII', etc.)

	>>> from fixif.LTI import Filter
	>>> from fixif.Structures import Structure
	>>> f = Filter( num=[1, 2, 3, 4], den=[5.0,6.0,7.0, 8.0])
	>>> R = Structure.makeARealization(f, 'DirectForms', transposed=True)
	>>> print(R)
	this code prints the Direct Form I transposed realization of the filter
	"""
	S = Structure.getFromName(realizationName)
	return S.makeRealization(filt, **options)
