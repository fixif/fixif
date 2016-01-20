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

from numpy import matrix as mat
from numpy import eye, c_, r_, zeros, multiply, all, diagflat, trace, ones, where, logical_or, ravel
from numpy import transpose, fmod, log2
from numpy.linalg import norm, inv, eig

from scipy import optimize

from copy import copy, deepcopy

__all__ = ['optimizeForm']

def optimizeForm(R, measures, startVals=None, stop_condition=None,  measureType=None, weigthingMethod=None, measureWeights=None, optMethod=None):
    
    """
    Generic optimization routine for all SIF subclasses
    
    For multi-parameter optimization this function is called recursively.
    
    """

    # Text Output line
    line = '---------------------------------------------------------'

    # Acceptable values for parameters
    def_opt_measureTypes = {'OL', 'CL'}
    def_opt_measureType = 'OL'

    def_opt_weightingMethods = {'equalWeight', 'customWeight'}
    def_opt_weightingMethod = 'equalWeight'
    
    def_opt_methods = {'basinHoping', 'min', 'simple', 'brute'}
    def_opt_method = 'basinHoping'

    def_opt_measures = {'MsensH', 'MsensPole', 'RNG', 'Mstability'}

    # supported forms of filter for optimization
    def_opt_forms = {'DFI', 'DFII', 'State_Space', 'rhoDFIIt'}

    # check input args, set defaults values if not provided, give user feedback on what's happening

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
    # special case if number of measures is 1
    elif len(measures) == 1:
        print('weightingMethod : N/A, single parameter')
        weigthingMethod = 'equalWeight'
        
    elif weightingMethod is not None:
        print('weightingMethod : {}'.format(weightingMethod))
        
    else:
        print('weightingMethod : not defined, using default : {}'.format(def_opt_weigthingMethod))
        print('weightingMethod : measureWeights will be IGNORED')
        weightingMethod = def_opt_weightingMethod

    #measureWeights
    if weightingMethod == 'equalWeight':
        measureWeights = [1./len(measures) for i in measures]
        
    elif weigthingMethod == 'simpleWeight':
        if sum(measureWeights != 1): # risky
            raise(ValueError, 'measureWeights : simpleWeight : sum of measures should be equal to 1')
        if len(measureWeights) != len(measures):
            raise(ValueError, 'measureWeights : simpleWeight : needs 1 coefficient per measure')
    
    #def _sameNumEl(listName1, listName2):
    #    return "{0} list should have same number of elements as {1} list".format(listName1, listName2)
    
    #opt_method
    if (optMethod not in def_opt_methods) and (optMethod is not None):
        raise(NameError, '{0} not defined as an optMethod, use one of : {1}'.format(optMethod, ' , '.join(def_opt_methods)))
    
    elif optMethod is None:
        print('optMethod : not defined, using default : {}'.format(def_opt_method))
        optMethod = def_opt_method
        
    else:
        print('optMethod : {}'.format(optMethod))
        
    # determine method used to get new form AND new measures from existing ones
    # from this we get a private variable named
    # those tests could be skipped by using a metaclass or a new class to inherit from

    # get name of base classes
    base_class_names = [myclass.__name__ for myclass in R.__class__.__bases__]
    
    if ('DFI'  or 'DFII' or 'State_Space') in base_class_names:
        _formOpt = 'UYW'
    elif 'rhoDFIIt' in base_class_names:
        _formOpt = 'gammaDelta' # in a later iteration if we define a dictionary correctly for instance.__init__, could be more generic like "brute"
#     elif 'Modal_delta' in base_class_names:
#         _formOpt = 'delta'
    else:
        raise(NameError, 'unsupported form of filter, supported forms are {}'.format(' , '.join(def_opt_forms)))
    
    
    # init_vals
    if startVals == 'default':
        
        print('startValues : Using default')
        
        if _formOpt == 'UYW':
            # U,Y,W transform
            startVals = [eye(R._n), eye(R._l), eye(R._l)] # could be uniformized by replacing existing or non-existing value of U, Y, W
        
        elif _formOpt == 'gammaDelta': #or _formOpt == 'delta'
            raise(ValueError, 'gamma,delta needs to be defined at instance creation, cannot supply default values (to be implemented)')
           
    # use data already in instance attributes 
    elif startVals is None:
        
        print('startValues : using stored values')
        
        if _formOpt == 'UYW':
            startVals = [self.U, self.Y, self.W] 
        elif _formOpt == 'gammaDelta':
            startVals = [R._gamma, R._delta]

    
    def _getOptParameter(vals, weights, weigthingMethod, best_vals = None):
        
        """
        This function returns a unique float which represents our optimization objective parameter,
        related to all values, weighted by weightingMethod
        Currently there's only one method when there is more than 1 parameter.
        For 1 parameter the function simply returns vals[0]
        """
        
        if len(vals)==1: # to allow recursive call 
            return vals[0]
           
        elif weightingMethod == 'equalWeight' or weightingMethod == 'simpleWeight':
            return sum([weights(i)*vals(i)/best_vals(i) for i in range(0, len(vals))])    
        

    # Optimization process
    
    print(line)
    
    if len(measures) > 1:
        
        print('Beginning process for multi variable optimization : {}'.format(' , '.join(measures)))
        print('Step 1 : get best criterion value for each criterion independently')

    else:
        
        print('Beginning process for single variable optimization : {}'.format(measures[0]))
        
    print(line)
    

    
    def _calc_crit(R, measure, measureType):
        
        if measure == 'MsensH':
            return R.MsensH(measureType=measureType)[0]
        elif measure == 'MsensPole':
            return R.MsensPole(measureType=measureType)[0]
        elif measure == 'RNG':
            return R.RNG(measureType = measureType)[0]
        elif measure == 'Mstability':
            return R.Mstability()
    
    def _func_opt(x, input_R):
        
        """
        This function takes a 1D x vector from scipy.optimize 
        and returns 
        a single optimization parameter 
        as required by scipy.optimize
        We need start_val to extract the shape of each matrix to reshape the x vector
        """

        tmp_optVals = []
        tmp_opt_crit = []
        
        # reshape x vector according to startVals
        # nparrays are immutable so we cannot use pop-like functions here
        
        current_pos = 0
        
        for mymat in startVals:
            
            A1_len = mymat.A1.shape[0]
            A1_array = x[current_pos:current_pos+A1_len]
            current_pos += A1_len
            tmp_optVals.append(A1_array.reshape(mymat.shape[0], mymat.shape[1]))
        
        # now we have a list to be inserted and the behaviour of the function depends on the form of R
        
        if _formOpt == 'UYW':
            
            tmp_obj = deepcopy(input_R)
            tmp_obj.U, tmp_obj.Y, tmp_obj.W = tmp_optVals
            tmp_obj._translate_realization()
           
        elif _formOpt == 'gammaDelta':
        
            #create new object with current gamma and delta
            tmp_obj = rhoDFIIt(R._num, R._den, gamma=tmp_optVals[0], delta=tmp_optVals[1]) # TODO strore isGammaExact, isDeltaExact in rhoDFIIt instance
        
        # if _formOpt == 'UYW', no recalculation needed here
        # if _formOpt == 'gammaDelta', calculation from scratch of measures
        
        for measure in measures:
               tmp_opt_crit.append(_calc_crit(tmp_obj, measure, measureType))
                  
        opt_crit = _getOptParameter(tmp_opt_crit, measureWeights, weightingMethod, bestVals)
        
        return opt_crit
        

    R_loc = deepcopy(R)
        
    init_crit_vals = []
    
    for measure in measures:
        init_crit_vals.append(_calc_crit(R_loc, measure, measureType))
         
    print('Starting point for optimization :')
    print('measureType : {}'.format(measureType))
    print('Used criterions / Start Value : ')
    for i in range(0,measures):
        print('{0:10} = {1:10}'.format(measures[i], init_crit_vals[i]))
    
    # recursive call for each parameter :
    # using the same init_vals
    # then once all best values of parameters are acquired, optimize for all parameters @ same time
    if len(measures) > 1 and bestVals is None:
        #best independent criterions values for separate optimization
        opt_forms = []
        bestVals = []
        # Optimize for each variable separately, starting from *init_vals*
        for measure in measures:
            # do we need to copy the object here ?
            R_loc_2 = deepcopy(R)
            R_ind = optimizeForm(R_loc_2, measure, startVals=None, measureType=measureType, optMethod=optMethod, bestVals = None) # start with same stored initial values of parameters
            ind_opt_forms.append(R_ind)
            bestVals.append(_calc_crit(R_ind, measure, measureType))
       
        R_loc_3 = deepcopy(R)
        R_opt = optimizeForm(R_loc_3, measures, startVals = None, measureType=measureType, weigthingMethod=weightingMethod, measureWeights=measureWeights, optMethod=optMethod, bestVals=bestVals)
        
        opt_forms.append(R_opt)
        
        return opt_forms
        
    else:
        
        #change list of arrays into unique, 1-D array as needed by scipy.optimize
        
        x0 = ravel([m.A1 for m in startVals])
        
        minimizer_kwargs = {'args':R_loc}
        
        if optMethod == 'basinHoping':
            
            # this parameter is passed to scipy.minimize
            #minimizer_kwargs['method'] = 'BFGS'
            # removed parameter T
            opt_result = optimize.basinhopping(_func_opt, x0, niter=2000, stepsize=0.5, minimizer_kwargs=minimizer_kwargs, take_step=None, accept_test=None, callback=None, interval=50, disp=True, niter_success=None)
        
        #reshape all matrixes
        
        
            
    print(opt_result)       
        
    return R_opt
           

        
            
            
        
        
       