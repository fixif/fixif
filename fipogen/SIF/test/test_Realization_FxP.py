_author__ = "Anastasia Volkova"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "CECILL-C"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import pytest

from fipogen.LTI import dSS, Butter
from fipogen.SIF import Realization, Realization_FxP
from numpy import matrix as mat, zeros, eye, empty, float64
import numpy as np
from numpy import all
import time

from fipogen.func_aux import write_matrix_hex

from fipogen.Structures import LWDF, DFII, State_Space

from fipogen.Structures import iterAllRealizations, iterAllRealizationsRandomFilter
from fipogen.LTI import Filter, iter_random_Filter, iter_random_dSS, random_Filter, random_dSS
from scipy.weave import inline

# from func_aux.get_data import get_data
# from func_aux.MtlbHelper import MtlbHelper



from numpy.random import seed, rand, randint, shuffle
from numpy.testing import assert_allclose


def test_computeMSBSIF():
	nu = 1
	ny = 1
	nx = 5
	F = random_Filter(nx, nu, ny)
	SS = State_Space.makeRealization(F)

	u_bar = np.bmat([np.ones([1, nu])])
	l_y_out = -16
	msb_u = np.bmat([np.zeros([1, SS.q])])
	lsb_u = -16 * np.bmat([np.ones([1, SS.q])])

	msb = SS.compute_MSB_allvar(u_bar)
	lsb = SS.compute_LSB_allvar(l_y_out)

	lsb_t = [lsb[0, i] for i in range(0, SS.l)]
	lsb_x = [lsb[0, i] for i in range(SS.l, SS.l + SS.n)]
	lsb_y = [lsb[0, i] for i in range(SS.l + SS.n, SS.l + SS.n + SS.p)]

	msb_ext = SS.compute_MSB_allvar_extended(u_bar, lsb_t, lsb_x, lsb_y)
	if ((msb != msb_ext).any()):
		print 'MSB computed with taking into account the propagation of the error due to the format (msb, lsb) differs from the initial format. Changing MSBs.\n'
		print 'new MSBs:'
		msb = msb_ext
		print msb

	msb_t = [msb[0, i] for i in range(0, SS.l)]
	msb_x = [msb[0, i] for i in range(SS.l, SS.l + SS.n)]
	msb_y = [msb[0, i] for i in range(SS.l + SS.n, SS.l + SS.n + SS.p)]

	fileID = 'SIF-' + time.strftime("%d%m%Y-%H%M%S")
	filename = fileID + '.txt'
	with open(filename, 'a') as f_handle:
		f_handle.write('%d\n%d\n%d\n%d\n' % (SS.q, SS.l, SS.n, SS.p))
		for i in range(0, SS.q):
			f_handle.write('%d %d\n' % (msb_u[i], lsb_u[i]))
		for i in range(0, SS.l):
			f_handle.write('%d %d\n' % (msb_t[i], lsb_t[i]))
		for i in range(0, SS.n):
			f_handle.write('%d %d\n' % (msb_x[i], lsb_x[i]))
		for i in range(0, SS.p):
			f_handle.write('%d %d\n' % (msb_y[i], lsb_y[i]))

		write_matrix_hex(f_handle, SS.Z, ' ')

	f_handle.close()

	print 'Filter: \n'
	print SS
	print 'y_out was initially set to: %d\n' %l_y_out
	print 'LSBs:\n'
	print lsb
	print 'MSBs:\n'
	print msb

	nSimulations = 100;
	u = np.random.rand(1,nSimulations)
	y_simulated = SS.simulate(u)

	filename = fileID + 'simulation' + '.txt'
	with open(filename, 'a') as f_handle:
		f_handle.write('%d' % nSimulations)
		write_matrix_hex(f_handle, u, ' ')
		write_matrix_hex(f_handle, y_simulated, ' ')
	f_handle.close()


test_computeMSBSIF()


