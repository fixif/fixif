# coding=utf8

"""Blablabla"""

# Object and "methods" for a Discrete State Space
# 2015 LIP6

from numpy                import inf, shape, identity, absolute, dot

from numpy.linalg               import inv, det, solve
from numpy.linalg.linalg        import LinAlgError

from scipy.linalg         import solve_discrete_lyapunov

# Module description
__author__ = "FiPoGen Team"
__email__ = "fipogen@lip6.fr"
__license__ = "CECILL-C"
__version__ = "0.0.1"  # Modify this to increment with git scripting

class dSS(object):

    """
    The dSS class describes a discrete state space realization
       
       A state space system is defined as
       
    .. math::
    
         A \\in \\mathbb{R}^{n \\times n}, \\ B \\in \\mathbb{R}^{n \\times p}, \\ C \\in \\mathbb{R}^{q \\times n} \\text{ and } D \\in \\mathbb{R}^{q \\times p}   
       
    .. math::
       :nowrap:
       
         \\begin{equation*}
         \\text{and }\\left\\lbrace\\begin{aligned}
         X(k+1) &= AX(k) + BU(k) \\\\
         Y(k)   &= CX(k) + DU(k)
         \\end{aligned}\\right.
         \\end{equation*}

    **Dimensions of the state space :**
       
    .. math::
       :align: left
       
         n,p,q \\in \\mathbb{N}
         
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

        self._A = A  # User input
        self._B = B
        self._C = C
        self._D = D

        # Initialize state space dimensions from user input

        (self._n, self._p, self._q) = self.__check_dimensions__()  # Verify coherence, set dimensions

        # Initialize observers
        self._Wo = None
        self._Wc = None 

        # Initialize norms

        self._norm_h2 = None
        self._WCPG = None

        # Other criterions,values

        self._DC_gain = None



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
        if (self._Wo == None): self.calc_Wo()
        return self._Wo

    @property
    def Wc(self):
        if (self._Wc == None): self.calc_Wc()
        return self._Wc

    @property
    def norm_h2(self):
        if (self._norm_h2 == None): self.calc_h2()
        return self._norm_h2

    @property
    def WCPG(self):
        if (self._WCPG == None): self.calc_WCPG()
        return self._WCPG

    @property
    def DC_gain(self):
        if (self._DC_gain == None): self.calc_DC_gain()
        return self._DC_gain



    #======================================================================================#      
    # Observers (Wo, Wc) calculation
    #======================================================================================#

    def calc_Wo(self):

        """
        Compute observer :math:`W_o` using ``scipy.linalg.solve_discrete_lyapunov``

        .. math::
        
           A^T * W_o * A + C^T * C = W_o

        """

        try:
            X = solve_discrete_lyapunov(self._A, self._C.transpose() * self._C)
            self._Wo = X
            
        except LinAlgError, ve:

            if (ve.info < 0):
                e = LinAlgError(ve.message)
                e.info = ve.info
            else:
                e = LinAlgError("scipy Linalg failed to compute eigenvalues of Lyapunov equation.")
                e.info = ve.info
                raise e


    def calc_Wc(self):

        """
        Compute observer :math:`W_c` using ``scipy.linalg.solve_discrete_lyapunov``

        .. math::

           A * W_c * A^T + B * B^T = W_c

        """

        try:
            
            X = solve_discrete_lyapunov(self._A.transpose(), self._B * self._B.transpose())
            self._Wc = X
            
        except LinAlgError, ve:

            if (ve.info < 0):
                e = LinAlgError(ve.message)
                e.info = ve.info 
            else:
                e = LinAlgError("scipy Linalg failed to compute eigenvalues of Lyapunov equation.")
                e.info = ve.info
                raise e
               
    #======================================================================================#      
    # Norms calculation
    #======================================================================================#

    def calc_h2(self):

        """
        Compute the H2-norm of the system
        
        .. math::
        
           \\langle \\langle H \\rangle \\rangle = \\sqrt{tr ( C*W_c * C^T + D*D^T )}
        
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
    def calc_WCPG(self,n_it):

        """
        Compute the Worst Case Peak Gain of the state space

        .. math::

           \\langle \\langle H \\rangle \\rangle \\triangleq |D| + \\sum_{k=0}^\\infty |C * A^k * B|
        
        Using algorithm developed in paper :
        
        [CIT001]_
        
        .. [CIT001]
        
           Lozanova & al., calculation of WCPG
        
        """
        #Method not precise
        #res = 0

        #try:
        #    for i in range(1, self._nit_WCPG):
        #        res += numpy.absolute(self._C * matrix_power(A, i) * B)
        #        #res += numpy.absolute(self._C * A**i * B)
        #except:
        #    raise ValueError, 'Impossible to compute WCPG at rank i = ' + str(i) + "\n"
        #else:
        #    self._WCPG = res + absolute(D)

        #

        return self._WCPG

    #======================================================================================#
    def calc_DC_gain(self):

        """
        Compute the DC-gain of the filter

        .. math::

           \\langle H \\rangle = C * (I_n - A)^{-1} * B + D
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



    #def __doc__(self):
    #  return "Class for discrete state-space, and aux functions"

    # def _latex_(self):
        # #TODO
        # return ""