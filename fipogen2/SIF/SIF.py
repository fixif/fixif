#coding=utf8

# This class describes the SIF object
# 2015 LIP6

from numpy import matrix as mat

class SIF(object):
 r"""
 This object represents a discrete state space in Special Implicit Form
 """
 
 def __init__(self, method, call_args): # one option JtoS, delta_epsilon 
   
   """
   Build a Special Implicit Form
   """
   
   # call_args : 
   # method = 'manual' : by hand, default method
   # '_from_dSS' : internal, depends of call
   # - source_dSS ; method
   
   if method == '_blank': # define a blank structure that gonna be filled
   	  _init_blank()
   elif method == 'manual' # default method, when used by user (CLI)
   
      _init_blank()
      _def_from_tuple()
      
   elif method == '_from_dSS' # internal call
   
      _init_blank()
      _def_from_dSS()
      
   elif method == '_from_SIF'
   
      _init_blank()
      _def_from_SIF()
      
   elif method == 'import_matlab'
   
      _init_blank()
      _def_from_import('matlab')
      
   else raise('Unknown init method for SIF object. Please review code.')
   
   # This list is a parent/child tree. Each time there's an action that
   # modifies the SIF, or create a new SIF, action is recorded in a stack
   # If there's no parent the parent is 'root'
   
   def _init_blank():
   	
   	# Define all the fields of struct as empty
   	# here we only define, not calculations.
   	
   	self._name = '' ;
   	self._id = '' ;
   	
   	(self._J,
   	self._K,
   	self._L,
   	self._M,
   	self._N,
   	self._O,
   	self._P,
   	self._Q,
   	self._R,
   	self._S) = None ;
   	
   	# dimensions all set to zero

   	(self._l,
   	self._m,
   	self._n,
   	self._p) = 0 ;
   
    # cannot build big boy Z without info about JtoS

    self._Z = None ;
   
    #initialize delta JtoS
    (self._dJ,
    self._dK,
    self._dL,
    self._dM,
    self._dN,
    self._dO,
    self._dP,
    self._dQ,
    self._dR,
    self._dS) = None ;
   
   # define properties to be able to extract all matrixes as a tuple
   @property
   # check that the user can get it (i.e. all matrixes exist)

   is_SIFmat_exists = !(self._J is None & 
					    self._K is None & 
					    self._L is None & 
					    self._M is None & 
					    self._N is None & 
					    self._O is None & 
					    self._P is None & 
					    self._Q is None & 
					    self._R is None & 
					    self._S is None) ;

   if is_SIFmat_exists:
    self._allmat = [self._J, 
				    self._K, 
				    self._L, 
				    self._M, 
				    self._N, 
				    self._O, 
				    self._P, 
				    self._Q, 
				    self._R, 
				    self._S] ;
				    
   else raise('Cannot output matrix tuple, at least one matrix is undefined')
   @property

   is_alldelta_exists = !(self._dJ is None & 
						  self._dK is None & 
						  self._dL is None & 
						  self._dM is None & 
						  self._dN is None & 
						  self._dO is None & 
						  self._dP is None & 
						  self._dQ is None & 
						  self._dR is None & 
						  self._dS is None) ;

   if is_alldelta_exits:
    self._alldelta = [self._dJ, 
					  self._dK, 
					  self._dL, 
					  self._dM, 
					  self._dN, 
					  self._dO, 
					  self._dP, 
					  self._dQ, 
					  self._dR, 
					  self._dS] ;
   else raise('Cannot output sensitivity tuple, at least one matrix is undefined')
   # define AZ, BZ, CZ, DZ
   
   self._AZ, self._BZ, self._CZ, self._DZ = None
   
   # Get an ID, then create a name from it
   
   prefix = "SIF_" ;
   
   
   
   
   # CALL DEFINITION ( python : #args !)
   # Mandatory arg :
   # init_mode = "scratch", simulink
   
   
   # From scratch
   
   # From matlab (simulink) data
   
  