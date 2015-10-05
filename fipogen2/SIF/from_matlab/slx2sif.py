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
	print "\n\x1b[34m\n------------------------------------"
	print "GENERATING S.I.F FROM SLX MATLAB FILE"
	print "-------------------------------------\n\x1b[0m\n"
	
	# Getting the slx file, containning the diagram, from the command line
	if len(sys.argv) < 2:
		print "give the archive file to continue\n"
		sys.exit()
	else:
		zfile = sys.argv[1]
	
	print "Analysing : ", zfile

	# check archive
	if slxe.isarchivevalid(zfile):
		print "\x1b[32m\narchive OK\x1b[0m\n"
	else:
		print "\x1b[31m\nmissing or bad archive\x1b[0m\n"
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
	print "\x1b[32m\n\nInitial Equations\x1b[0m\n"
	mysys.printequations()

	# Call summerge() before expandeqgain()
	# call it as much as there may be a cascaded Sum
	n_sum = len(mysys.getblocksbytype('Sum'))
	for i in range(n_sum):
		mysys.summerge() 

	mysys.expandeqgain() # put gain as Sum coeff 
	print "\x1b[32m\n\nFinal Equations\x1b[0m\n"
	mysys.printequations()

	# SIF Generation
	# just for SIF size
	u,x,t,y = mysys.getsysvar()	
	l = len(t)
	m = len(u)
	n = len(x)
	p = len(y)
	mysif = sif.Sif(l, m, n, p)
	# build the corresponding SIF
	mysif.build(mysys)
	mysif.reorganize()
	print "\x1b[32m\n\n\nSIF corresponding to initial diagram:\x1b[0m\n"
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

	print "\x1b[32m\n\nSIF matrix saved to : \x1b[0mSIF.txt\n"
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
