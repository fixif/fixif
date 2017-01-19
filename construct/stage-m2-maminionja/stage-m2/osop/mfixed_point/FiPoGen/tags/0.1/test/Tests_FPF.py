import unittest
from FxP.FPF import FPF

########################################################################
class Test_FPF(unittest.TestCase):
	""""""
	def test_construct(self):
		# construct empty FPF --> impossible		
		# construct FPF with only wl
		f = FPF(16)
		self.assertEqual(f.wml(),(16,None,None))
		# construct FPF with only wl and gamma
		f = FPF(16,lsb=-12)
		self.assertEqual(f.wml(),(16,3,-12))
		f = FPF(16,msb=3)
		self.assertEqual(f.wml(),(16,3,-12))
		f = FPF(16,msb=0)
		self.assertEqual(f.wml(),(16,0,-15))
		self.assertRaises(ValueError,FPF,16,12,-5)
		
		# construct form string
		f = FPF(format="Q8.12")
		self.assertEqual( f.wml(), (20,7,-12))
		f = FPF(format="sQ4.3")
		self.assertEqual( f.wml(), (7,3,-3))
		f = FPF(format="uQ4.3")
		self.assertEqual( f.wml(), (7,3,-3))
		f = FPF(format="<8,-12>")
		self.assertEqual( f.wml(), (21,8,-12))
		with self.assertRaises(ValueError):
			f = FPF(format="totoQ6.8")
		
	def test_wl(self):
		f = FPF(wl=16)
		self.assertEqual(f.wml(),(16,None,None))
		f.wl = 18
		self.assertEqual(f.wml(),(18,None,None))
		f = FPF(16,3,-12)
		f.wl = 18
		self.assertEqual(f.wml(),(18,3,-14))
		
	def test_msb(self):
		f = FPF()
		with self.assertRaises(ValueError):
			f.msb = 12
		
		f = FPF(16)
		f.msb = 3
		self.assertEqual(f.wml(),(16,3,-12))
		
		f = FPF(16,3,-12)
		with self.assertRaises(ValueError):
			f.msb = 6
			
	def test_lsb(self):
		f = FPF()
		with self.assertRaises(ValueError):
			f.lsb = -12
		
		f = FPF(16)
		f.lsb = -12
		self.assertEqual(f.wml(),(16,3,-12))
		
		f = FPF(16,3,-12)
		f.lsb = -14
		self.assertEqual(f.wml(),(18,3,-14))
		
	def test_shif(self):
		f = FPF(16,3,-12)
		f.shift(2)
		self.assertEqual(f.wml(),(16,5,-10))
		
	def test_approx(self):
		F=FPF(16,8)
		self.assertEqual(F.approx(25),25)
		self.assertEqual(F.approx(25.001),25)
		self.assertEqual(F.approx(25.26789),25.265625)
		
		

		

if __name__ == '__main__':
	unittest.main()