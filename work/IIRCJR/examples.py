
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

from numpy.linalg.linalg import LinAlgError

def CheckWCPG(b, a):
	"""
	Given a transfer function "H" in the form of the numerator and denumerator,
	this function tries to compute the WCPG of this filter "H" and
	the WCPG of the corresponding error filter "deltaH".


	Parameters
	----------
	b - numer
	a

	Returns
	-------

	boolean - whether we can or not compute the WCPGs

	"""

	H = dTF(num=b, den=a)
	try:
		WCPG = H.WCPG()
		print WCPG
	except:
		return False

	Heps = dTF(num=numpy.matrix([1]), den = a)

	try:
		wcpgHeps = Heps.WCPG()
		print wcpgHeps
	except:
		#raise ValueError("Could not compute the WCPG of the error system")
		return False

	return True




def example1():
	b = numpy.array([0.118370664306386721986719123833609046414, \
	              0.490401026793067740250364749954314902425, \
	              1.190570782819459605406109403702430427074, \
	              1.916028855100447181314393674256280064583, \
	              2.24415541717465805149345214886125177145, \
	              1.916028855100447181314393674256280064583, \
	              1.190570782819459383361504478671122342348, \
	              0.490401026793067740250364749954314902425, \
	              0.118370664306386721986719123833609046414])

	a = numpy.array([1, \
	              0.989003287123678465064813281060196459293, \
	              2.976167956020775662295818619895726442337, \
	              1.512781789805480725519259976863395422697, \
	              2.695082071017033342741342494264245033264, \
	              0.485244776245198516928525123148574493825, \
	              1.019697185038379139143671636702492833138, \
	              -0.018250143199271331995170442041853675619, \
	              0.19568726182868487195598561356746358797])

	return b,a

def example2():
	b = numpy.array([0.001024353901619323454347254553908896924, \
	               - 0.003663407014305803538478656378174491692, \
	               0.009922413988848466370740197817212902009, \
	               - 0.016887619213826352004836905962292803451, \
	               0.024684048139283695788570582863030722365, \
	               - 0.027439202723066401234941480424822657369, \
	               0.029769234201076827384113698826695326716, \
	               - 0.028347933334659319859483161962998565286, \
	               0.029769234201076827384113698826695326716, \
	               - 0.027439202723066401234941480424822657369, \
	               0.024684048139283695788570582863030722365, \
	               - 0.016887619213826352004836905962292803451, \
	               0.009922413988848466370740197817212902009, \
	               - 0.003663407014305803538478656378174491692, \
	               0.001024353901619323454347254553908896924])

	a = numpy.array([1, \
	               - 8.725375200483702187170820252504199743271, \
	               38.355219838025000456127600045874714851379, \
	               - 110.745294497399868305365089327096939086914, \
	               232.737270240590930825419491156935691833496, \
	               - 374.625496202077897578419651836156845092773, \
	               474.689127543620941196422791108489036560059, \
	               - 479.925865263857758691301569342613220214844, \
	               388.535887145793935815163422375917434692383, \
	               - 250.49976697946030412822437938302755355835, \
	               126.621475216987306566807092167437076568604, \
	               - 48.699249987806084050134813878685235977173, \
	               13.494402545098072465634686523117125034332, \
	               - 2.418212469015935894844915310386568307877, \
	               0.212424718070935131253307304177724290639])
	return b,a

def simpleFilter():
	# lowapass filter
	g = Gabarit(48000, [(0, 9600), (12000, None)], [(0, -1), -80])

	# transfer function for it
	H = g.to_dTF(ftype='ellip', method='matlab')

	return H

def underwaterAcousticsExample():
	b = numpy.matrix([
		0.000000459047935933202453993417623684392,\
		0,\
		- 0.000003213335551532417072074804959003202,\
		0,\
		0.000009640006654597252063257362131309947,\
		0,\
		- 0.00001606667775766208790147286655791703,\
		0,\
		0.00001606667775766208790147286655791703,\
		0,\
		- 0.000009640006654597252063257362131309947,\
		0,\
		0.000003213335551532417072074804959003202,\
		0,\
		- 0.000000459047935933202453993417623684392	])

	a = numpy.matrix([1,\
		10.119168425703881197819100634660571813583,\
		50.368718721819398354000441031530499458313,\
		162.169271594177132556069409474730491638184,\
		375.674400846890137017908273264765739440918,\
		660.571854665738555922871455550193786621094,\
		907.657287531431734350917395204305648803711,\
		989.117538197241401576320640742778778076172,\
		858.784412851431284252612385898828506469727,\
		591.350285655579909871448762714862823486328,\
		318.201031784725728357443585991859436035156,\
		129.967303320702541213904623873531818389893,\
		38.197046210551278022649057675153017044067,\
		7.262400616632169736419655237114056944847,\
		0.67943470904311342728476574848173186183])




	return b,a
#b,a = example1()
#res = CheckWCPG(b,a)
#print res

def printFLOPOCO(b,a):
	coeffa = ":".join(float.hex(float(a[0, i])) for i in range(0, a.shape[1]))
	coeffb = ":".join(float.hex(float(b[0, i])) for i in range(0, b.shape[1]))

	flopocostring = '/Users/anastasiialozanova/Work/flopoco/flopoco/build/flopoco generateFigures=1 FixIIR coeffb="' + coeffb + '" coeffa="' + coeffa + '" lsbIn=-12 lsbOut=-12 TestBench n=10000'
	return flopocostring

def callFLOPOCO(b,a):
	import subprocess
	command = printFLOPOCO(b,a)
	try:
		flopoco_output = subprocess.check_output(command, stderr = subprocess.STDOUT,shell = True)
	except subprocess.CalledProcessError as e:
		print e.message
		raise ValueError("FloPoCo call is not successful: %s\n", command)

	if flopoco_output.find("To run the simulation using gHDL, type the following in a shell prompt:") < 0:
		raise ValueError("FloPoCo call is not successful\n")

	flopoco_output = flopoco_output.split("\n")
	i = flopoco_output.index("To run the simulation using gHDL, type the following in a shell prompt:")
	ghdl1 = flopoco_output[i+1]
	ghdl2 = flopoco_output[i+2]
	ghdl3 = flopoco_output[i+3]

	try:
		ghdl1_output = subprocess.check_output(ghdl1, stderr=subprocess.STDOUT, shell=True)
	except:
		raise ValueError("Call \" %s \" is not successful\n", ghdl1)
	try:
		ghdl2_output = subprocess.check_output(ghdl2, stderr=subprocess.STDOUT, shell=True)
	except:
		raise ValueError("Call \" %s \" is not successful\n", ghdl2)

	try:
		ghdl3_output = subprocess.check_output(ghdl3, stderr=subprocess.STDOUT, shell=True)
	except:
		raise ValueError("Call \" %s \" is not successful\n", ghdl3)

	if ghdl3_output.find("(report note): 0 error(s) encoutered.") > 0:
		print "Success!"
		return 1
	else:
		print "Fail!\n %s" % ghdl3_output
		return 0


#
#b,a = underwaterAcousticsExample()
b = numpy.matrix([1, 2])
a = numpy.matrix([0.5, 0.25])

try:
	res = callFLOPOCO(b,a)
except ValueError as ve:
	print ve



g = Gabarit(48000, [(0, 9600), (12000, None)], [(0, -1), -20])
H = g.to_dTF(ftype='ellip', method='matlab')
print printFLOPOCO(H.num, H.den)



