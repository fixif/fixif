# coding: utf8

"""
This file contains tests for the SIF functions & class
"""

_author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof", "Benoit Lopez", "Anastasia Lozanova"]

__license__ = "GPL v3"
__version__ = "0.4"
__maintainer__ = "Thibault Hilaire"
__email__ = "thibault.hilaire@lip6.fr"
__status__ = "Beta"

import pytest
import numpy

from fixif.SIF import SIF
from numpy import matrix as mat
from fixif.Structures import iterAllRealizations
from fixif.LTI import Filter, iter_random_dTF, iter_random_dSS


#from func_aux.get_data import get_data
#from func_aux.MtlbHelper import MtlbHelper

from fixif.func_aux import mpf_to_numpy


from numpy.random import seed, rand, randint, shuffle
from numpy.testing import assert_allclose



@pytest.mark.parametrize( "S", iter_random_dSS(25, n=(5, 15), p=(1,5), q=(1,5) ))
def test_dSSexact( S ):

	l = randint(1, 10)
	myJtoS = (numpy.eye((l)), numpy.zeros((S.n, l)), numpy.zeros((S.p, l)), rand(l, S.n), rand(l, S.q), S.A, S.B, S.C, S.D)

	mySIF = SIF(myJtoS)

	SS = mySIF.dSS

	Sexact = mySIF.to_dSSexact()

	assert_allclose(SS.A, mpf_to_numpy(Sexact.A))
	assert_allclose(SS.B, mpf_to_numpy(Sexact.B))
	assert_allclose(SS.C, mpf_to_numpy(Sexact.C))
	assert_allclose(SS.D, mpf_to_numpy(Sexact.D))




def test_construction():

	for i in range( 50):
		l = randint( 0, 15)
		n = randint( 5, 20)
		p = randint( 1, 5)
		q = randint( 1, 5)

		# (n,n)
		myP = mat(rand(n,n))
		# (l,l)
		myJ = mat(rand(l,l))
		# (n,l)
		myK = mat(rand(n,l))
		# (p,l)
		myL = mat(rand(p,l))
		# (l,n)
		myM = mat(rand(l,n))
		# (l,q)
		myN = mat(rand(l,q))
		# (n,q)
		myQ = mat(rand(n,q))
		# (p,n)
		myR = mat(rand(p,n))
		# (p,q)
		myS = mat(rand(p,q))

		myJtoS = [myJ, myK, myL, myM, myN, myP, myQ, myR, myS]

		# test correct obj creation
		mySIF = SIF(myJtoS)

		#testing getters/properties
		assert_allclose( mySIF.J, myJ)
		assert_allclose( mySIF.K, myK)
		assert_allclose( mySIF.L, myL)
		assert_allclose( mySIF.M, myM)
		assert_allclose( mySIF.N, myN)
		assert_allclose(mySIF.P, myP)
		assert_allclose( mySIF.Q, myQ)
		assert_allclose( mySIF.R, myR)
		assert_allclose( mySIF.S, myS)

		assert mySIF.n == n
		assert mySIF.l == l
		assert mySIF.p == p
		assert mySIF.q == q



		# test the construction with not consistent matrices
		# when the 4 sizes are all different
		if len( set( (l,n,p,q) ) ) == 4:
			shuffle(myJtoS)
			with pytest.raises(ValueError):
				t = SIF(myJtoS)





		# def test_allSens(self):
	#
	# 	def _build_dict_ABCD(dSSobj_target, dSSobj_plant):
	#
	# 		dict_ABCD['A'] = dSSobj_target.A
	# 		dict_ABCD['B'] = dSSobj_target.B
	# 		dict_ABCD['C'] = dSSobj_target.C
	# 		dict_ABCD['D'] = dSSobj_target.D
	#
	# 		# plant
	# 		if dSSobj_plant is not None:
	# 			dict_ABCD['Ap'] = dSSobj_plant.A
	# 			dict_ABCD['Bp'] = dSSobj_plant.B
	# 			dict_ABCD['Cp'] = dSSobj_plant.C
	# 			dict_ABCD['Dp'] = dSSobj_plant.D
	#
	# 		return dict_ABCD
	#
	# 	n_obj = len(self.list_dSS)
	#
	# 	for i_obj, dSSobj in enumerate(self.list_dSS):
	#
	# 		print ("obj {0: >3d} / {1} ****************************************************".format(i_obj, n_obj), end="")
	#
	# 		fipVarz = {}
	# 		dict_ABCD = {}
	#
	# 		# open loop
	# 		varz = ["OH_M", "OH_MZ", "OP_M", "OP_dlambda_dZ", "OP_dlk_dZ", "ORNG_G", "ORNG_dZ"]
	#
	# 		mtlb_cmd  = 'R = SS2FWR(A,B,C,D); \n'
	#
	# 		mtlb_cmd += "[OH_M, OH_MZ] = MsensH(R); \n"
	# 		mtlb_cmd += "[OP_M, OP_dlambda_dZ, OP_dlk_dZ] = MsensPole(R); \n"
	# 		mtlb_cmd += "[ORNG_G, ORNG_dZ] = RNG(R); \n" # open-loop case
	#
	# 		SIFobj = State_Space(dSSobj.A,dSSobj.B,dSSobj.C,dSSobj.D)
	#
	# 		l0, m0, n0, p0 = SIFobj.size
	#
	# 		# find random_dSS satisfying size requirements
	#
	# 		for dSSobj2 in self.list_dSS:
	#
	# 			n1,p1,q1 = dSSobj2.size
	#
	# 			if not(p1 - p0 <= 0) and not(q1 - m0 <= 0) : # add test not equal to zero
	# 				dSSobj_plant = dSSobj2
	#
	# 				# FUCKING HACK : if some properties are already calculated this is all shitty
	# 				# see if we need to add special setters to dSS objject redefining properties and checking that D size is coherent
	# 				# with what already exists.
	# 				dSSobj_plant._D = zeros(dSSobj2.D.shape)
	#
	# 				is_plant_found = True
	# 				# closed loop
	# 				varz += ["CH_M", "CH_MZ", "CP_M", "CP_dlambdabar_dZ", "CP_dlbk_dZ", "CS_M", "CRNG_G", "CRNG_dZ", "CRNG_M1M2Wobar"]
	# 				#closed loop
	# 				mtlb_cmd += "ss_plant = ss(Ap, Bp, Cp, Dp); \n"
	# 				# closed-loop
	# 				mtlb_cmd += "[CH_M, CH_MZ] = MsensH_cl(R, ss_plant); \n"
	# 				mtlb_cmd += "[CP_M, CP_dlambdabar_dZ, CP_dlbk_dZ] = MsensPole_cl(R, ss_plant); \n"
	# 				mtlb_cmd += "CS_M = Mstability(R, ss_plant); \n"
	# 				mtlb_cmd += "[CRNG_G, CRNG_dZ, CRNG_M1M2Wobar] = RNG_cl(R, ss_plant); \n"
	# 				break
	#
	# 		else:
	# 			is_plant_found = False
	# 			dSSobj_plant = None
	#
	# 		dict_ABCD = _build_dict_ABCD(dSSobj, dSSobj_plant)
	#
	# 		self.engMtlb.setVar(dict_ABCD.keys(), dict_ABCD) # A,B,C,D, (if plant : Ap,Bp,Cp,Dp)
	#
	# 		#             print('SIZE OF controller')
	# 		#             print('(l, m2, n, p2)')
	# 		#             print(SIFobj.size)
	# 		#             print('SIZE of plant')
	# 		#             print('(np, p, m)')
	# 		#             print(dSSobj_plant.size)
	#
	# 		#try:
	# 		#    self.engMtlb.eng.eval(mtlb_cmd, nargout = 0)
	# 		#except matlab.engine.MatlabExecutionError:
	# 		#    print('shit in the fan')
	#
	# 		# open loop
	#
	# 		tmp_var = SIFobj.MsensH()
	#
	# 		fipVarz[varz[0]] = tmp_var[0]
	# 		fipVarz[varz[1]] = tmp_var[1]
	#
	# 		tmp_var = SIFobj.MsensPole()
	# 		fipVarz[varz[2]] = tmp_var[0]
	# 		fipVarz[varz[3]] = tmp_var[1]
	# 		fipVarz[varz[4]] = tmp_var[2]
	#
	# 		tmp_var = SIFobj.RNG()
	# 		fipVarz[varz[5]] = tmp_var[0]
	# 		fipVarz[varz[6]] = tmp_var[1]
	#
	# 		# closed-loop
	# 		if is_plant_found:
	#
	# 			tmp_var = SIFobj.MsensH(plant=dSSobj_plant)
	# 			fipVarz[varz[7]] = tmp_var[0]
	# 			fipVarz[varz[8]] = tmp_var[1]
	#
	# 			tmp_var = SIFobj.MsensPole(plant=dSSobj_plant)
	# 			fipVarz[varz[9]] = tmp_var[0]
	# 			fipVarz[varz[10]] = tmp_var[1]
	# 			fipVarz[varz[11]] = tmp_var[2]
	#
	# 			tmp_var = SIFobj.Mstability(plant=dSSobj_plant)
	# 			fipVarz[varz[12]] = tmp_var
	#
	# 			tmp_var = SIFobj.RNG(plant=dSSobj_plant)
	# 			fipVarz[varz[13]] = tmp_var[0]
	# 			fipVarz[varz[14]] = tmp_var[1]
	# 			fipVarz[varz[15]] = tmp_var[2]
	#
	# 			print('')
	#
	# 		else:
	# 			print(' : No suitable plant found, skipping tests involving plant')
	#
	# 		err_num = self.engMtlb.compare(mtlb_cmd, varz, fipVarz, decim = self.ndigit)
	#
	# 		self.engMtlb.cleanenv()
	#
	# 		if err_num == 0:
	# 			print('SUCCESS')

	# def test_UYW_transform(self):
	#
	# 	# generate random matrixes
	#
	# 	# generate random UYW matrixes from start matrixes
	#
	# 	n_obj = len(self.list_dSS)
	#
	# 	names_check_W  = ['Wc', 'Wo']
	# 	names_check_OL = ['MsensH(OL)[0]', 'MsensH(OL)[1]', 'MsensPole(OL)[0]', 'MsensPole(OL)[1]', 'MsensPole(OL)[2]', 'RNG(OL)[0]', 'RNG(OL)[1]']
	# 	names_check_CL = ['MsensH(CL)[0]', 'MsensH(CL)[1]', 'MsensPole(CL)[0]', 'MsensPole(CL)[1]', 'MsensPole(CL)[2]', 'RNG(CL)[0]', 'RNG(CL)[1]', 'RNG(CL)[2]', 'Mstability']
	#
	# 	names_all = names_check_W + names_check_OL + names_check_CL
	#
	# 	err_num = [0]*len(names_all)
	#
	# 	# number of dSS with associated plant
	# 	num_dSSplant = 0
	#
	# 	for i_obj, dSSobj in enumerate(self.list_dSS):
	#
	# 		print ("obj {0: >3d} / {1} ****************************************************".format(i_obj, n_obj), end="\n")
	#
	# 		SIFobj = State_Space(dSSobj.A,dSSobj.B,dSSobj.C,dSSobj.D)
	#
	# 		l0, m0, n0, p0 = SIFobj.size
	#
	#
	#
	# 		# find random_dSS satisfying size requirements
	#
	# 		for dSSobj2 in self.list_dSS:
	#
	# 			n1,p1,q1 = dSSobj2.size
	#
	# 			if not(p1 - p0 <= 0) and not(q1 - m0 <= 0) : # add test not equal to zero
	#
	# 				SIFobj_plant = dSSobj2
	# 				SIFobj_plant._D = zeros(dSSobj2.D.shape)
	#
	# 				# FUCKING HACK : if some properties are already calculated this is all shitty
	# 				# see if we need to add special setters to dSS objject redefining properties and checking that D size is coherent
	# 				# with what already exists.
	# 				SIFobj.plant = SIFobj_plant
	#
	# 				is_plant_found = True
	# 				num_dSSplant += 1
	# 				# closed loop
	# 				break
	#
	# 		else:
	#
	# 			is_plant_found = False
	#
	# 		if is_plant_found:
	# 			measureTypes = ['OL', 'CL']
	# 			print('plant found')
	# 		else:
	# 			measureTypes = ['OL']
	#
	# 		# generate UYW random matrixes
	# 		# replace existing ones that have been set using _set_default_UYW()
	#
	# 		# WARNING FIX SEED TO GET REPRODUCIBLE RESULTS IN DIFFERENT RUNS
	# 		seed(25499)
	#
	# 		SIFobj.U = rand(*SIFobj.U.shape)
	# 		SIFobj.Y = rand(*SIFobj.Y.shape)
	# 		SIFobj.W = rand(*SIFobj.W.shape)
	#
	# 		#SIFobj.U = 1.05*SIFobj.U
	#
	# 		SIFobj.Wo
	# 		SIFobj.Wc
	#
	# 		for myMeasure in measureTypes:
	#
	# 			SIFobj.MsensH(measureType=myMeasure)
	# 			SIFobj.MsensPole(measureType=myMeasure)
	# 			SIFobj.RNG(measureType=myMeasure)
	#
	# 			if (myMeasure == 'CL'):
	# 				SIFobj.Mstability()
	#
	# 		# manually trigger UYW transform
	# 		SIFobj._translate_realization()
	#
	# 		# create list for values after translation
	# 		vals_translated = []
	#
	# 		vals_translated.append(SIFobj.Wc)
	# 		vals_translated.append(SIFobj.Wo)
	#
	# 		for myMeasure in measureTypes:
	# 			# only possible in python3
	# 			#vals_translated.extend(*SIFobj.MsensH(measureType=myMeasure), *SIFobj.MsensPole(measureType=myMeasure), *SIFobj.RNG(measureType=myMeasure))
	#
	# 			vals_translated.extend(SIFobj.MsensH(measureType=myMeasure))
	# 			vals_translated.extend(SIFobj.MsensPole(measureType=myMeasure))
	# 			vals_translated.extend(SIFobj.RNG(measureType=myMeasure))
	#
	# 			if (myMeasure == 'CL'):
	# 				vals_translated.append(SIFobj.Mstability())
	#
	# 		# bruteforce calculation of data
	#
	# 		SIFobj._Wc = None
	# 		SIFobj._Wo = None
	#
	# 		SIFobj.Wc
	# 		SIFobj.Wo
	#
	# 		# trigger manual recalculation of measures, and use bruteforce calculation
	# 		for myMeasure in measureTypes:
	#
	# 			SIFobj._MsensH[myMeasure] = None
	# 			SIFobj._MsensPole[myMeasure] = None
	# 			SIFobj._RNG[myMeasure] = None
	#
	# 			SIFobj.MsensH(measureType=myMeasure)
	# 			SIFobj.MsensPole(measureType=myMeasure)
	# 			SIFobj.RNG(measureType=myMeasure)
	#
	# 			if (myMeasure == 'CL'):
	# 				SIFobj._Mstability = None
	# 				SIFobj.Mstability()
	#
	# 		# store bruteforce values
	# 		vals_bruteforce = []
	#
	# 		vals_bruteforce.append(SIFobj.Wc)
	# 		vals_bruteforce.append(SIFobj.Wo)
	#
	# 		for myMeasure in measureTypes:
	#
	# 			# python3 only
	# 			#vals_bruteforce.extend(*SIFobj.MsensH(measureType=myMeasure), *SIFobj.MsensPole(measureType=myMeasure), *SIFobj.RNG(measureType=myMeasure))
	#
	# 			vals_bruteforce.extend(SIFobj.MsensH(measureType=myMeasure))
	# 			vals_bruteforce.extend(SIFobj.MsensPole(measureType=myMeasure))
	# 			vals_bruteforce.extend(SIFobj.RNG(measureType=myMeasure))
	#
	# 			if (myMeasure == 'CL'):
	# 				vals_bruteforce.append(SIFobj.Mstability())
	#
	#
	# 		if is_plant_found:
	# 			names_check = names_check_W + names_check_OL + names_check_CL
	# 		else:
	# 			names_check = names_check_W + names_check_OL
	#
	# 		error_count = 0
	# 		err_str = ''
	#
	# 		for ind, item in enumerate(zip(vals_translated, vals_bruteforce)):
	#
	# 			try:
	# 				npt.assert_almost_equal(item[0], item[1], decimal=self.ndigit)
	# 			except AssertionError as e:
	# 				#print(e)
	# 				error_count += 1
	# 				err_str += names_check[ind] + '\n'
	# 				err_num[ind] += 1
	#
	# 				# ad-hoc debug
	# 				if names_check[ind] == 'Mstability':
	#
	# 					print('Mstability translated : {}'.format(item[0]))
	# 					print('Mstability bruteforce : {}'.format(item[1]))
	#
	# 		if error_count == 0:
	# 			print('SUCCESS')
	# 		else:
	# 			print('{} not equal in transformed and direct calculation with {} digits'.format(err_str, self.ndigit))
	#
	# 			# erase attribute and ask for property = brute force calculation (no transformation)
	#
	# 	num_cases = [len(self.list_dSS)]*len(names_check_W + names_check_OL) + [num_dSSplant]*len(names_check_CL)
	#
	# 	print('Total number of errors with {}-digit precision :'.format(self.ndigit))
	# 	for ind, item in enumerate(names_all):
	# 		print('{0:20} : {1:4} / {2:4}'.format(item, err_num[ind], num_cases[ind]))
	#
	#
	# 		if item == "RNG(CL)[1]":
	# 			print('matlab : value not changed by UYW transform')
	# 		elif item == "RNG(CL)[2]":
	# 			print('matlab : value not changed by UYW transform')
	# 		elif item == 'Mstability':
	# 			print('depends on RNG(CL)[2]')
	# 		elif item in {'MsensH(OL)[0]','MsensH(OL)[1]','MsensH(CL)[0]','MsensH(CL)[1]'}:
	# 			print('no transform ,calculated with bruteforce method')


#     def test_optimizeForm(self):
#         
#         #test optimizing from rhoDFIIt (no UYW transform)
#         
#         is_test_dSS = False
#         is_test_TF = True
#         
#         crit_list_OL = [['MsensH'], ['MSensPole'], ['RNG'], ['MsensH', 'MsensPole'], ['MsensH', 'RNG'], ['MsensPole', 'RNG'],['MsensH', 'MsensPole', 'RNG']]
#         
#         if is_test_dSS :
#         
#             #test optimizing from State_Space
#             for dSSObj in self.list_dSS[0:1]:
#               
#                 tmp_State_Space = State_Space(dSSObj.A, dSSObj.B, dSSObj.C, dSSObj.D)
# 
#                 for loc_crit_list in crit_list_OL:
# 
#                     print(loc_crit_list)
#     
#                     tmp_State_Space.optimizeForm(loc_crit_list, startVals = 'default', optMethod = 'basinHoping')
#         
#         if is_test_TF:
#             
#             for TFobj in self.list_dTF[0:1]:
#                 
#                 cur_gamma = mat(zeros((TFobj.num.shape[0], TFobj.num.shape[1] - 1)))
#                 cur_delta = ones(cur_gamma.shape)
#                 
#                 tmp_rhoDFIIt = RhoDFIIt(TFobj.num, TFobj.den, gamma=cur_gamma, delta=cur_delta, isGammaExact=True, isDeltaExact=True, opt = '1')        
#                 
#                 for loc_crit_list in crit_list_OL:
# 
#                     print(loc_crit_list)
#     
#                     tmp_rhoDFIIt.optimizeForm(    )


