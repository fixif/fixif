#!/usr/bin/python
"""
 Python Script for generating S.I.F representation
 for a given Simulink diagram in SLX format
 Author: Maminionja Ravoson - June 2015
"""

import sys
import os # for file writing

import slxextract as slxe
import sif
from diagram import System



def generatesif():
	""" Main function to generate SIF matrix from Simulink diagram"""
	print "\n------------------------------------"
	print "GENERATING S.I.F FROM SLX MATLAB FILE"
	print "-------------------------------------\n"
	
	# Getting the slx file, containning the diagram, from the command line
	if len(sys.argv) < 2:
		print "give the archive file to continue\n"
		sys.exit()
	else:
		zfile = sys.argv[1]
	
	print "Analysing : ", zfile

	# check archive
	if slxe.isarchivevalid(zfile):
		print "archive OK"
	else:
		print "missing or bad archive"
		sys.exit()

	# extract archive file
	if slxe.slxextract(zfile):
		print "blockdiagram extracted in blockdiagram.xml"
	else:
		print "blockdiagram not found in archive"
		sys.exit()

	file = "blockdiagram.xml"
	# processing blockdiagram.xml file
	mysys = System(file)
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
	print "input u", mysif.u
	print "state x", mysif.x
	print "inter t", mysif.t
	print"output y", mysif.y

	# Save SIF to file
	siffile = open("SIF.txt",'w')
	siffile.write(str(mysif))
	siffile.close()

	print "\nSIF matrix saved to SIF.txt"
	print "\n"
	

if __name__ == "__main__":
	generatesif()



# TODO
# Trigonaliser la matrice J V
# gerer les gain successives ( mettre des variables intermediaires)
# traiter les vecteurs X
# ajouter d'autres blocs X
# prise en charge d'un fichier MDL X
# gain parametrable (variable)

# ASSERTIONS
# - output or intermediate result always on Sum Block
# - No cascading Gain block (solution:make an inter var to preserve value)

# CAPABILITIES
# - can handle scalar multiples I/O
# - can handle SubSystem 
# - can merge cascaded Sum blocks
