

def write_matrix_hex(f_handle, M, delim):
	n,m = M.shape
	for i in range (0,n):
		for j in range (0,m):
			f_handle.write(M[i,j].hex() + delim)
		f_handle.write('\n')






