
from matlab.engine import connect_matlab
from numpy import mat
from fipogen.SIF import SIF
import numpy
import mpmath
from mpmath import *
#return { mat(ep  "JtoS": ((mat(R['J']), mat(R['K']), mat(R['L']), mat(R['M']), mat(R['N']), mat(R['P']), mat(R['Q']),


def get_eps_vectors(n):
	eng = connect_matlab()
	eng.addpath('construct', 'fwrtoolbox')
	eng.eval('[eps, R]=Test_FFT16(%d);'%n , nargout=0)
	# eng.eval('R=tfLWDF2FWR( %f, %f);'%(matlab.double(filter.dTF.num[0].tolist()), matlab.double(filter.dTF.num[0].tolist())), nargoutstruct = eng.eval('struct(e)')

	R = eng.eval('struct(R)')
	l = mat(R['J']).shape[0]
	n = 0
	p = 2*16
	q = 2*16
	S1 = SIF([mat(R['J']), numpy.zeros([0,l]),mat(R['L']), numpy.zeros([l,0]), mat(R['N']), numpy.zeros([0,0]), numpy.zeros([0,q]), numpy.zeros([p,0]), numpy.zeros([p,q])])
	e1 = eng.eval('eps')

	return mat(e1), S1

for i in range(1,6):
	E, S = get_eps_vectors(i)
	Eint = mpmath.iv.matrix(mpmath.zeros(E.shape[0], 1))
	for i in range(0, E.shape[0]):
		if E[i,0] != 0:
			Eint[i,0] = mpi(0, E[i,0])
	deltaT = -numpy.linalg.inv(S.J)*E
	deltaY = S.L*deltaT
	print mnorm(deltaY, p='f')









