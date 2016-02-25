from setuptools import setup

setup(
    name='fipogen',
    version='0.1.0dev',
    author='Thibault Hilaire, Joachim Kruithof',
    author_email='thibault.hilaire@lip6.fr, joachim.k@free.fr',
    packages=['dSS', 'SIF'],
#    scripts=['fipogen_run', 'fipogen_test'],
    scripts=[],
#    url='http://pypi.python.org/pypi/pyFWR/',
    license='LICENSE.txt',
    description='Finite Word-length Realization toolbox.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.10.4",
        "scipy >= 0.17.0",
        "slycot >= 0.2.0",
        "pytest >= 2.8.7',
	    "pyWCPG >= 0.1.0"
    ],
) 
