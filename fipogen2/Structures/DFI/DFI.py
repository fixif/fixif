#coding=UTF8

# dirty but quick fix otherwise doesn't work
import sys,os
sys.path.insert(0, os.path.abspath('../../'))

from SIF import SIF
from numpy import matrix as mat


class DFI(SIF):

    def __init__(self, num, den, father_obj = None, **event_spec):
        
        """
        Convert a transfer function to a Direct Form I SIF
        """
        
        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'DFI')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'State_Space.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        DFI_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        DFI_father_obj = father_obj

        num = mat(num).astype(float)
        den = mat(den).astype(float)

        # normalize coefficients
        
        num = num / den[0,0]
        den = den / den[0,0]
        
        n = max(num.shape[1], den.shape[1]) - 1
        
        J = mat([1])
        K = np.r_[np.zeros((n-1,1)), mat([1]), np.zeros((n,1))]
	L = mat([1])
	M = np.c_[ mat([-c for c in den[-1:0:-1]]), mat(num[-1:0:-1]) ]
	N = mat(num[0])
	
	P = np.diag([1]*(2*n-1), 1)
	P[n-1,n] = 0
	
	Q = np.r_[ np.zeros((2*n-1,1)), mat([1]) ]
	R = np.zeros((1,2*n))
	S = mat([0])

        JtoS = [J, K, L, M, N, P, Q, R, S]
        
        SIF.__init__(JtoS, DFI_father_obj, **DFI_event)
        
        
