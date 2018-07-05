# coding: utf8

"""
This file contains tests for the Realization class
"""

_author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


import pytest
from colorama import Fore
from itertools import chain
from fixif.SIF import Realization
from numpy import matrix as mat, zeros, eye, empty, float64

from fixif.Structures import iterAllRealizationsRandomFilter
from fixif.LTI import Filter, iter_random_Filter, iter_random_dSS, random_Filter
from fixif.Structures import State_Space

from latex import build_pdf, LatexBuildError
from latex.build import LatexBuilder



from numpy.random import seed, rand, randint, shuffle
from numpy.testing import assert_allclose




@pytest.mark.parametrize("S", iter_random_dSS(5, n=(5, 15), p=(1, 5), q=(1, 5)))
def test_construction_from_dSS(S):
	# random SIF from dSS (J=identity, K=zero, L=zero, M=random, N=random)
	l = randint(0, 10)
	JtoS = (eye(l), zeros((S.n, l)), zeros((S.p, l)), rand(l, S.n), rand(l, S.q), S.A, S.B, S.C, S.D)
	R = Realization(Filter(ss=S), JtoS)

	assert len(R._varNameT) == l
	assert len(R._varNameX) == S.n
	assert len(R._varNameY) == S.p
	assert len(R._varNameU) == S.q



@pytest.mark.parametrize("F", iter_random_Filter(10, ftype='SISO'), ids=lambda x: x.name)
def test_algorithmLaTeX(F):
	# iter on realizations
	for R in F.iterAllRealizations():
		print(R.name + "\t")
		# get LaTeX code
		code = R.algorithmLaTeX()
		# compile it
		try:
			build_pdf(code)
		except LatexBuildError as e:
			for err in e.get_errors():
				print(err["context"][1])
			raise LatexBuildError
		except RuntimeError:
			print("LaTeX is not installed")


@pytest.mak.parametrize("coefFormat", [None, '%.4f', '%e'], ids=['hexa', '4 digits', 'exp'])
@pytest.mark.parametrize("F", iter_random_Filter(10, ftype='SISO'), ids=lambda x: x.name)
def test_algorithmTxt(F, coefFormat):
	# iter on realizations
	for R in F.iterAllRealizations():
		print(R.name + "\t")
		print(R.algorithmTxt(coefFormat=coefFormat, withTime=True, withSurname=False, comments=True))
		print('---')
		print(R.algorithmTxt(coefFormat=coefFormat, withTime=True, withSurname=True, comments=True))
		print('---')
		print(R.algorithmTxt(coefFormat=coefFormat, withTime=False, withSurname=False, comments=True))



@pytest.mark.parametrize("F", iter_random_Filter(5, ftype='SISO'), ids=lambda x: x.name)
# @pytest.mark.parametrize("F", [random_Filter(name='RandomFilter-8/4/3-396548150')], ids=lambda x: x.name)
def test_implementCdouble(F):

	N = 10
	u = 3000 * rand(F.q, N)  # random input of N samples

	from numpy.linalg import norm

	for R in F.iterAllRealizations():
		print('\n'+Fore.RED + str(R.name) + Fore.RESET+'\n\t')

		# y = R.simulateMP(u)
		yb = R.simulate(u)
		yC = R.runCdouble(u)

		assert norm(yb-yC) < 1e-5



@pytest.mark.parametrize("F", iter_random_Filter(5, ftype='SISO'), ids=lambda x: x.name)
def test_makeModule(F):
	R = State_Space(F)
	R.makeModule()


@pytest.mark.parametrize("R", iterAllRealizationsRandomFilter(1), ids=lambda x: x.name)
def test_rea2(R):
	N = 10
	u = 300 * rand(R.filter.q, 1)  # random input of N samples

	print(str(R.name) + "\t")

	y = R.simulate(u)
	yC = R.runCdouble(u)
	assert_allclose(y, yC, atol=1e-5)

	R.filter.dSS.assert_close(R.dSS)
	if R.filter.isSISO():
		R.filter.dTF.assert_close(R.dSS.to_dTF())




