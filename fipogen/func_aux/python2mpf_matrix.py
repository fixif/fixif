
import mpmath as mp
def python2mpf_matrix(M):
	n,m = M.shape
	Mmp = mp.zeros(n, m)

	for i in range(0,n):
		for j in range(0,m):
			Mmp[i,j] = mp.mpf(str(M[i,j]))

	return Mmp
