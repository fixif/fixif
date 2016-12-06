
from fipogen.LTI import Gabarit, iter_random_Gabarit, random_Gabarit
from fipogen.LTI import dTF

g = Gabarit(48000,[ (0,9600), (12000,None) ], [(0,-1), -20])

#for g in iter_random_Gabarit(5, form='lowpass'):
#g = random_Gabarit(form='lowpass')
print(g)

# tfS = g.to_dTF(ftype='butter', method='scipy')
# print(tfS)
# g.plot(tfS)

tfM = g.to_dTF(ftype='butter', method='matlab')
print(tfM)
g.plot(tfM)

g.check_dTF(tfM, 0)