#coding=utf8

"""
This metaclass is base for optimization of SIFs

Each SIF coming from different origins have differents manners of undergoing the same treatments, namely optimization.

__metaclass__ = OPT_methods(form_type)

no no arg needed because we determine the type depending on the bases of the class


if form is of

1) form_type = 'SS' type, then we don't need to recalculate all the sensitivity measures from scratch


2) form_type = 'rhoDFIIt', 'modal_delta', 'LGS' then we recalculate all from scratch

the following methods are defined by the metaclass, and differ depending on the form_type

_iterate_form = 

                - _iterate_form_SS
                - _iterate_form_rhoDFIIt


_iterate_sens(type, list_of_sens, plant=None)

 - _iterate_sens_scratch (if form_type == 'rhoDFIIt' or any form that has no transformation process from one sensitivity measurement to another in new base)


On the basis of argument given to the metaclass, what's inside the method will change


"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

class OPT_methods(object):
	
	def __init__(self):

        pass

	def __call__(self, name, bases, dct):
			
		# Add generic method names,
		# Used by the optimize function

		# determine form type based on name contained in bases
		# that way it's more magic, we don't have to specify the type to be used by the metaclas
 
		if ('DFI' or 'DFII' or 'State_Space') in bases
		    self.calc_type = 'ss'
		elif ('rhoDFIIt' or 'LGS' or 'LCW' or 'Modal_delta') in bases:
			self.calc_type = 'recalc'
		else:
			raise(NameError, 'Cannot use this metaclass without corresponding baseclass')
		
		# use faster method to recalculate sensitivity
		if calc_type == 'ss':
		    dct['_iterate_form'] = _iterate_form_translate
		    dct['_iterate_sens'] = _iterate_sens_translate
		    
		# do all calculations at each step
		elif calc_type == 'recalc':
		    dct['_iterate_form'] = _iterate_form_recalc
		    dct['_iterate_sens'] = _iterate_sens_recalc
		    
		
			
