#coding=utf8

from SIF import SIF

# dirty but quick fix otherwise doesn't work
import sys,os
sys.path.insert(0, os.path.abspath('../../'))
from LTI import dSS

class Transfer_Function(SIF):
  
    def __init__(self, num, den, opt=1, father_obj = None, **event_spec):
  
        """
        Convert a trasfer function to a DF-I (Direct Form I) SIF
      
        Two options are available
      
        1 - compute num and den at the same time (normalize,...)
        2 - compute num and den separately (don't normalize, ...)
      
        """

        # create default event if no event specified
        
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'Transfer_Function')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'Transfer_Function.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        Transfer_Function_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        Transfer_Function_father_obj = father_obj
        
        if opt not in {1,2}:
	  raise("Unknown option...")
        
        # convert everything to matrix
        
        num = matrix(num)
        den = matrix(den)
        
        nnum = num.shape[0] - 1
        nden = den.shape[0] - 1
        
        if opt is 1:
	    # normalize
            num = num / den[0]
            den = den / den[0]
            
        # Compute gammas
        
        # gamma1 and gamma4 differ between options
        if opt is 1:
	    gamma1 = num[1:] - den[1:]
	elif opt is 2:
	    # Here a potential problem arises ?? verify with thibault
	    gamma1 = [[num[1:], zeros((1,nnum))],[zeros((1,nnum)) - den[1:]]]
	# ???    
	gamma2 = [[diag(ones((1,nnum-1)),-1), zeros((nnum, nden))],[zeros((nden,nnum)), diag(ones((1,nden-1)),-1)]]
	gamma3 = [[1], [zeros((nnum+nden-1, 1))]]
	
	if opt is 1:
	    gamma4 = [[zeros((nnum,1))],[1],[zeros((nden-1,1))]]
        elif opt is 2:
            gamma4 = [[zeros((nnum,2))],[1,1],[zeros((nden-1,2))]]
            
        # transformation to 'optimize' the code
        
        T = matrix(eye(2*nnum)).rot90()
        
        # build SIF
        

	JtoS = [den[0], gamma4, [1], gamma1, num[0], gamma2, gamma3, matrix(zeros((1, nnum+nden))), 0]
        
        # define event
        
        SIF.__init__(JtoS)