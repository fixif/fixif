file_in = open("./PECCS14.txt",'r')
STR=file_in.read()

L=STR.split('\n')
L.remove('')

LL=[]
for x in L:
	LL.append(x.split(' '))

for x in LL:
	while '' in x:
		x.remove('')

u=[]
for x in LL:
	u.append(x[1])

u=[abs(float(x)) for x in u]
u_max = max(u)

y=[]
for x in LL:
	y.append(x[3])

y=[abs(float(x)) for x in y]
y_max = max(y)

print y_max/u_max