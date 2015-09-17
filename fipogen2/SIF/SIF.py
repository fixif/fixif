#coding=utf8

# This class describes the SIF object
# 2015 LIP6

import numpy as np

class SIF(FIPObject):
	
 """
 This object represents a discrete state space in Special Implicit Form
 """
 
 def __init__(self, **event_spec): # one option JtoS, delta_epsilon 
   
   """
   Special Implicit Form (formely FWR, Finite Wordlength Realization)
   
   'l','m','n','p' : dimensions of the realization, checked with __check_dimensions__
   
   - 'l' intermediate variables
   
   - 'm' inputs
   - 'p' outputs
   
   - 'n' states
   
   'J, K, L, M, N, P, Q, R, S' matrices 'J' to 'S' (excluding 'O')
   
   'Z' is a big matrix regrouping all matrixes from 'J' to 'S' (11)
   
   'dJ, dK, dL, dM, dN, dP, dQ, dR, dS' are matrixes ::math`\delta J` to ::math`\delta S` (21)
   
   thoses matrixes represent exactly implemented parameters :
   
   .. math::
   
       \delta(Z)_{ij} \left\lbrace\begin{aligned}
                                 0 if Z_{ij} \pm 2, p \in \mathbb{Z}\\
                                 1 otherwise
                                  \end{aligned}\right.
   
   'dZ' is ::math`\delta Z`
   
   'AZ, BZ, CZ, DZ' matrixes ::math`A_Z, B_Z, C_Z, D_Z` (eq(7) and (8))
   
   When a SIF object is created, it is *not* possible to change its dimensions 'l,m,n,p' nor fields 'AZ,BZ,CZ,DZ'
   
   JOJO : Fields 'Z, dZ' are constructed from 'J' to 'S' and 'dJ' to 'dS' respectively, so those are
   
   Fields 'Z, dZ' are redundant with fields 'J ... S' but they can both be useful
   
   Changing 'Z' automatically changes fields 'J' to 'S' and reciprocally, 'dZ' changes 'dJ' to 'dS' respectively.
   
   'AZ, BZ, CZ, DZ' are deduced accordingly
   
   """
   
   def __init__(self, delta_eps, JtoS=None,
			                     dJtodS=None, 	          
			                     Z=None,
			                     dZ=None, father_obj=None, **event_spec): # name can be specified in e_desc

    # Define default event if not specified
    # default event : SIF instance created from user interface
		
	    my_e_type	   = event_spec.get('e_type', 'create')
	    my_e_subtype   = event_spec.get('e_subtype', 'new')	  
		my_e_subclass  = event_spec.get('e_subclass', 'SIF')
		my_e_source	   = event_spec.get('e_source', 'user_input')
		my_e_subsource = event_spec.get('e_subsource', 'SIF.__init__') # optional, could also be ''
		my_e_desc	   = event_spec.get('e_desc', '')

		dSS_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

		my_father_obj = father_obj
		
		#Init superclass
		# TODO: check if self.__class__.__name__ needed or can the superclass get it (in case of simple inheritance)
		FIPObject.__init__(self, self.__class__.__name__, father_obj=my_father_obj, **dSS_event)

    self._J,
    self._K,
    self._L,
	self._M,
	self._N,
	self._P,
	self._Q,
	self._R,
	self._S = [np.matrix(X) for X in JtoS]

    # check sizes
   	self._l,
   	self._m,
   	self._n,
   	self._p) = self.__check_set_dimensions__()
   	   	
   	# build Z from JtoS
   	self._Z = np.bmat([[-self._J, self._M, self._N], [self._K, self._P, self._Q], [self._L, self._R, self._S]])
   	
   	# dJ to dS
    self._dJ,
    self._dK,
	self._dL,
	self._dM,
	self._dN,
	self._dO,
	self._dP,
	self._dQ,
	self._dR,
	self._dS = [_nonTrivial(X, delta_eps) for X in JtoS]
   
    def __check_set_dimensions(self):
    	
        """
        Computes the size 'l,m,n,p' of SIF
        Check size of matrixes 'J' to 'S'
        """
        
        list_mat  = [self._J, self._K, self._L, self._M, self._N, self._P, self._Q, self._R, self._S]
        list_size = [(l,l),   (n,l),   (p,l),   (l,n),   (l,m),   (n,n),   (n,m),   (p,n),   (p,m) ]
        
        # J (l,l)
        
        # K (n,l)
        
        # L (p,l)
        
        # M (l,n)
        
        # N (l,m)
        
        # P (n,n)
        
        # Q (n,m)
        
        # R (p,n)
        
        # S (p,m)

   
  