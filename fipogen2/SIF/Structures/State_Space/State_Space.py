from ...SIF import SIF
from ....LTI import LTI

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
        toSIF_event = {'e_type':'create', 'e_subtype':'convert', 'e_source':'func', 'e_subsource':'State_Space.toSIF', 'e_desc':'', 'e_subclass':'State_Space'}

        toSIF_father_obj = self
        
        n = self._A.shape[0]
        p = self._B.shape[1]
        m = self._C.shape[0]
        l = 0

        JtoS = [eye((l)), zeros((n,l)), zeros((m,l)), zeros((l,n)), zeros((l,p)), self._A, self._B, self._C, self._D]
        
        return SIF(JtoS, toSIF_father_obj, toSIF_event)