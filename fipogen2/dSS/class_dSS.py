# coding=utf8

# Object and "methods" for a Discrete State Space
# 2015 LIP6

from numpy                import matrix as mat
from numpy                import inf, shape

from numpy.linalg               import inv, det, solve
from numpy.linalg.linalg        import LinAlgError

#IFDEF SLYCOT
#import slycot # lin eq solver

# Module description
__author__ = "FiPoGen Team"
__email__ = "fipogen@lip6.fr"
__license__ = "CECILL-C"
__version__ = "0.0.1"  # Modify this to increment with git scripting

class dSS(object):
    
  """
  The dSS class describes a discrete state space realization
     ---
     A state space system is defined as :math:A\in\mathbb{R}^{n \times n}, B\in\mathbb{R}^{n \times p}, C\in\mathbb{R}^{q \times n} and C\in\mathbb{q \times p}, and
  . . math::

  \left\lbrace\begin{array}{rcl}
  X(k+1) &=& AX(k) + BU(k) \\
  Y(k) &=& CX(k) + DU(k)

  n,p,q are the dimensions of the state-space (number of states, inputs and outputs, respectively)
  
  Additional data available, computed once when asked for :
  
  dSS.Wo, dSS.Wc, dSS.norm_h2, dSS.WCPG
  
  - Observers : Wo and Wc
  - "Norms"   : H2-norm (norm_h2), Worst Case Peak Gain (WCPG) 
  """
  
  def __init__(self, A, B, C, D):
      
    """
    Construction of a discrete state space
    """
    
    self._A = A  # User input, numpy matrixes
    self._B = B
    self._C = C
    self._D = D
    
    # Initialize state space dimensions from user input
    
    (self._n, self._p, self._q) = self.__check_dimensions__()  # Verify coherence, set dimensions

    # Initialize observers
    
    self._W_method = "linalg"  # "slycot"
    
    self._Wo = None
    self._Wc = None 
    
    # Initialize norms
    
    self._norm_h2 = None
    self._WCPG = None

  # Properties
    
  @property
  def A(self):
    return _A(self)
    
  @property
  def B(self):
    return _B(self)
    
  @property
  def C(self):
    return _C(self)
    
  @property
  def D(self):
    return _D(self)
    
  @property
  def n(self):
    return _n(self)
    
  @property
  def p(self):
    return _p(self)
    
  @property
  def q(self):
    return _q(self)

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
    
  #======================================================================================#      
  # Observers (Wo, Wc) calculation : solve Lyapunov equation
  #======================================================================================#
    
  def calc_Wo(self):
      
    """
    Compute observer Wo with one of available methods
    
    Using intrinsic solve.
    
    A^T * Wo * A + C^T * C = Wo
    
    """
    
    if (self._W_method == "linalg"):  # scipy intrinsic
            
      try:
	    X = scipy.linalg.solve_discrete_lyapunov(self._A, self._C.transpose() * self._C)
      except ValueError, ve:
              
        if (ve.info < 0):
          e = ValueError(ve.message)
          e.info = ve.info
        else:
          e = ValueError("scipy Linalg failed to compute eigenvalues of Lyapunov equation.")
          e.info = ve.info
          raise e     
          
      else:
        self._Wo = X
            
    elif (self._W_method == "slycot"):  # Slycot function sb03md
            
      try:
        X, scale, sep, ferr, w = slycot.sb03md(self.n, -self._C.transpose() * self._C, self._A.transpose(), eye(self.n, self.n), dico='D', trana='T')
      except ValueError, ve:

        if (ve.info < 0):
          e = ValueError(ve.message)
          e.info = ve.info
        else:
          e = ValueError("The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
          e.info = ve.info
          raise e  

      else:
        self._Wo = mat(X)
      
    return

  def calc_Wc(self):
      
    """
    Compute observer Wc with one of available methods
    
    A * Wc * A^T + B * B^T = Wc
    
    """
          
    if (self._W_method == "linalg"):  # scipy intrinsic
        
      try:
	    X = scipy.linalg.solve_discrete_lyapunov(self._A.transpose(), self._B * self._B.transpose())
      except ValueError, ve:
        
        if (ve.info < 0):
          e = ValueError(ve.message)
          e.info = ve.info
        else:
          e = ValueError("scipy Linalg failed to compute eigenvalues of Lyapunov equation.")
          e.info = ve.info
          raise e     
          
      else:
          self._Wc = X

        
    elif (self._W_method == "slycot"):  # Slycot function sb03md
        
      try:
            # X,scale,sep,ferr,w = slycot.sb03md( self.n, -self._B*self._B.transpose(), copy(self._A), eye(self.n,self.n), dico='D', trana='T')
        X, scale, sep, ferr, w = slycot.sb03md(self.n, -self._B * self._B.transpose(), self._A, eye(self.n, self.n), dico='D', trana='T')
      except ValueError, ve:

        if ve.info < 0:
          e = ValueError(ve.message)
          e.info = ve.info
        else:
          e = ValueError("The QR algorithm failed to compute all the eigenvalues (see LAPACK Library routine DGEES).")
          e.info = ve.info
          raise e
        
      else:
        self._Wc = mat(X)

    return
  
  #======================================================================================#      
  # Norms calculation
  #======================================================================================#
    

  def calc_h2(self):
      
    """
    Compute the H2-norm of the system
    """

    res = None
          
    try:
      M = self.C * self.Wc * self.C.transpose() + self.D * self.D.transpose()
    except:
      res = inf
    else:
      res = sqrt(M.trace())
    
    self._norm_h2 = res
    
    return
    
  def calc_WCPG(self):
        
    """
    Compute the Worst Case Peak Gain of the state space
    """
    
    #STUB
    if (self._WCPG == None): self._WCPG = 0
    
    return self._WCPG
    
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
      raise ValueError, 'D should be consistant with C and B'

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
    
    #======================================================================================#
  def __doc__(self):
    return "Class for discrete state-space, and aux functions"
  
  # def _latex_(self):
    # #TODO
    # return ""

