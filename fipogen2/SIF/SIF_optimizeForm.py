#coding=UTF8

__author__ = "Joachim Kruithof, Thibault Hilaire"
__copyright__ = "Copyright 2016, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof", "Thibault Hilaire"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from LTI import dSS

# cannot use this otherwise the instance of RhoDFIIt are not going to contain optimizeForm function.
# so we use instance.__class__.__init__
#from Structures import RhoDFIIt

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply, all, diagflat, trace, ones, where, logical_or, ravel
from numpy import transpose, fmod, log2, random
from numpy.linalg import norm, inv, eig

from scipy import optimize

from copy import copy, deepcopy

__all__ = ['optimizeForm']

iter_count = 0

def optimizeForm(R, measures, startVals=None, bounds = None, stop_condition=None,  measureType=None, weightingMethod=None, measureWeights=None, optMethod=None, bestVals=[], restartScenario = ['default']):
    
    """
    Generic optimization routine for all SIF subclasses
    
    For multi-parameter optimization this function is called recursively.
    
    """
    # hack, ugly bout working
    global iter_count

    # Text Output line
    line = '---------------------------------------------------------'

    # Acceptable values for parameters
    def_opt_measureTypes = {'OL', 'CL'}
    def_opt_measureType = 'OL'

    def_opt_weightingMethods = {'equalWeight', 'customWeight'}
    def_opt_weightingMethod = 'equalWeight'
    
    def_opt_methods = {'basinHoping', 'differentialEvolution', 'brute'}
    def_opt_method = 'basinHoping'

    def_opt_measures = {'MsensH', 'MsensPole', 'RNG', 'Mstability'}

    # supported forms of filter for optimization
    def_opt_forms = {'DFI', 'DFII', 'State_Space', 'RhoDFIIt'}

    # check input args, set defaults values if not provided, 
    # give user feedback on what's happening

    #measures
    for measure in measures:
        if measure not in def_opt_measures:
            raise(NameError, 'measure {0} not defined, use : {1}'.format(measure, ' or/and '.join(def_opt_measures)))        

    # measureType
    if (measureType not in def_opt_measureTypes) and (measureType is not None):
        raise(NameError, '{0} not defined as a measureType, use one of : {1}'.format(measureType, ' , '.join(def_opt_measureTypes)))
       
    elif measureType == 'OL' or measureType == 'CL':
        print('measureType : {}'.format(measureType))
        
    else: # measureType is None
        print('measureType : using default : {}'.format(def_opt_measureType))
        measureType = def_opt_measureType
      
    #weightingMethod
    if (weightingMethod not in def_opt_weightingMethods) and (weightingMethod is not None):
        raise(NameError, '{0} not defined as a weightingMethod, use one of : {1}'.format(weightingMethod, ' , '.join(def_opt_weightingMethods)))

    elif len(measures) == 1:
        print('weightingMethod : N/A, single parameter')
        weightingMethod = 'equalWeight'
        
    elif weightingMethod is not None:
        print('weightingMethod : {}'.format(weightingMethod))
        
    else:
        print('weightingMethod : not defined, using default : {}'.format(def_opt_weightingMethod))
        print('weightingMethod : measureWeights will be IGNORED')
        weightingMethod = def_opt_weightingMethod

    #measureWeights
    if weightingMethod == 'equalWeight':
        measureWeights = [1./len(measures) for i in measures]
        
    elif weightingMethod == 'simpleWeight':
        if sum(measureWeights != 1): # risky
            raise(ValueError, 'measureWeights : simpleWeight : sum of measures should be equal to 1')
        if len(measureWeights) != len(measures):
            raise(ValueError, 'measureWeights : simpleWeight : needs 1 coefficient per measure')
    
    print('measureWeights = {}'.format(measureWeights))
    
    #opt_method
    if (optMethod not in def_opt_methods) and (optMethod is not None):
        raise(NameError, '{0} not defined as an optMethod, use one of : {1}'.format(optMethod, ' , '.join(def_opt_methods)))
    
    elif optMethod is None:
        print('optMethod : not defined, using default : {}'.format(def_opt_method))
        optMethod = def_opt_method
        
    else:
        print('optMethod : {}'.format(optMethod))
        
    # determine method used to get new form and new measures from existing ones
    # those tests could be skipped by using a metaclass or a new class to inherit from

    if R.__class__.__name__ in {'DFI', 'DFII', 'State_Space'}:
        _formOpt = 'UYW'
    elif R.__class__.__name__ == 'RhoDFIIt':
        _formOpt = 'gammaDelta' # in a later iteration if we define a dictionary correctly for instance.__init__, could be more generic like "brute"
#     elif R.__class__.__name__ == 'Modal_delta':
#         _formOpt = 'delta'
    else:
        raise(NameError, 'unsupported form of filter, supported forms are {}'.format(' , '.join(def_opt_forms)))
    
    
    # init_vals
    if startVals == 'default':
        
        if _formOpt == 'UYW':
            # U,Y,W transform
            print('startVals : using default U, Y, W values')
            #R.U = multiply(10,eye(R._n)) # be carfeul to use property so that nparray is transformed into matrix
            #print('l={0} m={1} n={2} p={3}'.format(R._l, R._m, R._n, R._p))
            #R.U = multiply(3, ones((R._n,R._n)))
            
            #R.U = random.rand(R._n, R._n)
            #R.Y = eye(R._l)
            #R.W = eye(R._l)
        
            startVals = [eye(R._n), eye(R._l), eye(R._l)]
        
            #startVals = [random.rand(R._n, R._n), eye(R._l), eye(R._l)]]
        
        elif _formOpt == 'gammaDelta': #or _formOpt == 'delta'
            
            print('startVals : using default gamma and delta values')
            
            # starting with 2's, not zeros, not ones
            #[gamma, delta]
            def_gamma_delta = ones((R._num.shape[0], R._den.shape[1]-1))
            startVals = multiply(2, [def_gamma_delta, def_gamma_delta])
            
            #raise(ValueError, 'gamma,delta needs to be defined at instance creation, cannot supply default values (to be implemented)')
           
    # use data already in instance attributes 
    elif startVals is not None:
        
        print('startVals : using user-supplied values')
    
    else: # startVals is None
        
        print('startVals : using values stored in obj instance')
        
        if _formOpt == 'UYW':
            startVals = [R.U, R.Y, R.W] 
        elif _formOpt == 'gammaDelta':
            startVals = [R._gamma, R._delta]

    print('startVals : {}'.format(startVals))
        
    #change list of arrays into unique, 1-D array as needed by scipy.optimize
    x0 = ravel([m.A1 for m in startVals if  m.A1.size != 0])
    
    #bounds
    if bounds is None:
        
        print('bounds : using default values')
        
        if _formOpt == 'UYW':
            bounds = [(0.01, 100)]*len(x0)
            
        elif _formOpt == 'gammaDelta':
            bounds = [(0.05, 10)]*len(x0)

    else:
        print('bounds : using supplied values')
        
    print("bounds = {}".format(bounds))

    # check restartScenario
    for restartS in restartScenario:
        if restartS not in measures + ['all', 'default']:
            raise(ValueError, 'restartScenario : impossible value')

    print('measureType : {}'.format(measureType))
    
    def _getOptParameter(vals, weights, weightingMethod, best_vals = None):
        
        """
        This function returns a unique float which represents our optimization objective parameter,
        related to all values, weighted by weightingMethod
        Currently there's only one method when there is more than 1 parameter.
        For 1 parameter the function simply returns vals[0]
        """
        
        if len(vals)==1: # to allow recursive call 
            return vals[0]
           
        elif weightingMethod == 'equalWeight' or weightingMethod == 'simpleWeight':
            
            return sum([weights[i]*vals[i]/best_vals[i] for i in range(0, len(vals))])    
        

#     # Optimization process
#     
#     print(line)
#     
#     if len(measures) > 1:
#         
#         print('Beginning process for multi variable optimization : {}'.format(' , '.join(measures)))
#         print('Step 1 : get best criterion value for each criterion independently')
# 
#     else:
#         
#         print('Beginning process for single variable optimization : {}'.format(measures[0]))
#         
#     print(line)
    

    
    def _calc_crit(R, measure, measureType):
        
        if measure == 'MsensH':
            return R.MsensH(measureType=measureType)[0]
        elif measure == 'MsensPole':
            return R.MsensPole(measureType=measureType)[0]
        elif measure == 'RNG':
            return R.RNG(measureType = measureType)[0]
        elif measure == 'Mstability':
            return R.Mstability()
    
    def _rebuild_matrixes(mat_list, mat_flat):
        
        """
        Rebuild 2d list of ndarrays, from a 1D, flat ndarray,
        according to shapes found in mat_list
        """
        
        current_pos = 0
        
        mat_list_out = []
        
        for mymat in mat_list:
            
            A1_len = mymat.A1.shape[0]
            A1_array = mat_flat[current_pos:current_pos+A1_len]
            current_pos += A1_len
            mat_list_out.append(A1_array.reshape(mymat.shape[0], mymat.shape[1]))            
        
        return mat_list_out    
    
    def _generate_updated_instance(input_R, optVals):
        
        """
        This functions generates a new instance of an existing object using either
        - UYW matrixes
        - gamma and delta
        stored in optVals
        """
        
        output_R = deepcopy(input_R)
        
        #translate using UYW matrixes
        if _formOpt == 'UYW':
                        
            output_R.U, output_R.Y, output_R.W = optVals
            output_R._translate_realization()

        #create new object with current gamma and delta        
        elif _formOpt == 'gammaDelta':
            #print('Sum of all parameters : {} '.format(sum(x)))
            
            if isinstance(input_R, list):
            	print(input_R)
            
            input_R.__class__.__init__(output_R, input_R._num, input_R._den, gamma=optVals[0], delta=optVals[1], isGammaExact=input_R._isGammaExact, isDeltaExact=input_R._isDeltaExact, opt=input_R._opt)
    
        return output_R
    
    def _func_opt(x, input_R):
        
        """
        This function takes a 1D x vector from scipy.optimize 
        and returns 
        a single optimization parameter 
        as required by scipy.optimize
        We need start_val to extract the shape of each matrix to reshape the x vector
        """
        global iter_count

        tmp_opt_crit = []
        
        for measure in measures:
            tmp_opt_crit.append(_calc_crit(_generate_updated_instance(input_R, _rebuild_matrixes(startVals, x)), measure, measureType))         
     
        opt_crit = _getOptParameter(tmp_opt_crit, measureWeights, weightingMethod, bestVals)

        iter_count += 1
        
        if iter_count == 1:
            
            print('\n'+line)         
            print('Initial values (first iteration) :')
            print(line)
            
            if len(measures)>1:
                print('Overall criterion = {}'.format(opt_crit))
            
            for i in range(0, len(measures)):
                print('{0:10} = {1:10}'.format(measures[i], tmp_opt_crit[i]))            
        
            print(line)
        
        if iter_count%1000 == 0:
            
            print('opt_crit after {} iter = {}'.format(iter_count, opt_crit))
        
        return opt_crit
    
    R_loc = deepcopy(R)
    
    #init_crit_vals = []
    
    #for measure in measures:
    #    init_crit_vals.append(_calc_crit(R_loc, measure, measureType))
        
#     print(line)         
#     print('Initial values (first iteration) :')
#     print(line)
#     for i in range(0, len(measures)):
#         print('{0:10} = {1:10}'.format(measures[i], init_crit_vals[i]))
    
    # recursive call for each parameter :
    # using the same init_vals
    # then once all best values of parameters are acquired, optimize for all parameters @ same time
    if len(measures) > 1 and len(bestVals) < len(measures):
        

        #best independent criterions values for separate optimization
        opt_forms = []
        bestVals = []
        # Optimize for each variable separately, starting from *init_vals*
        for measure in measures:
            # do we need to copy the object here ?
            print(line)
            print('Optimizing for single parameter : {}'.format(measure))
            print(line)
            R_ind = R_loc.optimizeForm([measure], startVals=None, measureType=measureType, optMethod=optMethod) # start with same stored initial values of parameters
            # reset R_loc
            R_loc = deepcopy(R)
            opt_forms.append(R_ind)
            bestVals.append(_calc_crit(R_ind, measure, measureType))

        print(line)
        print('Best values found for individual parameters : ')
        for i in range(0, len(measures)):
             print('{0:10} = {1:10}'.format(measures[i], bestVals[i]))
        print(line)

        print('Entering multiparameter optimization')
        print(line)

        if restartScenario == ['default']:
            
            R_opt = R_loc.optimizeForm(measures, startVals=None, measureType=measureType, weightingMethod=weightingMethod, measureWeights=measureWeights, optMethod=optMethod, bestVals=bestVals)
            opt_forms.append(R_opt)
            
        elif restartScenario == ['all']:

            print(line)
            print('startVals / multiparameter : Using all individual criterion final values for multiparameter optimization')
            
            for i in range(0, len(measures)):
                
                print(line)
                print('startVals / multiparameter : Using best values found for {} as starting parameters'.format(measures[i]))
                print(line)
                
                if _formOpt == 'UYW':
                    loc_startVals = [opt_forms[i].U, opt_forms[i].Y, opt_form[i].W]
                elif _formOpt == 'gammaDelta':
                    loc_startVals = [opt_forms[i]._gamma, opt_forms[i]._delta]
                
                R_opt = R_loc.optimizeForm(measures, startVals=loc_startVals, measureType=measureType, weightingMethod=weightingMethod, measureWeights=measureWeights, optMethod=optMethod, bestVals=bestVals)
                
                R_loc = deepcopy(R)
                
                opt_forms.append(R_opt)
                
        else:
            
            for restartS in restartScenario:
            
                print(line)
                print('startVals / multiparameter : Using best values found for {} as starting parameters'.format(restartS))
                print(line)
       
                ind = measures.index(restartS)
            
                if _formOpt == 'UYW':
                    loc_startVals = [opt_forms[ind].U, opt_forms[ind].Y, opt_form[ind].W]
                elif _formOpt == 'gammaDelta':
                    loc_startVals = [opt_forms[ind]._gamma, opt_forms[ind]._delta]            
        
                R_opt = R_loc.optimizeForm(measures, startVals=loc_startVals, measureType=measureType, weightingMethod=weightingMethod, measureWeights=measureWeights, optMethod=optMethod, bestVals=bestVals)            
        
                opt_forms.append(R_opt)            
        
        return opt_forms
        
    else:
        

        
        #print(x0)
        #print(x0.shape)
        #hack

        
        minimizer_kwargs = {'args':R_loc, 'bounds':bounds}
        
        if optMethod == 'basinHoping':
            
            # this parameter is passed to scipy.minimize
            #minimizer_kwargs['method'] = 'BFGS'
            # removed parameter T
            
            # I think there is a bug with new parameter calculation for optimize :
            # If a small change in parameters don't change result much, then parameters skyrocket
            # It may be due to the fact that we use initial parameters = zeros (I think a formula like (x -x 0)/delta_params is used or delta_params/(x -x0) so
            # that if the dividing factor is small, parameters can skyrocket.

            #niter = 2000 and stepsize = 0.01 gives good result but not stable
            minimizer_kwargs = {'args':R_loc, 'bounds':bounds}
            opt_result = optimize.basinhopping(_func_opt, x0, niter=2000, stepsize=0.01, minimizer_kwargs=minimizer_kwargs, take_step=None, accept_test=None, callback=None, interval=1, disp=False, niter_success=1)
        
        elif optMethod == 'differentialEvolution':
        
            # QUICK HACK HERE
            # THE POLISHING STEP GIVES A BUG SO WE DON'T USE IT.
            # see for example
            # https://github.com/scipy/scipy/issues/4880
            # WARNING FOR "RESULT AT THE FIRST STEP WITH THIS METHOD"
            # it's given after a first tset of parameters by the optimizer so not always the same.
            # also not possible to set initial value and multiparmaeter opt is dependent from starting paramters.
        
            minimizer_kwargs = [R_loc]
            opt_result = optimize.differential_evolution(_func_opt, bounds, args=minimizer_kwargs, maxiter = 50000, polish=False)

        elif optMethod == 'brute':
        
            # there seems to be no way to specifiy a starting point for the optimizer...
        
            minimizer_kwargs = [R_loc]
            
            opt_result = optimize.brute(_func_opt, bounds, args = minimizer_kwargs)

        iter_count = 0
        
        #print(opt_result)
        
        R_opt = _generate_updated_instance(R_loc, _rebuild_matrixes(startVals, opt_result.x))
        
        
        tmp_opt_crit = []
        
        for measure in measures:
            tmp_opt_crit.append(_calc_crit(R_opt, measure, measureType))         
     
            
        print(line)         
        print('Result values (after last iteration) :')
        print(line)
        
        if len(measures)>1:
            print('Overall criterion : {}'.format(opt_result.fun))
        
        for i in range(0, len(measures)):
            print('{0:10} = {1:10}'.format(measures[i], tmp_opt_crit[i]))            
        
        print(line+'\n')

        
        return R_opt
   
        
       