#coding=UTF8

# This class contains routine to convert to FWR

from SIF import SIF
from LTI import TF, dSS

from numpy import zeros, all, poly, matrix, sqrt, prod, transpose, diagflat, r_, c_, ones, atleast_2d, eye
from numpy import matrix as mat
from numpy.linalg import cond, inv

#FIXME this seems like an error should depend on SIF class see why we did this with thib
class RhoDFIIt(SIF):

    @staticmethod
    def F2(x):
        return log2(x)-floor(log2(x))

    def __init__(self, num, den, gamma=None, isGammaExact=True, delta=None, isDeltaExact=False, opt=1, cond_limit=1.e20, father_obj = None, **event_spec):

        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'RhoDFIIt')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'RhoDFIIt.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        RhoDFIIt_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        RhoDFIIt_father_obj = father_obj
          
        # warning if we don't use matrixes transpose is not going to work correctly 
              
        if gamma is None:
            raise(ValueError, "Specifying gamma is mandatory")
                
        if delta is None:
            self._delta = mat(zeros(gamma.shape))
        else:
            self._delta = mat(delta)
        
        self._num = num
        self._den = den

        self._gamma = mat(gamma)
        
        #those values needs to be stored because they are going to be used as reference by optimizeForm
        self._isGammaExact = isGammaExact
        self._isDeltaExact = isDeltaExact
        self._opt = opt
        
        # use the 'gammaDelta' method to get new form from old form
        # this value can be modified if we decide to keep gamma constant
        self._avail_formOpt = {'gammaDelta', 'delta'}
        self._formOpt = 'gammaDelta'
        #self._formOpt = 'delta'
        
        
        Va = transpose(mat(self._den))/self._den[0,0]
        Vb = transpose(mat(self._num))/self._den[0,0]
        
        # Compare #column (#lines is 1 ?)
        p1 = Va.shape[0] - 1
        p2 = Vb.shape[0] - 1
        p3 = self._gamma.shape[1]
        p4 = self._delta.shape[1]

        if not (all(mat([p1, p2, p3]) == p4)):
            raise(ValueError, "Dimensions not coherent")
        
        p = p1
        
        # =====================================
        # Step 1 : build Valapha_bar, Vbeta_bar
        # by considering Delta_k = 1 for all k
        # =====================================
        
        # Build Tbar
        
        Tbar = mat(zeros((p+1,p+1)))
        Tbar[p,p] = 1
        
        for i in range(p-1,-1,-1):
            Tbar[i, i:p+1] = poly(self._gamma[0, i:p].A1)# if we use matlab-like syntax, namely i:p+1 there's no check on matrix boundary (if p+1 exceeds boundary we got a result)
        
        #check for ill-conditioned matrix (relaxed check)
        
        my_cond = cond(Tbar,2)/cond(Tbar,-2) # (larger / smaller) singular value like cond() of MATLAB
        
        #if (my_cond > cond_limit):
        #    raise(ValueError, 'Cannot compute matrix inverse') 
        
        #Valpha_bar, Vbeta_bar
        

        Valpha_bar = transpose(inv(Tbar))* Va
        Vbeta_bar  = transpose(inv(Tbar))* Vb
        
        # Equivalent state space (Abar, Bbar, Cbar, Dbar)
        
        A0 = diagflat(mat(ones((p-1,1))),1)
        
        A0[:,0] = - Valpha_bar[1:,0]
        
        Abar = diagflat(self._gamma) + A0
        
        Bbar = Vbeta_bar[1:,0] - Vbeta_bar[0,0]*Valpha_bar[1:, 0]
        
        Cbar = mat(zeros((1,p)))
        Cbar[0,0] = 1
        
        Dbar = Vbeta_bar[0,0]
        
        # ============================
        # Step 2 : L2-scaling
        # ============================
        
        # compute delta (leading to a l2-scaled realization) 
        # when delta is not given (or null)
        
        Wc = dSS(Abar, Bbar, Cbar, Dbar).Wc
        
        if (all(self._delta == mat(zeros(self._gamma.shape)))):
            
            self._delta[0,0] = sqrt(Wc[0,0])
            
            for i in range(1,p):
                self._delta[0,i] = sqrt( Wc[i,i] / Wc[i-1,i-1] )
        
        elif self._delta[0,0] < 0:
            
            self._delta[0,0] = sqrt(Wc[0,0]) * 2^-F2(sqrt(Wc[0,0]))
            
            for i in range(1,p):
                self._delta[0,i] = sqrt(Wc[i,i] / Wc[i-1, i-1]) * 2^(F2(sqrt(Wc[i-1,i-1])) - F2(sqrt(Wc[i,i])) )
                
        # compute Valpha and Vbeta
        # compute Tbar
        
        # Tbar
        # Valpha used in A0 calculation
        #Vbeta used in second variant
        
        Tbar = mat(zeros((p+1,p+1)))
        
        Tbar[p,p] = 1
        
        for i in range(p-1,-1,-1):
            Tbar[i, i:p+1] = poly( (self._gamma[0, i:p] / prod(self._delta[0, i:p])).A1 )
        
        
            
        Ka = prod(self._delta[0,:])
        
        Valpha = transpose(inv(Ka * Tbar))*Va
        Vbeta  = transpose(inv(Ka * Tbar))*Vb
        
# Valpha, Vbeta OK
        
        # equivalent l2-scaled state space
        
        d = mat(zeros((1,p)))
        
        for i in range(0, p):    
            d[0,i] = inv( atleast_2d(prod(self._delta[0, 0:i])) ) # maybe faster to use 1 / blabla here

        # ============================
        # Step 3 : build SIF from state space or JtoS
        # ============================

        if opt == '1':

            Tsc = mat(diagflat(d))
        
            invTsc = inv(Tsc)
        
            A = Tsc*Abar*invTsc
            B = Tsc*Bbar
            C = Cbar*invTsc
            D = Dbar  # can also be computed from Valpha and Vbeta

            State_Space.__init__(self, A, B, C, D)
        
            A0 = mat(diagflat(ones((p-1,1)),1)) # NOT USED ???
        
            A0[:,0] = -Valpha[1:, 0] # NOT USED ???
        
            if isGammaExact:
                for i in range(1,p):
                    self.dP[i, i] = 0 # loss of efficiency because dZ is rebuilt each time
        
            if isDeltaExact:
                for i in range(1,p):
                    self.dP[i-1, i] = 0

        elif opt == '2':

            K = mat(diagflat(ones((1, p-1)), 1))
        
            K[:,1] = -Valpha[1:p+1, 0] # maybe transpose is needed here ?

            JtoS = eye(p), K, c_[atleast_2d(1), zeros((1,p-1))], mat(diagflat(self._delta)), r_[atleast_2d(Vbeta[1, 0]), zeros((p-1, 1))], mat(diagflat(gamma)), Vbeta[1:p+1, 0], zeros((1, p)), 0
        
            SIF.__init__(self, JtoS)
        