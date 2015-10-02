#coding=utf8

"""
This class describes the SIF object
"""

__author__ = "Thibault Hilaire, Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Thibault Hilaire", "Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

from TRK.FIPObject import FIPObject
import numpy as np

class SIF(FIPObject):
    
    """
    Special Implicit Form (formely FWR, Finite Wordlength Realization)
   
    'l','m','n','p' : dimensions of the realization, set from JtoS, and checked with __check_set_dimensions__
   
    - 'l' intermediate variables
   
    - 'm' inputs
    - 'p' outputs
   
    - 'n' states
   
    'J, K, L, M, N, P, Q, R, S' matrices 'J' to 'S' (excluding 'O')
   
    'Z' is a big matrix regrouping all matrixes from 'J' to 'S' (11)
   
    'dJ, dK, dL, dM, dN, dP, dQ, dR, dS' are matrixes :math:`\delta J` to :math:`\delta S` (21)
   
    thoses matrixes represent exactly implemented parameters :
   
    .. math::
   
        \delta(Z)_{ij} \left\lbrace\begin{aligned}
                                 0 if Z_{ij} \pm 2, p \in \mathbb{Z}\\
                                 1 otherwise
                                  \end{aligned}\right.
   
    'dZ' is :math:`\delta Z`
   
    'AZ, BZ, CZ, DZ' matrixes :math:`A_Z, B_Z, C_Z, D_Z` (eq(7) and (8))
   
    When a SIF object is created, it is *not* possible to change its dimensions 'l,m,n,p' nor fields 'AZ,BZ,CZ,DZ'
    
    JOJO : Fields 'Z, dZ' are constructed from 'J' to 'S' and 'dJ' to 'dS' respectively, so those are
   
    Fields 'Z, dZ' are redundant with fields 'J ... S' but they can both be useful
   
    Changing 'Z' automatically changes fields 'J' to 'S' and reciprocally, 'dZ' changes 'dJ' to 'dS' respectively.
   
    'AZ, BZ, CZ, DZ' are deduced accordingly
   
    TODO:with current routine SIF can only be defined from JtoS
    we should be able to define it from Z and cut the matrix to get JtoS (thib ? mandatory ?)
   
   """
   
    @staticmethod
    def _isTrivial(x, eps):
       
        """
        _isTrivial(x, epsilon)
       
        Checks if a parameter is trivial based on the following definition
       
        :math:`x` is trivial if :
       
        .. math::
            x ~ 0
            x ~ 1
            x ~ -1
           
        With :math:`\epsilon` as threshold, the criterions are
       
        .. math::
       
            |x| < \epsilon
            |x - 1| < \epsilon
            |x + 1| < \epsilon
           
        return value is boolean
        """
       
        return (abs(x) < eps) or (abs(x-1) < eps) or (abs(x+1) < eps)
   
    @staticmethod
    def _nonTrivial(X, eps):
       
        """
        
        Check all coefficients of a matrix for triviality relative to _isTrivial definition
        
        Build a matrix filled with the following values depending on triviality of coefficients :
        
        - trivial, returned coefficient is 0
        
        - not trivial, returned coefficent is 1
        
        NOTE JOA : mask for coefficients ???
        
        """
          
        return np.vectorize(lambda x:int(not SIF._isTrivial(x, eps))) (X)
   
    @staticmethod
    def _build_Z_or_dZ(9matrix):
			
		"""
		build Z or dZ depending on provided matrix tuple
		"""
			
		J, K, L, M, N, P, Q, R, S = [np.matrix(X) for X in 9matrix]
			
		return np.bmat([[-J, M, N], 
						[ K, P, Q], 
						[ L, R, S]])   
    
    
    
    def __init__(self, JtoS, delta_eps=1.e-8, father_obj=None, **event_spec): # name can be specified in e_desc

        # Define default event if not specified
        # default event : SIF instance created from user interface
        
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'new')      
        my_e_subclass  = event_spec.get('e_subclass', 'SIF')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'SIF.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        SIF_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        my_father_obj = father_obj
        
        #Init superclass
        FIPObject.__init__(self, self.__class__.__name__, father_obj=my_father_obj, **SIF_event)

        self._J, self._K, self._L, self._M, self._N, self._P, self._Q, self._R, self._S = [np.matrix(X) for X in JtoS]

        # set and check sizes
        self._l, self._m, self._n, self._p = self.__check_set_dimensions__()
        
        self._Z = _build_Z_or_dZ(JtoS)

        def _build_dX(X, eps=1.e-8):
            
	    	"""
		    Build dZ from Z
		
		    During the quantization process, :math:`Z` is perturbed to become :math:`Z + r_Z \times \Delta` where
		
    		.. math:
		
		    	r_Z \triangleq \left\lbrace\begin{aligned}
	    							 W_Z \text{for fixed-point representation,}\\
			    					 2 \eta_Z \times W_Z \text{for floating-point representation,}
				    				  \end{aligned}\right.
								  
		    and :math:`\eta_Z` is such that
		
    		.. math:
		
	    		\left( \eta_Z \right)_{i,j} \left\lbrace\begin{aligned}
		    								\text{the largest absolute value of} \\
			    							\text{the block in which} Z_{i,j} \text{resides.}
				    						\end{aligned}\right.
										
    		"""
            
            return SIF._nonTrivial(X, eps)

        # Initial version of dZ from Z
        self._dZ = _build_dX(self._Z)

        # build dJ to dS because we may need those afterwards (modification)
        self._dJ, self._dK, self._dL, self._dM, self._dN, self._dP, self._dQ, self._dR, self._dS = [_build_dX(X) for X in JtoS]

        
        # AZ, BZ, CZ, DZ
        def _build_AZtoDZ(self):
        
            inv_J = np.linalg.inv(self._J)
        
            AZ = self._K * inv_J * self._M + self._P
            BZ = self._K * inv_J * self._N + self._Q
            CZ = self._L * inv_J * self._M + self._R
            DZ = self._L * inv_J * self._N + self._S
        
            return (AZ, BZ, CZ, DZ)

        self._AZ, self._BZ, self._CZ, self._DZ = self._build_AZtoDZ()
   
   	def _refresh_dZ():
			
		"""
		- rebuild dZ if some matrix from dJ to dS has changed (manual use as of 02/10/2015)
		"""
		
		dJtodS = self._dJ, self._dK, self._dL, self._dM, self._dN, self._dP, self._dQ, self._dR, self._dS
		
		self._dZ = _build_Z_or_dZ(dJtodS)
   
    def __check_set_dimensions__(self):
        
        """
        Computes the size 'l,m,n,p' of SIF
        Check size of matrixes 'J' to 'S'
        """
        
        #list_mat  = [self._J, self._K, self._L, self._M, self._N, self._P, self._Q, self._R, self._S]
        #list_size = [(l,l),   (n,l),   (p,l),   (l,n),   (l,m),   (n,n),   (n,m),   (p,n),   (p,m) ]

        # P (n,n)
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

        return (l,m,n,p)
       
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
        
        mystr = "Realization " + self.obj_events[0].e_desc + " : \n"
        mystr += "m = " + str(self._m) + " input"  + plural(self._m) + "\n"
        mystr += "p = " + str(self._p) + " output" + plural(self._p) + "\n"
        mystr += "n = " + str(self._n) + " state"  + plural(self._n) + "\n"
        mystr += "l = " + str(self._l) + " intermediate variable" + plural(self._l) + "\n"
        
        mystr += "Z = \n"+ str(self._Z) + "\n"
        
        mystr += "dZ = \n" + str(self._dZ) + "\n"
        
        #TODO show matrix Z (see matlab display method for FWR object)
        
        return mystr
