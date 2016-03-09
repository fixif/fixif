from fipogen.LTI import LTI
from fipogen.Structures import State_Space, Structure

print("ok")


f = LTI( num=[1, 2, 3], den=[5.0,6.0,7.0])

for R in Structure.iterStructures(f):
	print(R)

