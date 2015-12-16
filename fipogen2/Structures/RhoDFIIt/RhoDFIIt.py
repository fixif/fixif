#coding=UTF8

# This class contains routine to convert to FWR

from SIF import SIF
from LTI import TF, dSS
from numpy import zeros, all, poly, matrix, sqrt, prod, transpose, diagflat, r_, c_
from numpy import matrix as mat
from numpy.linalg import cond, inv

class RhoDFIIt(SIF):

    @staticmethod
    def F2(x):
        return log2(x)-floor(log2(x))

    def __init__(self, num, den, gamma, isGammaExact = True, delta = None, isDeltaExact = False, father_obj = None, cond_limit=1.e20, **event_spec):
        
        
        
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
                
        if not delta:
            self._delta = mat(zeros(gamma.shape))
        else:
            self._delta = delta
        
        self._num = num
        self._den = den

        self._gamma = mat(gamma)
        
        Va = transpose(mat(self._den))/self._den[0]
        Vb = transpose(mat(self._num))/self._den[0]
        
        # Compare #column (#lines is 1 ?)
        p1 = Va.shape[1] - 1
        p2 = Vb.shape[1] - 1
        p3 = self._gamma.shape[1]
        p4 = self._delta.shape[1]

        if not (all(mat([p1, p2, p3]) == p4)):
            raise(ValueError, "Dimensions not coherent")
        
        p = p1
        
        # =====================================
        # Step 1 : build Valapha_bar, Vbeta_bar
        # =====================================
        
        # by considering Delta_k = 1 for all k
        
        # Build Tbar
        
        Tbar = mat(zeros((p+1,p+1)))
        Tbar[p,p] = 1
        
        for i in range(p-1,-1,-1):
            Tbar[i, i:p] = poly(self._gamma[0, i:p])# if we use matlab-like syntax, namely i:p+1 there's no check on matrix boundary (if p+1 exceeds boundary we got a result)
        
        #check for ill-conditioned matrix (relaxed check)
        
        my_cond = cond(Tbar,2)/cond(Tbar,-2) # (larger / smaller) singular value like cond() of MATLAB
        
        if (my_cond > cond_limit):
            raise('Cannot compute matrix inverse') 
        
        #Valpha_bar, Vbeta_bar
        
        Valpha_bar = transpose(inv(Tbar))* Va
        Vbeta_bar  = transpose(inv(Tbar))* Vb
        
        # Equivalent state space (Abar, Bbar, Cbar, Dbar)
        
        A0 = diagflat(mat(ones((p-1,1))),1)
        A0[0:,0] = - Valpha_bar[1:]
        
        Abar = diagflat(self._gamma) + A0
        
        Bbar = Vbeta_bar[1:] - Vbeta_bar[0,0]*Valpha_bar[0, 1:]
        
        Cbar = mat(zeros((1,p)))
        Cbar[0,0] = 1
        
        Dbar = Vbeta_bar[0,0]
        
        # ============================
        # Step 2 : L2-scaling
        # ============================
        
        # compute delta (leading to a l2-scaled realization) 
        # when delta is not given (or null)
        
        Wc = dSS(Abar, Bbar, Cbar, Dbar).Wc
        
        if (self._delta == mat(zeros(self._gamma.shape))):
            
            self._delta[0,0] = sqrt(Wc[0,0])
            
            for i in range(1,p):
                self._delta[0,i] = sqrt( Wc[i,i] / Wc[i-1,i-1] )
        
        elif delta[0,0] < 0:
            
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
            Tbar[i, i:p+1] = poly( self._gamma[0, i:p] / prod(self._delta[0, i:p]))
            
        Ka = mat(prod(self._delta[0,:]))
        
        Valpha = transpose(inv(Ka * Tbar))*Va
        Vbeta  = transpose(inv(Ka * Tbar))*Vb
        
        # equivalent l2-scaled state space
        
        d = mat(zeros((1,p)))
        
        for i in range(0, p):
            d[0,i] = inv( prod(self._delta[0, 0:i]) )

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

            State_Space.__init__(A, B, C, D)
        
            A0 = diagflat(ones((p-1,1)),1) # NOT USED ???
        
            A0[:,0] = -Valpha[0, 1:] # NOT USED ???
        
            if isGammaExact:
                for i in range(1,p):
                    self.dP[i, i] = 0 # loss of efficiency because dZ is rebuilt each time
        
            if isDeltaExact:
                for i in range(1,p):
                    self.dP[i-1, i] = 0

        elif opt == '2':

            K = diagflat(ones((1, p-1)), 1)
        
            K[:,1] = -Valpha[0, 1:p+1] # maybe transpose is needed here ?

            JtoS = eye(p), K, c_[1, zeros((1,p-1))], diagflat(delta), r_[Vbeta[0, 1], zeros((p-1, 1))], diagflat(gamma), Vbeta[0, 1:p+1], zeros((1, p)), 0
        
            SIF.__init__(JtoS)
        