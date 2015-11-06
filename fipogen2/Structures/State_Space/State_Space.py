from SIF import SIF

# dirty but quick fix otherwise doesn't work
import sys,os
sys.path.insert(0, os.path.abspath('../../'))
from LTI import dSS

from numpy import eye, zeros

class State_Space(SIF):

    def __init__(self, A, B, C, D, eps = 1.e-8, father_obj = None, **event_spec):
        
        """
        Convert a discrete state space to to SIF
        """
        
        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'State_Space')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'State_Space.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        State_Space_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        State_Space_father_obj = father_obj
        
        n = A.shape[0]
        p = B.shape[1]
        m = C.shape[0]
        l = 0

        JtoS = eye((l)), zeros((n,l)), zeros((m,l)), zeros((l,n)), zeros((l,p)), A, B, C, D
        
        SIF.__init__(self, JtoS, eps, State_Space_father_obj, **State_Space_event)
