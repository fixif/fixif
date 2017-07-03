from setuptools import setup

setup(
	name= 'fipogen',
	version= '0.4',
	author= 'Thibault Hilaire, Joachim Kruithof, Benoit Lopez, Anastasia Volkova',
	author_email= 'thibault.hilaire@lip6.fr',
	packages= ['fipogen'],
	scripts= [],
#    url='http://pypi.python.org/pypi/fipogen/',
	license= 'CeCCIL-B',
	description= 'Finite Word-length Realization toolbox.',
	long_description= open('README.txt').read(),
	install_requires= [
		"numpy >= 1.10.4",
		"scipy >= 0.17.0",
		"slycot >= 0.2.0",
		"pytest >= 2.8.7",
		"jinja2 >= 2.8",
#		"sphinx >= 1.3",
#		"lxml >= 3.6",
		"matlabengineforpython",
		"sollya",
		"cython",
		"bottle",
		"jinja2",
		"mpmath"
	],
) 
