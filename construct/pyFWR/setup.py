from setuptools import setup

setup(
    name='pyFWR',
    version='0.1.0dev',
    author='Thibault Hilaire',
    author_email='thibault.hilaire@lip6.fr',
    packages=['pyFWR', 'pyFWR.test'],
    scripts=[],
#    url='http://pypi.python.org/pypi/pyFWR/',
    license='LICENSE.txt',
    description='Finite Word-length Realization toolbox.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.6.1",
        "scipy >= 0.9.0",
        "slycot >= 0.1.0"
    ],
)