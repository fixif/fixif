# coding=utf8

# This metaclass (from which all classes that wanna be adressed, derive) 
# enables history, tagging and logging features

# Joachim Kruithof, LIP6 2015

class FIPObject(object):
    
    """
    This metaclass enables logging history of objects relative to events we consider important,
    relative to our goal.
    
    It contains functions to tag objects, one table per object.
    
    It tracks objects relative to a father/son model with the following events :
    
    - creation
    - transformation (from 1 obj gives another, can be of same or different subclass (relative to FiPObject)
    
    Class variables used as triggers :
    
    - is_log_on : event log system
    - is_trk_on : ???
    - is_idx_on : global index on (???)
    
    Class variables (shared across all FipObject instances)
    
    - idx_data : index data : contains all objects at metaclass (FipObject) level
    
    - idx_n_subclass : number of FipObject subclasses indexed by reference system
    FIPObject
    Subclass variables (each instance got its own variable)
    FIPObject
    - trk_data can be considered as a label for the object. It contains all the information relative to the object.
    
    {TODO  : use nametuples to simplify code}
    
    """
    
    is_log_on = True ;  # global logging switch
    is_trk_on = True ;  # global tracking switch
    
    # global index tracked instances, to each class.__name__ its index
    
    idx_data = [[]] ;  # global index
    log_data = [] ;  #  global log

    idx_n_subclass = 0 ;  # number of FipObject subclasses indexed
    
    idx_subclass = {} ;  # dictionary of FipObject subclasses

    idx_data_fields = {'obj_id':0, 'obj_name':2, 'obj_':3, 'free_id':4} ;
    idx_data_type = ['list', 'list', 'list', 'int'] ;
    
    trk_data_fields = {'subclassname':0, 'obj_id':1, 'obj_name':2, 'father':3, 'offsprings':4} ;
    trk_data_type = ['str', 'int', 'str', 'obj', 'list'] ;
    
    log_data_fields = {'e_type':0, 'e_desc':1, 'e_src':2, 'e_opt':3} ;  # 'create' from 'e_desc/import' of object 'e_o_src'
    log_data_type = ['str', 'str', 'str', 'str'] ;
    
    def _init_idx_subclass_data(self):
        
        """
        Initializes global index data (self.idx_data) at FipObject superclass level
        Little cheat here : we know the index is idx_n_subclass at this point, so there's no
        need to use idx_subclass[tgt_classname]
        """
        
        self.idx_data[self.idx_n_subclass] = [[] for k in range(0, len(self.idx_data_fields.values()) - 1)] ;

        # Init self.idx_data, based on self.idx_data_fields & self.idx_data_type
        
        for i in range(0, len(self.idx_data_fields.values()) - 1):
            
            if self.idx_data_type[i] == 'str':
                selnumberf.idx_data[self.idx_n_subclass][i].append('') ;
                
            elif self.idx_data_type[i] == 'int':
                self.idx_data[self.idx_n_subclass][i].append(-1) ;  # assigned tracknum : >=0
                
            elif self.idx_data_type[i] == 'obj': 
                self.idx_data[self.idx_n_subclass][i].append(None) ;
                
            elif self.idx_data_type[i] == 'list': 
                self.idx_data[self.idx_n_subclass][i].append([]) ;
                
            else:
                raise('FIPObject : unknown self.idx_data_type') ;

            self.idx_data[self.idx_n_subclass][self.idx_data_fields['free_id']] = 0 ;
        
    def _init_trk_obj_data(self):
        
        """
        Initialize the tracking label at instance level (trk_data)
        """
        
        for i in range(0, len(self.trk_data_fields.values()) - 1):
        
            if self.trk_data_type[i] == 'str':
                self.trk_data[i] = '' ;
                
            elif self.trk_data_type[i] == 'int':
                self.trk_data[i] = -1 ;  # normal tracknum should always be >=0 ;
                
            elif self.trk_data_type[i] == 'obj':
                self.trk_data[i] = None ;
                
            elif self.trk_data_type[i] == 'list':
                self.trk_data[i] = [];
                
            else:
                raise('FIPObject : unknown self.trk_data_type') ;
    
    def _set_trk_obj_data(self, tgt_subclassname, father_obj):
        
        """
        Fill the tracking label with relevant information at instance level (creation of instance)
        """
        
        self.trk_data[self.trk_data_fields['subclassname']] = tgt_subclassname ;  # not __class__.__name__, we are looking for subclass type
        
        if father_obj:
            
            self.trk_data[self.trk_data_fields['father']] = father_obj ;
            # Register object as offspring of cais_lling father
            father_obj.trk_data[self.trk_data_fields['offsprings']].append(self) ;
            
        else:
            
            self.trk_data[self.trk_data_fields['father']] = None ;


        self.trk_data[self.trk_data_fields['obj_id']] = self.idx_data[idx_subclass[tgt_subclassname]][self.idx_data_fields['free_id']] ;
        # Increment free_id for current subclass
        self.idx_data[idx_subclass[tgt_subclassname]][self.idx_data_fields['free_id']] += 1 ;
        
        # The name of an object instance in python does not respect namespaces convention, 
        # so we build a name from scratch, which is not the name of the object instance
        
        self.trk_data[self.trk_data_fields['obj_name']] = self.trk_data[self.trk_data_fields['subclassname']] + '_' + self.trk_data[self.trk_data_fields['obj_id']] ;
    
    def _set_idx_obj_data(self, tgt_subclassname):
        
        """
        Fill the global index data relative to current instance at FipObject class level
        """
        print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA' ;
        print tgt_subclassname + '\n' ;
        print repr(self.idx_subclass) + '\n' ;
        print '\n' ;
        print type(self.idx_subclass[tgt_subclassname]) ;
        print repr(self.idx_subclass[tgt_subclassname]) ;
        
        self.idx_data[self.idx_subclass[tgt_subclassname]][self.idx_data_fields['obj_id']] = self.idx_data[self.idx_subclass[tgt_subclassname]][self.idx_data_fields['free_id']] ;
        self.idx_data[self.idx_subclass[tgt_subclassname]][self.idx_data_fields['free_id']] += 1 ;
        
        self.idx_data[self.idx_subclass[tgt_subclassname]][self.idx_data_fields['obj_name']] = tgt_subclassname + '_' + str(self.idx_data[tgt_subclassname][self.idx_data_fields['obj_id']]) ;
        # Pointer to obj, obj is mutable, so no duplication of obj
        self.idx_data[self.idx_subclass[tgt_subclassname]][self.idx_data_fields['obj_']] = self ;
    
    def __init__(self, tgt_subclassname):

        """
        Create index for subclass obj instances at FipObject class level
        Init tracking label at instance level
        TODO : write event in logger upon call
        """

        # individual obj labels can be defined without global index,
        # global index cannot be defined if there's no individual obj instance label

        #tgt_classname = self.__class__.__name__ ;  #  verify that name subspace is correctly defined so that no name conflict is possible ?
        
        if self.is_trk_on:
        
            if not(self.idx_subclass.has_key(tgt_subclassname)):  # CREATE new index for first class encounter
                
                self.idx_subclass[tgt_subclassname] = self.idx_n_subclass ;
                    
                self._init_idx_subclass_data(self) ;
                    
                self.idx_n_subclass += 1 ;
                
                
            # Register object in global index
            self._set_idx_obj_data(tgt_subclassname) ;
            
            # Label object
            self._init_trk_obj_data() ;
            
            # set_trk_data needs idx_subclass initialized correctly ;
            self._set_trk_obj_data(tgt_subclassname) ;

        # idx_subclass[target_obj.__name__][self.trk_data_fields['offsprings']] only iterated on "create from" events
            
    def _set_track_data_idx(self, target_obj, father):    
            
        self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['subclassname']].append(target_obj.__name__) ;
        self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['obj_id']].append(self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['free_id']]) ;
        self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['obj_name']].append(target_obj.__name__ + '_' + self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['obj_id']]) ;
        self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['obj_']].append(target_obj) ;
        
        self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['free_id']] += 1 ;
            

            

#     def _get_free_id(self, target_obj, father):
#         
#         idx_subclass[target_obj.__name__][self.trk_data_fields['obj_id']] = self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['free_id']]
#         
#         self.idx_data[idx_subclass[target_obj.__name__]][self.idx_data_fields['free_id']] += 1 ;
    
    def _init_local_log(self, target_obj, father):
        """
        Local log inumbers defined as a list of lists that should be read from left to right
        """
        
    #def _init_glob_log(self, target_obj, father):    
        
    def send_event(self, **kwargs):  # should be e_type = 'create',''
        """
        This function must be called whenever an event happens.
        Called by init send_event('create',)
        Log data is not sorting things by class type because it is not an object tracker
        It should reflect what the user / the computer did do
        """
        for key, val in kwargs.items():
            if log_data_fields.has(key):
                # Fill global event log
                pass ;
                # Fill local event log
            else:
            	raise('Event sender is ill-mannered : I cannot handle //' + str(key) + '// type');
        # Fill history of obj
        
        # Fill history of father
        
    def get_history(self):    
        # Fill local history

        pass ;
        
        # Classe connue de nos services ?
        
    def _repr_index(self):
    	
    	"""
    	Print the current index for all objects in all subclasses
    	TODO : pythonify correctly with __repr__
    	"""
    	
    	pass ;
    
    def repr_instance_label(self):
    	
    	"""
    	TODO
    	Query/Print label for current instance
    	"""
    	
    	pass ;
    
    def repr_global_log(self):
    	
    	"""
    	TODO
    	Print a log of all events, time-ordered
    	"""
    	
    	pass ;
    
    def repr_inst_log(self):
    	
    	"""
    	TODO
    	Print a log of events for current instance of FIPObject
    	"""
    	
    	pass ;
