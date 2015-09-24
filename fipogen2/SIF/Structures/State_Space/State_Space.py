from ...SIF import SIF

# dirty but quick fix otherwise doesn't work
import sys,os
sys.path.insert(0, os.path.abspath('../../'))
from LTI import dSS

from numpy import eye, zeros

class State_Space(dSS):

    def __init__(self, A, B, C, D, father_obj = None, **event_spec):
        
        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'new')      
        my_e_subclass  = event_spec.get('e_subclass', 'State_Space')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'State_Space.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        State_Space_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        my_father_obj = father_obj
        
        # call super
        dSS.__init__(self, A, B, C, D, my_father_obj, **State_Space_event)
        
    #======================================================================================#    
    def toSIF(self, delta_eps=1.e-8):
      
        """
        Convert a discrete state space to to SIF
        """
    
        # Convert event : we generate a SIF from dSS
        toSIF_event = {'e_type':'create', 'e_subtype':'convert', 'e_source':'func', 'e_subsource':'State_Space.toSIF', 'e_desc':'', 'e_subclass':'State_Space'}

        toSIF_father_obj = self
        
        n = self._A.shape[0]
        p = self._B.shape[1]
        m = self._C.shape[0]
        l = 0

        JtoS = [eye((l)), zeros((n,l)), zeros((m,l)), zeros((l,n)), zeros((l,p)), self._A, self._B, self._C, self._D]
        
        return SIF(JtoS, delta_eps, toSIF_father_obj, **toSIF_event)