
from fipogen.LTI import Butter
from fipogen.Structures.Simulink import importSimulink


F = Butter(3,0.2, name='SiPS16')

dico = {'-a1':-F.dTF.den[0,1], '-a2':-F.dTF.den[0,2], '-a3':-F.dTF.den[0,3], 'b0':F.dTF.num[0,0], 'b1':F.dTF.num[0,1], 'b2':F.dTF.num[0,2], 'b3':F.dTF.num[0,3] }

R = importSimulink("DFIIt.slx", constants=dico)

print( R.to_dTF())
print( F.dTF )