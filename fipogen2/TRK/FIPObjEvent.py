from time import time

class FIPObjEvent(object):
    
    """
    This class defines an event that can be logged and output
    We define two different kinds of events
    
    - Object tracking events
    - User-defined events
    
    The events are logged at subclass level, get a global event number to organize global log, and timestamped
    
    """
    # Definition of available events
    
    set_e_type = {'create'}
    
    set_obj_origin = {'user_input', 'external', 'func'}
    
    set_create_origin = {'new', 'convert'}
    
    set_ext_obj_origin = {'simulink', 'py_file'}
    
    e_src_func = '' # should be programmer_defined, correctly otherwise needs introspect module
    e_src_subclass = '' # should be programmer_defined, otherwise needs wiseness (multiple inheritance)
    
    def __init__(self, (e_type, e_obj_origin, e_create_origin, e_ext_obj_origin=''), global_obj_event_num):
        
        # check if event is known
        if (e_type not in set_e_type): # if not(e_type in set / if e_type not in set
            raise "FIPObjEvent : unknown event type"
        elif (e_obj_origin not in set_obj_origin):
            raise "FIPObjEvent : unknown object origin"
        elif (e_create_origin not in set_create_origin):
            raise "FIPObjEvent : unknown origin of object"
        
        if (e_obj_origin == 'external') and (e_ext_obj_origin not in set_ext_obj_origin):
            raise "FIPObjEvent : unknown external origin for object"
            
        self.obj_event_num = global_obj_event_num
        self.e_timestamp = time()
        self.e_type = e_type
        self.e_obj_origin = 
        self.e_create_origin = e_create_origin
        
        if e_type == 'convert':
            self.e_obj_origin = e_obj_origin
            
            if e_obj_origin == '':

    def __repr__(self):
        
        str_repr = ''
        
        fmt = '{0:5} {1:10} {2:10} {3:10}'

        return str_repr
       
    def _human_readable_repr(self):
    	
    	fmt_num = '{0:5}' # up to 9999 events
    	
    	str_hr = ''
    	
    	str_hr += fmt.format(str(self.obj_event_num))
    	
    	if self.e_type == 'create':
    		str_hr += 'Object created from '
    		if self.e_obj_origin == 'user_input': # interface chaise/clavier (error-prone)
    			str_hr += 'user input '
    		elif self.e_obj_origin == 'external' # simulink, text file
    		    str_hr += 'external source : '
    		elif self.e_obj_origin == 'func'
    		    str_hr += 'function : ' # typically random_dSS
