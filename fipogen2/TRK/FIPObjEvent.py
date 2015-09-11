#coding=utf8

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
    
    dict_e_type = {'create':{'new','convert'}} # set inside a dict to give all possible subtypes =-]
    
    dict_e_source = {'user_input':{''}, 'external':{'simulink', 'py_file'}, 'func':{''}} # same struct
    
    #e_src_func = '' # should be programmer_defined, correctly otherwise needs introspect module
    #e_src_subclass = '' # should be programmer_defined, otherwise needs wiseness (multiple inheritance)
    
    def __init__(self, **event, global_obj_event_num):
        
        #syntaxe : (type= , subtype=, source=, subsource=, func= , subclass= )
        
        #unpack args
        e_type      = event.get(type,'')
        e_subtype   = event.get(subtype,'')
        e_source    = event.get(source,'')
        e_subsource = event.get(subsource,'')
        e_func      = event.get(func,'')
        e_subclass  = event.get(subclass,'')
        
        # check if event is known
        # src_func and src_subclass we rely on user here so no check
        # all cases where user specifies shit for event is taken into account, hopefully
        
        if (e_type not in dict_e_type.keys()):
            raise "FIPObjEvent : unknown event type"
            if (e_subtype not in dict_e_type[e_type]):
                raise "FIPObjEvent : unknown event subtype"
               
        if (e_source not in dict_e_source.keys()):
            raise "FIPObjEvent : unknown source"
            if (e_subsource not in dict_e_source[e_source]) 
                raise "FIPObjEvent : unknown subsource"

        # timestamp event
		self.e_timestamp = time()
            
        self.e_glob_num = global_obj_event_num # var at FIPObject class level, incremented at FIPObject class level

        self.e_type = e_type
        self.e_subtype = e_subtype
        self.e_source = e_source
        self.e_subsource = e_subsource
        
        self.e_func = e_func
        self.e_subclass = e_subclass

    def __repr__(self):
        
        str_repr = ''
        
        fmt = '{0:20} | {1:15} | {2:15} | {3:15} | {4:15} | {5:15}\n'

        str_repr += fmt.format('time', 'glob_e_num', 'e_type', 'e_subtype', 'e_source', 'e_subsource')
        str_repr += fmt.format(str(self.e_timestamp), str(self.obj_event_num), self.e_type, self.e_subtype, self.e_source, self.e_subsource)

        return str_repr
       
    def _human_readable_repr(self): # should be __str__ ??? THIB
        
        fmt_num = '{0:5}' # up to 99999 events
        
        str_hr = ''
        
        str_hr += fmt.format(str(self.obj_event_num))
        
        if self.e_type == 'create':
            str_hr += 'Object created from '
            if self.e_subtype == 'user_input': # interface chaise/clavier (error-prone)
                str_hr += 'user input '
            elif self.e_obj_origin == 'external' # simulink, text file
                str_hr += 'external source : '
            elif self.e_obj_origin == 'func'
                str_hr += 'function : ' # typically random_dSS
