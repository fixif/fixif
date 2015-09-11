#coding=utf8

import FIPLabel
import FIPObjEvent

class FIPObject(object):
    
    """
    This class contains an index of instances of subclasses of FIPObject
    """
    
    is_debug_print = True # print __repr__ at end of init
    
    idx_subclass = {}

    # assign a global log number to all events regardless
    # of subclass to enable global log repr
    global_obj_event_num = 0

    def __repr__(self):
        
        str_repr = ''
        
        sep = '---\n'
        
        str_repr += sep
        str_repr += self.__class__.__name__ + " index" + "\n"
        str_repr += sep
        
        for str_subclass in FIPObject.idx_subclass.keys():
            str_repr += str_subclass + ' : ' + str(len(FIPObject.idx_subclass[str_subclass])) + " objects indexed\n"
            str_repr += sep
             
            for obj in FIPObject.idx_subclass[str_subclass]:
                str_repr += obj.trk_info.trk_label['obj_name'] + "\n"
        
            str_repr += sep
   
        return str_repr
   
    def __init__(self, tgt_subclassname, event, father_obj = None):
        
        #Create label
        self.trk_label = FIPLabel.FIPLabel(tgt_subclassname, father_obj)
        
        # Add instance to instance index
        FIPObject.idx_subclass.setdefault(tgt_subclassname, []).append(self)
        
        # create event stack
        self.obj_events = []
        
        # append first event in stack
        self.obj_events.append(FIPObjEvent.FIPObjEvent(event, FIPObject.global_obj_event_num))
        
        #increase global event counter at FIPObject class level
        FIPObject.global_obj_event_num += 1
        
        if FIPObject.is_debug_print: print(FIPObject)
        
    def repr_obj_event_stack(self):
    	
    	str_obj_event_stack = ''
    	
    	for obj_event in self.obj_events:
    		str_obj_event_stack += str()
        pass
    
    
    