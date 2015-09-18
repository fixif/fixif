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

		SIF_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

		my_father_obj = father_obj
		
		#Init superclass

		FIPObject.__init__(self, self.__class__.__name__, father_obj=my_father_obj, **SIF_event)

        self._J,
    	self._K,
    	self._L,
		self._M,
		self._N,
		self._P,
		self._Q,
		self._R,
		self._S = [np.matrix(X) for X in JtoS]

    	# set and check sizes
   		self._l,
   		self._m,
   		self._n,
   		self._p = self.__check_set_dimensions__()
   	   	
   		# build Z from JtoS
   		self._Z = np.bmat([[-self._J, self._M, self._N], 
						   [ self._K, self._P, self._Q], 
						   [ self._L, self._R, self._S]])
   	
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
   
    def __check_set_dimensions__(self):
    	
        """
        Computes the size 'l,m,n,p' of SIF
        Check size of matrixes 'J' to 'S'
        """
        
        l,m,n,p = 0 # set all dimensions to zero
        
        s1,s2 = 0 # temp sizes
        
        #list_mat  = [self._J, self._K, self._L, self._M, self._N, self._P, self._Q, self._R, self._S]
        #list_size = [(l,l),   (n,l),   (p,l),   (l,n),   (l,m),   (n,n),   (n,m),   (p,n),   (p,m) ]

		# P (n,n)
		# define n from matrix p
		
		s1,s2 = self._P.shape
		
		if (s1 != s2):
			raise ValueError, 'P should be a square matrix'
		else:
		    n = s1 # set n from P
        
        # J (l,l)
        
        s1,s2 = self._J.shape
        
        if (s1 != s2):
            raise ValueError, 'J should be a square matrix'
        else:
        	l = s1 # set l from J
        
        # K (n,l)
        
        s1,s2 = self._K.shape
        
        if (s1 != n) or (s2 != l):
        	raise ValueError, 'Dimensions of matrix K not coherent with dimensions of P and/or J'

        # L (p,l)
        
        s1,s2 = self._L.shape
        
        if (s2 != l):
        	raise ValueError, 'Dimension 2 of matrix L not coherent with dimension of J'
        else:
        	p = s1 # set p from L
        
        # M (l,n)
        
		s1,s2 = self._M.shape
        
        if (s1 != l) or (s2 != n):
        	raise ValueError, 'Dimensions of matrix M not coherent with dimensions of P and/or J'
        
        # N (l,m)
        
        s1,s2 = self._N.shape
        
        if (s1 != l):
        	raise ValueError, 'Dimension 1 of matrix N not coherent with dimensions of J'
        else:
        	m = s2 # set m from N
        
        # Q (n,m)
        
        s1,s2 = self._Q.shape
        
        if (s1 != n) or (s2 != m):
        	raise ValueError, 'Dimensions of Q not coherent with dimensions of P and/or N'
        
        # R (p,n)
        
        s1,s2 = self._R.shape
        
        if (s1 != p) or (s2 != n):
        	raise ValueError, 'Dimensions of R not coherent with dimensions of L and/or P'
        
        # S (p,m)
        
        s1,s2 = self._S.shape
        
        if (s1 != p) or(s2 != m):
        	raise ValueError, 'Dimensions of S not compatible with dimensions of L and/or N'

        return(l,m,n,p)
       
    @property
    def size(self):
       	
       	"""
       	Return size of realization
       	"""
       	   
        return (self._l, self._m, self._n, self._p)
          
    def __str__(self):
    	
    	def plural(n):
    		
    	    if (n > 1):
    		    str='s'
    	    else:
    		    str=''
    		
    	    return str
    	
    	str = "Realization " + self.trk_info[0].e_desc + " : \n"
    	str += "m = " + str(self._m) + "input"  + plural(m) + "\n"
    	str += "p = " + str(self._p) + "output" + plural(p) + "\n"
    	str += "n = " + str(self._n) + "state"  + plural(n) + "\n"
    	str += "l = " + str(self._l) + "intermediate variable" + plural(l) + "\n"
    	
    	return str
