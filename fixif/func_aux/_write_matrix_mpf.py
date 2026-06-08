import mpmath as mp
import numpy as np

def write_matrix_mpf(f_handle, M, delim):
	n = M.rows
	m = M.cols
	for i in range (0,n):
		for j in range (0,m):
			f_handle.write(str(M[i,j]) + delim)
		f_handle.write('\n')