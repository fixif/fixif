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

from numpy import c_, r_, eye, zeros, all, transpose
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
    
    def _translate_Z_AZtoDZ_W(self):
        
        """
        Calculate Z, AZtoDZ and W in the same function to factorize invU calculation
        """
        
        # _build_Z
        #             J                     K                        L              M                     N              P                        Q                 R              S
        self._build_Z((self.Y*self.J*self.W, self.invU*self.K*self.W, self.L*self.W, self.Y*self.M*self.U, self.Y*self.N, self.invU*self.P*self.U, self.invU*self.Q, self.R*self.U, self.S))
    
        self._invJ = inv(self.J)
    
        # _build_AZtoDZ
        
        self._AZ = self.invU*self._AZ*self.U
        self._BZ = self.invU*self._BZ
        self._CZ = self._CZ*self.U
        #self._DZ = self._DZ not modified by transformation
        
        self._Z_dSS = dSS(self._AZ,self._BZ,self._CZ,self._DZ)
        
        
        # update Wo and Wc if they exist
        if self._Wo is not None:
            self._Wo = transpose(self.U)*self._Wo*self.U
        
        if self._Wc is not None:
            self._Wc = self.invU*self._Wc*transpose(self.invU)
        
    
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

        # Not calculated at instance creation, consumes time and not always useful
        # All measures are initialized as None.
        
        # When the optimization routine is used, two possible ways :
        # - recalculate the value from scratch 
        # - use the existing value and UYW matrixes to get new value (if is_use_UYW_transform set to true)

        # Open-Loop and Closed-Loop
        
        
        
        self._measureTypes = ['OL','CL']

        self._MsensH = {key:None for key in self._measureTypes}
        self._MsensPole = {key:None for key in self._measureTypes}
        self._RNG = {key:None for key in self._measureTypes}

        # CL only
        self._Mstability = None        
        
        # the values of those parameters needs to be kept
        # because we have to test those against the user's input or program input
        # to know if spitting out the old result is correct or if a recalculation is needed
        self._MsensPole_moduli = None

        # set UYW attributes
        # those attributes are not used unless UYW transformation is possible on the form
        self._U = None
        self._invU = None
        self._Y = None
        self._W = None
        
        # two different cases : or we can use UYW transform, or we cannot
        # this should be modified in each subclass AFTER using the init routine of SIF class
        # if a class variable is used it implies using a metaclass
        # if an object attribute is used it implies that it's not the cleanest way, 
        # programmatically wise but avoids error (changing val at instance level does not,
        # by reference change the value at the superclass level
        #self.is_use_UYW_transform = True

        # in fact there are many different cases here : either we can use the UYW transform
        # self._formOpt = 'UYW'
        # or we can use the gammaDelta transform
        # self._formOpt = 'gammaDelta'
        # or we can use the delta transform
        # 'delta'
        
        # this parameter has to be set in each SIF subclass
        
        self._formOpt = None

        #_dynMethodAdder(SIF)

    @staticmethod
    def _check_MeasureType(fname, target, words):
        
         if target not in words:
            raise(ValueError, '{0} type not recognized (use {1})'.format(fname, ' OR '.join(words)))

    # Function to set default UYW matrixes, called in inheriting classes after init
    def _set_default_UYW(self):
    	
    	self.U = np.matrix(eye(self._n))
    	self.Y = np.matrix(eye(self._l))
    	self.W = self.Y

    # Functions to calculate measures. 
    # We keep updated closed-loop measures with stored plant at SIF instance level 
        
    # MsensH
    def MsensH(self, measureType='OL', plant=None):
        
        """
        If plant is specified here, CL will *always* be recalculated (we don't compare input with existing self._plant)
        We need input of measureType with plant = None, to get access to the stored CL value without recalculating it. 
            
        inst.MsensH(measureType='CL') gives the stored value for closed-loop case without recalculation (if there's a value) 
        or calculates from stored plant (if there's no stored value)
        """
            
        self._check_MeasureType('MsensH', measureType, self._measureTypes)
        
        is_calc_modified = False
        
        # force CL calculation if there's a plant defined in call
        if plant is not None :
                
            self.plant = plant # calculate or recalculate intermediate bar matrixes
            measureType = 'CL'
            is_calc_modified = True
                
        elif measureType == 'CL' and self.plant is None:
            
            raise(NameError, 'Cannot provide MsensH closed-loop measure as no plant is defined')
                 
        if (self._MsensH[measureType] is None) or (is_calc_modified):
                
              self._MsensH[measureType] = self.calc_MsensH(measureType)

        return self._MsensH[measureType]
      
      
    #MsensPole   
    def MsensPole(self, measureType='OL', plant=None, moduli=1):
          
        self._check_MeasureType('MsensPole', measureType, self._measureTypes)
        
        is_calc_modified = False
        
        if plant is not None:
                
            self.plant = plant # calculate or recalculate intermediate bar matrixes
            measureType = 'CL'
            is_calc_modified = True
                
        elif measureType == 'CL' and self.plant is None:
            
            raise(NameError, 'Cannot provide MsensPole closed-loop measure as no plant is defined')
        
        if not(moduli == self._MsensPole_moduli): # dangerous if not integer value
            
            self._MsensPole_moduli = moduli
            is_calc_modified = True
                               
        if (self._MsensPole[measureType] is None) or (is_calc_modified):
                
            self._MsensPole[measureType] = self.calc_MsensPole(measureType, moduli)

        return self._MsensPole[measureType]
            
    
    #RNG       
    def RNG(self, measureType='OL', plant=None, eps=None, is_rebuild_dZ = False):
            
        self._check_MeasureType('RNG', measureType, self._measureTypes)
            
        is_calc_modified = False
            
        if plant is not None:
                
            self.plant = plant # trigger recalculation of plantSIF intermediate matrixes by calling setter
            measureType = 'CL'
            is_calc_modified = True

        elif measureType == 'CL' and self.plant is None:
            
            raise(NameError, 'Cannot provide RNG closed-loop measure as no plant is defined')
        
        if (eps != self._eps) and not(eps is None):
             
            self._eps = eps
            is_calc_modified = True
            is_rebuild_dZ = True
        
        if is_rebuild_dZ:
        	self._build_dZ()
                    
        if (self._RNG[measureType] is None) or is_calc_modified:
                
            self._RNG[measureType] = self.calc_RNG(measureType, self._eps)
                
        return self._RNG[measureType]
    
    
    #Mstability        
    def Mstability(self, plant=None, moduli=1):
        
        is_calc_modified = False
        
        if plant is not None:
                
            self.plant = plant
            is_calc_modified = True
                
        elif self.plant is None:
            
            raise(NameError, 'Cannot provide Mstability measure as no plant is defined')
        
        if not(moduli == self._MsensPole_moduli):
             
            self._MsensPole_moduli = moduli
            is_calc_modified = True       
                 
        if (self._Mstability is None) or is_calc_modified:
                
            self._Mstability = self.calc_Mstability(moduli)
        
        return self._Mstability
    

    
    # Hypothesis : plant is kept UNCHANGED from start to end of _recalc routine
    
    # Sensitivity criterions are recalculated if they already exist. If they exist as None, they're untouched
    
    # This is not needed because if we use the "dumb" method we need to recalculate everything from the start
    # so we're going to use the regular __init__ from class
    
    def _recalc_sensitivity(self):
        
        for cur_type in self._measureTypes:
        
            if self._MsensH[cur_type] is not None:
                self._MsensH[cur_type] = None
                self.MsensH(measureType=cur_type)
                
            if self._MsensPole[cur_type] is not None:
                self._MsensPole[cur_type] = None
                self.MsensPole(measureType=cur_type)
                
            if self._RNG[cur_type] is not None:
                self._RNG[cur_type] = None
                self.RNG(measureType=cur_type)
                
        if self._Mstability is not None:
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
    
    def _translate_realization(self, is_rebuild_dZ = False):
        """
        This function calculates an equivalent realization by updating all instance attributes 
        that needs to be updated
        
        As a first step we update Z by transforming it,
        then the associated state space
        then Wo and Wc if they exist (and they should already exist otherwise they are going to be recalculated then transformed, for example for RNG)
        but if RNG has already been calculated, then they exist.
        We should then try to see if there is a UYW transform that needs old value of Wo and Wc, and that needs not to be calculated by initial routine
        
        """
        
        #translate from self.U, self.Y, self.W, self.invU
        self._translate_Z_AZtoDZ_W()
        
        # mimic matlab code (could it destroy information during the process, if some coeffs go under the threshold after translation to equivalent form ??)
        if is_rebuild_dZ:
            self._build_dZ()
        
        # rebuild remaining matrixes used in sensitivity calculations
        self._build_M1M2N1N2()
    
        # if there's a plant, let's rebuild all bar matrixes
        if self.plant is not None:
            self._build_plantSIF()

        # we don't call _set_check_dimensions bacause SIF dimension should remain the same
        
        
        for cur_type in self._measureTypes:
            # no need to check for Mstability because if it is present, then MsensPole has been calculated for CL case
            if (self._RNG[cur_type] is not None) or (self._MsensPole[cur_type] is not None):
                is_calc_T1T2 = True
                break
        else:
            
            is_calc_T1T2 = False
        
        # not necessary if we only need MsensH
        if is_calc_T1T2:
            
            T1, T2 = self.calc_transform_UYW()
        
        for cur_type in self._measureTypes:
            
            # uses 
            # - previous value of self._RNG[cur_type]
            # - new value of Wo calculated from UYW transform
            # - previous value of dZ
            # - previous value of M1M2Wobar for CL calculation
            if self._RNG[cur_type] is not None: # use instance attribute here, not  self.RNG() otherwise we're going to calculate it. set to None initially)             
                self.transform_UYW_RNG(cur_type, T1)
                
            if self._MsensH[cur_type] is not None:
            	self.transform_UYW_MsensH(cur_type) # FIXME uses bruteforce method ATM
            	#self._MsensH[cur_type] = None
                #self.MsensH(measureType=cur_type) # UYW transform for MsensH not defined
                
            if self._MsensPole[cur_type] is not None:
                self.transform_UYW_MsensPole(cur_type, T1, T2)
                
        if self._Mstability is not None:
            self.transform_UYW_Mstability(T1, T2)

        
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
    
    @property
    def U(self):
        return self._U
    
    @property
    def Y(self):
        return self._Y
    
    @property
    def W(self):
        return self._W
    
    @property
    def invU(self):
        return self._invU
    
    # Z, dZ getters

    # needs to be set to define properties relying on it
    # FIXME thib : find another solution
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


    # U, Y, W attributes
    @U.setter
    def U(self, mymat):
        if (mymat.shape[0] != mymat.shape[1]) or mymat.shape[0] != self._n :
            raise(ValueError, 'Wrong dimension for U')
        self._U = np.matrix(mymat)
        self._invU = inv(self._U)
        
    @Y.setter
    def Y(self, mymat):
        if (mymat.shape[0] != mymat.shape[1]) or mymat.shape[0] != self._l :
            raise(ValueError, 'Wrong dimension for Y')
        self._Y = np.matrix(mymat)       
        
    @W.setter
    def W(self, mymat):
        if (mymat.shape[0] != mymat.shape[1]) or mymat.shape[0] != self._l :
            raise(ValueError, 'Wrong dimension for W')
        self._W = np.matrix(mymat)  

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
