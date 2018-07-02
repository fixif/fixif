# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# Get the long description from the README file
import os
import codecs
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open('README.rst', encoding='utf-8') as f:
	long_description = f.read()



# setup arguments
setup(
	name='fixif.fixif',
	#namespace='fixif',
	version='0.4',
	description='Fixed-Point filters',
	long_description=long_description,
	url='https://github.com/FiXiF/fixif',
	author='Thibault Hilaire, Anastasia Volkova, Joachim Kruithof, Benoit Lopez',
	author_email='thibault.hilaire@lip6.fr',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Topic :: Scientific/Engineering',
		'Topic :: Software Development :: Embedded Systems',
		'Topic :: Software Development :: Code Generators',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	keywords='fixed-point arithmetic',
	packages=find_packages(exclude=['tests']),
	install_requires=[
		"numpy", "scipy",
		"colorama",
		"matplotlib",
		"fixif.FxP>=0.1",
		# "sollya",
		# "matlabengineforpython",
		# "sollya",
		# "cython",
		"lxml",		# used for the simulink import
		"colorama",
		"mpmath",
		'jinja2',
		'pytest', 'pytest-cov', 'coveralls'],
	 extras_require={
	 	'slicot':  ['slycot'],
	 	'sollya': ['sollya'],
	 },
	dependency_links = ["https://github.com/fixif/fixif.FxP/archive/master.zip#egg=fixif.FxP-0.2"], # install fixif.FxP from github
	project_urls={
		'Bug Reports': 'https://github.com/FiXiF/fixif/issues',
		'Source': 'https://github.com/FiXiF/fixif/',
	},
)
