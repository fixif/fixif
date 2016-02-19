#coding=UTF8

from func_aux.get_data import get_data
from Structures import *
import numpy as np

list_dTF = get_data("TF", "signal", "butter", is_refresh=False)

# Tests work great with this one
#TFobj = list_dTF[2]

# this one is giving us a lot of problems, seems noot optimizable
#TFobj = list_dTF[20]

TFobj = list_dTF[30]


#cur_gamma = np.matrix(np.zeros((TFobj.num.shape[0], TFobj.num.shape[1] - 1)))

cur_gamma = np.multiply(2, np.ones((TFobj.num.shape[0], TFobj.num.shape[1] - 1)))

#cur_delta = np.ones(cur_gamma.shape)

cur_delta = np.multiply(2, np.ones(cur_gamma.shape))

myRhoDFIIt = RhoDFIIt(TFobj.num, TFobj.den, gamma=cur_gamma, delta=cur_delta, isGammaExact=True, isDeltaExact=True, opt = '1')

list_dSS = get_data("SS", "random", is_refresh=False)

# tests work great with this one
#SSobj = list_dSS[2]
# works great
#SSobj = list_dSS[20]

SSobj = list_dSS[30]


myState_Space = State_Space(SSobj.A, SSobj.B, SSobj.C, SSobj.D)

# tests for State_Space (UYW transform)

# For this case MsensH = 0 so we cannot use the MsensH criterion (div by 0)
# Otherwise optimization vs. MsensPole works
#my_opt_StSp = myState_Space.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'basinHoping', restartScenario=['MsensH'])

#print('Optimized UYW Matrixes')
#print(my_opt_StSp[0].U)
#print(my_opt_StSp[0].Y)
#print(my_opt_StSp[0].W)

my_opt_StSp = myState_Space.optimizeForm(['MsensPole'], optMethod = 'basinHoping', startVals = 'random')
# the basinHoping explores the boundaries of the values domain, so it gives a singular U matrix at first step using random values.
# to avoid this error we should add an epsilon to the boundaries if random is used so that optim step 1 does not do shit


print('Optimized UYW Matrixes')
print(my_opt_StSp.U)
print(my_opt_StSp.Y)
print(my_opt_StSp.W)

#OK
#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH'], optMethod = 'basinHoping')

# problem to calculate MsensH with starting parameters from MsensPole
#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'basinHoping', restartScenario='all')

# mgrid or lgrid seems to be too memory-greedy (AKA shitty).
# we should modifiy it inside scipy to be able to bruteforce correctly
#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH'], optMethod = 'brute')

#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'brute', restartScenario=['MsensH', 'MsensPole'])

#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH'], optMethod = 'differentialEvolution')

#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'differentialEvolution', restartScenario=['MsensH', 'MsensPole'])

myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'basinHoping', restartScenario=['MsensH'])

# msensPole restart Values are shit (but now we can avoid shit by using "robust" calculations
#myOptimizedRhoDFIIt = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole'], optMethod = 'basinHoping', restartScenario=['MsensH', 'MsensPole'])

# problem to get MsensH with starting parameters from MsensPole
myOptimizedRhoDFIIt_all = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole', 'RNG'], optMethod = 'basinHoping', restartScenario=['all'])

myOptimizedRhoDFIIt_all = myRhoDFIIt.optimizeForm(['MsensH', 'MsensPole', 'RNG'], optMethod = 'basinHoping', restartScenario=['MsensH', 'RNG'])