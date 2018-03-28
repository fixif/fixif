

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

import matplotlib.pyplot as plt
from scipy.fftpack import fft

g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])
H = g.to_dTF(ftype='ellip', method='python')

H_SS = State_Space(Filter(tf=H), form='balanced')
W = H_SS.dSS.WCPG()
print ("<<H>> = %s"% W)
N = 10000
seq = (numpy.zeros([N]))
for i in range(1, N):
    hk = H_SS.dSS.C * ((H_SS.dSS.A ** (N - i)) * H_SS.dSS.B)
    seq[i] = numpy.sign(hk)


SamplingPoints = 1000
SEQ = fft(seq, SamplingPoints)
xf = numpy.linspace(0.0, 2*pi, SamplingPoints)

#plotting the WC sequence of H
plt.plot(xf, numpy.abs(SEQ[0:SamplingPoints]), color='red', label='seq : worst-case sequence of H')
plt.legend()
#plt.show()



coeff = -20 * numpy.log10((0.75 + 0.125 + (numpy.pi - 1)/100)/numpy.pi)
g2 = Gabarit(48000, [(0, 24000*0.75/pi), (24000*1/pi, None)], [-40+coeff, (0+coeff,-1+coeff)])

F = g2.to_dTF(ftype='ellip', method='python')
F_SS = State_Space(Filter(tf=F), form='balanced')
WF = H_SS.dSS.WCPG()
print ("<<F>> = %s"% WF)


seq_filtered = F_SS.simulate(seq)
merde = seq_filtered.transpose().flatten().tolist()[0]
SEQ_filtered = fft(merde, SamplingPoints)
plt.plot(xf, numpy.abs(SEQ_filtered), color='blue', label='seq filtered through F')
plt.legend()
#plt.show()


HF = F_SS.dSS * H_SS.dSS
WHF = HF.WCPG()
HF_SIF = State_Space(Filter(A=HF.A, B=HF.B, C=HF.C, D=HF.D))
print ("<<HF>> = %s"% WHF)



seq_HF = (numpy.zeros([N]))
for i in range(1, N):
    hk = HF_SIF.dSS.C * ((HF_SIF.dSS.A ** (N - i)) * HF_SIF.dSS.B)
    seq_HF[i] = numpy.sign(hk)

SEQ_HF = fft(seq_HF, SamplingPoints)
plt.plot(xf, numpy.abs(SEQ_HF), color='green', label='seq_HF : worst-case sequence of HF')
plt.legend()
plt.show()

output_seq_HF = HF_SIF.simulate(seq_HF)
output_seq = H_SS.simulate(seq_filtered)

seq_filtered2 = F_SS.simulate(seq_HF)
output_seq2 = H_SS.simulate(seq_filtered2)

print numpy.max(numpy.abs(output_seq_HF))
print numpy.max(numpy.abs(output_seq))
print numpy.max(numpy.abs(seq_filtered2))
#g2.plot(F)









