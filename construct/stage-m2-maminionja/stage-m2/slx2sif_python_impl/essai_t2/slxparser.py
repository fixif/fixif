#!/usr/bin/python
######################################################
#  Python Script for generating S.I.F representation #
#  for a given Simulink diagram in SLX format		 #
#  Author: Maminionja Ravoson - mai 2015             #
######################################################

from lxml import etree
import sys

print "\n------------------------------------"
print "GENERATING S.I.F FROM SLX MATLAB FILE"
print "-------------------------------------\n"

# Getting the xml file, containning the diagram, from the command line
if len(sys.argv) < 2:
    print "give the diagram file to continue\n"
    sys.exit()
else:
    file = sys.argv[1]

print "Analysing : ", file


# -----------------
# BLOCK FUNCTIONS

# Get block type, given a block SID and blocks table
# return : Sum / Gain / Delay / Inport / Outport
def getblocktype(sid, allblocks):
    for block in allblocks:
        if block[0] == sid:
            return block[1]
    return 'unknown'  # missing block


# getblocktype('7',lallblocks) return type of the block with SID 7


# Get block param, given a block SID and blocks table
# return :  Gain / DelayLength (for Gain or Delay block)
def getblockparam(sid, allblocks):
    for block in allblocks:
        if block[0] == sid:
            return block[3]
    return '-'  # no parameter


# Get the SID of Input block
# assume that there is only one Inport 
# ( improvement : make a list in the function if there is multiple Inport)
def getinblock(allblocks):
    for block in allblocks:
        if block[1] == 'Inport':
            return block[0]
    return '-'


# Get the SID of Output block
# assume that there is only one Outport 
# ( improvement : make a list in the function if there is multiple Outport)
def getoutblock(allblocks):
    for block in allblocks:
        if block[1] == 'Outport':
            return block[0]
    return '-'


# Function : get the label of the block
# ( the name given in simulink block )
def getblocklabel(block, blocklist):
    for b in blocklist:
        if b[0] == block:
            return b[2]


# End block Functions



# ------------------
# LINES FUNCTIONS

# Getting block number in the line String
# ex : getblocknum('12#out:1') must return '12'
def getblocknum(str):
    b = str.partition('#')
    return b[0]


# End lines Functions



# ---------------------
# PRINT FUNCTIONS

# Print list elements line by line
def afficher(list):
    for l in list:
        print l

        # Construct block label for display


# labelblock('6',lallblocks) return 't6' if block 6 is a Sum
def labelblock(sid, allblocks):
    if getblocktype(sid, allblocks) == 'Sum':
        return 't' + sid
    elif getblocktype(sid, allblocks) == 'Delay':
        return 'x' + sid
    elif getblocktype(sid, allblocks) == 'Inport':
        return 'u' + sid
    elif getblocktype(sid, allblocks) == 'Outport':
        return 'y' + sid
    elif getblocktype(sid, allblocks) == 'Gain':
        return 'k' + sid
    else:
        return '-' + sid


# Print a human readable SoP equation (with no coeff)
# [s, a1, a2, ...] --> s = a1 + a2 + ...
# labelblock() insert block type before block sid : 'type+sid'
def eqafficher(eqlist):
    for eq in eqlist:
        seq = labelblock(eq[0], lallblocks) + ' = '
        for i in range(1, len(eq)):
            seq += labelblock(eq[i], lallblocks)
            if i <> len(eq) - 1:
                seq += ' + '

        print seq


# Print a human readable SoP equation (with coeff)
# [s, a1, a2, ...][1, k1, k2, ...] --> s = k1.a1 + k2.a2 + ...
def exteqafficher(eqlist):
    for eq in eqlist:
        seq = labelblock(eq[0][0], lallblocks) + ' = '
        for i in range(1, len(eq[0])):
            seq += str(eq[1][i]) + '.' + labelblock(eq[0][i], lallblocks)
            if i <> len(eq[0]) - 1:
                seq += ' + '

        print seq


# End Printing functions



# ---------------------------------------------------------------
# PROGRAM START
# --------------------------------------------------------------

# Open the file for processing
# load an entire xml file to an element tree instance
tree = etree.parse(file)

# Getting Block and some parameters from file  ------------------- 
lallblocks = []
for block in tree.xpath("/ModelInformation/Model/System/Block"):
    blocktype = block.get("BlockType")  # recupere un attribut
    lblock = [block.get("SID"), blocktype, block.get("Name")]

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

    else:
        lblock[3] = '-'

    lallblocks.append(lblock)  # all blocks are here

print "\n- blocks : brute -"
print "[ SID , BlockType , Name , param ]"
print "----------------------------------"
afficher(lallblocks)


# Getting Line from file --------------------------------------
lalllines = []
for line in tree.xpath("/ModelInformation/Model/System/Line"):
    lline = []
    params = line.findall("P")
    for p in params:
        if p.get("Name") == "Src" or p.get("Name") == "Dst":
            lline.append(p.text)

    branchs = line.findall("Branch")
    if branchs:
        for b in branchs:
            for pi in b.findall("P"):
                if pi.get("Name") == "Dst":
                    lline.append(pi.text)

    lalllines.append(lline)  # all lines are here

print "\n\n- lines : brute -"
print "[ src , dest1, dest2, ...]"
print "----------------------------------"
afficher(lalllines)



# Get just the start and stop block SID for lines --------
print "\n\n- lines : with just start and stop block sid -"
print "[src, dst1, dst2, ...]"
print "----------------------------------------------"
lalllines2 = []
for ltemp in lalllines:
    simple_line = [getblocknum(sx) for sx in ltemp]
    lalllines2.append(simple_line)

afficher(lalllines2)



# Break branch in multiples lines --------------------------
print "\n\n- lines : with branch broken in multiples lines -"
print "[src, dst]"
print "-------------------------------------------------"
lalllines3 = []
for ltemp in lalllines2:
    for i in range(1, len(ltemp)):
        lalllines3.append([ltemp[0], ltemp[i]])  # all lines table are here : [ src , dst ]

afficher(lalllines3)



# Sort lines list by destination block -------------------
print "\n\n- destination sorted lines -"
print "[src, dst]"
print "-------------------------------"


def fkey(v):
    return v[1]


lalllines3.sort(key=fkey)
afficher(lalllines3)
# alllines3 : now contain lines sorted by destination block


# Group lines with the same destination together
# in order to know all blocks which feed a given block
tempo = '-'  # to store previous destination sid ( for comparison)
i = 0
newlist = []
lalllines4 = []

for l in lalllines3:
    if l[1] <> tempo:
        if i <> 0:
            lalllines4.append(newlist)  # append constructed newlist, except for the 1st time
        newlist = []  # reset list to each new destination : l[1]
        tempo = l[1]
        i += 1

    # append to a newlist each time we find new destination
    newlist.append(l)

lalllines4.append(newlist)  # append for the last one
# afficher(lalllines4)
# lalllines4 : contain list of lines grouped in a list by destination



# List all feeder blocks for each destination
# --> Make equation for each block
print "\n- blocks equations -"
print "[dst, src1, src2, ...]"
print "--------------------------"
lequations = []

for l in lalllines4:
    newlist = ['-']
    for branch in l:
        newlist[0] = branch[1]  # put destination block first
        newlist.append(branch[0])  # append input for each branch

    lequations.append(newlist)

afficher(lequations)
# lequations : contain a list of block with their inputs : [dst, src1, src2, ...]



# Remove temporary variable in output --------------
# ( the last adder give directly the output, no need for an inter var )
# ( Assume tha there is only one Outport )
# Get outpout equation, store it
for eq in lequations:
    if getblocktype(eq[0], lallblocks) == 'Outport':
        bout = eq[0]
        binter = eq[1]

# Remove it from equation list
for eq in lequations:
    if eq[0] == bout:
        lequations.remove(eq)

# Make temporary output as final outpout
for eq in lequations:
    if eq[0] == binter:
        eq[0] = bout


# Classify Equations in equation list --------------------------
# if it's a temporary result or a state equation or an output

# define a comparison function for the sort() method:
# Sum < Delay < Outport
def cmpeq(eq1, eq2):
    s1 = eq1[0]
    s2 = eq2[0]

    lorder = ['Sum', 'Delay', 'Outport']

    # Sum
    if getblocktype(s1, lallblocks) == lorder[0]:
        if getblocktype(s2, lallblocks) == lorder[0]:
            return 0
        else:
            return -1
    # Delay
    elif getblocktype(s1, lallblocks) == lorder[1]:
        if getblocktype(s2, lallblocks) == lorder[1]:
            return 0
        elif getblocktype(s2, lallblocks) == lorder[0]:
            return 1
        else:  # if getblocktype(s2,lallblocks) == lorder[2]:
            return -1
    # Outport
    elif getblocktype(s1, lallblocks) == lorder[2]:
        if getblocktype(s2, lallblocks) == lorder[2]:
            return 0
        else:
            return 1

    else:
        return 1


# Sort equation
lequations.sort(cmp=cmpeq)
# afficher(lequations)



# Extend Equations list to support coefficients -------------------

# each equation term has its coeff
ext_equations = [[list(eq), list(eq)] for eq in lequations]

# Set all coeff to 1, initially
for eq in ext_equations:
    for k in range(len(eq[1])):
        eq[1][k] = 1

    # Set gain for Gain block
    block = eq[0][0]
    param = getblockparam(block, lallblocks)

    if getblocktype(block, lallblocks) == 'Gain':
        if not (
                    param in ['*',
                              '-']):  # '*':gain not given in diagram (=1 by default) / '-':missing param for this bloc
            eq[1][1] = param

print "\n\n- with coeff block equations : internal representation -"
print "------------------------------------------------------"
afficher(ext_equations)
print "\n\n- with coeff block equations : human readable -"
print "-----------------------------------------------"
exteqafficher(ext_equations)


# Develop Gain block in equation terms -----------------------

# Function : get Gain and input for Gain block
# 	suppose that the given SID is a Gain and existing block
def getkparam(sid, exteq):
    for eq in exteq:
        if eq[0][0] == sid:
            return (eq[0][1], eq[1][1])  # (in , k)


# input,gain = getkparam('6',ext_equations) #test
# print input, gain

# Gain Development - 1 pass
# Can be called anytime you like;-)
def eqrefactorgain(exteq, blocklist):
    for eq in exteq:
        for i in range(1, len(eq[0])):
            if getblocktype(eq[0][i], blocklist) == 'Gain':
                input, gain = getkparam(eq[0][i], exteq)
                eq[0][i] = input
                eq[1][i] *= gain


eqrefactorgain(ext_equations, lallblocks)
eqrefactorgain(ext_equations, lallblocks)

print "\n\n- exp block equations : internal representation -"
print "-----------------------------------------"
afficher(ext_equations)
print "\n\n- exp block equations : human readable -"
print "-----------------------------------------"
exteqafficher(ext_equations)


# SIF Matrix generation ---------------------------------------------------

# Determine l, m, n, p
# 	l = intermediate result nbr
# 	m = input nbr ( =1 for this time ) 
# 	n = state nbr
# 	p = output nbr ( =1 for this time )
# count block and increment corresponding variable 
def getsifsize(blocklist):
    l = 0
    n = 0
    m = 0
    p = 0
    for b in blocklist:
        if b[1] == 'Sum':
            l += 1
        elif b[1] == 'Inport':
            m += 1
        elif b[1] == 'Delay':
            n += 1
        elif b[1] == 'Outport':
            p += 1

    l -= 1  # we work with the brute block list, we have remove one  intermediate res in output
    return (l, m, n, p)


l, m, n, p = getsifsize(lallblocks)
print "\n\n- SIF Matrix Generation -"
print "--------------------------"
print ' l=', l, ' m=', m, ' n=', n, ' p=', p


# Function : Buid a matrix with a given size
def mat(a, b):
    m = [[0 for i in range(b)] for j in range(a)]
    return m


# Build SIF matrix
J = mat(l, l)
K = mat(n, l)
L = mat(p, l)
M = mat(l, n)
P = mat(n, n)
R = mat(p, n)
N = mat(l, m)
Q = mat(n, m)
S = mat(p, m)


# Fill SIF matrix ---------------------------------------------------------------------
# build t , x , u , y vectors
# coeff placement in SIF matrix rely on it, so it is important 
t = []
x = []
u = []
y = []

for b in lallblocks:
    if getblocktype(b[0], lallblocks) == 'Sum':
        if b[0] <> binter:  # the removed temporary variable (in output)
            t.append(b[0])
    if getblocktype(b[0], lallblocks) == 'Delay':
        x.append(b[0])
    if getblocktype(b[0], lallblocks) == 'Inport':
        u.append(b[0])
    if getblocktype(b[0], lallblocks) == 'Outport':
        y.append(b[0])

print "\n\n- System Vectors -"
print "-------------------"
print 't=', t
print 'x=', x
print 'u=', u
print 'y=', y


# Build system vector with label ( just for printing)
tl = [getblocklabel(b, lallblocks) for b in t]
xl = [getblocklabel(b, lallblocks) for b in x]
ul = [getblocklabel(b, lallblocks) for b in u]
yl = [getblocklabel(b, lallblocks) for b in y]
print "--------------------"
print 't=', tl
print 'x=', xl
print 'u=', ul
print 'y=', yl


# Scan equations list to build J,K,L,M,N,P,Q,R,S matrix
# eq[0] : equations
# eq[1] : coefficients
for eq in ext_equations:
    if eq[0][0] in y:  # output eq
        for block, coeff in zip(eq[0][1:], eq[1][1:]):  # scan current equation inputs
            if block in t:
                L[y.index(eq[0][0])][t.index(block)] = int(coeff)
            elif block in x:
                R[y.index(eq[0][0])][x.index(block)] = int(coeff)
            elif block in u:
                S[y.index(eq[0][0])][u.index(block)] = int(coeff)


    elif eq[0][0] in x:  # state eq
        for block, coeff in zip(eq[0][1:], eq[1][1:]):  # scan current equation inputs
            if block in t:
                K[x.index(eq[0][0])][t.index(block)] = int(coeff)
            elif block in x:
                P[x.index(eq[0][0])][x.index(block)] = int(coeff)
            elif block in u:
                Q[x.index(eq[0][0])][u.index(block)] = int(coeff)

    elif eq[0][0] in t:  # intermediate eq
        for block, coeff in zip(eq[0][1:], eq[1][1:]):  # scan current equation inputs
            if block in t:
                J[t.index(eq[0][0])][t.index(block)] = 0 - int(coeff)
            elif block in x:
                M[t.index(eq[0][0])][x.index(block)] = int(coeff)
            elif block in u:
                N[t.index(eq[0][0])][u.index(block)] = int(coeff)

# additional assignement for J matrix
for i in range(l):
    for j in range(l):
        if i == j:
            J[i][j] = 1

# Display SIF Matrix
print "\n\nthe SIF Matrix corresponding to the initial Simulink Block Diagram:"
print "- J, K, L, M, N, P, Q, R, S -"
print "\nJ:", l, 'x', l
afficher(J)
print "\nK:", n, 'x', l
afficher(K)
print "\nL:", p, 'x', l
afficher(L)
print "\nM:", l, 'x', n
afficher(M)
print "\nP:", n, 'x', n
afficher(P)
print "\nR:", p, 'x', n
afficher(R)
print "\nN:", l, 'x', m
afficher(N)
print "\nQ:", n, 'x', m
afficher(Q)
print "\nS:", p, 'x', m
afficher(S)

# Saving Result to a file SIF.txt
