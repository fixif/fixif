# -*- coding: utf-8 -*-


"""Function to create/generate images
"""

from os.path import exists
from subprocess import call, Popen, PIPE
from bottle import static_file

from fipogen.server.path import Config

from mpmath import nstr

import logging

# Define the colors for the different color themes (named "BW" and "YG" for the moment)
colorThemes = {"YG": ("orange!60", "yellow!30", "green!15", "Yellow&amp;Green"),
               "BW": ("black!60", "black!30", "white", 'Black&amp;White'),
               "RB": ("red!40", "blue!15", "purple!15", "Red&amp;Blue")}

# Define the available image formats
imageFormats = ('pdf', 'jpg', 'png', 'tiff', 'eps')

# Corresponds to log of latex compilation
latexLogger = logging.getLogger('Latex')

class optionManager:
	"""class to mangage and process the parameters (here coming from an html form)
	
	The idea is to define a set of parameters, possible values for these parameters, and a method to transform these values into final values
	Ex: the option 'isOk' that can accept the values 'yes' and 'no' and should return True or False. And 'yes' as a default Value
	Or the parameter 'width' associated with an integer only (with 100 as default value), etc.
	Ex:
		options.addOptionalOption( 'isOk', {'yes':True,'no':False}, 'yes')
		options.addOptionalOption( 'width', lambda x:int(x), '100')
		
	For that purpose, the optionManager is composed of rules. Each rules will associate a parameterName to a) a method and b) a defaultValue
	a method transform the value associated with the parameter to a final returned value. A method can be a dictionary, a liste/tuple or a function.
	If the value is not in the dictionary, the list or cannot be transformed by the function, the value associated to the defaultValue is returned
	
	Finally, a dictionary, with all the pairs parameter/final value can be obtained with the getValues method.	
	"""

	def __init__(self, query):
		self._query = query	        # initial dictionary where we want to look for the optional parameters
		self._options = {}			# dictionary parameter/value
		self._finalValues = {}      # dictionary parameter/final returned value

	def addOptionalOption(self, parameterName, method, defaultValue):
		# get the value associated with the parameterName, if exits (otherwise, use the defaultValue)
		value = self._query.get(parameterName, defaultValue)

		# transform this value to a final value via the method (can be a disctionary, a list or a function)
		if isinstance(method, dict):
			if value not in method:
				value = defaultValue
			finalValue = method[value]
		elif isinstance(method, list) or isinstance(method, tuple):
			if value not in method:
				value = defaultValue
			finalValue = value
		else:
			try:
				finalValue = method(value)
			except:
				finalValue = method(defaultValue)
				value = defaultValue
	
		# store the value and final value
		self._options[parameterName] = value
		self._finalValues[parameterName] = finalValue
		
	def __str__(self):
		return "&".join(k+"="+v for k, v in self._options.items())
	
	def getValues(self, d=None):
		# TODO: si d est None, alors on renvoie le dico de finalValues...
		# when d is not given
		if d is None:
			d = {}
		# merge the dictionary d and the finalValue dictionary, and return it
		# in Python 3.5+: return {**d, **self._finalValues}
		z = d.copy()
		z.update(self._finalValues)
		return z
	
	def __getitem__(self, attr):
		# 
		return self._finalValues[attr]
	
	
	



def createImageFromLaTeX(baseName, latexStr, outputFormat):
	""""create an image from LaTeX code
	the function generate the associated pdf file (or take it from the cache if it already exists)
	and then convert it in the right outputFormat"""
	filename = baseName+"." + outputFormat
	# check if already created
	if not exists(Config.cache+filename):
		# write the latex code in a file and compile it
		tex_file = open(Config.generated+"FPF.tex", "w")
		tex_file.write(latexStr)
		tex_file.close()
		# compile latex and convert to image format
		command1 = "cd " + Config.generated + " && " + " pdflatex -shell-escape FPF.tex "
		command2 = "cp " + Config.generated + "FPF." + outputFormat + " \"" + Config.cache + filename + "\""
		latexLogger.info("##\tCompile Latex\t##")

		# TODO: check if pdflatex has compiled without errors (call returns the output code)

		proc =Popen(command1, stdout= PIPE, shell=True)
		out, err = proc.communicate()

		latexLogger.info(command1 + "\n")

		proc = Popen(command2, stdout=PIPE, shell=True)
		out, err = proc.communicate()
		latexLogger.info(command2 + "\n")

		latexLogger.info("##\tDone\t##")
	# then return image file
	if outputFormat == "pdf":
		return static_file(filename, root=Config.cache, mimetype="application/pdf")
	else:
		return static_file(filename, root=Config.cache, mimetype="image/"+outputFormat)



def clean_caches():
	"""Clean caches (remove all files in the cache directory)"""
	# TODO: potentially very dangerous !!!
	# TODO: check if Config.cache is not empty !
	try:
		call("rm -r " + Config.cache)
		call("mkdir " + Config.cache)
	except:
		pass


def tobin(x, wl=8):
	"""Convert an integer x in binary
	Returns a string of it's binary representation (two's complement)
	from : http://code.activestate.com/recipes/219300-format-integer-as-binary-string/ """
	# TODO: to move to constant class ! (and use mpmath for that)
	x = int(x)
	return "".join(map(lambda y: str((x >> y) & 1), range(wl-1, -1, -1)))

def returnDictionaryConstant(C):
	""" Takes a constant c and builds a dictionary containing its attributes
	Returns a dictionary"""
	dico = {}
	dico = {
		'value': '',
		'error': '',
		'FPF': str(C.FPF),
		'integer': nstr(C.mantissa),
		'lsb': str(C.FPF.lsb),
		'bits': tobin(C.mantissa, C.FPF.wl),
		'FPF_image': Config.baseURL + 'FPF/' + str(C.FPF) + '.jpg?notation=mlsb&numeric=no&colors=RB&binary_point=yes&label=no&intfrac=no&power2=no&bits=' + tobin(C.mantissa, C.FPF.wl),
		'approx': nstr(C.approx),
		'latex': C.FPF.LaTeX(notation="mlsb", numeric=False, colors=colorThemes["RB"], binary_point=True,label="no", intfrac=False, power2=False, bits=tobin(C.mantissa, C.FPF.wl)),
		'error_abs': nstr(C.absError),
		'error_rel': nstr(C.realError),
		}
	return dico


def evaluateExp(input, wl):
	""" Takes a mathematical expression and evaluates its value with Sollya from bash """
	inputFile = open("input.sollya", "w")

	inputFile.writelines(["verbosity=0;"])
	inputFile.writelines(["display=decimal;"])
	inputFile.writelines(["prec = " + str(min(wl * 10, 1215752192)) + ";"])

	inputFile.writelines(["x=" + input + ";"])

	inputFile.writelines(["x ;"])

	inputFile.close()

	proc = Popen("sollya input.sollya", stdout=PIPE, shell=True)
	out, err = proc.communicate()
	# print(err.decode())
	print("out:"+out.decode())
	if len(out.decode()):
		outs = out.decode().split("\n")
		return outs[len(outs)-2]
	return "NaN"

def getIntervalInf(interval, wl):
	n = len(interval)
	if interval[0] != '[' or interval[n-1] != ']':
		return None
	if interval.find(',') != -1:
		splitter = ','
	elif interval.find(';') != -1:
		splitter = ';'
	else:
		return None

	ind_splitter = interval.index(splitter)
	firstExp = interval[1:ind_splitter]
	secExp = interval[ind_splitter+1:len(interval)-1]

	firstExp = evaluateExp(firstExp, min(wl*100, 1215752192))
	secExp = evaluateExp(secExp, min(1215752192, wl*100))

	if firstExp == "NaN" or secExp == "NaN":
		return None
	return '[' + firstExp + ';' + secExp + ']'






