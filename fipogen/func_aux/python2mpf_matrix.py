
import mpmath as mp
import numpy as np
def python2mpf_matrix(M):
	Mmp = mp.zeros(1,1)
	if(isinstance(M, np.matrix)):
		n,m = M.shape
		Mmp = mp.zeros(n, m)

		for i in range(0,n):
			for j in range(0,m):
				Mmp[i,j] = mp.mpf(str(M[i,j]))

	#else I need to raise an error

	return Mmp
