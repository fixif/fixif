#coding=UTF8

# This class contains routine to convert to FWR

from SIF import SIF
from LTI import TF, dSS
from numpy import zeros, all, poly, matrix, sqrt, prod
from numpy.linalg import cond, inv, transpose, diag

class RhoDFIIt(SIF):

    @staticmethod
    def F2(x):
        return log2(x)-floor(log2(x))

    def __init__(self, num, den, gamma, isGammaExact = None, delta = None, isDeltaExact = None, father_obj = None, **event_spec):
        
        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'RhoDFIIt')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'RhoDFIIt.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        RhoDFIIt_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        RhoDFIIt_father_obj = father_obj
        
        if not isGammaExact:
            isGammaExact = True   
          
        # warning if we don't use matrixes transpose is not going to work correctly 
                
        if not delta:
            delta = matrix(zeros(gamma.shape))
            
        if not isDeltaExact:
            isDeltaExact = False
        
        self._num = num
        self._den = den
        
        self._delta = delta
        self._gamma = matrix(gamma)
        
    def toSIF(self, cond_limit = 1.e20):
        
        """
        Warning : 2 matrixes as output
        """
        
        Va = transpose(matrix(self._den))/self._den[0]
        Vb = transpose(matrix(self._num))/self._den[0]
        
        # Compare #column (#lines is 1 ?)
        p1 = Va.shape[1] - 1
        p2 = Vb.shape[1] - 1
        p3 = self._gamma.shape[1]
        p4 = self._delta.shape[1]

        if not (np.all(np.matrix([p1, p2, p3]) == p4)):
            raise("Dimensions not coherent")
        
        p = p1
        
        # =====================================
        # Step 1 : build Valapha_bar, Vbeta_bar
        # =====================================
        
        # by considering Delta_k = 1 for all k
        
        # Build Tbar
        
        Tbar = zeros((p+1,p+1))
        Tbar[p,p] = 1
        
        for i in range(p-1,-1,-1):
            Tbar[i,range(i,p)] = poly(self._gamma[1, range(i,p+1)])# if we use matlab-like syntax, namely i:p+1 there's no check on matrix boundary (if p+1 exceeds boundary we got a result)
        
        #check for ill-conditioned matrix (relaxed check)
        
        my_cond = cond(Tbar,2)/cond(Tbar,-2) # (larger / smaller) singular value like cond() of MATLAB
        
        if (my_cond > cond_limit):
            raise('Cannot compute matrix inverse') 
        
        #Valpha_bar, Vbeta_bar
        Valpha_bar = dot(transpose(inv(Tbar)), Va)
        Vbeta_bar  = dot(transpose(inv(Tbar)), Vb)
        
        # Equivalent state space (Abar, Bbar, Cbar, Dbar)
        
        A_0 = diag(matrix(ones((p-1,1))),1)
        A_0[0:,0] = - Valpha_bar[1:]
        
        Abar = diag(self._gamma) + A_0
        
        Bbar = Vbeta_bar[1:] - Vbeta_bar[0]*Valpha_bar[1:]
        
        Cbar = matrix(zeros((1,p)))
        Cbar[0,0] = 1
        
        Dbar = Vbeta_bar[0]
        
        # ============================
        # Step 2 : L2-scaling
        # ============================
        
        # compute delta (leading to a l2-scaled realization) 
        # when delta is not given (or null)
        
        Sbar = dSS(Abar, Bbar, Cbar, Dbar)
        Wc = Sbar.Wc
        
        if (self._delta == matrix(zeros(gamma.shape))):
            
            self._delta[0] = sqrt(Wc[0,0])
            
            for i in range(1,p+1):
                self._delta[i] = sqrt( Wc[i,i] / Wc[i-1,i-1] )* 2^(F2(sqrt(Wc[i-1,i-1])) - F2(sqrt(Wc[i,i])) )
                
        # compute Valpha and Vbeta
        
        Tbar = matrix(zeros((p+1,p+1)))
        
        Tbar[p,p] = 1
        
        for i in range(p-1,-1,-1):
            Tbar[i, range(i,p+2)] = poly( self._gamma[range(i,p+1)] / prod(self._delta[range(i,p+1)]))
            
        Ka = prod(self._delta[:])
        
        Valpha = dot(transpose(inv(dot(Ka, Tbar))), Va)
        Vbeta  = dot(transpose(inv(dot(Ka, Tbar))), Vb)
        
        # equivalent l2-scaled state space
        
        d = matrix(zeros((p,1)))
        
        for i in range(0, p):
            d[i] = inv(prod(self._delta(range(0, i))))

        Tsc = diag(d)
        
        A = dot(dot(Tsc, Abar),inv(Tsc))
        B = dot(Tsc, Bbar)
        C = dot(Cbar, inv(Tsc))
        D = Dbar  # can also be computed from Valpha and Vbeta
        
        S = State_Space(A,B,C,D) # TODO add special event / PROBLEM HERE REGARDING OOP
        
        A0 = diag(ones((p-1,1)),1)
        
        A0[:,0] = -Valpha[1:]
        
        # ============================
        # Step 3 : build SIF
        # ============================
               
        R2 = S.toSIF()
        
        if isGammaExact:
            
            for i in range(1,p):
                R2._dP[i, i] = 0 # should rebuild dZ after that
        
        if isDeltaExact:
            
            for i in range(1,p):
                R2._dP[i-1, i] = 0
        
        R2._refresh_dZ()
        
        # There's an old version of following code in rhoDFIIt2FWR.m
        
        K = diag(ones((1, p-1)), 1)
        
        K[:,1] = -Valpha[range(1,p+1)]
        
        
        # this is surely wrong with Vbeta
        JtoS = eye(p), K, [1,zeros((1,p-1))], diag(delta), [[Vbeta[1]],[zeros((p-1, 1))]], diag(gamma), Vbeta[range(1, p+1)], zeros((1, p)), 0
        
        R1 = SIF(JtoS)
          
        return R1, R2
        