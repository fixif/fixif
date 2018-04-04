
import numpy, scipy
import mpmath
import sollya


#from fipogen.LTI import dTFmp, dSSmp, dSS, dTF, Gabarit
from numpy.ma import angle
from scipy.signal import freqz

from fipogen.LTI import dTFmp, dTF, dSSmp, Filter
from fipogen.SIF import SIF
from fipogen.LTI import Gabarit
from fipogen.Structures import State_Space, DFI, DFII, rhoDFII
from fipogen.FxP import Constant
import matplotlib.pyplot as plt
from numpy import array, pi, log10, infty

def iterSimpleGabarit():
	# lowpass
	yield Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
	# highpass
	yield Gabarit(48000,[ (0,9600), (12000,None) ], [-20, (0,-1)])
	# bandpass
	yield Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [-20, (0, -1), -20])
	# bandstop
	yield Gabarit(48000, [(0, 9600), (12000, 14000), (16400, None)], [(0,-1), -20, (0,-1)])
	# multibands
	#yield Gabarit(48000, [(0, 9600), (12000, 14000), (16400, 19000), (19000,None)], [(0,-1), -20, (0,-1),-40])


def QuantizeAndPlot(R,b, color, ls, label, mark):
	R2 = R.quantize(b)
	H = R2.to_dTF()
	w, h = freqz(H.num.transpose(), H.den.transpose())
	plt.plot(w/pi, 20 * log10(abs(h)), color=color, linestyle=ls, marker=mark, label=label)

def QuantizeAndPlotWrapper(R, ls):
	QuantizeAndPlot(R, 53, 'black', ':', 'FP double')
	QuantizeAndPlot(R, 16, 'yellow', ls, 'FxP 16 bits')
	QuantizeAndPlot(R, 12, 'green', ls, 'FxP 12 bits')
	QuantizeAndPlot(R, 8, 'red', ls, 'FxP 8 bits')

def fpoles(H):
	r =array([H.den[0,i] for i in range(0,H.den.shape[1])])
	return numpy.roots(r)

def fzeros(H):
	r = array([H.num[0,i] for i in range(0,H.num.shape[1])])
	return numpy.roots(r)



def nastyFilter():
	# coefficients of the 8th oder elliptic lowpass filter with Rs=80.
	b = array([3.896743970688874e-03, \
	           9.298820313339720e-03, \
	           1.978336478271946e-02, \
	           2.756771345282585e-02, \
	           3.172027987863041e-02, \
	           2.756771345282586e-02, \
	           1.978336478271947e-02, \
	           9.298820313339734e-03, \
	           3.896743970688876e-03])
	a = array([1.000000000000000e+00, \
	           - 3.759692968107118e+00, \
	           8.197633474616900e+00, \
	           - 1.185239940874394e+01, \
	           1.233138152518530e+01, \
	           - 9.297438276083913e+00, \
	           4.976676394723544e+00, \
	           - 1.741888789594852e+00, \
	           3.171876879095002e-01])

	H = dTF(num=b, den=a)
	return H, b, a


def GraphPolesZeros(H):
	# lowapass filter
	#g = Gabarit(48000, [(0, 9600), (12000, None)], [(0, -1), -80])

	# transfer function for it
	#H = g.to_dTF(ftype='ellip', method='matlab')


	R_DFII = DFII(Filter(tf=H), transposed=True)
	R_DFII = R_DFII.quantize(8)
	R_rho = rhoDFII(Filter(tf=H), transposed='True')
	R_rho = R_rho.quantize(8)
	R_SS = State_Space(Filter(tf=H), form='balanced')
	R_SS = R_SS.quantize(8)


	p_ini = fpoles(H)
	z_ini = fzeros(H)
	p_DFII = fpoles(R_DFII.to_dTF())
	z_DFII = fzeros(R_DFII.to_dTF())
	p_rho = fpoles(R_rho.to_dTF())
	z_rho = fzeros(R_rho.to_dTF())
	p_SS = fpoles(R_SS.to_dTF())
	z_SS = fzeros(R_SS.to_dTF())

	ax = plt.subplot(111)
	plt.scatter(p_ini.real, p_ini.imag, color='yellow', label='Initial FP double')
	plt.scatter(p_DFII.real, p_DFII.imag, color='red', marker='v', label='DFIIt FxP 8 bits')
	plt.scatter(p_rho.real, p_rho.imag, color='green', marker='x', label=r'$\rho$'+'DFIIt FxP 8 bits')
	plt.scatter(p_SS.real, p_SS.imag, color='blue', marker='+', label='SS FxP 8 bits')
	currentAxis = plt.gca()
	currentAxis.add_patch(plt.Circle((0,0), radius=1, fill=False, color='black', ls='dashed'))

	r = 1.5
	plt.axis('scaled')
	plt.axis([-r, r, -r, r])
	ticks = [-1, -.5, .5, 1]
	plt.xticks(ticks)
	plt.yticks(ticks)

	ax.spines['left'].set_position('center')
	ax.spines['bottom'].set_position('center')
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)



	plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)


	plt.show(block=True)



def simpleFilter():
	# lowapass filter
	g = Gabarit(48000, [(0, 9600), (12000, None)], [(0, -1), -20])

	# transfer function for it
	H = g.to_dTF(ftype='cheby1', method='matlab')

	return H



def QuantErrorsPlot(H):
	plt.interactive(False)

	w, h = freqz(H.num.transpose(), H.den.transpose())
	plt.plot(w/pi, 20 * log10(abs(h)), color='black', linestyle='-', linewidth=2, label='TF in double precision')


	R_DFII = DFII(Filter(tf=H), transposed=True)
	QuantizeAndPlot(R_DFII, 12, 'green', '-', 'DFIIt FxP 12 bits', '')
	QuantizeAndPlot(R_DFII, 8, 'red', '-', 'DFIIt FxP 8 bits', '')

	# R_SS = State_Space(Filter(tf=H), form='ctrl')
	# QuantizeAndPlotWrapper(R_SS, '--')

	R_SS = State_Space(Filter(tf=H), form='balanced')
	#QuantizeAndPlot(R_SS, 12, 'green', '-', 'SS FxP 12 bits', 'v')
	#QuantizeAndPlot(R_SS, 8, 'red', '-', 'SS FxP 8 bits', 'v')

	R_rho = rhoDFII(Filter(tf=H), transposed='True')
	QuantizeAndPlot(R_SS, 12, 'green', '-.', r'$\rho$' + 'DFIIt FxP 12 bits', '')
	QuantizeAndPlot(R_SS, 8, 'red', '-.', r'$\rho$' + 'DFIIt FxP 8 bits', '')

	currentAxis = plt.gca()
	currentAxis.add_patch(plt.Rectangle((0, -1), 0.4, 1, facecolor="blue", alpha=0.3))
	plt.legend()
	plt.xlabel('Normalized frequency' + r'$(\times \pi$' + '/sample)')
	plt.ylabel('Magnitude (dB)')
	plt.show(block=True)


def plotUnitStepResponse(H):

	b = array([H.num[0,i] for i in range(0, H.num.shape[1])])
	a = array([H.den[0,i] for i in range(0, H.den.shape[1])])
	[T, y] = scipy.signal.dstep((b, a, 1))

	R_DFII = DFII(Filter(tf=H), transposed=True)
	R_DFII = R_DFII.quantize(8)
	b_df = array([R_DFII.to_dTF().num[0, i] for i in range(0, R_DFII.to_dTF().num.shape[1])])
	a_df = array([R_DFII.to_dTF().den[0, i] for i in range(0, R_DFII.to_dTF().den.shape[1])])
	[T, y_df] = scipy.signal.dstep((b_df, a_df, 1))

	R_rho = rhoDFII(Filter(tf=H), transposed='True')
	R_rho = R_rho.quantize(8)
	b_rho = array([R_rho.to_dTF().num[0, i] for i in range(0, R_rho.to_dTF().num.shape[1])])
	a_rho = array([R_rho.to_dTF().den[0, i] for i in range(0, R_rho.to_dTF().den.shape[1])])
	[T, y_rho] = scipy.signal.dstep((b_rho, a_rho, 1))

	R_SS = State_Space(Filter(tf=H), form='balanced')
	R_SS = R_SS.quantize(8)
	b_ss = array([R_SS.to_dTF().num[0, i] for i in range(0, R_SS.to_dTF().num.shape[1])])
	a_ss = array([R_SS.to_dTF().den[0, i] for i in range(0, R_SS.to_dTF().den.shape[1])])
	[T, y_ss] = scipy.signal.dstep((b_ss, a_ss, 1))

	plt.bar(T, y[0], color='black', width=1)
	plt.bar(T, y_df[0], color='red', width=1)
	plt.bar(T, y_rho[0], color='green', width=1)
	plt.bar(T, y_ss[0], color='blue', width=1)



	plt.show()



(H, b, a) = nastyFilter()
#plotUnitStepResponse(H)


#QuantErrorsPlot(H)
GraphPolesZeros(H)


print 'Ho ho ho'










#g.plot(tf=H, dB=False)