#coding=utf8

import FIPLabel

class FIPObject(object):
    
    """
    This class contains an index of instances of subclasses of FIPObject
    """
    
    is_debug_print = True # print __repr__ at end of init
    
    idx_subclass = {}

    def __repr__(self):
        
        sep = '---'
        
        print sep
        print self.__class__.__name__ + " index"
        print sep
        
        for str_subclass in FIPObject.idx_subclass.keys():
        
            print str_subclass + ' : ' + str(len(FIPObject.idx_subclass[str_subclass])) + " objects indexed"
             
            print sep
             
            for obj in FIPObject.idx_subclass[str_subclass]:
                 
                print obj.trk_label['obj_name']
        
            print sep
   
    def __init__(self, tgt_subclassname, event, father_obj = None):
        
        #Create label
        FIPLabel.FIPLabel(tgt_subclassname, father_obj)
        
        # Add instance to instance index
        FIPObject.idx_subclass.setdefault(tgt_subclassname, []).append(self)
        
        # Append event to object log
        
        # Append event to global log (with simple_log)
        
        if FIPObject.is_debug_print: FIPObject.__repr__(self)
        
