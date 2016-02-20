

def DirectFormII( num, den):
	
	# normalisation des coefs
	a0 = den[0]
	num = [ c/a0 for c in num ]
	den = [ c/a0 for c in den ]
	n = max(len(num),len(den))
	
	J = matrix(1,1,1)
	K = block_matrix(2,1,[1,zero_matrix(n-2,1)],subdivide=False)
	L = matrix(1,1,num[0])
	M = matrix([ -c for c in den[1:] ])
	N = matrix(1,1,1)
	P = block_matrix([0, zero_matrix(1,1), identity_matrix(n-2), 0],subdivide=False)
	Q = zero_matrix(n-1,1)
	R = matrix(1,n-1,den[1:])
	S = matrix(1,1,0)
	
	return pyFWR( J, K, L, M, N, P, Q, R, S, name='Direct Form II' )