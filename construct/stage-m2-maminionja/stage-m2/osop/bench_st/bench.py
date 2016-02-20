import pickle, copy_reg, os
from oSoP.oSoP_class_st import oSoP_st

#for filename in ["liste_osops.pkl","liste_osops_19.pkl","liste_osops_32.pkl"]:
for filename in ["liste_osops_32.pkl"]:
    file = open(filename ,'r')
    L_osops = pickle.load(file)
    file.close()
    res = open("result",'a')
    res.write(filename+"\n")
    res.close()
    i = -1
    for osop in L_osops:
      i += 1
      if i == 1:
          res = open("result",'a')
          res.write(str(i)+"\n")
          res.close()
          #print i
          osop.__class__ = oSoP_st
          #osop.Code("Tikz")
          from stratus import Cfg
          osop.To_Stratus(i)
          #os.system("source synth.sh bip")
          os.system("source synth.sh")
          #if i==1:
          #  break
          osop.cell.Delete()
          #os.system("rm -f *.vst *.vhd *.txt")
