
from fipogen.LTI import Gabarit

g = Gabarit(48000,9600,12000,20,1)

tf = g.to_dTF(ftype='butter')

g.check_dTF(tf)