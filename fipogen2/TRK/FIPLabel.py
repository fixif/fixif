#coding=utf8

"""
This file contains label class for FIPObjects
"""

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithopf@lip6.fr"
__status__ = "Beta"

class FIPLabel(object):
    
    """
    
    This class is used to label objects, that can be indexed in a FIPindex
    
    A label contains the following parts :
    
    - ``obj_class`` : master class of the object (surely == ``FIPObject``
    - ``obj_subclass`` : subclass of instance (programmer defined, in case of multiple inheritance)
    - ``obj_id`` : ``id(obj)``
    - ``obj_num`` : number of object relative to all instances of ``obj_subclass`` in global index
    - ``obj_name`` : name made with ``obj_num`` and ``obj_subclass`` (example : ``dSS_0``)
    
    """
    
    is_debug_print = True # print label at end of __init__
    
    # Contains subclass:free_num items
    free_num = {}

    def __repr__(self):
        
        fmt = '{0:20} = {1:20} \n'
        
        str_repr = ''
        
        str_repr += fmt.format('obj_class', self.obj_class)
        str_repr += fmt.format('obj_subclass', self.obj_subclass)
        str_repr += fmt.format('obj_id', str(self.obj_id))
        str_repr += fmt.format('obj_num', str(self.obj_num))
        str_repr += fmt.format('obj_name', str(self.obj_name))
        
        
        if self.obj_father is not None:
            father_name = self.obj_father.obj_name
        else:
            father_name = 'None'
            
        str_repr += fmt.format('obj_father', father_name)
        
        str_list_offsprings = []
        
        if self.obj_offsprings:
            for offspring_obj in self.obj_offsprings:
               str_list_offsprings.append(offspring_obj.obj_name)
        else: 
            str_list_offsprings.append('No offspring')
        
        str_repr += fmt.format('obj_offsprings', str_list_offsprings[0])
        
        for str_offspring in str_list_offsprings[1:]:
            str_repr += fmt.format('', str_offspring)
    
        return str_repr
    
    def __init__(self, tgt_subclass, father = None):
        
        str_allbaseclass = []
        
        for str_baseclass in self.__class__.__bases__:
            str_allbaseclass.append(str_baseclass.__name__)

        self.obj_class = ' '.join(str_allbaseclass)
        
        self.obj_subclass = tgt_subclass # corresponds to the tracked subclass
        
        self.obj_id = id(self)
        
        # set obj num : init classvariable if not, assign value in label, increment class variable
        FIPLabel.free_num.setdefault(self.obj_subclass, 0)
        self.obj_num = FIPLabel.free_num[self.obj_subclass]
        FIPLabel.free_num[self.obj_subclass] += 1

        self.obj_name = self.obj_subclass + "_" + str(self.obj_num)
        
        self.obj_father = father
        
        if father is not None:
            father.obj_offsprings.append(self)
        
        self.obj_offsprings = []
    
        if FIPLabel.is_debug_print: print(FIPLabel.__repr__(self))

        
    def __str__(self):
        
        return __repr__(self)
        

        