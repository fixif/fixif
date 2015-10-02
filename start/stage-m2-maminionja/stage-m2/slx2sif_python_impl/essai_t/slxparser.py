#/usr/bin/python
#####################################################################
#  script python pour generer le SIF                                #
#  correspondant a un diagramme simulink SLX                        #
#  Auteur: Maminionja Ravoson - mai 2015                            #
#####################################################################
from lxml import etree
import sys

print "\n-------------------------------"
print "Analyse d'un fichier Matlab SLX"
print "-------------------------------\n"

#print sys.argv
if len(sys.argv) < 2:
	print "specifiez le fichier a analyser\n"
	sys.exit()
else:
	file = sys.argv[1]

print "analyse du fichier : ", file

tree = etree.parse(file)
#block processing
print "\n- block : brute-----"
i=0
lallblocks = []
for block in tree.xpath("/ModelInformation/Model/System/Block"):
	blocktype =  block.get("BlockType") #recupere un attribut
	lblock = [ block.get("SID") , blocktype ,  block.get("Name")]

	lblock.append('*')
	if blocktype == 'Gain':
		params = block.findall("P")
		for p in params:
			if p.get("Name") == "Gain":
				lblock[3] = p.text

	elif blocktype == 'Delay':
		params = block.findall("P")
		for p in params:
			if p.get("Name") == "DelayLength":
				lblock[3] = p.text
 
	else :
		lblock[3] = '-'
  
	lallblocks.append(lblock) #all blocks are here
	print "B"+str(i),":",lblock
	i+=1
# block : [ SID , BlockType , Name , param ]


#line processing
print "\n- line : brute----"
i=0
lalllines = []
for line in tree.xpath("/ModelInformation/Model/System/Line"):
	lline = []
	params =  line.findall("P")
	for p in params:
		if p.get("Name") == "Src" or p.get("Name") == "Dst":
			lline.append(p.text)

	branchs = line.findall("Branch")
	if branchs:
		for b in branchs:
			for pi in b.findall("P"):
				if pi.get("Name") == "Dst":
					lline.append(pi.text)

	lalllines.append(lline) #all lines are here
	print "L"+str(i),":",lline
	i+=1
# line : [ src , dest1, dest2, ...]


# fonctions utiles
# pour recuperer les blocs dans les lignes
# print getblocknum('12#out:1') doit retourner '12'
def getblocknum( str ):
	b = str.partition('#')
	return b[0]


# pour recuperer le type d'un block
# arg : SID
# retour : Sum / Gain / Delay / Inport / Outport
def getblocktype( sid ,allblocks):
	for block in allblocks:
		if block[0] == sid :
			return block[1]
	return 'unknown'
print 'd - 7:', getblocktype('7',lallblocks)


# pour recuperer le param d'un block
# arg : SID
# retour : Sum / Gain / Delay / Inport / Outport
def getblockparam( sid ,allblocks):
	for block in allblocks:
		if block[0] == sid :
			return block[3]
	return '-'



#retourner le block avec son type : T+SID : pour affichage
def getblocklabel(sid, allblocks):
	if getblocktype(sid,allblocks) == 'Sum':
		return 't'+sid
	elif getblocktype(sid,allblocks) == 'Delay':
		return 'x'+sid
	elif getblocktype(sid,allblocks) == 'Inport':
		return 'u'+sid
	elif getblocktype(sid,allblocks) == 'Outport':
		return 'y'+sid
	elif getblocktype(sid,allblocks) == 'Gain':
		return 'k'+sid
	else:
		return '-'+sid

print 'd---6: ', getblocklabel('6',lallblocks)

#pour recuperer le bloc input
def getinblock(allblocks):
	for block in allblocks:
		if block[1] == 'Inport':
			return block[0]
	return '-'
#print 'd - in:', getinblock(lallblocks)


#pour recuperer le bloc input
def getoutblock(allblocks):
	for block in allblocks:
		if block[1] == 'Outport':
			return block[0]
	return '-'
#print 'd - out:', getoutblock(lallblocks)


#suite du traitement
#simplification de la liste line
print "\n--- lines : [src, dst1, dst2, ... ]"
lalllines2 = []
for ltemp in lalllines:
	simple_line = [getblocknum(sx) for sx in ltemp]
	lalllines2.append(simple_line)
	print simple_line

#distribuer les lines
lalllines3 = []
for ltemp in lalllines2:
	for i in range(1,len(ltemp)):
		lalllines3.append( [ltemp[0] , ltemp[i]] ) #all lines table are here : [ src , dst ]


#pour afficher une liste verticalement
def afficher( list):
	for l in list:
		print l 

print "\n---lines : [src,dst]"
afficher(lalllines3)


# trier les lines par dst - lallines3
def fkey( v ):
	return v[1]

lalllines3.sort(key=fkey)
print "\n---dst sorted lines : [src,dst]"
afficher(lalllines3)


#grouper par destination les lines
#-->ecriture des equations de chaque sortie
print "\n---lines : dst gathered ---"
tempo = '-'
i=0
newlist = [] 
lalllines4 = []

for l in lalllines3:
	if l[1] <> tempo:
		if i <> 0:
			#print newlist
			lalllines4.append(newlist)
		newlist = []
		tempo = l[1]
		i+=1

	newlist.append(l)

#print newlist
lalllines4.append(newlist)

afficher(lalllines4)


#ecriture des equations de chaque sortie
print "\n---equations sorties ---"
lequations = []

for l in lalllines4:
	newlist = ['-']
	for branch in l:
		newlist[0] = branch[1]
		newlist.append(branch[0])

	lequations.append(newlist)
	
afficher(lequations)




#simplifier la variable temporaire a la sortie --------------
for eq in lequations:
	if getblocktype(eq[0],lallblocks) == 'Outport':
		bout = eq[0]
		binter = eq[1]

#supprimer l'equation inutile : la sortie initiale
for eq in lequations:
	if eq[0] == bout:
		lequations.remove(eq)

#remplacer par la sortie
for eq in lequations:
	if eq[0] == binter:
		eq[0] = bout



# fonction pour afficher les equations
def eqafficher( eqlist):
	for eq in eqlist:
		seq = getblocklabel(eq[0], lallblocks) + ' = '
		for i in range(1,len(eq)):
			seq += getblocklabel(eq[i], lallblocks) 
			if i <> len(eq)-1:
				seq += '+'

		print seq

print "\n--- les equations de sorties ---"		
eqafficher(lequations)
		

#fonction pour trier les equations : Sum < Delay < Outport
def cmpeq( eq1, eq2):
	s1 = eq1[0]
	s2 = eq2[0]
	
	lorder = ['Sum','Delay','Outport']
	
	#Sum	
	if getblocktype(s1,lallblocks) == lorder[0]:
		if getblocktype(s2,lallblocks) == lorder[0]:
			return 0
		else:
			return -1
	#Delay
	elif getblocktype(s1,lallblocks) == lorder[1]:
		if getblocktype(s2,lallblocks) == lorder[1]:
			return 0
		elif  getblocktype(s2,lallblocks) == lorder[0]:
			return 1
		else: #if getblocktype(s2,lallblocks) == lorder[2]:
			return -1
	#Outport
	elif getblocktype(s1,lallblocks) == lorder[2]:
		if getblocktype(s2,lallblocks) == lorder[2]:
			return 0
		else:
			return 1

	else:
		return 1

#classer les equations
print "\n--- equations sorties : triees : t-Sum < x-Delay < y-Outport ---"
lequations.sort(cmp=cmpeq)
afficher(lequations)

#etendre les equations pour integrer les coefficients
ext_equations = [ [list(eq),list(eq)] for eq in lequations ]
 #initilasiation de tous les coefficients a 1
print "\n---eq etendus---"
afficher(ext_equations)
for eq in ext_equations:
	for k in range(len(eq[1])):
		eq[1][k] = 1
	#integration des coefficients des Gains
	block = eq[0][0] 
	param = getblockparam(block,lallblocks)

	if getblocktype(block,lallblocks) == 'Gain':
			if not( param in ['*','-']): # '*':gain non donnee dans le diagramme (=1 par defaut) / '-':param absent pour ce bloc 
				eq[1][1] = param


print "\n--- eq etendus initialisees ---"
afficher(ext_equations)

# fonction pour afficher les equations etendues
def exteqafficher( eqlist):
	for eq in eqlist:
		seq = getblocklabel(eq[0][0], lallblocks) + ' = '
		for i in range(1,len(eq[0])):
			seq += str(eq[1][i]) + '.' + getblocklabel(eq[0][i], lallblocks) 
			if i <> len(eq[0])-1:
				seq += ' + '

		print seq

print "\n--- eq etendues : \"human readable\" --"
exteqafficher(ext_equations)


#simplification des equations:w
print "\n--- eq etendues : simplifiees :H ---"

#fonction pour recuperer l'entree et le gain de d'un bloc Gain
# suppose que SID represente un Gain et est un bloc existant
# a ameliorer pour la robustesse
def getkparam( sid, exteq ):
	for eq in exteq:
		if eq[0][0] == sid:	
			return ( eq[0][1],eq[1][1] ) # (in , k)
#test
#input,gain = getkparam('6',ext_equations)
#print input, gain



#simplification - 1 passe
#a appeler autant de fois qu'on veut ;-)
def eqrefactorgain(exteq, blocklist):
	for eq in exteq:
		for i in range(1,len(eq[0])):
			if getblocktype(eq[0][i],blocklist) == 'Gain':
				input,gain = getkparam(eq[0][i],exteq)
				eq[0][i] = input
				eq[1][i] *= gain

eqrefactorgain(ext_equations,lallblocks)
eqrefactorgain(ext_equations,lallblocks)
exteqafficher(ext_equations)
print "\n--- eq etendues : simplifiees :M ---"
afficher(ext_equations)


#determination de : l:nbr resultats intermediaires / m:nbr entree
# n:nbr etats / p:nbr sortie
def getsifsize( blocklist ):
	l=0
	n=0
	m=0
	p=0
	for b in blocklist:
		if b[1] == 'Sum':
			l += 1
		elif b[1] == 'Inport':
			m += 1
		elif b[1] == 'Delay':
			n += 1
		elif b[1] == 'Outport':
			p += 1
	
	l -= 1 # on a enleve une equation intermediaire a la sortie -------------------
	return (l,m,n,p)
	
print "\n--- taille du SIF ---" 
l,m,n,p = getsifsize(lallblocks)
print ' l=',l,' m=',m,' n=',n,' p=',p

#fonction : construire une matrice de taille a,b 
def mat(a,b):
	m = [[0 for i in range(b)] for j in range(a) ]
	return m

#contruire les matrices du SIF
J = mat(l,l)
K = mat(n,l) 
L = mat(p,l)
M = mat(l,n)
P = mat(n,n)
R = mat(p,n)
N = mat(l,m)
Q = mat(n,m)
S = mat(p,m)


#remplissage des matrices du SIF
#ordonner les variables du systeme : construire les vecteurs t , x , u , y
#important pour l'ordre des equations 
t = []
x = []
u = []
y = []

for b in lallblocks:
	if getblocktype(b[0],lallblocks) == 'Sum':
		if b[0] <> binter: # la variable temporaire de sortie supprimee ------------------
			t.append(b[0])
	if getblocktype(b[0],lallblocks) == 'Delay':
		x.append(b[0])
	if getblocktype(b[0],lallblocks) == 'Inport':
		u.append(b[0])
	if getblocktype(b[0],lallblocks) == 'Outport':
		y.append(b[0])


print "--- les variables du systeme ---"
#print 't=',t
#print 'x=',x
#print 'u=',u
#print 'y=',y

#fonction pour obtenir le label d'un bloc
def getblocklabel( block,blocklist ):
	for b in blocklist:
		if b[0] == block:
			return b[2]

#affichage des variables du systeme avec leur label
tl = [getblocklabel(b,lallblocks) for b in t]
xl = [getblocklabel(b,lallblocks) for b in x]
ul = [getblocklabel(b,lallblocks) for b in u]
yl = [getblocklabel(b,lallblocks) for b in y]
print 't=',tl
print 'x=',xl
print 'u=',ul
print 'y=',yl


#parcours des equations pour etablir les matrices J,K,L,M,N,P,Q,R,S
# eq[0] : equations
# eq[1] : coefficients
for eq in ext_equations:
	if eq[0][0] in y: #sortie
		for block,coeff in zip(eq[0][1:],eq[1][1:]): # balayage des entrees de l'equation courante
			if block in t:
				L[y.index(eq[0][0])] [t.index(block)] = int(coeff)
			elif block in x:                   
				R[y.index(eq[0][0])] [x.index(block)] = int(coeff)
			elif block in u:                   
				S[y.index(eq[0][0])] [u.index(block)] = int(coeff)


	elif eq[0][0] in x: #etat
		for block,coeff in zip(eq[0][1:],eq[1][1:]): # balayage des entrees de l'equation courante
			if block in t:
				K[x.index(eq[0][0])] [t.index(block)] = int(coeff)
			elif block in x:                    
				P[x.index(eq[0][0])] [x.index(block)] = int(coeff)
			elif block in u:                    
				Q[x.index(eq[0][0])] [u.index(block)] = int(coeff)

	elif eq[0][0] in t: #intermediaire
		for block,coeff in zip(eq[0][1:],eq[1][1:]): # balayage des entrees de l'equation courante
			if block in t:
				J[t.index(eq[0][0])] [t.index(block)] = 0-int(coeff)
			elif block in x:
				M[t.index(eq[0][0])] [x.index(block)] = int(coeff)
			elif block in u:
				N[t.index(eq[0][0])] [u.index(block)] = int(coeff)

#traitement de la matrice J
for i in range(l):
	for j in range(l):
		if i == j:	
			J[i][j] = 1

#affichage du SIF
print "\n-- les matrices representant le SIF --"
print "\nJ:",l,'x',l
afficher(J)
print "\nK:",n,'x',l
afficher(K)
print "\nL:",p,'x',l
afficher(L)
print "\nM:",l,'x',n
afficher(M)
print "\nP:",n,'x',n
afficher(P)
print "\nR:",p,'x',n
afficher(R)
print "\nN:",l,'x',m
afficher(N)
print "\nQ:",n,'x',m
afficher(Q)
print "\nS:",p,'x',m
afficher(S)

		
	











