# coding=utf8

"""
Python function used to generate Realization object
for a given Simulink diagram in SLX format
Done by Maminionja Ravoson, during its MsC thesis (June 2015)
Refactored later by Thibault Hilaire
"""


__author__ = "Maminionja Ravoson, Thibault Hilaire"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Maminionja Ravoson"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"



import sif
from diagram import System
from zipfile import is_zipfile, ZipFile
from os.path import split

from fipogen.SIF import Realization
from numpy import mat

from fipogen.LTI.Filter import random_Filter


def importSimulink( fileName, constants={}):
	""" create a Realization object from a Simulink diagram (a slx file)
	Parameters:
		- fileName: name of the slx file
		- constants: dictionary of name->value, to give values to constant used in gain blocks
	"""
	# check slx file
	if not is_zipfile(fileName):
		raise ValueError( "importSimulink: the file doesn't exist or is not a valid slx file")

	# extract archive file and get the `blockdiagram.xml` file
	with ZipFile(fileName) as zfile:
		bd = [ ffname for ffname in zfile.namelist() if split(ffname)[1]=='blockdiagram.xml' ]
		if len(bd)==1:
			blockdiagram = zfile.read(bd[0])
		else:
			raise ValueError("importSimulink: `blockdiagram.xml` not found")

	# processing the `blockdiagram.xml` file
	mysys = System( blockdiagram, constants )
	# blocks and lines
	mysys.printblocks()
	mysys.printlines()
	print "\nInitial Equations"
	mysys.printequations()

	# Call summerge() before expandeqgain()
	# call it as much as there may be a cascaded Sum
	mysys.summerge() 
	mysys.summerge()
	mysys.summerge()
	mysys.expandeqgain() # put gain as Sum coeff 
	print "\nFinal Equations"
	mysys.printequations()

	# SIF Generation
	u,x,t,y = mysys.getsysvar()	
	l = len(t)
	m = len(u)
	n = len(x)
	p = len(y)
	mysif = sif.Sif(l, m, n, p)
	# build the corresponding SIF
	mysif.build(mysys)
	mysif.reorganize()
	print "\n\nSIF corresponding to initial diagram:"
	print mysif	

	print "\nSystem variables:"
	print "input u", u
	print "state x", x
	print "inter t", t
	print "output y", y

	return Realization(random_Filter(5,1,1), (mat(mysif.J), mat(mysif.K), mat(mysif.L), mat(mysif.M), mat(mysif.N), mat(mysif.P), mat(mysif.Q), mat(mysif.R), mat(mysif.S)))




# TODO
# Trigonaliser la matrice J
# gerer les gain successives ( mettre des variables intermediaires)
# traiter les vecteurs X
# ajouter d'autres blocs X
# prise en charge d'un fichier MDL X
# (--> test library linked subsys)
# gain parametrable (variable)

# ASSERTIONS
# - output or intermediate result always on Sum Block
# - No cascading Gain block (solution:make an inter var to preserve value)

# CAPABILITIES
# - can handle scalar multiples I/O
# - can handle SubSystem 
# - can merge cascaded Sum blocks
