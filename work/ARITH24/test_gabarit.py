
from fipogen.LTI import Gabarit
from fipogen.LTI import dTF
g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])


tf = g.to_dTF(ftype='ellip')


g.plot(tf)


g.check_dTF(tf, 1e-4)