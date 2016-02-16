# -*- coding: utf-8 -*-


"""Function to create/generate images
"""

from os.path import exists
from subprocess import call
from bottle import static_file

from path import CACHE_PATH, GENERATED_PATH


# Define the colors for the different color themes (named "BW" and "YG" for the moment)
colorThemes = { "YG" : ("orange!60","yellow!30","green!15","Yellow&amp;Green") , "BW": ("black!60","black!30","white",'Black&amp;White'), "RB":("red!60","blue!30","purple!15","Red&amp;Blue") }

#Define the available image formats
imageFormats = ('pdf','jpg','png','tiff','eps')


class optionManager(object):
	"""class to mangage and process the parameters (here coming from an html form)
	
	The idea is to define a set of parameters, possible values for these parameters, and a method to transform these values into final values
	Ex: the option 'isOk' that can accept the values 'yes' and 'no' and should return True or False. And 'yes' as a default Value
	Or the parameter 'width' associated with an integer only (with 100 as default value), etc.
	Ex:
		options.addOptionalOption( 'isOk', {'yes':True,'no':False}, 'yes')
		options.addOptionalOption( 'width', lambda x:int(x), '100')
		
	For that purpose, the optionManager is composed of rules. Each rules will associated a parameterName to a) a method and b) a defaultValue
	a method transform the value associated with the parameter to a final returned value. A method can be a dictionary, a liste/tuple or a function.
	If the value is not in the dictionary, the list or cannot be transformed by the function, the value associated to the defaultValue is returned
	
	Finally, a dictionary, with all the pairs parameter/final value can be obtained with the getValues method.	
	"""

	def __init__(self, query):
		self._query = query	#initial dictionary where we want to look for the optional parameters
		self._options = {}			# dictionary parameter/value
		self._finalValues = {}	# dictionary parameter/final returned value

	def addOptionalOption( self, parameterName, method, defaultValue):
		# get the value associated with the parameterName, if exits (otherwise, use the defaultValue)
		value = self._query.get( parameterName, defaultValue)

		# transform this value to a final value via the method (can be a disctionary, a list or a function)
		if isinstance(method, dict):
			if value not in method:
				value = defaultValue
			finalValue = method[value]
		elif isinstance(method,list) or isinstance(method,tuple):
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
		self._options[ parameterName ] = value
		self._finalValues[ parameterName ] = finalValue
		
	def __str__(self):
		return "&".join( k+"="+v for k,v in self._options.items() )
	
	def getValues( self, d={} ):
		# merge the dictionary d and the finalValue dictionary, and return it
		return dict( self._finalValues.items() + d.items() )
	
	def __getitem__(self, attr):
		# 
		return self._finalValues[attr]
	
	
	



def createImageFromLaTeX(baseName,latexStr,outputFormat):
	""""create an image from LaTeX code
	the function generate the associated pdf file (or take it from the cache if it already exists)
	and then convert it in the right outputFormat"""
	filename = baseName+"." +outputFormat
	# check if already created
	if not exists(CACHE_PATH+filename):
		# write the latex code in a file and compile it
		tex_file = open( GENERATED_PATH+"FPF.tex", "w" )
		tex_file.write( latexStr )
		tex_file.close()
		# compile latex and convert to image format
		print "Compile Latex"
		call( "echo $PATH", shell=True)
		call( "cd "+GENERATED_PATH+" && pdflatex --shell-escape FPF.tex >output.log", shell=True)
		#TODO: check if pdflatex has compiled without errors (call returns the output code)
		print "Done"
		call("cp " + GENERATED_PATH + "FPF." + outputFormat + " \"" + CACHE_PATH + filename + "\"", shell=True)
	# then return image file 
	if outputFormat=="pdf":
		return static_file( filename, root=CACHE_PATH, mimetype="application/pdf")
	else:
		return static_file( filename, root=CACHE_PATH, mimetype="image/"+outputFormat)



def clean_caches():
	"""Clean caches (remove all files in the cache directory)"""
	call( "rm "+CACHE_PATH+ "* ",shell=True)
	
	
def tobin(x, wl=8):
	"""Convert an integer x in binary
	Returns a string of it's binary representation (two's complement)
	from : http://code.activestate.com/recipes/219300-format-integer-as-binary-string/ """
	return "".join(map(lambda y:str((x>>y)&1), range(wl-1, -1, -1)))	
