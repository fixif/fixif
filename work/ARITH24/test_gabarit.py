
from fipogen.LTI import Gabarit
from fipogen.LTI import dTF
g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])


tfS = g.to_dTF(ftype='butter', method='scipy')
tfM = g.to_dTF(ftype='butter', method='matlab')
print(tfS.num)
print(tfS.den)
print(tfM.num)
print(tfM.den)


g.plot(tfS)

g.plot(tfM)

g.check_dTF(tfS, 0)
g.check_dTF(tfM, 0)