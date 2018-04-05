cimport numpy as np
import numpy as np
import cython

# declare interface to the C code
cdef extern:
	void runCdouble(double* u, double* y, int N)



@cython.boundscheck(False)
@cython.wraparound(False)
def simCdouble( np.ndarray[np.double_t, ndim=2, mode="c"] input):
	"""
	Simulate the system using the `runCdouble` C-function (that use the `implementCdouble` function)
	Parameters
	----------
	- input: vector Nxq (N is the number of sample, q the number of inputs)

	Returns a Nxp vector (p the number of outputs)
	-------

	"""
	N = input.shape[0]
	print("N=%d"%N)
	assert(input.shape[1]==1)

	if not input.flags.c_contiguous:
		raise ValueError("Only C-contiguous arrays are supported!")

	cdef np.ndarray[np.double_t, ndim=2, mode="c"] output = np.ascontiguousarray( np.zeros( (N,4), dtype=np.float64) )

	runCdouble( &input[0,0], &output[0,0], N)

	return output