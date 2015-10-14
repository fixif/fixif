#coding=utf8

from SIF import SIF

from numpy import matrix as mat
from numpy import diag, zeros, eye, rot90, ones, r_, c_

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
        
        if opt is 1:
        # normalize
            num = num / den[0,0]
            den = den / den[0,0]
            
        # Compute gammas
        
        # gamma1 and gamma4 differ between options
        if opt is 1:
            gamma1 = num[0,1:] - den[0,1:]
        elif opt is 2:
            # Here a potential problem arises ?? verify with thibault
            gamma1 = r_[c_[num[0,1:], zeros((1,nnum))], zeros((1,nnum)) - den[0,1:]]
    # ???    
        #gamma2 = [[diag(ones((1,nnum-1)),-1), zeros((nnum, nden))],[zeros((nden,nnum)), diag(ones((1,nden-1)),-1)]]
        gamma2 = r_[c_[diagflat(ones((1,nnum-1)),-1), zeros((nnum, nden))],c_[zeros((nden,nnum)), diagflat(ones((1,nden-1)),-1)]]
        #CurrentWork
        gamma3 = [[1], [zeros((nnum+nden-1, 1))]]
    
        if opt is 1:
            gamma4 = [[zeros((nnum,1))],[1],[zeros((nden-1,1))]]
        elif opt is 2:
            gamma4 = [[zeros((nnum,2))],[1,1],[zeros((nden-1,2))]]
            
        # transformation to 'optimize' the code
        
        T = mat(rot90(eye(2*nnum)))
        
        # build SIF
        

        JtoS = den[0], gamma4, [1], gamma1, num[0], gamma2, gamma3, mat(zeros((1, nnum+nden))), [0]
        
        # define event
        
        SIF.__init__(self, JtoS, DFI_father_obj, **DFI_event)
        
        