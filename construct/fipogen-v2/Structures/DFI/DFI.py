#coding=utf8

from SIF import SIF

from numpy import matrix as mat
from numpy import diagflat, zeros, eye, rot90, ones, r_, c_, atleast_2d
from numpy.linalg import inv

class DFI(SIF):
  
    def __init__(self, num, den, opt=1, eps=1.e-8, father_obj = None, **event_spec):
  
        """
        Convert a trasfer function to a DF-I (Direct Form I) SIF
      
        Two options are available
      
        1 - compute num and den at the same time (normalize,...)
        2 - compute num and den separately (don't normalize, ...)
      
        """

        # create default event if no event specified
        
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'DFI')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'DFI.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        DFI_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        DFI_father_obj = father_obj
        
        if opt not in {1,2}:
            raise("Unknown option...")
        
        # convert everything to mat
        
        num = mat(num)
        den = mat(den)
        
        nnum = num.shape[1] - 1
        nden = den.shape[1] - 1
        
        if opt == 1:
        # normalize
            num = num / den[0,0]
            den = den / den[0,0]
            
        # Compute gammas
        
        # gamma1 and gamma4 differ between options
        if opt == 1:
            gamma1 = c_[[num[0, 1:]],[-den[0, 1:]]]
        elif opt == 2:
            gamma1 = r_[[c_[num[0, 1:], zeros((1, nden))]], [c_[zeros((1, nnum)), -den[0, 1:]]]]
    # ???    
        #gamma2 = [[diag(ones((1,nnum-1)),-1), zeros((nnum, nden))],[zeros((nden,nnum)), diag(ones((1,nden-1)),-1)]]
        gamma2 = r_[c_[diagflat(ones((1, nnum-1)), -1), zeros((nnum, nden))],c_[zeros((nden, nnum)), diagflat(ones((1, nden-1)), -1)]]
        #CurrentWork
        gamma3 = r_[atleast_2d(1), zeros((nnum+nden-1, 1))]
    
        if opt == 1:
            gamma4 = r_[zeros((nnum, 1)), atleast_2d(1), zeros((nden-1, 1))]
        elif opt == 2:
            gamma4 = r_[zeros((nnum, 2)), [[1,1]], zeros((nden-1, 2))]
            
        gamma1 = mat(gamma1)
        gamma2 = mat(gamma2)
        gamma3 = mat(gamma3)
        gamma4 = mat(gamma4)

	# transformation to 'optimize' the code
        
        T = mat(rot90(eye(2*nnum)))
        
        invT = inv(T)
        
        # build SIF
        
        if opt == 1:
            
            JtoS = atleast_2d(den[0,0]), invT*gamma4, atleast_2d(1), gamma1*T, atleast_2d(num[0,0]), invT*gamma2*T, invT*gamma3, mat(zeros((1, nnum+nden))), atleast_2d(0)
        
        elif opt == 2:
            
            JtoS = mat(eye(2)), invT*gamma4, mat([1,1]), gamma1*T, r_[atleast_2d(num[0,0]),atleast_2d(0)], invT*gamma2*T, invT*gamma3, mat(zeros((1, nnum+nden))), atleast_2d(0)

        #print(JtoS)

        SIF.__init__(self, JtoS, eps, DFI_father_obj, **DFI_event)

        