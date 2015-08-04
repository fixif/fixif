# We generate UIDs for objects here
# Needs global variables

from dSS import dSS # import class
from SIF import SIF

# global variable
id_dict = None ;

# dictionary :
# struct / free_id / [allocated_ids / var_name]

class Id_manage(object):
  """
  This class manipulates UIDs for objects. 
  The ID numbers are class-specific and everything is held in a dictionary
  """

  idx_class = {} ; # dictionary which contains all classname

  id_class = _id_class ;
  id_idx_nclass = 0 # never touch this
  id_classname = [];
  id_obj_id = [] ; # one sublist per class
  id_next_id = [] ;
  #classtuple=(dSS.dSS, SIF.SIF)
  
  #if id_dict is None: _ID_dict._create_dict(id_dict, classtuple)
  # Change to def referring to constructed array


  
  
  def __init__():
    
    @property
    self.id = [0]

    @property
    self.inst_name = ['']
    
    @property
    self.class_name = ['']

  def _augment_class_idx(cls):
    
    key = type(cls).__name__ ; # name in master 
    val = id_idx_nclass ;
        
    id_idx_nclass += 1 ;
	
    idx_class[key]=val ;

  
  class _id_class(object):
    """
    For a given target class, the present class provides 
    - an id for each instance of the class
    And keeps track of all instances of the class.
    First version : deletion of objects not taken into account for reference management (del)
    """
    idx_refdata = {'class_name':0,'obj_id':1,'obj_name':2,'next_id':3}
    refdata = [] ;
    for i in range(0,idx_refdata.len()-1):refdata.append([]) ;
    #refdata = [[],[],[],[]]
    def __init__():
    
      self.class_name = ''
      self.obj_id = [] # contains all allocated obj ID
      self.obj_name = [] # contains all instance names, indexed by objID
      self.next_id = 0 # a free id (next avail)
  
  def __init__()
  
      self.oindex = 0 # object index
      
  def _reference_obj_idx(self, obj):
    """
    When obj requests an id, it is automatically put in the database
    _get_id should be only used internally because any misuse will result in invalid database.
    """
    key = type(obj).__name__ # does this give good name ??
    num = idx_class.get(key)

    cur_idx = self.oindex ;

    i_cls = idx_refdata.get('class_name')
    i_obi = idx_refdata.get('obj_id')
    i_ona = idx_refdata.get('obj_name')
    i_nid = idx_refdata.get('next_id')
    
    
    
    self.oindex += 1
    