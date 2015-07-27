# coding=utf8

"""Blablabla"""

# Object and "methods" for a Discrete State Space
# 2015 LIP6

from numpy                import inf, shape, identity, absolute, dot, eye#, astype
from numpy                import matrix as mat

from numpy.linalg         import inv, det, solve
from numpy.linalg.linalg  import LinAlgError

from scipy.linalg         import solve_discrete_lyapunov

# slycot method for observers Wo and Wc
from copy                 import copy
from slycot               import sb03md

#WCPG calculation needs mpmath
from mpmath import mp

# Module description
__author__ = "FiPoGen Team"
__email__ = "fipogen@lip6.fr"
__license__ = "CECILL-C"
__version__ = "0.0.1"  # Modify this to increment with git scripting

class dSS(object):

    r"""
    The dSS class describes a discrete state space realization
       
     A state space system :math:`(A,B,C,D)` is defined by 
      
    .. math::
       
        \left\lbrace\begin{aligned}
         X(k+1) &= AX(k) + BU(k) \\
         Y(k)   &= CX(k) + DU(k)
         \end{aligned}\right.


    with :math:`A \in \mathbb{R}^{n \times n}, B \in \mathbb{R}^{n \times p}, C \in \mathbb{R}^{q \times n} \text{ and } D \in \mathbb{R}^{q \times p}`. 
    

    **Dimensions of the state space :**
       
    .. math::
       :align: left
       
         n,p,q \in \mathbb{N}
         
    ==  ==================
    n   number of states
    p   number of inputs
    q   number of outputs
    ==  ==================

       Additional data available, computed once when asked for :
       dSS.Wo, dSS.Wc, dSS.norm_h2, dSS.WCPG
    
       - Observers : Wo and Wc
       - "Norms"   : H2-norm (norm_h2), Worst Case Peak Gain (WCPG) (see doc for each)
    """

    def __init__(self, A, B, C, D):

        """
        Construction of a discrete state space
        """

        self._A = mat(A)  # User input
        self._B = mat(B)
        self._C = mat(C)
        self._D = mat(D)

        # Initialize state space dimensions from user input

        (self._n, self._p, self._q) = self.__check_dimensions__()  # Verify coherence, set dimensions
        
        # Initialize observers and method for computation of those
        
        self._W_method = 'slycot1'  # linalg, slycot1
        self._Wo = None
        self._Wc = None 

        # Initialize norm

        self._norm_h2 = None

        # Other criterions,values

        self._DC_gain = None
        
        # WCPG
        self._WCPG = None
        
        # set precision for mpmath
        mp.dps = 64
        



    # Properties

    @property
    def A(self):
        return self._A

    @property
    def B(self):
        return self._B

    @property
    def C(self):
        return self._C

    @property
    def D(self):
        return self._D

    @property
    def n(self):
        return self._n

    @property
    def p(self):
        return self._p

    @property
    def q(self):
        return self._q

    @property
    def Wo(self):
        if (self._Wo is None): self.calc_W('Wo', self._W_method)
        return self._Wo

    @property
    def Wc(self):
        if (self._Wc is None): self.calc_W('Wc', self._W_method)
        return self._Wc

    @property
    def norm_h2(self):
        if (self._norm_h2 is None): self.calc_h2()
        return self._norm_h2

    @property
    def WCPG(self):
        if (self._WCPG is None): self.calc_WCPG()
        return self._WCPG

    @property
    def DC_gain(self):
        if (self._DC_gain is None): self.calc_DC_gain()
        return self._DC_gain



    #======================================================================================#      
    # Observers (Wo, Wc) calculation
    #======================================================================================#

    def calc_W(self, Woc, meth):

        """
        Computes observers :math:`Wo` and :math:`Wc` as :

        :math:`W_o` is solution of equation :

        .. math::
        
           A^T * W_o * A + C^T * C = W_o
           
        :math:`W_c` is solution of equation :
        
        .. math::

           A * W_c * A^T + B * B^T = W_c
        
        Available methods :
        
        - ``linalg`` : ``scipy.linalg.solve_discrete_lyapunov``, 4-digit precision with small sizes,
        1 digit precision with bilinear algorithm for big matrixes (really bad). 
        not good enough with usual python data types
        
        - ``slycot1`` : using ``slycot`` lib with func ``sb03md``, like in [matlab ,pydare]
        see http://slicot.org/objects/software/shared/libindex.html
        
        ..Example::
        
          >>>mydSS = random_dSS() ## define a new state space from random data
          >>>mydSS.calc_W('Wo','linalg') # use numpy
          >>>mydSS.calc_W('Wo','slycot1') # use slycot
          >>>mydSS.calc_W('Wc','linalg')
          >>>mydSS.calc_W('Wc','slycot1')    

        .. warning::
        
           solve_discrete_lyapunov does not work as intended, see http://stackoverflow.com/questions/16315645/am-i-using-scipy-linalg-solve-discrete-lyapunov-correctl
           Precision is not good (4 digits, failed tests)
           
        .. todo::
        
           - octave routine in http://octave.sourceforge.net/control/function/dlyap.html uses another function from slicot
           - scilab routine https://www.scilab.org/product/man/linmeq.html uses slicot too

        """
        
        # DEVNOTE / We could try to use mpmath in the current function as a test bench for gain in precision using multiprecision
        # data types
        
        if (self._W_method == 'linalg'):
            
          try:
              
              if (Woc == 'Wo'):
                  
                X = solve_discrete_lyapunov(self._A.transpose(), self._C.transpose() * self._C)
                self._Wo = mat(X)
                
              elif (Woc == 'Wc'):
                  
                X = solve_discrete_lyapunov(self._A, self._B * self._B.transpose())
                self._Wc = mat(X)
                
              else: raise "unknown Woc for W calculation"
            
          except LinAlgError, ve:

              if (ve.info < 0):
                  e = LinAlgError(ve.message)
                  e.info = ve.info
              else:
                  e = LinAlgError(Woc + " : " + "scipy Linalg failed to compute eigenvalues of Lyapunov equation")
                  e.info = ve.info
              raise e

        # Solve the Lyapunov equation by calling the Slycot function sb03md
        # If we don't use "copy" in the call, the result is plain false
          
        elif (self._W_method == 'slycot1'):
            
            try:
                if (Woc == 'Wo'):
                    
                  X, scale, sep, ferr, w = sb03md(self.n, -self._C.transpose() * self._C, copy(self._A.transpose()), eye(self.n, self.n), dico='D', trana='T')
                  self._Wo = mat(X)
                  
                elif (Woc == 'Wc'):
                    
                  X, scale, sep, ferr, w = sb03md(self.n, -self._B * self._B.transpose(), copy(self._A), eye(self.n, self.n), dico='D', trana='T')
                  self._Wc = mat(X)
                  
                else: raise "unknown Woc for W calculation"
                
            except ValueError, ve:
                
              if ve.info < 0:
                e = ValueError(ve.message)
                e.info = ve.info
              else:
                e = ValueError(Woc + " : " + "The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
                e.info = ve.info
              raise e
        
        else: raise "unknown _W_method to calculate observers"

               
    #======================================================================================#      
    # Norms calculation
    #======================================================================================#

    def calc_h2(self):

        r"""
        Compute the H2-norm of the system
        
        .. math::
        
           \langle \langle H \rangle \rangle = \sqrt{tr ( C*W_c * C^T + D*D^T )}
        
        """

        res = None

        try:
            M = self._C * self._Wc * self._C.transpose() + self._D * self._D.transpose()
        except:
            res = inf
            raise ValueError, "Impossible to compute H2-norm of current discrete state space. Default value is 'inf'" 
        else:
            res = sqrt(M.trace())

        self._norm_h2 = res

        return

    #======================================================================================#
    def calc_WCPG(self, n_it):

        r"""
        Compute the Worst Case Peak Gain of the state space

        .. math::

           \langle \langle H \rangle \rangle \triangleq |D| + \sum_{k=0}^\infty |C * A^k * B|
        
        Using algorithm developed in paper :
        
        [CIT001]_
        
        .. [CIT001]
        
           Lozanova & al., calculation of WCPG
        
        """
        
        def cast2uint64(val): # uint64_t type in C
          
            cast_val = val.astype(uint64)
          
            return cast_val
      
        def flatten2float64(matrix): # long type int C
            
            flat_mat = matrix.astype(float64, casting='safe').flatten()
            
            return flat_mat
        
        # Prepare array for result
        
        c_WCPG = mp.matrix(self._n, self._n)
        
        # Convert array dimensions to uint64
        #n = self._n.np.astype(uint64)
        
        n = cast2uint64(self._n)
        p = cast2uint64(self._p)
        q = cast2uint64(self._q)
        
        # Convert numpy matrixes to mpmath matrix
        
        #A = array2mp(self._A)
        #B = array2mp(self._B)
        #C = array2mp(self._C)
        #D = array2mp(self._D)
        
        # create matrix for result
        
        loc_WCPG = flatten2float64(mp.matrix(self._n,self._n))

        # convert matrix to 1D array
        
        A = flatten2float64(self._A)
        B = flatten2float64(self._B)
        C = flatten2float64(self._C)
        D = flatten2float64(self._D)
        
        

        
        # CALL WCPG IN DOUBLE PRECISION
        
        #A = self._A.astype(float64, casting='safe').flatten()



        
        # Method not precise
        # res = 0

        # try:
        #    for i in range(1, self._nit_WCPG):
        #        res += numpy.absolute(self._C * matrix_power(A, i) * B)
        #        #res += numpy.absolute(self._C * A**i * B)
        # except:
        #    raise ValueError, 'Impossible to compute WCPG at rank i = ' + str(i) + "\n"
        # else:
        #    self._WCPG = res + absolute(D)

        self._WCPG = mparray2npfloat(c_WCPG)

    #======================================================================================#
    def calc_DC_gain(self):

        r"""
        Compute the DC-gain of the filter

        .. math::

           \langle H \rangle = C * (I_n - A)^{-1} * B + D
        """

        try:
            self._DC_gain = self._C * inv(identity(self._n) - self._A) * self._B + self._D
        except:
            raise ValueError, 'Impossible to compute DC-gain from current discrete state space'

        return self._DC_gain  

    #======================================================================================#
    def __check_dimensions__(self):

        """
        Computes the number of inputs and outputs.
        Check for concordance of the matrixes' size
        """

        # A
        a1, a2 = self._A.shape

        if a1 != a2:
            raise ValueError, 'A is not a square matrix'
        n = a1

        # B
        b1, b2 = self._B.shape

        if b1 != n:
            raise ValueError, 'A and B should have the same number of rows'
        inputs = b2

        # C
        c1, c2 = self._C.shape

        if c2 != n:
            raise ValueError, 'A and C should have the same number of columns'
        outputs = c1

        # D
        d1, d2 = self._D.shape

        if (d1 != outputs or d2 != inputs):
            raise ValueError, 'D should be consistent with C and B'

        return n, inputs, outputs


    #======================================================================================#
    def __str__(self):

        """
        Display the state-space
        """

        str_mat = "State Space\nA=" + repr(self._A) + "\nB=" + repr(self._B) + "\nC=" + repr(self._C) + "\nD=" + repr(self._D) + "\n\n"

        str_mat += "Path used to compute observers : " + self._W_method + "\n"

        # Observers Wo, Wc
        if (self._Wc != None): 
            str_mat += "Wc = " + repr(self._Wc) + "\n"
        else:
            str_mat += "Wc not computed" + "\n"

        if (self._Wo != None):
            str_mat += "Wo = " + repr(self._Wo) + "\n"
        else:
            str_mat += "Wo not computed" + "\n"

        if (self._norm_h2 != None):
            str_mat += "\nnorm_h2 = " + repr(self._norm_h2) + "\n"
        else:
            str_mat += "\nnorm_h2 not computed" + "\n"

        if (self._Wc != None):
            str_mat += "\nWCPG = " + repr(self._WCPG) + "\n"
        else:
            str_mat += "WCPG not computed" + "\n"

        return str_mat

    #======================================================================================#
    def __repr__(self):
        return str(self)

    if __name__ == "__main__":
        import doctest
        doctest.testmod()

    # def __doc__(self):
    #  return "Class for discrete state-space, and aux functions"

    # def _latex_(self):
        # #TODO
        # return ""
