#coding=UTF8

from func_aux.get_data import get_data
from Structures import *
import numpy as np

list_dTF = get_data("TF", "signal", "butter", is_refresh=False)

TFobj = list_dTF[2]

#cur_gamma = np.matrix(np.zeros((TFobj.num.shape[0], TFobj.num.shape[1] - 1)))

cur_gamma = np.multiply(2, np.ones((TFobj.num.shape[0], TFobj.num.shape[1] - 1)))

#cur_delta = np.ones(cur_gamma.shape)

cur_delta = np.multiply(2, np.ones(cur_gamma.shape))

myRhoDFIIt = RhoDFIIt(TFobj.num, TFobj.den, gamma=cur_gamma, delta=cur_delta, isGammaExact=True, isDeltaExact=True, opt = '1')
#OK
#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH'], optMethod = 'basinHoping')

# problem to calculate MsensH with starting parameters from MsensPole
#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'basinHoping', restartScenario='all')

myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH'], optMethod = 'differentialEvolution')

myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'differentialEvolution', restartScenario=['MsensH', 'MsensPole'])

myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'basinHoping', restartScenario=['MsensH', 'MsensPole'])

# problem to get MsensH with starting parameters from MsensPole
myOptimizedRhoDFIIt_all = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole', 'RNG'], optMethod = 'basinHoping', restartScenario=['all'])

myOptimizedRhoDFIIt_all = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole', 'RNG'], optMethod = 'basinHoping', restartScenario=['MsensH', 'RNG'])