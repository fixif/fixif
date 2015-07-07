from scipy.signal import butter
from ..dSS import dSS
import unittest


class tototest_forms(unittest.TestCase):

	def test_DirectForms(self):
		
		for n,wc in zip([4,8,10],[0.12,0.15,0.45]):
			num,den = butter(n,wc)
			R1 = directFormI(num, den)
			# via matlab
			matlab.eval( "[num,den]=butter(%f,%f)"%(n,wc) )
			matlab.eval("R1 = DFIq2FWR(num,den)")
			Z = matlab2mat("R1.Z")
			print norm(Z - R1.Z) 
			self.assertAlmostEqual(  norm(Z - R1.Z) , 0 )

		