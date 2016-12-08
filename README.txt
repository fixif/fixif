--------------------
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
- WCPG


-----
TESTS

- Run all the tests (-v is for verbose)
$ py.test fipogen/ -v

- Run some tests (like those about LTIs)
$ py.test fipogen/LTI -v

- Run some specific tests (like those with the name 'wcpg')
$ py.test -v -k wcpg

