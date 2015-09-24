from ..SIF import SIF #...
from ..LTI import dSS

class State_Space(dSS):

    def __init__(self, A, B, C, D, father_obj = None, **event_spec):
      
        # recopier function toSIF
        
        # creer JtoS
        
        # create event
        
        # call super
        dSS.__init__(A, B, C, D, father_obj, event_spec)
        
        
    #======================================================================================#    
    def toSIF(self):
      
        """
        Convert a discrete state space to to SIF
        """
    
        # Convert event : we generate a SIF from dSS
        
        my_e_type      = 'create'
        my_e_subtype   = 'convert'    
        my_e_subclass  = 'SIF'
        my_e_source    = 'func'
        my_e_subsource = 'dSS.toSIF'
        my_e_desc      = ''

        toSIF_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        toSIF_father_obj = self
        
        n = self._A.shape[0]
        p = self._B.shape[1]
        m = self._C.shape[0]
        l = 0

        JtoS = [eye((l)), zeros((n,l)), zeros((m,l)), zeros((l,n)), zeros((l,p)), self._A, self._B, self._C, self._D]
        
        return SIF(JtoS, toSIF_father_obj, toSIF_event)