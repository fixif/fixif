from setuptools import setup, find_packages

setup(
	name= 'fixif',
	version= '0.4',
	author= 'Thibault Hilaire, Joachim Kruithof, Benoit Lopez, Anastasia Volkova',
	author_email= 'thibault.hilaire@lip6.fr',
	packages= find_packages(),  #TODO: list manually the packages we want (FxP, LTI, etc.)
	scripts= [],
#    url='http://pypi.python.org/pypi/fipogen/',
	license= 'GPLv3',
	description= 'Finite Word-length Realization toolbox.',
	long_description= open('README.rst').read(),
	install_requires= [
		"numpy >= 1.10.4",
		"scipy >= 0.17.0",
#		"slycot >= 0.2.0",
		"pytest >= 2.8.7",
#		"jinja2 >= 2.8",
#		"matlabengineforpython",
#		"sollya",
#		"cython",
#		"bottle",
#		"jinja2",
#		"docopt",
		"mpmath"
	],
	include_package_data=True
) 
