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
from fixif.LTI import Filter, iter_random_Filter
from latex import build_pdf, LatexBuildError



@pytest.mark.parametrize("F", iter_random_Filter(10, ftype='SISO'), ids=lambda x: x.name)
def test_algorithmLaTeX(F):
	# iter on realizations
	for R in F.iterAllRealizations():
		print(R.name + "\t")
		# get LaTeX code
		code = R.algorithmLaTeX()
		print(code)
		# compile it
		try:
			build_pdf(code)
		except LatexBuildError as e:
			for err in e.get_errors():
				print(err["context"][1])
			raise LatexBuildError
		except RuntimeError:
			print("LaTeX is not installed")


@pytest.mark.parametrize("coefFormat", [None, '%.4f', '%e'], ids=['hexa', '4 digits', 'exp'])
@pytest.mark.parametrize("F", iter_random_Filter(10, ftype='SISO'), ids=lambda x: x.name)
def test_algorithmTxt(F, coefFormat):
	# iter on realizations
	for R in F.iterAllRealizations():
		print(R.name + "\t")
		print(R.algorithmTxt(coefFormat=coefFormat, withTime=True, withSurname=False, comments=True))
		R.algorithmTxt(coefFormat=coefFormat, withTime=True, withSurname=True, comments=True)
		R.algorithmTxt(coefFormat=coefFormat, withTime=False, withSurname=False, comments=True)




def test_algorithmTxt2():
	F = Filter(num=[2, 3, 4], den=[1, 5, 6])
	res = iter(["""t(k+1) <- -6*x1(k) + -5*x2(k) + 4*x3(k) + 3*x4(k) + 2*u(k)
x1(k+1) <- x2(k)
x2(k+1) <- t(k+1)
x3(k+1) <- x4(k)
x4(k+1) <- u(k)
y(k) <- t(k+1)""",
"""t <- -6*y(k-2) + -5*y(k-1) + 4*u(k-2) + 3*u(k-1) + 2*u(k)
y(k) <- t""",
"""t <- -6*x1 + -5*x2 + 4*x3 + 3*x4 + 2*u
x1 <- x2
x2 <- t
x3 <- x4
x4 <- u
y <- t""",
"""t1(k+1) <- 4*x3(k) + 3*x4(k) + 2*u(k)
t2(k+1) <- t1(k+1) + -6*x1(k) + -5*x2(k)
x1(k+1) <- x2(k)
x2(k+1) <- t2(k+1)
x3(k+1) <- x4(k)
x4(k+1) <- u(k)
y(k) <- t2(k+1)""",
"""t1 <- 4*u(k-2) + 3*u(k-1) + 2*u(k)
t2 <- t1 + -6*y(k-2) + -5*y(k-1)
y(k) <- t2""",
"""t1 <- 4*x3 + 3*x4 + 2*u
t2 <- t1 + -6*x1 + -5*x2
x1 <- x2
x2 <- t2
x3 <- x4
x4 <- u
y <- t2""",
"""t(k+1) <- x3(k) + u(k)
x1(k+1) <- 3*t(k+1) + x2(k)
x2(k+1) <- 4*t(k+1)
x3(k+1) <- -5*t(k+1) + x4(k)
x4(k+1) <- -6*t(k+1)
y(k) <- 2*t(k+1) + x1(k)""",
"""t <- x3(k) + u(k)
x1(k+1) <- 3*t + x2(k)
x2(k+1) <- 4*t
x3(k+1) <- -5*t + x4(k)
x4(k+1) <- -6*t
y(k) <- 2*t + x1(k)""",
"""t <- x3 + u
x1 <- 3*t + x2
x2 <- 4*t
x3 <- -5*t + x4
x4 <- -6*t
y <- 2*t + x1""",
"""t(k+1) <- -6*x1(k) + -5*x2(k) + u(k)
x1(k+1) <- x2(k)
x2(k+1) <- t(k+1)
y(k) <- 2*t(k+1) + 4*x1(k) + 3*x2(k)""",
"""v <- -6*v(k-2) + -5*v(k-1) + u(k)
y(k) <- 2*v + 4*v(k-2) + 3*v(k-1)""",
"""t <- -6*x1 + -5*x2 + u
x1 <- x2
x2 <- t
y <- 2*t + 4*x1 + 3*x2""",
"""t(k+1) <- x1(k) + 2*u(k)
x1(k+1) <- -5*t(k+1) + x2(k) + 3*u(k)
x2(k+1) <- -6*t(k+1) + 4*u(k)
y(k) <- t(k+1)""",
"""t <- x1(k) + 2*u(k)
x1(k+1) <- -5*t + x2(k) + 3*u(k)
x2(k+1) <- -6*t + 4*u(k)
y(k) <- t""",
"""t <- x1 + 2*u
x1 <- -5*t + x2 + 3*u
x2 <- -6*t + 4*u
y <- t"""])

	# iter on realizations
	from fixif.Structures import DFI, DFII
	for R in [DFI(F, nbSum=1, transposed=False), DFI(F, nbSum=2, transposed=False), DFI(F, nbSum=1, transposed=True), DFII(F, transposed=False), DFII(F, transposed=True)]:
		# print(R.name)
		for wT, wS in [(True, False), (True, True), (False, False)]:
			st = R.algorithmTxt(coefFormat="%d", withTime=wT, withSurname=wS, comments=False)
			algo = next(res)
			assert st == algo


