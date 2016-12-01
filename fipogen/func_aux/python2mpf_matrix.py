
import mpmath as mp
import numpy
def python2mpf_matrix(M):

	if not isinstance(M, numpy.matrix):
		raise ValueError('Expected a numpy matrix, instead have %s' %type(M))


	n, m = M.shape
	Mmp = mp.zeros(n, m)
	for i in range(0, n):
		for j in range(0, m):
			Mmp[i, j] = mp.mpf(repr(numpy.float_(M[i, j])))


	return Mmp
