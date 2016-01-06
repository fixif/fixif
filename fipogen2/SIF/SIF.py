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

from LTI import dSS

from TRK.FIPObject import FIPObject

from func_aux import _dynMethodAdder

import numpy as np

from numpy import c_, r_, eye, zeros
from numpy.linalg import inv

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
    def _build_Z(my9matrix):
            
        """
        build Z or dZ depending on provided matrix tuple
        """
            
        J, K, L, M, N, P, Q, R, S = [np.matrix(X) for X in my9matrix]
            
        return np.bmat([[-J, M, N], 
                        [ K, P, Q], 
                        [ L, R, S]])   

    def _build_dZ(self):
            
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
            
        return SIF._nonTrivial(self._Z, self._eps)
    
    # AZ, BZ, CZ, DZ
    def _build_AZtoDZ(self):
        
        AZ = self.K * self._invJ * self.M + self.P
        BZ = self.K * self._invJ * self.N + self.Q
        CZ = self.L * self._invJ * self.M + self.R
        DZ = self.L * self._invJ * self.N + self.S
        
        temp_dSS = dSS(AZ,BZ,CZ,DZ)
        
        Wo = temp_dSS.Wo
        Wc = temp_dSS.Wc
        
        return (AZ, BZ, CZ, DZ, Wo, Wc)
    
    def _build_M1M2N1N2(self):
        
        M1 = c_[self.K*self._invJ, eye(self._n), zeros((self._n, self._p))]
        M2 = c_[self.L*self._invJ, zeros((self._p, self._n)), eye(self._p)]
        N1 = r_[self._invJ*self.M, eye(self._n), zeros((self._m, self._n))]
        N2 = r_[self._invJ*self.N, zeros((self._n, self._m)), eye(self._m)]
        
        return (M1, M2, N1, N2)
    
    def __init__(self, JtoS, eps=1.e-8, father_obj=None, **event_spec): # name can be specified in e_desc

        # Define default event if not specified
        # default : SIF instance created from user interface
        
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'new')      
        my_e_subclass  = event_spec.get('e_subclass', 'SIF')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'SIF.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        SIF_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        my_father_obj = father_obj
        
        #Init FIPObject superclass
        FIPObject.__init__(self, self.__class__.__name__, father_obj=my_father_obj, **SIF_event)

        # set and check sizes
        self._l, self._m, self._n, self._p = self.__check_set_dimensions__(JtoS)
        
        self._Z = SIF._build_Z(JtoS)

        self._eps = eps

        # dZ from Z
        self._dZ = self._build_dZ()
        
        self._invJ = inv(JtoS[0])

        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()  

        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()

        # sensitivity measures
        # important note
        # those are not calculated at instance creation because it consumes time and we don't
        # know what there is to do at instance creation.
        # So all measures are initialized as None.
        # when the optimization routine is used, there are two possible ways
        # or we recalculate the value from scratch (same scenario as if value not instantiated)
        # or we use the existing value and UYW matrixes to get new value
        
        # ATM we can only set plant after obj creation
        self._plant = None

        self._measureTypes = ['OL','CL']
        
        # OL & CL
        self._MsensH = {key:None for key in self._measureTypes}
        self._MsensPole = {key:None for key in self._measureTypes}
        self._RNG = {key:None for key in self._measureTypes}
        
        # CL only
        self._Mstability = None

    @staticmethod
    def _check_MeasureType(fname, target, words):
        
         if target not in words:
            raise(ValueError, '{0} type not recognized (use {1})'.format(fname, ' OR '.join(words)))
        

        
    # Functions to calculate measures. 
    # We keep updated closed-loop measures with stored plant at SIF instance level 
        
    def MsensH(self, measureType='OL', plant=None):
        """
        If plant is specified here, CL will *always* be recalculated (we don't compare input with existing _plant)
        We need manual possible input of type because, we may want access to the stored CL MsensH without recalculating it. 
            
        inst.MsensH(measureType='CL')
        """
            
        self._check_MeasureType('MsensH', measureType, self._measureTypes)
        
        cur_plant = None
        
        # force CL calculation if there's a plant
        if plant is not None :
                
            self._plant = plant
            measureType = 'CL'
            is_plant_modified = True
            cur_plant = plant
                
        else:
                
            is_plant_modified = False
                
            if measureType == 'CL':
                    
                if self._plant is None:
                     raise(ValueError, 'Cannot provide MsensPole closed-loop measure as no plant is defined')
                                
                cur_plant = self._plant
                 
        if (self._MsensH[measureType] is None) or (is_plant_modified):
                
              self._MsensH[measureType] = self.calc_MsensH(loc_plant = cur_plant)

        return self._MsensH[measureType]
        
    def MsensPole(self, measureType = 'OL', plant = None, moduli=1):
          
        self._check_MeasureType('MsensPole', measureType, self._measureTypes)
            
        cur_plant = None
            
        if plant is not None:
                
            self._plant = plant
            measureType = 'CL'
            is_plant_modified = True
            cur_plant = plant
                
        else:
                
            is_plant_modified = False
                
            if measureType == 'CL':
                    
                if self._plant is None:
                    raise(ValueError, 'Cannot provide MsensPole closed-loop measure as no plant is defined')
                                
                cur_plant = self._plant
                                
        if (self._MsensPole[measureType] is None) or (is_plant_modified):
                
            self._MsensPole[measureType] = self.calc_MsensPole(loc_plant = cur_plant, moduli = moduli)

        return self._MsensPole[measureType]
            
            
    def RNG(self, measureType = 'OL', plant=None):
            
        self._check_MeasureType('RNG', measureType, self._measureTypes)
            
        cur_plant = None
            
        if plant is not None:
                
            self._plant = plant
            measureType = 'CL'
            is_plant_modified = True
            cur_plant = plant
                                
        else:
                
            is_plant_modified = False
                
            if measureType == 'CL':
                    
                if self._plant is None:
                    raise(ValueError, 'Cannot provide RNG closed-loop measuer as no plant is defined')
                    
                cur_plant = self._plant
                    
        if (self._RNG[measureType] is None) or is_plant_modified:
                
            self._RNG[measureType] = self.calc_RNG(loc_plant = cur_plant)
                
        return self._RNG[measureType]
            
    def Mstability(self, plant=None):
            
        if plant is not None:
                
            self._plant = plant
            is_plant_modified = True
                
        else:
                
            is_plant_modified = False            
            
            if self._plant is None:
                raise(ValueError, 'Cannot provide Mstability measure as no plant is defined')
                   
        if (self._Mstability is None) or is_plant_modified:
                
            self._Mstability = self.calc_Mstability(self._plant)
        
        return self._Mstability
    
    def _refresh_sensitivity(self):
        
        for cur_type in self._measureTypes:
        
            if not(self._MsensH[cur_type] is None):
                self._MsensH[cur_type] = None
                self.MsensH(measureType=cur_type)
                
            if not(self._MsensPole[cur_type] is None):
                self._MsensPole[cur_type] = None
                self.MsensPole(measureType=cur_type)
                
            if not(self._RNG[cur_type] is None):
                self._RNG[cur_type] = None
                self.RNG(measureType=cur_type)
                
        if not(self._Mstability is None):
            self._Mstability = None
            self.Mstability()
        
        
    # if plant is new then we renew plant in SIF to have data updated @ same time.
    # a SIF cannot keep two value for two different plant at the same time
        
    @property
    def plant(self):
        return _plant(self)
        
    @plant.setter
    def plant(self, mymat):
        self._plant = mymat    

    # Only matrix Z is kept in memory
    # JtoS extracted from Z matrix, dJtodS from dZ resp.

    @property
    def invJ(self):
        return self._invJ

    # AZ to DZ getters
    
    @property
    def AZ(self):
        return self._AZ
    
    @property
    def BZ(self):
        return self._BZ
    
    @property    
    def CZ(self):
        return self._CZ
    
    @property    
    def DZ(self):
        return self._DZ

    # Wo and Wc are from AZ to DZ state space

    @property
    def Wo(self):
        return self._Wo
    
    @property
    def Wc(self):
        return self._Wc

    # M1 to N2 are used in sensitivity calculations

    @property
    def M1(self):
        return self._M1
    
    @property
    def M2(self):
        return self._M2
        
    @property
    def N1(self):
        return self._N1
    
    @property
    def N2(self):
        return self._N2
    
    # Z, dZ getters

    _l, _m, _n, _p = (0, 0, 0, 0)

    @property
    def Z(self):
        return self._Z
       
    @property
    def dZ(self):
        return self._dZ

    # Z, dZ setters

    @Z.setter
    def Z(self, mymat):
        self._Z = mymat
        self._dZ = self._build_dZ(self._eps)
        self._invJ = inv(self.J)
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()
        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()
        
    @dZ.setter
    def dZ(self, mymat):
        self._dZ = mymat
        
    # JtoS getters

    @property
    def J(self):
        return -self._Z[ 0 : self._l, 0 : self._l ]
    @property
    def K(self):
        return self._Z[ self._l : self._l+self._n, 0 : self._l ]   
    @property
    def L(self):
        return self._Z[ self._l+self._n : self._l+self._n+self._p, 0:self._l ]  
    @property
    def M(self):
        return self._Z[ 0 : self._l, self._l : self._l + self._n ]
    @property
    def N(self):
        return self._Z[ 0 : self._l, self._l+self._n : self._l+self._n+self._m]
    @property
    def P(self):
        return self._Z[ self._l : self._l+self._n, self._l : self._l + self._n ]
    @property
    def Q(self):
        return self._Z[ self._l : self._l+self._n, self._l+self._n : self._l+self._n+self._m]
    @property
    def R(self):
        return self._Z[ self._l+self._n : self._l+self._n+self._p, self._l : self._l + self._n ]
    @property
    def S(self):
        return self._Z[ self._l+self._n : self._l+self._n+self._p, self._l+self._n : self._l+self._n+self._m]

    # dJtodS getters

    @property
    def dJ(self):
        return -self._dZ[ 0 : self._l, 0 : self._l ]
    @property
    def dK(self):
        return self._dZ[ self._l : self._l+self._n, 0 : self._l ]   
    @property
    def dL(self):
        return self._dZ[ self._l+self._n : self._l+self._n+self._p, 0:self._l ]  
    @property
    def dM(self):
        return self._dZ[ 0 : self._l, self._l : self._l + self._n ]
    @property
    def dN(self):
        return self._dZ[ 0 : self._l, self._l+self._n : self._l+self._n+self._m]
    @property
    def dP(self):
        return self._dZ[ self._l : self._l+self._n, self._l : self._l + self._n ]
    @property
    def dQ(self):
        return self._dZ[ self._l : self._l+self._n, self._l+self._n : self._l+self._n+self._m]
    @property
    def dR(self):
        return self._dZ[ self._l+self._n : self._l+self._n+self._p, self._l : self._l + self._n ]
    @property
    def dS(self):
        return self._dZ[ self._l+self._n : self._l+self._n+self._p, self._l+self._n : self._l+self._n+self._m]

    # JtoS setters

    @J.setter
    def J(self, mymat):
        self._Z[ 0 : self._l, 0 : self._l ] = - mymat
        self._dZ = self._build_dZ()
        self._invJ = inv(mymat)
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()
        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()
    @K.setter
    def K(self, mymat):
        self._Z[ self._l : self._l+self._n, 0 : self._l ] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()
        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()
    @L.setter
    def L(self, mymat):
        self._Z[ self._l+self._n : self._l+self._n+self._p, 0:self._l ] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()
        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()
    @M.setter
    def M(self, mymat):
        self._Z[ 0 : self._l, self._l : self._l + self._n ] = mymat
        self._dZ = self._build_dZ(self._eps)
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()
        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()
    @N.setter
    def N(self, mymat):
        self._Z[ 0 : self._l, self._l+self._n : self._l+self._n+self._m] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ()
        self._M1, self._M2, self._N1, self._N2 = self._build_M1M2N1N2()
    @P.setter
    def P(self, mymat):
        self._Z[ self._l : self._l+self._n, self._l : self._l + self._n ] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ() 
    @Q.setter
    def Q(self, mymat):
        self._Z[ self._l : self._l+self._n, self._l+self._n : self._l+self._n+self._m] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ() 
    @R.setter
    def R(self, mymat):
        self._Z[ self._l+self._n : self._l+self._n+self._p, self._l : self._l + self._n ] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ() 
    @S.setter
    def S(self, mymat):
        self._Z[ self._l+self._n : self._l+self._n+self._p, self._l+self._n : self._l+self._n+self._m] = mymat
        self._dZ = self._build_dZ()
        self._AZ, self._BZ, self._CZ, self._DZ, self._Wo, self._Wc = self._build_AZtoDZ() 

    #dJtodS setters

    @dJ.setter
    def dJ(self, mymat):
        self._dZ[ 0 : self._l, 0 : self._l ] = mymat
    @dK.setter
    def dK(self, mymat):
        self._dZ[ self._l : self._l+self._n, 0 : self._l ] = mymat
    @dL.setter
    def dL(self, mymat):
        self._dZ[ self._l+self._n : self._l+self._n+self._p, 0:self._l ] = mymat
    @dM.setter
    def dM(self, mymat):
        self._dZ[ 0 : self._l, self._l : self._l + self._n ] = mymat
    @dN.setter
    def dN(self, mymat):
        self._dZ[ 0 : self._l, self._l+self._n : self._l+self._n+self._m] = mymat
    @dP.setter
    def dP(self, mymat):
        self._dZ[ self._l : self._l+self._n, self._l : self._l + self._n ] = mymat
    @dQ.setter
    def dQ(self, mymat):
        self._dZ[ self._l : self._l+self._n, self._l+self._n : self._l+self._n+self._m] = mymat
    @dR.setter
    def dR(self, mymat):
        self._dZ[ self._l+self._n : self._l+self._n+self._p, self._l : self._l + self._n ] = mymat
    @dS.setter
    def dS(self, mymat):
        self._dZ[ self._l+self._n : self._l+self._n+self._p, self._l+self._n : self._l+self._n+self._m] = mymat  



    def __check_set_dimensions__(self, JtoS):
        
        """
        Compute the size 'l, m, n, p' of SIF
        
        Check size of matrixes 'J' to 'S'
        """
        
        #list_mat  = [self._J, self._K, self._L, self._M, self._N, self._P, self._Q, self._R, self._S]
        #list_size = [(l,l),   (n,l),   (p,l),   (l,n),   (l,m),   (n,n),   (n,m),   (p,n),   (p,m) ]

        #print(JtoS)

        J, K, L, M, N, P, Q, R, S = [np.matrix(X) for X in JtoS]


        # P (n,n)
        s1,s2 = P.shape
        
        if (s1 != s2):
            raise ValueError, 'P should be a square matrix'
        else:
            n = s1 # set n from P
        
        # J (l,l)
        s1,s2 = J.shape
        
        if (s1 != s2):
            raise ValueError, 'J should be a square matrix'
        else:
            l = s1 # set l from J
        
        # K (n,l)
        s1,s2 = K.shape
        
        if (s1 != n) or (s2 != l):
            raise ValueError, 'Dimensions of matrix K not coherent with dimensions of P and/or J'

        # L (p,l)
        s1,s2 = L.shape
        
        if (s2 != l):
            raise ValueError, 'Dimension 2 of matrix L not coherent with dimension of J'
        else:
            p = s1 # set p from L
        
        # M (l,n)
        
        s1,s2 = M.shape
        
        if (s1 != l) or (s2 != n):
            raise ValueError, 'Dimensions of matrix M not coherent with dimensions of P and/or J'
        
        # N (l,m)
        s1,s2 = N.shape
        
        if (s1 != l):
            raise ValueError, 'Dimension 1 of matrix N not coherent with dimensions of J'
        else:
            m = s2 # set m from N
        
        # Q (n,m)
        s1,s2 = Q.shape
        
        if (s1 != n) or (s2 != m):
            raise ValueError, 'Dimensions of Q not coherent with dimensions of P and/or N'
        
        # R (p,n)
        
        s1,s2 = R.shape
        
        if (s1 != p) or (s2 != n):
            raise ValueError, 'Dimensions of R not coherent with dimensions of L and/or P'
        
        # S (p,m)
        s1,s2 = S.shape
        
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
            
            if (n > 1): str='s'
            else: str=''
            
            return str
        
        mystr = "Realization {0} : \n".format(self.obj_events[0].e_desc)
        mystr += "m = {0} input{1} \n".format(self._m, plural(self._m))
        mystr += "p = {0} output{1} \n".format(self._p, plural(self._p))
        mystr += "n = {0} state{1} \n".format(self._n, plural(self._n))
        mystr += "l = {0} intermediate variable{1} \n".format(self._l, plural(self._l))
        
        mystr += "eps = {}".format(self._eps) + "\n"
        
        mystr += "Z = \n"+ str(self._Z) + "\n"
        
        mystr += "dZ = \n" + str(self._dZ) + "\n"
        
        #TODO show matrix Z (see matlab display method for FWR object)
        
        return mystr

# Add additional methods SIF_othermoethods.py 
# from modules in current folder
_dynMethodAdder(SIF)
