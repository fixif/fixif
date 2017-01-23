
from matlab.engine import connect_matlab
from numpy import mat
from fipogen.SIF import SIF

def fft2fwr(n):

	eng = connect_matlab()
	eng.addpath('construct', 'fwrtoolbox')

	eng.eval('R=FFT2FWR( %d);' % (n), nargout=0)
	# eng.eval('R=tfLWDF2FWR( %f, %f);'%(matlab.double(filter.dTF.num[0].tolist()), matlab.double(filter.dTF.num[0].tolist())), nargout=0)
	R = eng.eval('struct(R)')

	return {"JtoS": ((mat(R['J']), mat(R['K']), mat(R['L']), mat(R['M']), mat(R['N']), mat(R['P']), mat(R['Q']),
	                  mat(R['R']), mat(R['S'])))}


FFT = fft2fwr(8)

print FFT

