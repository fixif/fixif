# coding=utf-8

# inspired by http://sourceforge.net/apps/mediawiki/python-control

#inclure licence CECILL-C

"""
This module contains the class `dTF`, that defines a SISO discrete-time Transfer Function.

Properties:
- num,den: numerator and denominator of the transfer function
- Te: sampling time (can be unknown)

Methods:
#Todo#
__str__: string representation
__repr__: representation
normH2: compute the H2-norm of the state-space
_latex_: to be used with Sage
__add__  __radd__
__sub__  __rsub__
__mul__   __rmul__
normHinf: compute the H-infiny norm
dSS: convert to discrete-time State-Space
"""


import numpy as np
import scipy as sc
mat = np.matrix	#alias
from math import sqrt

import slycot

__author__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__license__ = "CECILL-C"
__version__ = "$Id$"
