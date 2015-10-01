#! /usr/bin/env python
""" Script to implement toplogical search in Python.
	It will be used to make J matrix of SIF to be lower triangular.
	Note that J matrix hold the operation order in SIF."""

#from random import randint
import sys

def dmat(m,n):
	""" Construire une matrice diagonale m x n """
	matr = [[0 for i in range(n)] for j in range(m)]
	for i in range(n):
		for j in range(m):
			if i == j:
				matr[i][j] = 1
	return matr

def printmat(matr):
	""" Print a matrix"""
	for line in matr:
		print line


if __name__ == "__main__":
	
	######
	N = 5 #size of J matrix
	nodes = {}
	N_VISITED = 0
	J = dmat(5,5)

	#define J
	J[4][1] = -1
	J[0][4] = -1 # i depend de j
	J[3][4] = -1
	J[2][0] = -1
	printmat(J)
	#--------------------------
	#J[3][2] = -1 # i depend de j
	#J[1][3] = -1
	#J[1][0] = -1
	#J[4][1] = -1
	#printmat(J)

	# deduce adjacency matrix from J
	for i in range(N):
		for j in range(N):
			if J[i][j] == -1:
				J[i][j] = 1
			else :
				J[i][j] = 0
	print "\n"
	printmat(J)

	# list of all nodes with their state
	# list of forward nodes for each node:
	

	
	# function that build node - state - list of forward nodes
	def ladj(J, i):
		col = [line[i] for line in J]
		adj_list = [index for index, elt in enumerate(col) if elt == 1]
		return  adj_list 

	for i in range(N):
		nodes[i] = [i] 
		nodes[i].append(0) 
		nodes[i].append(ladj(J,i))		
		print "n"+str(i), nodes[i]

	#node / mark / forward nodes
	# unmarked : 0
	# tempo mark : 1
	# perm mark : 2

	#------ topo sort ------

	def visit( node ):
		global N_VISITED
		print node[0], node[1], node[2]
#		sys.exit()
		if node[1] == 1:
			print "\nerror - not a DAG !!!"
			sys.exit()
		if node[1] == 0: # not yet visited	
			node[1] = 1
			for m in node[2]:
				visit(nodes[m])
			node[1] = 2
			N_VISITED += 1 
			lorder.append(node[0])

	# order list
	lorder = []
	
	i=0
	while N_VISITED < N:
		if nodes[i][1] == 0:
			visit(nodes[i])
		i +=  1
		if i == N:
			i = 0
	
	print "\nordered nodes:"
	lorder.reverse()
	print lorder	

	# Make J lower triangular
	print "\n"
	printmat(J)	 

	Jn = dmat(N,N)
	# order line : equation order
	for i in range(N): 
		Jn[i] = J[lorder[i]]
	
	# order also column (for var vector consistency)
	J = dmat(N,N)
	for i in range(N): 
		for j in range(N): 
			J[i][j] = Jn[i][lorder[j]]
		
	print "\n"
	printmat(J)	 
