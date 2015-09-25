#coding=UTF8

# This class contains routine to convert to FWR

from SIF import SIF
from LTI import TF
from numpy import zeros, all, poly
from numpy.linalg import cond

class RhoDFIIt(TF):
    
    def __init__(self, num, den, father_obj = None, **event_spec):
        
        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'new')      
        my_e_subclass  = event_spec.get('e_subclass', 'RhoDFIIt')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'RhoDFIIt.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        RhoDFIIt_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        my_father_obj = father_obj
        
        # call super
        TF.__init__(self, num, den, my_father_obj, **RhoDFIIt_event)
        
        pass
        
    def toSIF(self, gamma, isGammaExact = None, delta = None, isDeltaExact = None):
        
        if not isGammaExact:
            isGammaExact = True   
                 
        if not delta:
            delta = zeros(gamma.shape)
            
        if not isDeltaExact:
            isDeltaExact = False
            
        # Normalize num and den vs. first coefficient
        Va = num/num[0]
        Vb = den/den[0]
        
        # Compare #column (#lines is 1 ?)
        p1 = Va.shape[1] - 1
        p2 = Vb.shape[1] - 1
        p3 = gamma.shape[1]
        p4 = delta.shape[1]

        if not (np.all(np.matrix([p1, p2, p3]) == p4)):
            raise("Dimensions not coherent")
        
        p = p1
        
        # Step 1 : build Valapha_bar, Vbeta_bar
        # by considering Delta_k = 1 for all k
        
        # Build Tbar
        
        Tbar = zeros((p+1,p+1))
        Tbar[p,p] = 1
        
        for i in range(p-1,-1,-1):
            Tbar[i,range(i,p+2)] = poly(gamma[1, range(i,p+1)])# if we use matlab-like syntax, namely i:p+1 there's no check on matrix boundary (if p+1 exceeds boundary we got a result)
            
        