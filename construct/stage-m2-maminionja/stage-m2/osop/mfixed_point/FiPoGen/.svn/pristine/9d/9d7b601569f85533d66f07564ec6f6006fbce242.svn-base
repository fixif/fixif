# -*- coding: utf-8 -*-

# the path should be set at the root of FiPoGen (ie, with
# $export PYTHONPATH=~/work/thesards/Benoit/FiPoGen
# ) and the server should be run from server folder, with
# $cd server
# $python server·py


# bottle is the web server used
from bottle import route, run, error, static_file, request, post, get

# jinja is the template engine used
from jinja2 import Environment, FileSystemLoader


# oSoP packages
from oSoP.FPF import FPF
from SoP_bits_cleaner.Test_suppr_bits import simple_cleaned_SoP
from oSoP.Variable import Variable
from oSoP.Constant import Constant

from math import floor, ceil, log

# utilities and path definition
from utilities import createImageFromLaTeX, optionManager, colorThemes, clean_caches, imageFormats
from path import VIEWS_PATH, TEMPLATE_PATH, BASE_URL		#paths



# define the template function, so as to use Jinja template exactly as we use bottle template
# add the base_url in the dictionnary...
def template(name, ctx={}):
	t = jinja2_env.get_template(name)
	ctx['base_url'] = BASE_URL
	return t.render(**ctx)




#### Specific files, to be returned  ####
#CSS file
@route('/style.css')
def css():
	return static_file('style.css', root=VIEWS_PATH)

#logos and basic image
@route('/<image_name>.jpg')
def logo(image_name):
	return static_file(image_name+'.jpg', root=VIEWS_PATH)
@route('/<image_name>.gif')
def logo(image_name):
	return static_file(image_name+'.gif', root=VIEWS_PATH)

# favicon
@get('/favicon.ico')
def get_favicon():
	return static_file('favicon.ico', root=VIEWS_PATH)


#### Specific pages ####
# Main page
@route('/')
@route('/index.html')
def main():
	return template( 'index.html')

# 404 error
@error(404)
def error404(error):
	return template( '404.html')



#### Fixed-Point Arithmetic ####

# /FPF
@route('/FPF')
@route('/FPF.html')
def input_FPF():
	return template('FPF.html', {'imageFormats':imageFormats})


# /Constant
@route('/Constant')
@route('/Constant.html')
def input_Constant():
	return template('Constant.html')

#### Services ####
## Services should return text error when an error occurs

# Generate FPF with LaTeX or image output
@route('/FPF/<FPForm>.<outputFormat:re:%s>'%'|'.join(imageFormats+('tex',)) )
def FPF_outputformat_options(FPForm,outputFormat):
	'''Process the request, to produce the FPForm in the format outputFormat with the options (dictionnary)
	called by FPF_outputformat_options and FPF_options_outputformat'''
	# check if the FPF is valid
	FPForm = FPForm.replace('_','.')		# allow '_' (underscore) caracters, and translate them in '.' (point)
	try:
		F = FPF(format=FPForm)
	except:
		return "Invalid FPF format"	#TODO: eventually return a fake image if the outputFormat is an image (fake image with an error message)
	# process the options
	options = optionManager( request.query )
	options.addOptionalOption( "color", colorThemes, "YG")
	options.addOptionalOption( "binary_point", {"yes":True,"no":False}, "no")
	options.addOptionalOption( "FPF_label", ('none', 'left', 'right', 'above','below'), 'none')
	options.addOptionalOption( "bag_label", {"yes":True,"no":False}, "no")
	options.addOptionalOption( "power2", {"yes":True,"no":False}, "no")
	options.addOptionalOption( "notation", ('numeric','bag','w'), "w")
	options.addOptionalOption( "width",  lambda x:int(x), '500' )		# used for jpg, png, tiff only
	options.addOptionalOption( "height",  lambda x:int(x), '300' )		# used for jpg, png, tiff only
	# generate LaTeX code for the FPF only
	latexFPF = F.LaTeX(**options.getValues())
	# create and return image (or latex code)
	if outputFormat != 'tex':
		# encompass it into a complete latex file	
		latexStr = template(  "latex-FPF.tex", options.getValues( {"FPF":latexFPF, "format":outputFormat }  ) )
		return createImageFromLaTeX( F.Qnotation().replace('.','_')+"?"+str(options), latexStr, outputFormat, options)
	else:
		return "\t%Generated from "+BASE_URL+"FPF/latex/"+FPForm+"?"+request.query_string+"\n"+latexFPF	



#---> j'ai pas traité le reste...

# /Sum of FPFs
@route('/Sum')
def input_Sum():
	return static_file('Sum.html', root=VIEWS_PATH)


# /Sum when data are posted
@post('/Sum')
def Sum_submit():
	# get data
	formats = request.forms.get('sum').split("\r\n")
	color = request.forms.get('color')=='on' and "yes" or "no"
	image = request.forms.get('image')

	bits_clean = request.forms.get('bits_clean')=='on' and "yes" or "no"
	if bits_clean == 'yes':
		N=len(formats)
		d2 = request.forms.get('d2')
		if d2 == "N":
			delta = log(N,2)
		else:
			delta = log(N-1,2)
		d1 = request.forms.get('d1')
		delta = d1=='ceil' and int(ceil(delta)) or int(floor(delta))
		d3 = request.forms.get('d3')
		try:
			d3 = int(d3)
			delta += d3
		except:
			return "Invalid value for delta"

	# dictionary creation
	try:
		F = [FPF(format=f) for f in formats]
	except:
		return "Invalid FPF format"
	max_alpha = max(f.alpha for f in F)
	d={}
	d["FPF"] = "\n".join([f.latex(i,max_alpha) for i,f in enumerate(F)])

	return create_image(d,"+".join(formats),image, color )


# /aSoP
@route('/aSoP')
def input_SoP():
	return static_file('aSoP.html', root=VIEWS_PATH)

# /aSoP when data are posted
@post('/aSoP')
def aSoP_submit():
	# get data
	constants = request.forms.get('constants').split("\r\n")
	var_FPF = request.forms.get('var_FPF').split("\r\n")
	var_wi = request.forms.get('var_wi').split("\r\n")
	beta_final = request.forms.get('beta_final') 
	# conversion
	try:
		beta_final = float (beta_final)
	except:
		return "the beta final is not valid"

	cons=[]
	for c in constants:
		try:
			c_v,c_w = c.split(',')
			cons.append(Constant(float(c_v),int(c_w)))
		except:
			return "The constants cannot be converted to float"

	try:
		var_FPF = [FPF(format=f) for f in var_FPF]
	except:
		return "Invalid FPF format"

	var_w = []		# variable wordlength
	var_i = []			# variable interval	
	for wi in var_wi:
		try:
			w,i1,i2 = wi.split(',')
			var_w.append( int(w))
			var_i.append( (float(i1),float(i2)) ) 
		except:
			return "Invalid wordlength,inteval format"
	# now call Benoit's function to do the aSoP...
	interval_var = []	
	for w,i in zip(var_w,var_i):
		interval_var.append(Variable(value_inf=i[0], value_sup=i[1], beta=w))
	return simple_cleaned_SoP( cons, interval_var,beta_final)

	#or return dummy string
	#return 'constants=%s\n var_FPF=%s\n var_w=%s\n var_i=%s'%(constants,var_FPF,var_w, var_i)




# /clean-caches
@route('/clean-caches')
def clean():
	clean_caches()
	return static_file('clean-caches.html',root=VIEWS_PATH)



DEBUG = True		# set this to True for debug

# initialize the template engine
if DEBUG:
	jinja2_env = Environment(loader=FileSystemLoader( TEMPLATE_PATH), cache_size=0)
else:
	jinja2_env = Environment(loader=FileSystemLoader( TEMPLATE_PATH) )
# clean caches in Debug mode
if DEBUG:
	clean_caches()

# run the server
run(host='localhost', port=8080, debug=DEBUG, reloader=False)