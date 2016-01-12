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

from numpy import c_, r_, eye, zeros, all
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
   

    def _build_Z(self, my9matrix):
            
        """
        build Z or dZ depending on provided matrix tuple
        """
            
        J, K, L, M, N, P, Q, R, S = [np.matrix(X) for X in my9matrix]
            
        self._Z =  np.bmat([[-J, M, N], 
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
            
        self._dZ = SIF._nonTrivial(self._Z, self._eps)
    
    # AZ, BZ, CZ, DZ
    # and reset Wo and Wc because when this function is called, it means either we are initializing the structure
    # or we have refreshed any of JtoS matrix which invalidates calculation of Wc and Wo
    def _build_AZtoDZ(self):

        # reset Wc and Wo attributes without recalculation
        self._Wo = None
        self._Wc = None
        
        self._AZ = self.K * self._invJ * self.M + self.P
        self._BZ = self.K * self._invJ * self.N + self.Q
        self._CZ = self.L * self._invJ * self.M + self.R
        self._DZ = self.L * self._invJ * self.N + self.S
        
        self._Z_dSS = dSS(self._AZ,self._BZ,self._CZ,self._DZ)
    
    def _build_W(self, opt):
        
        if opt == 'o':
            self._Wo = self._Z_dSS.Wo
        elif opt == 'c':
            self._Wc = self._Z_dSS.Wc
    
    def _build_M1M2N1N2(self):
        
        self._M1 = c_[self.K*self._invJ, eye(self._n), zeros((self._n, self._p))]
        self._M2 = c_[self.L*self._invJ, zeros((self._p, self._n)), eye(self._p)]
        self._N1 = r_[self._invJ*self.M, eye(self._n), zeros((self._m, self._n))]
        self._N2 = r_[self._invJ*self.N, zeros((self._n, self._m)), eye(self._m)]
    
    def _build_fromZ(self):
        
        self._build_dZ()
        self._build_AZtoDZ()
        self._build_M1M2N1N2()
    
    def _build_plantSIF(self):
    
        """
        This function sets intermediate matrixes
        for sensitivity measurements
        """
    
        # dimensions of self.plant system
    
        l, m2, n, p2 = self.size
        np, p, m = self.plant.size
        
        m1 = m - m2 
        p1 = p - p2
        
        if p1 <= 0 or m1 <= 0:
            raise(ValueError, "dimension error : check self.plant and realization dimension")
        
        
        B1 = self.plant.B[:, 0:p1]
        B2 = self.plant.B[:, p1:p]
        C1 = self.plant.C[0:m1, :]
        C2 = self.plant.C[m1:m, :]
    
        D11 = self.plant.D[0:m1, 0:p1] # correct bug from matlab code
        D12 = self.plant.D[0:m1, p1:p]
        D21 = self.plant.D[m1:m, 0:p1]
        D22 = self.plant.D[m1:m, p1:p]
    
        if not (all(D22 == zeros(D22.shape))):
            raise(ValueError, "D22 needs to be null")
        
         # closed-loop related matrices
        self._Abar = r_[ c_[self.plant.A + B2*self.DZ*C2, B2*self.CZ], c_[self.BZ*C2, self.AZ] ]
        self._Bbar = r_[ B1 + B2*self.DZ*D21, self.BZ*D21 ]
        self._Cbar = c_[ C1 + D12*self.DZ*C2, D12*self.CZ ]
        self._Dbar = D11 + D12*self.DZ*D21
        
         # intermediate matrices
        self._M1bar = r_[ c_[B2*self.L*self.invJ, zeros((np, n)), B2], c_[self.K*self.invJ, eye(n), zeros((n, p2))] ]
        self._M2bar = c_[ D12*self.L*self.invJ, zeros((m1, n)), D12 ]
        self._N1bar = r_[ c_[self.invJ*self.N*C2, self.invJ*self.M], c_[zeros((n, np)), eye(n)], c_[C2, zeros((m2, n))] ]
        self._N2bar = r_[ self.invJ*self.N*D21, zeros((n, p1)), D21 ]
    
    def _translate_Z_AZtoDZ_W(self, UYW):
        
        """
        Calculate Z, AZtoDZ and W in the same function to factorize invU calculation
        """
        
        U,Y,W = UYW
        
        U = mat(U)
        Y = mat(Y)
        W = mat(W)
        
        invU = inv(U)
        
        # _build_Z
        #             J           K              L         M           N         P              Q            R         S
        self._build_Z(Y*self.J*W, invU*self.K*W, self.L*W, Y*self.M*U, Y*self.N, invU*self.P*U, invU*self.Q, self.R*U, self.S)
    
    
        # _build_AZtoDZ
        self._AZ = invU*self._AZ*U
        self._BZ = invU*self._BZ
        self._CZ = self._CZ*U
        #self._DZ = self._DZ not modified by transformation
        
        self._Z_dSS = dSS(self._AZ,self._BZ,self._CZ,self._DZ)
        
        if self._Wo is not None:
            self._Wo = transpose(U)*self._Wo*U
        
        if self._Wc is not None:
            self._Wc = invU*self._Wc*transpose(invU)
        
    
    def __init__(self, JtoS, eps=1.e-8, plant=None, father_obj=None, **event_spec): # name can be specified in e_desc

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
        
        self._build_Z(JtoS)

        self._eps = eps

        self._invJ = inv(JtoS[0])

        # dZ from Z
        #self._build_dZ()
        # build AZ_to_DZ (implies setting or resetting wo and wc to None)
        #self._build_AZtoDZ()  
        #self._build_M1M2N1N2()
        
        # build
        # _dZ 
        # _AZ to _DZ plus associated state space _Z_dSS (implies setting _wo and _wc to None)
        # _M1 _M2 _N1 _N2

        self._build_fromZ()

        # default plant
        if plant is not None :
            self.plant = plant # calculate intermediate matrixes
        else:
            self._plant = None # do not trigger calculation : set private attribute w/o setter
            # all following matrixes are relative to a SIF-plant couple
            # they are built when self.plant setter is used
            self._Abar, self._Bbar, self._Cbar, self._Dbar, self._M1bar, self._M2bar, self._N1bar, self._N2bar = [None]*8



        # sensitivity measures
        # important note
        # those are not calculated at instance creation because it consumes time and we don't
        # know what there is to do at instance creation.
        # So all measures are initialized as None.
        # when the optimization routine is used, there are two possible ways
        # or we recalculate the value from scratch (same scenario as if value not instantiated)
        # or we use the existing value and UYW matrixes to get new value

        self._measureTypes = ['OL','CL']
        
        # OL & CL
        self._MsensH = {key:None for key in self._measureTypes}
        self._MsensPole = {key:None for key in self._measureTypes}
        self._RNG = {key:None for key in self._measureTypes}
        
        self._MsensPole_moduli = None
        self._RNG_tol = None
        
        # CL only
        self._Mstability = None
        
        # define two different cases : or we can use UYW transform, or we cannot
        # this should be modified in each subclass AFTER using the init routine of SIF class
        is_use_UYW_transform = True

    @staticmethod
    def _check_MeasureType(fname, target, words):
        
         if target not in words:
            raise(ValueError, '{0} type not recognized (use {1})'.format(fname, ' OR '.join(words)))

    # Functions to calculate measures. 
    # We keep updated closed-loop measures with stored plant at SIF instance level 
        
    def MsensH(self, measureType='OL', plant=None):
        
        """
        If plant is specified here, CL will *always* be recalculated (we don't compare input with existing self._plant)
        We need manual possible input of type because, we may want access to the stored CL MsensH without recalculating it. 
            
        inst.MsensH(measureType='CL') gives the stored value for closed-loop case without recalculation (if there's a value) 
        or calculates from stored plant (if there's no value)
        """
            
        self._check_MeasureType('MsensH', measureType, self._measureTypes)
        
        is_calc_modified = False
        
        # force CL calculation if there's a plant defined in call
        if plant is not None :
                
            self.plant = plant # calculate or recalculate intermediate bar matrixes
            measureType = 'CL'
            is_calc_modified = True
                
        elif measureType == 'CL' and self.plant is None:
            
            raise(ValueError, 'Cannot provide MsensH closed-loop measure as no plant is defined')
                 
        if (self._MsensH[measureType] is None) or (is_calc_modified):
                
              self._MsensH[measureType] = self.calc_MsensH(measureType)

        return self._MsensH[measureType]
        
    def MsensPole(self, measureType='OL', plant=None, moduli=1):
          
        self._check_MeasureType('MsensPole', measureType, self._measureTypes)
        
        is_calc_modified = False
        
        if plant is not None:
                
            self.plant = plant # calculate or recalculate intermediate bar matrixes
            measureType = 'CL'
            is_calc_modified = True
                
        elif measureType == 'CL' and self.plant is None:
            
            raise(ValueError, 'Cannot provide MsensPole closed-loop measure as no plant is defined')
        
        if not(moduli == self._MsensPole_moduli): # dangerous if not integer value
            
            self._MsensPole_moduli = moduli
            is_calc_modified = True
                               
        if (self._MsensPole[measureType] is None) or (is_calc_modified):
                
            self._MsensPole[measureType] = self.calc_MsensPole(measureType, moduli)

        return self._MsensPole[measureType]
            
            
    def RNG(self, measureType='OL', plant=None, tol=1.e-8):
            
        self._check_MeasureType('RNG', measureType, self._measureTypes)
            
        is_calc_modified = False
            
        if plant is not None:
                
            self.plant = plant # trigger recalculation of plantSIF intermediate matrixes by calling setter
            measureType = 'CL'
            is_calc_modified = True

        elif measureType == 'CL' and self.plant is None:
            
            raise(ValueError, 'Cannot provide RNG closed-loop measure as no plant is defined')
        
        if not(tol == self._RNG_tol):
             
            self._RNG_tol = tol
            is_calc_modified = True           
                    
        if (self._RNG[measureType] is None) or is_calc_modified:
                
            self._RNG[measureType] = self.calc_RNG(measureType, tol)
                
        return self._RNG[measureType]
            
    def Mstability(self, plant=None, moduli=1):
        
        is_calc_modified = False
        
        if plant is not None:
                
            self.plant = plant
            is_calc_modified = True
                
        elif self._plant is None:
            
            raise(ValueError, 'Cannot provide Mstability measure as no plant is defined')
        
        if not(moduli == self._MsensPole_moduli):
             
            self._MsensPole_moduli = moduli
            is_calc_modified = True       
                 
        if (self._Mstability is None) or is_calc_modified:
                
            self._Mstability = self.calc_Mstability(moduli)
        
        return self._Mstability
    

    
    # Hypothesis : plant is kept UNCHANGED from start to end of routine
    
    def _recalc_sensitivity(self):
        
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
    
    # use the UYW transform to get 
    # equivalent realization from existing realization
    # new values of sensitivity measurements
    
    # Order of calculations is fundamental here, otherwise we are not efficient :
	# RNG needs no other measure calculated
	# MsensH needs no other measure calculated
	# MsensPole needs MsensH calculation
	# Mstability needs MsensPole calculation
	
	# So, to MsensH and MsensPole are free once you want Mstability.
	# MsensH is free once you want MsensPole
    
    def _translate_realization(self, UYW):
        
        self._translate_Z_AZtoDZ_W(UYW)
        
        # mimic matlab code (could it destroy information during the process ??)
        self._build_dZ()
        
        # rebuild remaining matrixes
        self._buildM1M2N1N2()
    
        # if there's a plant, let's rebuild all bar matrixes
        if self.plant is not None:
            self._build_plantSIF()
        
        # rebuild plant matrixes (or erase in that case, because we don't use the usual path for recalculation ???)
        
        for cur_type in self._measureTypes:
            
            if not(self._RNG[cur_type] is None):
                
                pass
                
        

        
    # if plant is new then we renew plant in SIF to have data updated @ same time.
    # a SIF cannot keep two value for two different plant at the same time
        
    @property
    def plant(self):
        return self._plant
        
    # if plant is modified, then all matrixes relative to SIF-plant couple are recalculated (keep them
    # up-to-date and ready to use for all sensitivity calculations
        
    @plant.setter
    def plant(self, mymat):
        self._plant = mymat
        self._build_plantSIF()
        

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
        
        if self._Wo is None:
            self._build_W('o')
        
        return self._Wo
    
    @property
    def Wc(self):
        
        if self._Wc is None:
            self._build_W('c')
        
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

    # Only for coherence we define properties for all plantSIF matrixes event if slower.
    # May be useful in the future
    
    #Abar to Dbar
    
    @property
    def Abar(self):
        return self._Abar
    
    @property
    def Bbar(self):
        return self._Bbar
    
    @property
    def Cbar(self):
        return self._Cbar
    
    @property
    def Dbar(self):
        return self._Dbar
    
    #M1bar to N2bar
    
    @property
    def M1bar(self):
        return self._M1bar
    
    @property
    def M2bar(self):
        return self._M2bar
    
    @property
    def N1bar(self):
        return self._N1bar
    
    @property
    def N2bar(self):
        return self._N2bar
    
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
        self._invJ = inv(self.J) 
        self._build_fromZ()
  
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
    # J to N : we rebuild all matrixes

    @J.setter
    def J(self, mymat):
        self._Z[ 0 : self._l, 0 : self._l ] = - mymat
        self._invJ = inv(mymat)
        self._build_fromZ()

    @K.setter
    def K(self, mymat):
        self._Z[ self._l : self._l+self._n, 0 : self._l ] = mymat
        self._build_fromZ()
        
    @L.setter
    def L(self, mymat):
        self._Z[ self._l+self._n : self._l+self._n+self._p, 0:self._l ] = mymat
        self._build_fromZ()

    @M.setter
    def M(self, mymat):
        self._Z[ 0 : self._l, self._l : self._l + self._n ] = mymat
        self._build_fromZ()
        
    @N.setter
    def N(self, mymat):
        self._Z[ 0 : self._l, self._l+self._n : self._l+self._n+self._m] = mymat
        self._build_fromZ()
    
    # no need to rebuild M1M2N1N2 in the following cases
    
    @P.setter
    def P(self, mymat):
        self._Z[ self._l : self._l+self._n, self._l : self._l + self._n ] = mymat
        self._build_dZ()
        self._build_AZtoDZ() 
    @Q.setter
    def Q(self, mymat):
        self._Z[ self._l : self._l+self._n, self._l+self._n : self._l+self._n+self._m] = mymat
        self._build_dZ()
        self._build_AZtoDZ() 
    @R.setter
    def R(self, mymat):
        self._Z[ self._l+self._n : self._l+self._n+self._p, self._l : self._l + self._n ] = mymat
        self._build_dZ()
        self._build_AZtoDZ() 
    @S.setter
    def S(self, mymat):
        self._Z[ self._l+self._n : self._l+self._n+self._p, self._l+self._n : self._l+self._n+self._m] = mymat
        self._build_dZ()
        self._build_AZtoDZ() 

    #dJtodS setters
    # we only modify dZ matrix so no need to rebuild anything

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
