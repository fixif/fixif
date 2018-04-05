import numpy
import mpmath
import sollya

from fixif.func_aux import MPFMatrix

import pytest



def test_construction():
	A = mpmath.zeros(5, 5)
	Amp = MPFMatrix(A)
	assert (Amp.almost_close(A))
	assert A == Amp.matrix

	A = numpy.matrix(numpy.zeros([5,5]))
	Amp = MPFMatrix(A)
	assert (Amp.almost_close(A))

	A = numpy.zeros(5)
	Amp = MPFMatrix(A)
	assert (Amp.almost_close(A))

	B = MPFMatrix(A)
	assert (B.almost_close(A))


def test_add():
	A = numpy.zeros([5, 5])
	B = numpy.eye(5)

	Amp = MPFMatrix(A)
	Bmp = MPFMatrix(B)

	Cmp1 = Amp + Bmp
	assert Cmp1.almost_close(MPFMatrix(B))


	Cmp2 = Amp + B
	assert Cmp2.almost_close(MPFMatrix(B))

	Cmp3 = Bmp + Bmp
	assert Cmp3.almost_close(MPFMatrix(2*B))

def test_sub():
	A = numpy.zeros([5, 5])
	B = numpy.eye(5)

	Amp = MPFMatrix(A)
	Bmp = MPFMatrix(B)

	Cmp1 = Amp - Bmp
	assert Cmp1.almost_close(MPFMatrix(-B))

	Cmp2 = Amp - B
	assert Cmp2.almost_close(MPFMatrix(-B))

	Cmp3 = Bmp - Bmp
	assert Cmp3.almost_close(MPFMatrix(A))

def test_mul():
	A = numpy.random.rand(5, 5)
	I = numpy.eye(5)
	Z = numpy.zeros([5, 5])
	Impmath = mpmath.eye(5)
	Zmpmath = mpmath.zeros(5,5)
	A = MPFMatrix(A)


	C0 = A * I
	assert C0.almost_close(A)

	C1 = A * Impmath
	assert C1.almost_close(A)

	C2 = MPFMatrix(I) * A
	assert C2.almost_close(A)

	C3 = A * Z
	assert C3.almost_close(Z)

	C4 = A * Zmpmath
	assert C4.almost_close(Zmpmath)

def test_add_exact():
	A = numpy.random.rand(5, 5)
	A = MPFMatrix(A)
	B = MPFMatrix(mpmath.zeros(5,5))

	C0 = A.add_exact(B)
	assert C0.equal(A)

	C1 = A.add_exact(A)
	C1 = C1.sub_exact(A)
	assert C1.equal(A)

def test_mul_exact():
	Impmath = mpmath.eye(5)
	A = numpy.random.rand(5, 5)
	A = MPFMatrix(A)

	C0 = A.mul_exact(MPFMatrix(Impmath))
	assert C0.equal(A)


def test_inv_lowtr():
	A = numpy.random.rand(5, 5)
	L = numpy.zeros([5,5])
	for j in range(0,5):
		for i in range(j+1, 5):
			L[i,j] = A[i,j]

	L = MPFMatrix(L) + MPFMatrix(mpmath.eye(5))

	Linv = L.inv_lowtr()
	assert (Linv * L).almost_close(MPFMatrix(mpmath.eye(5)))


def test_to_numpy():
	A = numpy.random.rand(5, 5)
	Amp = MPFMatrix(A)
	assert (A == Amp.to_numpy()).all()

def test_to_sollya():
	import sollya

	A = numpy.random.rand(5, 5)
	S_A = [sollya.SollyaObject(a) for a in A.flatten()]

	Amp = MPFMatrix(A)
	S, _, _ = Amp.to_sollya()

	assert S == S_A























