import unittest
from FxP.FPF import FPF
from FxP.Constant import Constant
from FxP.Variable import Variable



########################################################################
class Test_Variable(unittest.TestCase):
	""""""

	#----------------------------------------------------------------------
	def test_construct(self):
		#construct Variable by given FPF
		f = FPF(wl=8, msb=4)
		V = Variable(fpf=f)
		self.assertEqual(V.FPF.wl , 8)
		self.assertEqual(V.values , (-16,15.875))
		self.assertEqual(V.integers,(-128,127))
		
		value_inf = - 16.118
		value_sup = 15.562
		wl = 8
		V = Variable(value_inf=value_inf, value_sup=value_sup, wl=wl)
		self.assertEqual(V.values , (value_inf,value_sup))
		self.assertEqual(V.integers,(-128,124))
		
		value_inf = - 16.118
		value_sup = 15.957
		V = Variable(value_inf=value_inf, value_sup=value_sup, wl=wl)
		self.assertEqual(V.values , (value_inf,value_sup))
		self.assertEqual(V.FPF.wml(), (8,5,-2))
		self.assertEqual(V.integers,(-64,64))	

		with self.assertRaises(AssertionError):
			V = Variable(fpf=f, wl=wl)
			V = Variable(value_inf=value_inf, value_sup=value_sup, wl=wl, fpf=f)
			V = Variable(value_inf=value_inf, value_sup=value_sup, integer_inf=-128,integer_sup=124)
		
	def test_add(self):
		f = FPF(wl=8, msb=4)
		V1_before_shift = Variable(fpf=f)
		V1_after_shift = V1_before_shift.copy()
		V2 = V1_after_shift.add(V1_after_shift,8)
		self.assertEqual(V2.integers,(-128,126))
		self.assertEqual(V2.FPF.wml(),(8,5,-2))
		self.assertEqual(V1_after_shift.FPF.wml(),(8,5,-2))
		rshift = [-V1_before_shift.FPF.lsb+V1_after_shift.FPF.lsb , -V1_before_shift.FPF.lsb+V1_after_shift.FPF.lsb]
		self.assertEqual(rshift,[1,1])
		
		V1 = Variable(value_inf=-2.156732, value_sup=5.572124, wl=8)
		V2 = Variable(value_inf=-12.3642, value_sup=14.7524, wl=8)
		VC1 = V1.copy()
		VC2 = V2.copy()
		V3 = VC1.add(VC2,8)
		self.assertEqual(V3.values,(-14.520932,20.324524))
		self.assertEqual(V3.integers,(-59,81))
		rshift = [-V1.FPF.lsb + VC1.FPF.lsb , -V2.FPF.lsb + VC2.FPF.lsb]
		self.assertEqual(rshift,[2,1])
		
		with self.assertRaises(AssertionError):
			#V4 = V1 + f, Variable + FPF, AssertionError expected
			V4,rshift = V1_before_shift.add(f,8)
		
		#test msb_final and Jackson's rule
		V1 = Variable(value_inf=-0.5, value_sup=1.5, wl=4)
		V2 = Variable(value_inf=-0.25, value_sup=1.0, wl=4)
		VC1 = V1.copy()
		VC2 = V2.copy()
		V3 = VC1.add(VC2,4,msb_final=2)
		self.assertEqual(V3.FPF.wml(),(4,1,-2))
		
		V4 = Variable(value_inf=-1.25, value_sup=-0.75, wl=4)
		VC3 = V3.copy()
		VC4 = V4.copy()
		V5 = VC3.add(VC4, 4, 2)
		self.assertEqual(V5.FPF.wml(),(4,1,-2))
		self.assertEqual(V5.values,(-2.0,1.75))
		
    
	def test_mult(self):
		V1 = Variable(value_inf=-12.3642, value_sup=14.7524, wl=8)
		with self.assertRaises(AssertionError):
			#V2 = V1 * 3, Variable * int, AssertionError expected
			V2, rshift = V1.mult(3,16)
		
		C = Constant(value=3.754652 , wl=8)
		V2, rshift= V1.mult(C,16)
		self.assertEqual(V2.integers,(-11880,14160))
		self.assertEqual(V2.FPF.wml(), (16,7,-8))
		
		V3, rshift = V1.mult(C,14)
		
		
		
	
if __name__ == '__main__':
	unittest.main()