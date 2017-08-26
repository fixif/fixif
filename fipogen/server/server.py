# -*- coding: utf-8 -*-

"""
Web server used to display web pages as front-end for the FiPoGen tool suite.
the run server is run from runServer.py
"""

# bottle is the web server used
from bottle import route, run, error, static_file, request, post, get, response
from bottle import jinja2_template as template
from bottle import Jinja2Template, TEMPLATE_PATH
from bottle import install, default_app

# FiPoGen packages
from fipogen.FxP import FPF
from fipogen.FxP import Variable
from fipogen.FxP import Constant

# utilities and path definition
from fipogen.server.utilities import createImageFromLaTeX, optionManager, colorThemes, clean_caches, imageFormats
from fipogen.server.path import Config  # paths
from fipogen.server.utilities import return_dictionary_constant, evaluate_exp, get_interval_inf, is_sollya_installed

from operator import attrgetter
from functools import wraps  # use to wrap a logger for bottle
import os
import re
from logging import getLogger

import hashlib



# weblogger
weblogger = getLogger('bottle')
# Path to the template
TEMPLATE_PATH[:] = ['templates/']

# todo: delete the following lines
# regexs
lit = "[+-]?\\d+(?:\\.\\d+)?"  # literal
# lit = "[+-]?\\d+[.]?\\d+[[e][-]?\\d+]?"
reobj_constant = re.compile("^" + lit + "$")  # regex defining a constant
reobj_interval = re.compile("^\\[(" + lit + ");(" + lit + ")\\]$")  # regex defining an interval


# --- Specific pages ---
# Main page
@route('/')
@route('/index.html')
def main():
	"""Returns the main page '/index.html'"""
	return template('index.html')


# 404 error
@error(404)
def error404(_):
	"""Handles the 404 error (Not Found), and returns the specific page :-)"""
	return template('404.html')


# --- Fixed-Point Arithmetic ---

# /FPF
@route('/FPF')
@route('/FPF.html')
def input_FPF():
	"""Returns the /FPF page that display Fixed-Point Format"""
	return template('FPF.html', {'imageFormats': imageFormats, 'colors': reversed(list(colorThemes.items()))})


# /Constant
@route('/Constant')
@route('/Constant.html')
def input_Constant():
	"""Returns the /Constant page that helps to transform/approach real constant into fixed-point constant"""
	if is_sollya_installed():
		return template('Constant.html', {'imageFormats': imageFormats, 'mode': 'sollya'})
	else:
		return template('Constant.html', {'imageFormats': imageFormats, 'mode': 'simple'})


# /Sum of FPFs
@route('/Sum')
@route('/Sum.html')
def input_Sum():
	"""Returns the /Sum page
	that display a sum of fixed-point numbers"""
	return template('Sum.html', {'imageFormats': imageFormats, 'colors': reversed(list(colorThemes.items()))})


# --- Services ---
# TODO: Services should return text error when an error occurs

# Generate FPF with LaTeX or image output
@route('/FPF/<FPForm>.<outputFormat:re:%s>' % '|'.join(imageFormats + ('tex', 'json')))
def FPF_service(FPForm, outputFormat):
	"""
	Service that generates a FPF image (or LaTeX or informations encapsulated in json) from a FPF description
	Ex: answer to /FPF/uQ3.5.pdf?option1=value1&option2=value2
	Process the request, to produce the FPF `FPForm` in the format `outputFormat` with the various options taken from the request
	
	The FPF should be given in Q-notation or in Parentheses-notation
	The outputFormat can be image ('pdf','jpg','png','tiff' or 'eps' (see utilities.imageFormats)), 'tex' or 'json' 
	
	Possible options:
		colors: indicates the color theme ('YG' for yellow and green, 'BG' for black and white, etc.)
		binary_point: (boolean) indicates if the binary point is displayed 
		numeric: (boolean) display numeric values (instead of symbolic) if True
		notation: use MSB/LSB notation if 'mlsb', or integer/fractional part if 'ifwl'
		label: indicates where to display the label ('left'/'right'/'above'/'below' or 'no' if the label should not be displayed)
		intfrac: (boolean) display integer/fractional parts if True
		power2: (boolean) display power-of-2 if True 
		height: image's height (for jpg, png, tiff only)
		widht: image's width (for jpg, png, tiff only)
		bits: binary value to be displayed (nothing if no bit is given)
	"""
	# check if the FPF is valid

	# TODO: Change the name of the generated file:
	"""
	Qd on demande une constante sur un grand nombre de bits (j'ai fait 124 bits), on a l'erreur suivante:
	127.0.0.1 - - [24/Jul/2017 22:18:52] "GET /Constant/121545@12121?WL=125 HTTP/1.1" 200 22523
	cp: cache/Q18_107?numeric=no&power2=no&intfrac=no&bits=01110110101100100100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000&width=500&binary_point=yes&notation=mlsb&drawMissing=no&label=no&height=1300&y_origin=0&colors=RB.jpg: File name too long
	Cela est du au fait que le champs bits est trop grand, ce qui donne un nom de fichier stocké en cache trop grand. Une solution pourrait-être de former le nom du fichier autrement : en stockant un hash (genre md5) pour le nom du fichier dès que le nom devient trop grand. On peut aussi, au lieu de stocker tous les bits dans le nom, juste stocker la même chose en décimal (ou en hexa), mais cela ne fait que repousser le problème.
	À mon avis, la bonne solution est de faire un mélange des deux (on ne met plus "bits=...." dans le nom du fichier, mais value=..., et dès que le nom du fichier dépasse le nombre maximum de caractères pour un fichier (255 sous Mac, 4069 sous Unix, le tout étant défini dans limits.h, cf https://stackoverflow.com/questions/32807560/how-do-i-get-in-python-the-maximum-filesystem-path-length-in-unix)
	"""

	FPForm = FPForm.replace('_', '.')  # allow '_' (underscore) characters, and translate them in '.' (point)
	try:
		F = FPF(formatStr=FPForm)
	except ValueError:
		return {'error': "Invalid FPF format"}
	# process the options
	options = optionManager(request.query)
	options.addOptionalOption("colors", colorThemes, "YG")  # color theme
	options.addOptionalOption("binary_point", {"yes": True, "no": False}, "no")  # show the binary-point
	options.addOptionalOption("numeric", {"yes": True, "no": False}, "no")  # display numeric values (instead of symbolic)
	options.addOptionalOption("notation", ("mlsb", "ifwl"), "mlsb")  # notation chosen for the display (MSB/LSB or integer/fractional part)
	options.addOptionalOption("label", ('no', 'left', 'right', 'above', 'below'), 'no')  # display the label
	options.addOptionalOption("intfrac", {"yes": True, "no": False}, "no")  # display the integer/fractional part
	options.addOptionalOption("power2", {"yes": True, "no": False}, "no")  # display the power-of-2
	options.addOptionalOption("width", lambda x: int(x), '500')  # used for jpg, png, tiff only
	options.addOptionalOption("height", lambda x: int(x), '1300')  # used for jpg, png, tiff only (default value is very large, to let the user specify width=2000 without being blocked by the height:300)
	options.addOptionalOption("bits", lambda x: str(x), "")  # value of the bits to be displayed
	options.addOptionalOption("y_origin", lambda x: float(x), "0")
	options.addOptionalOption("drawMissing", {"yes": True, "no": False}, "no")
	# generate LaTeX code for the FPF only
	latexFPF = F.LaTeX(**options.getValues())

	# initializing the hash object
	m = hashlib.md5()
	m.update(str(options).encode('UTF-16'))

	# create and return image (or latex code)
	if outputFormat != 'tex' and outputFormat != 'json':
		# prepare the conversion argument (in the LaTeX class 'standalone')
		if outputFormat != "pdf":
			convert = "convert={size=%dx%d,outext=.%s}," % (options['width'], options['height'], outputFormat)
		else:
			convert = ""
		# encompass it into a complete latex file
		latexStr = template("latex-FPF.tex", options.getValues({"FPF": latexFPF, "format": outputFormat, "convert": convert}))
		# and create the image from the latex
		return createImageFromLaTeX(F.Qnotation().replace('.', '_') + "?" + m.hexdigest(), latexStr, outputFormat)
	elif outputFormat == 'json':
		return {'latex': latexFPF, 'interval': '[%f;%f]' % F.minmax(), 'quantization': '2^%d = %f' % (F.lsb, 2 ** F.lsb)}
	else:
		return "\t%Generated from " + Config.baseURL + "FPF/" + FPForm + ".tex?" + request.query_string + "\n" + latexFPF


# TODO: - régler le découpage de la page (à gauche le formulaire, à droite *centré* l'image avec les liens et le code


# Generate informations for a constant/interval in FxP
@route('/Constant/<constantsInter>')
def Constant_service(constantsInter):
	"""Service that generates all the information for the transformation of a constant
	It returns a JSON object, containing dictionaries of: the FPF, the integer associated, the errors, etc. of the constants and intervals given in constantsInter.
	Ex: answer to /Constant/zzzz?option1=xxx&option2=yyy
	where zzzz is string of constants or a intervals seperated by @
	
	Possible options:
		FPF: string describing the FPF (Q-notation or parenthesis notation) 
		WL: word-length
			-> only one of these two options should be given !
		signed: (bool) indicates if the constant is represented with a signed constant

	It returns a json object containing dictionaries related to each constant or interval with the following fields
		error: (string) indicates if there is an error
		FPF: (string) the FPF used for the conversion (usefull if the WL was given)
		FPF_image: (url) the url used for the image of the FPF
	and for a constant (not for an interval)	
		integer: the associated Fixed-Point integer
		bits: 2's complement binary of the integer
		approx: the approximated value
		error_abs: absolute error
		error_rel: relative error"""
	# get the FPF
	q = request.query
	if "FPF" in q:
		try:
			F = FPF(formatStr=q["FPF"])
			WL = None
		except ValueError:
			return {"error": "invalid FPF"}
	# or get the word-length
	elif "WL" not in q:
		# return {'error':"At least one option 'FPF' or 'WL' must be given"}
		WL = 8
		F = None
	else:
		try:
			WL = int(q["WL"])
		except ValueError:
			return {"error": " The Word-length must be an integer"}
		F = None
	# and get the signedness
	if "signed" in q:
		signed = q["signed"] != 'no'
	else:
		signed = True

	returningJson = {}


	exps = []   # List containing input constants / intervals / their evaluation.

	# Treating the raw input from client:
	for i in range(0, len(constantsInter.split("@"))):
		line = constantsInter.split("@")[i].replace("div", "/")  # replacing div with the real division sign
		line = line.strip()
		if len(line) > 0:  # empty strings shouldn't be treated
			try:    # if it's a normal constant then it should simply be added to exps
				Constant(value=line, wl=100, signed=signed)
				exps.append({'exp': line, 'val': line, 'const': True})
			except ValueError:     # it's either an interval or a mathematical expression that needs to be evaluated
				if line[0] == '[':  # Since the input format is once validated in client side, we can simply use this condition to determine whether it's an interval or not
					if WL:
						exps.append({'exp': line, 'val': get_interval_inf(line, WL), 'const': False})
					else:
						exps.append({'exp': line, 'val': get_interval_inf(line, F.wl), 'const': False})
				else:   # Not an interval but a mathematical expression that needs to be evaluated
					if WL:
						exps.append({'exp': line, 'val': evaluate_exp(line, WL), 'const': True})
					else:
						exps.append({'exp': line, 'val': evaluate_exp(line, F.wl), 'const': True})

	counter = 0
	for expression in exps:
		constInter = expression['val']
		if len(constInter) != 0:
			inter = reobj_interval.match(constInter)  # is it an interval ?

			# get the constant
			if expression['const'] and expression['val'] != "NaN":
				try:
					C = Constant(value=expression['val'], wl=WL, signed=signed, fpf=F)
					dico = return_dictionary_constant(C)
					dico['value'] = expression['exp']
					returningJson[counter] = dico
				except ValueError:
					Cs = Constant(value=expression['val'], wl=F.wl, signed=signed)
					dico = return_dictionary_constant(Cs)
					dico['value'] = expression['exp']
					errStr = "Not possible with the asked FPF; suggestion: " + str(Cs.FPF)
					dico["error"] = errStr
					returningJson[counter] = dico
			elif inter:
				try:
					val_inf = float(inter.group(1))
					val_sup = float(inter.group(2))
				# TODO: conversion str->float... faire avec GMP?
				except ValueError:
					returningJson[counter] = {'value': expression['exp'], 'error': 'The interval must be of the form [xxx;yyy] where xxx and yyy are litteral'}
				try:
					if WL:
						C = Constant(value=val_sup, wl=WL)
						if float(Constant(value=val_inf, wl=WL).FPF.msb) > float(C.FPF.msb):
							C = Constant(value=val_inf, wl=WL)
					else:
						C = Constant(value=val_sup, fpf=F)
						if float(Constant(value=val_inf, fpf=F).FPF.msb) > float(C.FPF.msb):
							C = Constant(value=val_inf, fpf=F)
					dico = return_dictionary_constant(C)
					dico["value"] = expression['exp']
					returningJson[counter] = dico
				except ValueError:  # None of the interval values could be represented with the given format
					Cs = Constant(value=val_sup, wl=F.wl, signed=signed)
					if float(Constant(value=val_inf, wl=F.wl).FPF.msb) > float(Cs.FPF.msb):
						Cs = Constant(value=val_inf, wl=F.wl)
					dico = return_dictionary_constant(Cs)
					dico["value"] = expression['exp']
					errStr = "Not possible with the asked FPF; suggestion: " + str(Cs.FPF)
					dico["error"] = errStr
					returningJson[counter] = dico
			else:
				if expression["val"] != "NaN":
					returningJson[counter] = {
						'value': expression['exp'],
						'error': "The url should contain the constant or the interval (ex '/Constant/12.44' or '/Constant/[-120;10])'"
					}  # General Error
				else:
					returningJson[counter] = {
						'value': expression['exp'],
						'error': "Arithmetic problem"
					}
			counter += 1
	return returningJson


# Generate Sum of FPF image (or LaTeX)
@route('/Sum.<outputFormat:re:%s>' % '|'.join(imageFormats + ('tex',)))
def Sum_service(outputFormat):
	"""Generate Sum of FPF image (or LaTeX)"""
	# TODO: add docstring
	try:
		# get data
		formats = request.query.sum.split(":")
		# build each FPF
		F = [FPF(formatStr=f.replace('_', '.')) for f in formats]
		resultFPF = FPF(formatStr=request.query.result.replace('_', '.'))
	except ValueError:
		return "Invalid Fixed-Point Formats"  # TODO: message d'erreur plus explicite ?
	# process the options
	options = optionManager(request.query)
	options.addOptionalOption("colors", colorThemes, "YG")  # color theme
	options.addOptionalOption("width", lambda x: int(x), '500')  # used for jpg, png, tiff only
	options.addOptionalOption("height", lambda x: int(x), '1300')  # used for jpg, png, tiff only (default value is very large, to let the user specify width=2000 without being blocked by the height:300)
	options.addOptionalOption("axis", {"yes": True, "no": False}, "no")  # display a vertical axis on bit=0
	options.addOptionalOption("sort", ("no", "lsb", "msb"), "no")
	options.addOptionalOption("hatches", {"yes": True, "no": False}, "no")  # display hatches for the bits outside the FPF of the result
	options.addOptionalOption("xshift", lambda x: float(x), '0')
	options.addOptionalOption("yshift", lambda x: float(x), '0')
	# sorting the FPF
	if options["sort"] == 'msb':
		F.sort(key=attrgetter('msb'), reverse=True)
	elif options["sort"] == 'lsb':
		F.sort(key=attrgetter('lsb'))
	# generate LaTeX code for the FPFs
	latexFPF = "\n".join([f.LaTeX(x_shift=options["xshift"], y_origin=-i * 1.3 + options["yshift"], colors=options["colors"], hatches=((resultFPF.msb, resultFPF.lsb) if options["hatches"] else None)) for i, f in enumerate(F)])
	latexFPF += "\n\t%result\n" + resultFPF.LaTeX(x_shift=options["xshift"],
	                                              y_origin=-len(F) * 1.3 - 0.3 + options["yshift"],
	                                              colors=options["colors"]
	                                              )
	minlsb = min(f.lsb for f in F + [resultFPF])
	maxmsb = max(f.msb for f in F + [resultFPF])
	latexFPF += "\n\t\\draw (%f,%f) -- (%f,%f) [color=black,line width=1pt];" % (
		-maxmsb - 1.2 + options["xshift"], -len(F) * 1.3 + 1 + options["yshift"], -minlsb + 0.2 + options["xshift"],
		-len(F) * 1.3 + 1 + options["yshift"])
	if options["axis"]:
		latexFPF += "\n\n\t\\draw (%f,%f) -- (%f,%f) [color=red];" % (
			options["xshift"], 1.2 + options["yshift"], options["xshift"], -len(F) * 1.3 - 0.5 + options["yshift"])

	sumName = "-".join([f.Qnotation() for f in F + [resultFPF]])
	if outputFormat != 'tex':
		# prepare the conversion argument (in the LaTeX class 'standalone')
		if outputFormat != "pdf":
			convert = "convert={size=%dx%d,outext=.%s}," % (options['width'], options['height'], outputFormat)
		else:
			convert = ""
		# encompass it into a complete latex file
		latexStr = template("latex-FPF.tex",
		                    options.getValues({"FPF": latexFPF, "format": outputFormat, "convert": convert}))
		# create the image from the latex
		return createImageFromLaTeX(sumName + "?" + str(options), latexStr, outputFormat)
	else:
		return "\t%Generated from " + Config.baseURL + "Sum.tex?" + request.query_string + "\n" + latexFPF


# /aSoP
@route('/aSoP')
def input_SoP():
	"""Generate the aSoP HTML file"""
	return static_file('aSoP.html', root=Config.views)


# /aSoP when data are posted
@post('/aSoP')
def aSoP_submit():
	"""Manage the aSoP data"""
	# get data
	constants = request.forms.get('constants').split("\r\n")
	var_FPF = request.forms.get('var_FPF').split("\r\n")
	var_wi = request.forms.get('var_wi').split("\r\n")
	beta_final = request.forms.get('beta_final')
	# conversion
	try:
		beta_final = float(beta_final)
	except ValueError:
		return "the beta final is not valid"

	cons = []
	for c in constants:
		try:
			c_v, c_w = c.split(',')
			cons.append(Constant(float(c_v), int(c_w)))
		except ValueError:
			return "The constants cannot be converted to float"

	try:
		_ = [FPF(formatStr=f) for f in var_FPF]
	except ValueError:
		return "Invalid FPF format"

	var_w = []  # variable wordlength
	var_i = []  # variable interval
	for wi in var_wi:
		try:
			w, i1, i2 = wi.split(',')
			var_w.append(int(w))
			var_i.append((float(i1), float(i2)))
		except ValueError:
			return "Invalid wordlength,inteval format"
	# now call Benoit's function to do the aSoP...
	interval_var = []
	for w, i in zip(var_w, var_i):
		interval_var.append(Variable(value_inf=i[0], value_sup=i[1], wl=w))  # beta=w changed in wl=w
	return simple_cleaned_SoP(cons, interval_var, beta_final)


# or return dummy string
# return 'constants=%s\n var_FPF=%s\n var_w=%s\n var_i=%s'%(constants,var_FPF,var_w, var_i)


# /clean-caches
@route('/clean-caches')
def clean():
	"""Clean the caches"""
	# TODO: keep the clean caches page ?
	clean_caches()
	return static_file('clean-caches.html', root=Config.views)


# --- Specific files, to be returned  ---
# CSS file
@route('/style.css')
def css():
	"""Returns the '/style.css' file located in the 'views' folder"""
	return static_file('style.css', root=Config.views)


# JS files
@route('/<filename>.js')
def js(filename):
	"""Returns the '/*.js' files"""
	return static_file(filename + '.js', root=Config.views)

# # ACE files
# @route('/ace-builds-master/src/<filename>.js')
# def ACE(filename):
#     """Returns the ace files"""
#     return static_file(filename + '.js', root=Config.views + 'ace-builds-master/src/')


# Code Mirror, mostly files in lib directory
@route('/plugins/codemirror/codemirror-5.28.0/<path>/<filename>.js')
def plugins(filename, path):
	"""Returns the ace files"""
	return static_file(filename + '.js', root='plugins/codemirror/codemirror-5.28.0/' + path + '/')


# Code Mirror style file
@route('/plugins/codemirror/codemirror-5.28.0/<path>/<filename>.css')
def plugins(filename, path):
	"""Returns the ace files"""
	return static_file(filename + '.css', root='plugins/codemirror/codemirror-5.28.0/' + path + '/')


# Code Mirror 2 layers: js
@route('/plugins/codemirror/codemirror-5.28.0/<path1>/<path2>/<filename>.js')
def plugins(filename, path1, path2):
	"""Returns the ace files"""
	return static_file(filename + '.js', root='plugins/codemirror/codemirror-5.28.0/' + path1 + '/' + path2 + '/')


# Code Mirror 2 layers: css
@route('/plugins/codemirror/codemirror-5.28.0/<path1>/<path2>/<filename>.css')
def plugins(filename, path1, path2):
	"""Returns the ace files"""
	return static_file(filename + '.css', root='plugins/codemirror/codemirror-5.28.0/' + path1 + '/' + path2 + '/')


# logos and basic image
@route('/<image_name>.<outputFormat:re:jpg|gif>')
def getImage(image_name, outputFormat):
	"""Returns the /*.jpg or /*.gif images"""
	return static_file(image_name + '.' + outputFormat, root=Config.views)


# favicon
@get('/favicon.ico')
def get_favicon():
	"""Returns the favicon"""
	return static_file('favicon.ico', root=Config.views)


# a test page
@get('/test')
def test():
	"""Returns the test page"""
	# TODO: to be removed...
	return template('test.html')


# add a logger wrapper for bottle (in order to log its activity)
# See http://stackoverflow.com/questions/31080214/python-bottle-always-logs-to-console-no-logging-to-file
def log_to_logger(fn):
	"""	Wrap a Bottle request so that a log line is emitted after it's handled."""

	@wraps(fn)
	def _log_to_logger(*_args, **_kwargs):
		actual_response = fn(*_args, **_kwargs)
		weblogger.info('%s %s %s %s' % (request.remote_addr, request.method, request.url, response.status))
		return actual_response

	return _log_to_logger


def runServer(host, port, debug, cache, generated):
	"""Run the webserver
	Parameters:
	- host: (string) name of the host (usually 'localhost')
	- port: (int) port of the server (ususally 8080)
	- debug: (bool) True if debug mode
	- cache: (string) path where to cache the files
	- generated: (string) path where to generate the LaTeX files
	"""
	# store the paths
	Config.cache = cache
	Config.generated = generated
	Config.baseURL = 'http://%s:%s/' % (host, port)

	# clean caches in Debug mode
	if debug:
		clean_caches()

	# some checks
	# TODO: check that we can run pdflatex
	# TODO: add this in the command line
	os.environ["PATH"] = os.getenv(
		"PATH") + ":/usr/texbin:/usr/local/bin/"  # Q&D : add the paths to run it on 'Bethmale' with Eclipse...

	# TODO: check that we can copy files in generated folder
	# TODO: etc.

	# add the base url to all the templates
	Jinja2Template.defaults['base_url'] = 'http://%s:%s/' % (host, port)
	# configure the web server
	install(log_to_logger)
	weblogger.info("Run the web server on port %d...", port)
	default_app().catchall = True  # all the exceptions/errors are catched, and re-routed to error500
	# run the server
	run(host='localhost', port=8080, debug=debug, quiet=not debug, reloader=False)
