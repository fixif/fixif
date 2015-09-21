#coding=utf8

from FIPLabel import FIPLabel
from FIPObjEvent import FIPObjEvent

class FIPObject(object):
    
    """
    
    This class contains an index of instances of subclasses of FIPObject
    
    The index is user-accessible with ``__repr__`` function
    
    """
    
    is_debug_print = True # print __repr__ at end of init
    
    idx_subclass = {}

    def __repr__(self):
    	
    	"""
    	
    	Outputs the index of indexed objects of all subclasses indexed by superclass FIPObject
    	
    	"""
    	
        str_repr = ''
        
        sep = '---\n'
        
        str_repr += sep
        str_repr += self.__class__.__name__ + " index" + "\n"
        str_repr += sep
        
        for str_subclass in FIPObject.idx_subclass.keys():
            str_repr += str_subclass + ' : ' + str(len(FIPObject.idx_subclass[str_subclass])) + " objects indexed \n"
            str_repr += sep
             
            for obj in FIPObject.idx_subclass[str_subclass]:
                str_repr += obj.trk_label.obj_name + "\n"
        
            str_repr += sep
   
        return str_repr
   
    def __init__(self, tgt_subclassname, father_obj, **event_spec):
        
        #Create label
        self.trk_label = FIPLabel(tgt_subclassname, father_obj)
        
        # Add instance to index of labeled instances for programmer_defined tgt_subclass
        FIPObject.idx_subclass.setdefault(tgt_subclassname, []).append(self)
        
        # create event stack of FIPObject instance
        self.obj_events = []
        
        # Init event stack and add event
        FIPObject.stack_event(self, self.trk_label.obj_name, **event_spec)
        
        if FIPObject.is_debug_print: 
        	print(FIPObject.__repr__(self))
        	print(FIPObject.repr_obj_event_stack(self))
        	print(FIPObject.repr_hr_obj_event_stack(self))
    
    
    def repr_obj_event_stack(self):
    	
    	"""
    	Outputs string of the event stack of a FIPObject instance
    	"""
    	
    	
    	str_obj_event_stack = ''
    	
    	# call repr of FIPObjEvent with is_print_labels = True once only
    	
    	str_obj_event_stack += self.obj_events[0].__repr__(is_repr_label = True)
    	
    	for obj_event in self.obj_events[1:]:
    		str_obj_event_stack += str(obj_event)

        return str_obj_event_stack
    
    def repr_hr_obj_event_stack(self):
    	
    	"""
    	
    	Get a human readable string of the event stack of a FIPObject instance
    	
    	"""
    	
    	str_hr_obj_event_stack = ''
    	
    	for obj_event in self.obj_events:
    	    str_hr_obj_event_stack += obj_event._human_readable_repr()
    	
    	return str_hr_obj_event_stack
    
    def stack_event(self, obj_name, **event_spec):
    	
    	"""
    	
    	Add new event to FIPObject instance. 
    	We call it stack because it remembers the order in which the events came
    	
    	"""
    	
    	
    	self.obj_events.append(FIPObjEvent(obj_name, **event_spec))
    	
    def build_global_event_stack(self, tgt_subclass, order='time'):
    	
    	"""
    	
    	Returns an ordered list of all events relative to an indexed subclass
    	
    	Accepts the following arguments :
    	
    	tgt_subclass is an array of indexed classes 
    	
    	.. TODO
    	
    	  implement
    	
    	"""
    	
    	pass
    
    