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
from fipogen.LTI.Filter import iter_random_Filter

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
		return self._fullname


	def canAcceptFilter(self, filter, **options):
		"""
		Indicates if the structure is able to implement the filter
		(some structures cannot implement MIMO filters, some are dedicated to butterworth, etc.)
		Returns a boolean
		"""
		return self._accept( filter, **options)


	def makeRealization(self, filter, **options):
		"""
		Factory function
		Return the structured realization of a given filter
		the options passed should correspond to the possible options of the structure
		if no value is passed for a given option, the DEFAULT value for is option (FIRST value in the tuple of possible values) is chosen
		"""
		if self._options:
			Ropt = { k:v[0] for k,v in self._options.items() }
		else:
			Ropt = {}
		# check the options
		for opt, val in options.items():
			if self._options is None:
				raise ValueError( self._shortName + ": the option " + opt + "=" + str(val) + " is not correct")
			if opt not in self._options:
				raise ValueError( self._shortName + ": the input argument " + opt + " doesn't exist")
			if val not in self._options[opt]:
				raise ValueError( self._shortName + ": the option " + opt + "=" + str(val) + " is not correct")
			# fill the dictionary of option's value with the options given
			Ropt[opt] = val

		# call the "factory" function
		d = self._make( filter, **Ropt)
		structName = self._fullName + " (" + ", ".join( '%s:%s'%(key,str(val)) for key,val in Ropt.items() ) + ")"

		# build the realization
		return Realization( filter, structureName = structName, **d)

	def __call__(self, *args, **kwargs):
		"""
		Call the factory
		StateSpace(filter, ...) is equivalent to StateSpace.makeRealization(filter,...)
		"""
		return self.makeRealization( *args, **kwargs)


def iterAllRealizations(filter):
	"""
	Iterate over all the possible structures, to build (and return through a generator) all the possible realization
	of a given Filter filter (lti)
	Parameters
	----------
	- filter: the filter (Filter object) we want to implement

	Returns
	-------
	a generator of

	>>>> f = Filter( num=[1, 2, 3, 4], den=[5.0,6.0,7.0, 8.0])
	>>>> for R in Structure.iterAllRealizations(f):
	>>>>    print(R)

	print the realizations (filter f implemeted in all the existing structures wih all the possible options)
	(ie Direct Form I (with nbSum=1 and also nbSum=2), State-Space (balanced, canonical observable form, canonical controlable, etc.), etc.)

	"""
	for st in Structure._allStructures.values():
		if st._options:
			# list of all the possible values for dictionnary
			# see http://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
			vl = ( dict(izip(st._options, x)) for x in product(*st._options.itervalues()) )
			for options in vl:
				if st.canAcceptFilter(filter, **options):
					yield st.makeRealization(filter, **options)
		else:
			if st.canAcceptFilter(filter):
				yield st.makeRealization(filter)



def iterAllRealizationsRandomFilter(number, n = (5, 10), p = (1, 5), q = (1, 5), seeded=True, type='all'):
	"""
	Iterate over all the possible structures (exactly like iterAllRealizations), except that it does it for `number` random filters
	it just call iterAllRealization for all the random filters
	Parameters are those of iter_random_Filter
	"""
	for F in iter_random_Filter( number, n, p, q, seeded, type):
		for R in iterAllRealizations(F):
			yield R





def makeARealization( filter, realizationName, **options):
	"""
	Factory function to make a realization given its name (among 'DirectForms', 'DFII', etc.)

	>>> f = Filter( num=[1, 2, 3, 4], den=[5.0,6.0,7.0, 8.0])
	>>> R = Structure.makeARealization(f, 'DirectForms', transposed=True)
	>>> print(R)

	print the Direct Form I transposed realization of the filter
	"""
	try:
		R = Structure._allStructures[ realizationName]
	except:
		raise ValueError( "Structure: the realization '%s' doesn't exist (must be in {%s}", realizationName, ", ".join(Structure._allStructures.keys()))

	return R.makeRealization( filter, **options)