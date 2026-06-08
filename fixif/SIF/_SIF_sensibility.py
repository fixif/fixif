__author__ = "Thibault Hilaire"
__copyright__ = "Copyright 2015, FiXiF Project, LIP6"
__credits__ = ["Thibault Hilaire"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"


from fixif.LTI import dSS
from numpy import zeros, matrix as mat, multiply, conj, transpose, real, diag
from numpy.linalg import norm, eig, inv


def _w_norm_prod(G, H, W):
	r"""Compute the weighting $L_2$-norm of the system composed by $G \cd H = Vec(G).(Vec(H ^\top)) ^ \top$
	Each system is weighted by the weighting matrix W.
	$G$ and $H$ are dSS object (State-Space systems)

	Returns:
		- M: weighted norm
		- MX: sensibility matrix of $G \cd 	H$
	Parameters :
		- systems G and H
		- W: weighting matrix
	"""

	#TODO: use same method as in @FWR/private/w_prod_norm_SISO.m (FWRToolbox) for SISO systems
	#(see Lyapunov.pdf)

	MX = zeros(W.shape)

	for i in range(0, W.shape[0]):
		for j in range(0, W.shape[1]):
			if not (W[i, j] == 0):
				MX[i, j] = (G[:, i] * H[j, :]).H2norm()

	MX = multiply(MX, W)

	N = norm(MX, 'fro')
	N = N * N

	return N, MX



def deigdZ(A, M1, M2, shapeZ, moduli=True):
	"""
	Compute $M_1^\top \dd{\lambda}{A} M_2^\top$.
	Returns:
	- dlambda_dZ: the pole sensitivity matrix
	- dlk_dZ: pole sensitivity matrices for each pole
	Parameters:
	- A: matrix from whom the eigenvalues are taken
	- M1,M2: such that $\dd{\lambda}{Z} = M1^\top \dd{\lambda}{A} M2^\top$
	- moduli : True (default value) : compute $\dd{\abs{\lambda}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
            : False: compute $\dd{\lambda}{Z}$ (without the moduli)
	"""

	mylambda, Mx = eig(A)

	Mx = mat(Mx)

	My = inv(Mx).transpose()

	# numpy gives conjugate solutions (vs. matlab)
	My = mat(conj(My))

	# order of eigenvalues is not guaranteed to be the same in matlab and numpy so
	# that discrepancies appear in resulting matrixes.
	# the ideal check of compliance would check if there is the same value at some, or at another position in the matrix
	# the check should be careful about repeating coefficients (count them etc.)
	mylambda = mat(conj(mylambda))

	# sensitivity matrix
	dlk_dZ = zeros((shapeZ[0], shapeZ[1], mylambda.shape[1]))  #  numpy does not know about hypermatrixes

	for k in range(0, mylambda.shape[1]):
		if moduli == 1:
			dlk_dZ[:, :, k] = transpose(M1) * (1 / abs(mylambda[0, k]) * real(
				conj(mylambda[0, k] * conj(My[:, k]) * transpose(Mx[:, k])))) * transpose(M2)
		else:
			dlk_dZ[:, :, k] = transpose(M1) * (conj(My[:, k]) * transpose(Mx[:, k])) * transpose(M2)

	# dlambda_dZ

	dlambda_dZ = zeros(shapeZ)

	for i in range(0, shapeZ[0]):
		for j in range(0, shapeZ[1]):

			if len(dlk_dZ[i, j, :].shape) == 1:
				norm_target = mat(diag(dlk_dZ[i, j, :]))  # maybe there's a missing func or bug in numpy here, cannot calculate froebenius norm on a 1D vector
			else:
				norm_target = dlk_dZ[i, j, :]

			dlambda_dZ[i, j] = norm(norm_target, 'fro')

	return dlambda_dZ, dlk_dZ




class SIF_sensibility:
	"""
	Mixin class (see https://groups.google.com/forum/?hl=en#!topic/comp.lang.python/goLBrqcozNY)
	Allow to embedd the following methods in the SIF class
	the SIF class will inherit from SIF_FxP class

	This class adds methods to compute the sensibility (wrt Z)
	"""

	def dTFsensitivity(self):
		"""Compute the transfer function sensitivity measure and matrix
		Returns
			- M: tf sensitivity measure
			- MX: tf sensitivity matrix
		"""
		return _w_norm_prod(dSS(self.AZ, self._M1, self.CZ, self._M2), dSS(self.AZ, self.BZ, self._N1, self._N2), self.dZ)
		#TODO: check if the object is a controller, and use M1bar, M2bar, N1bar and N2bar instead of M1, M2, N1 and N2


	def poleSensitivity(self, moduli=True):
		"""Compute the pole sensitivity measure and matrices
		Paramters:
			- moduli: (boolean) sensitivity of the poles (False) or of the moduli of the poles (True)
		Returns:
			- M: pole sensitivity measure
			- MX: pole sensitivity matrix
			- MXk: pole sensitivity matrices for each pole
		"""

		dlambda_dZ, dlk_dZ = deigdZ(self.AZ, self._M1, self._N1, self.Z.shape, moduli)

		#TODO: check if the object is a controller, and then
		# Abar, Bbar, Cbar, Dbar, M1bar, M2bar, N1bar, N2bar = calc_plantSIF(R, plant)
		# dlambda_dZ, dlk_dZ = deigdZ(R.Abar, R.M1bar, R.N1bar, R.Z.shape, moduli)

		M = norm(multiply(dlambda_dZ, self.dZ), 'fro')
		M = M * M

		return M, dlambda_dZ, dlk_dZ


