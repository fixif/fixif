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
        
        #print self.trk_info.trk_label
        # why does that not work
        #print self.trk_info
        
        # Add instance to instance index
        FIPObject.idx_subclass.setdefault(tgt_subclassname, []).append(self)
        
        self.obj_events = []
        
        # stack creation event on instance event list
        
        self.obj_events.append(FIPObjEvent.FIPObjEvent(event, FIPObject.global_obj_event_num))
        FIPObject.global_obj_event_num += 1
        
        
        # Append event to object log
        
        # Append event to global log (with simple_log)
        
        if FIPObject.is_debug_print: print(FIPObject)
        
