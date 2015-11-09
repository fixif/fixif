#coding=utf8

from SIF import SIF
from State_Space import State_Space


from numpy import matrix as mat
from numpy import zeros, diag, real, imag, diagflat
from numpy.linalg import eig, lstsq

# relaxedl2scaling
from numpy import ones, log2, floor, sqrt #diagflat

class ModalDelta(SIF):

    def canon_modal(A, B, C, D):
        
        """
        Canon modal form of dSS
        """
        
        A = mat(A)
        B = mat(B)
        C = mat(C)
        D = mat(D)
        
        # Modal form
        mylambda, E = eig(A)
        
        V = diagflat(mylambda)
        
        T = mat(zeros((A.shape[0], A.shape[1])))
        
        if np.all(np.isreal(A)):
            
            # transformation to modal form based on eigenvectors
            
            k = 0
            
            while k <= (mylambda.shape[0]-1):
          
                if not(imag(mylambda[k]) == 0):
                    
                    rel = real(mylambda[k])
                    iml = imag(mylambda[k])
                    T[:,k] = real(V[:,k])
                    T[:,k+1] = imag(V[:,k])
                    E[k:k+1,k:k+1] = c_[r_[rel, iml],r_[-iml, rel]]
                    k = k + 2
                    
                else:
                    
                    T[:,k] = V[:,k]
                    k = k + 1
            
        else:
            
            T = V
            
        
        A = E
        B = lstsq(T, B)[0]
        C = C*T
        D = D
        
        return A, B, C, D
  
    def relaxedl2scaling(mySIF, Umax=None, delta=None):
        
        # change of behaviour vs. old code : if Umax is specified it overrides other data
        
        if Umax is None:
        
            if not hasattr(mySIF, 'FPIS'):
                Umax = 1 # any power of 2
            else:
                Umax = mySIF.FPIS.Umax
        
        if delta is None:
            delta = 1
            
        # SISO test
        
        l, m, n, p = mySIF.size()
        
        if not (not(m == 1) and not(p == 1)):
            raise('The system must be SISO!')
        
        # alpha
        
        if not hasattr(mySIF, 'FPIS'):
            alphaX = mat(- ( log2(Umax) - floor(log2(Umax)) )*ones((n, 1)))
            alphaT = mat(- ( log2(Umax) - floor(log2(Umax)) )*ones((l, 1)))
        else:
            alphaX = mat( mySIF.FPIS.betaX - (mySIF.FPIS.betaU + log2(Umax) - floor(log2(Umax)))*ones(n, 1))
            alphaT = mat( mySIF.FPIS.betaT - (mySIF.FPIS.betaU + log2(Umax) - floor(log2(Umax)))*ones(l, 1))
            
        # U, V, W transformation matrixes
        
        def toto(self, M, alpha = None, beta = None):
            
            if alpha is not None:
                
                d = delta*sqrt(diagflat(M))
                
                #WORK_MARKER
                
        
        return SIF, Y ,W
        
  
    def __init__(self, A, B, C, D, Delta = None, isDeltaExact = None, father=None, **event_spec):
    
        #create default event if no event given
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'convert')      
        my_e_subclass  = event_spec.get('e_subclass', 'ModalDelta')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'ModalDelta.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        Modal_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        ModalDelta_father_obj = father_obj
    
        Aq = mat(A)
        Bq = mat(B)
        Cq = mat(C)
        Dq = mat(D)
    
        if Delta is None:
            Delta = zeros((1, Aq.shape[0]))
            isDeltaExact = True
        elif (Delta is not None and isDeltaExact is None):
            isDeltaExact = False
    
        # Conflit dans le code matlab, voir ModalDelta2FWR.m
    
        #if isDeltaExact is None: # see https://www.python.org/dev/peps/pep-0008/#id42 / point 2
        #isDeltaExact = False
        
    
        n = Aq.shape[0]
        
        A, B, C, D = canon_modal(Aq, Bq, Cq, Dq)
        
        R_modale = State_Space(A, B, C, D)
    
        #R_modale = State_Space(canon_modal(mat(A), mat(B), mat(C), mat(D)))
    
    
