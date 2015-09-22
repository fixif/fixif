#coding=utf8

"""
This file contains event class for FIPObjects
"""

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

from time import time

class FIPObjEvent(object):
    
    """
    
    This class defines an object event that is logged and stacked at instance level
    
    Objects get a global event number and a timestamp
    
    Syntax of events :
    
    ``(e_type, e_subtype, e_source, e_subsource, e_subclass, e_desc)``
    
    Mandatory args ``(e_type, e_subtype, e_source, e_subsource)`` are verified against :
    
    - ``dict_e_type``  which contains event type and subtype 
    - ``dict_e_source``  which contains event source and subsource
    
    * ``e_type`` : 
    
        - ``create`` (new obj instance)
    
    * ``e_subtype`` : 
        
      + For ``e_type = create``
        
        - ``new``     new instance from scratch)
        - ``convert`` new instance from existing instance of same or different subclass
                   
    * ``e_source`` : 
        
      + For ``e_type = create``
                 
        - ``user_input`` source of new obj is python interactive prompt or python script
        - ``external`` new obj from external source defined in e_subsource
        - ``func`` internal FIPOGEN function, programmer_defined
                 
    * ``e_subsource`` : 
    
	  + For ``e_type = create``    
    
        - if ``(e_source == 'user_input')``  don't define it
        - if ``(e_source == external)``  defined as ``simulink`` or ``file``
        - if ``(e_source == ``func)``  ``e_subsource`` is originating function, programmer_defined
    
    * ``e_desc`` : optional parameter, contains

        - if ``e_source = external``, ``e_desc`` contains filename
        - can be used as custom note but not recommended.
    
    Example event : new instance of dSS subclass from user input
    
    ``(e_type='create', e_subtype='new', e_source='user_input', e_subclass='dSS')``
    
    Example event : new instance from simulink file
    
    ``(e_type='create', e_subtype='new', e_source='external', e_subsource='simulink', e_desc='myfile.xyz', e_subclass='dSS')``
    
    Example event : new instance from converted dSS obj into ???
    
    ``(e_type='create', e_subtype='convert', e_source='func', e_subsource='func_name', e_subclass='bzzz')``
    
    """
    
    # global event log number regardless
    # of subclass, to enable global log output ordered correctly
    global_obj_event_num = 0
    
    # Definition of available events
    
    dict_e_type = {'create':{'new','convert'}} # set inside a dict to give all possible subtypes =-]
    
    dict_e_source = {'user_input':{''}, 'external':{'simulink', 'file'}, 'func':{''}} # same struct  

    def __init__(self, obj_name, **event_spec):
		
		"""
		
		Define event based on programmer input, but we add some salt too (timestamp, global_obj_event_num
		
		"""
		
		# timestamp event
		self.e_timestamp = time()

		self.e_obj_name = obj_name # object should already be tagged with trk_label
		self.e_glob_num = FIPObjEvent.global_obj_event_num # var at FIPObject class level, incremented at FIPObject class level

		# increment global event number
		FIPObjEvent.global_obj_event_num += 1

		self.e_type	  = event_spec['e_type']
		self.e_subtype   = event_spec['e_subtype']
		
		self.e_source	= event_spec['e_source']
		self.e_subsource = event_spec.get('e_subsource','') # optional, do not trip if not specified

		self.e_subclass  = event_spec['e_subclass']
		
		self.e_desc = event_spec.get('e_desc','') # optional, not checked, do not trip if not specified
		
		if (self.e_type not in FIPObjEvent.dict_e_type):
			raise "FIPObjEvent : unknown event type"
		if (self.e_subtype not in FIPObjEvent.dict_e_type[self.e_type]):
			raise "FIPObjEvent : unknown event subtype"
		if (self.e_source not in FIPObjEvent.dict_e_source):
			raise "FIPObjEvent : unknown source"
		   
		# if e_source == 'user_input' or e_source == 'func' 
		# we don't verify subsource, should be wisely programmer_defined
		
		if (self.e_source == 'external'):
			if (self.e_subsource not in dict_e_source['external']):
				raise "FIPObjEvent : unknown external subsource"
        
    def __repr__(self, is_repr_label = False):
        
        str_repr = ''
        
        fmt = '{0:20} | {1:15} | {2:15} | {3:15} | {4:15} | {5:15} | {6:15} | {7:15} \n'

        if is_repr_label:

            str_repr += fmt.format('time', 'obj_name', 'glob_e_num', 'e_type', 'e_subtype', 'e_source', 'e_subsource', 'e_desc')
        
        str_repr += fmt.format(str(self.e_timestamp), self.e_obj_name, str(self.e_glob_num), self.e_type, self.e_subtype, self.e_source, self.e_subsource, self.e_desc)

        return str_repr
     
    # PROBLEM when representing a stack of events
       
    def _human_readable_repr(self): # should be __str__ ??? THIB
        
        """
        
        Output a human-readable sentence from event
        
        """
        
        fmt_num = '{0:5}' # up to 99999 events
        
        str_hr = 'Event '
        
        str_hr += fmt_num.format(self.e_glob_num)
        
        str_hr += " : "
        
        if self.e_type == 'create':
            
            # str_hr += self.trk_label.obj_name + ' '
            # not possible with current struct, but not needed (??)
            
            if self.e_subtype == 'new':
                
                str_hr += ' New '
                
            elif self.e_subtype == 'convert':
                
                str_hr += 'Converted '
                
            str_hr += 'object ' + self.e_obj_name +' created from '
            
            if self.e_source == 'user_input': 
                
                str_hr += 'user input' # interface chaise/clavier (error-prone)
                
            elif self.e_source == 'external': # simulink, text file
                
                str_hr += 'external source, '
                
                if self.e_subsource == 'simulink':
                        
                    str_hr += 'simulink file '
                        
                elif self.e_subsource == 'simple_file':
                
                    str_hr += 'simple file '
                
                str_hr += self.e_desc + ' ' # contains filename
                
            elif self.e_source == 'func':
                
                str += 'function ' + self.e_subsource # typically random_dSS, conversion function, ...
                
        return str_hr
       

       
                