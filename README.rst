FiXiF
*****

FiXiF is a suite of tools to implement filters on embedded devices (usually DSPs, micro-controllers or FPGAs) with finite-precision effects in mind.
It allows to transform a filter/controller into some code (to be executed on a given target) using Fixed-Point Arithmetic, and guaranteeing that the final output error (due to the quantization of the coefficients and the round-off error) is less than a given epsilon.
It allows to consider various possible equivalent (in infinite precision, but no more in finite precision) algorithms (like direct Forms, lattice, state-space, rho-operator based, etc), and find a "good" one, and perform the error analysis.

For the moment FiXif is not fully usable (partly because it is the merge of various previous tools) for everyone, but we want to make "soon" a release. It is based on a several years research work done in academic lab.

====================
INSTALL/REQUIREMENTS

regular packages:
- numpy (>=1.11)
- scipy (>=0.18)
- matplotlib (>=1.5)
- cython (>= 0.25)
- mpmath (>=0.19)
- bottle (>=0.12)
- jinja2 (>=2.8)
- pytest (>=3.0)

    $ pip install numpy scipy matplotlib cython mpmath bottle jinja2 pytest

Others:
- pythonsollya (needs Sollya)
- slycot (pip install slycot, see https://github.com/avventi/Slycot)
- matlabengineforpython (needs Matlab http://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
- WCPG (needs the fixif.WCPG library and its Python wrapper, see https://github.com/fixif/WCPG)

You can have a look at the `travis.yml` file to see how we install it on a fresh linux (and osx) machine for the tests.


=====
TESTS

- Run all the tests (-v is for verbose)
$ py.test fixif/ -v

- Run some tests (like those about LTIs)
$ py.test fixif/LTI -v

=======
AUTHORS
- Thibault HILAIRE
- Anastasia VOLKOVA
- Benoit LOPEZ
- Joachim KRUITHOF
- Maminionja RAVOSON



.. image:: https://travis-ci.org/fixif/fixif.svg?branch=master
    :target: https://travis-ci.org/fixif/fixif
    :align: right
.. image:: https://coveralls.io/repos/github/fixif/fixif/badge.svg?branch=master
    :target: https://coveralls.io/github/fixif/fixif?branch=master
    :align: right


