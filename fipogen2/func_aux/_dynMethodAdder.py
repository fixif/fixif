#coding=UTF8

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from glob import glob
from os import getcwd
from imp import find_module, load_module

def _dynMethodAdder(t_class):

    """
    This function enables importing of functions as attributes of class defined in arg t_class, with following conventions :

    - function modules are contained in same location as target class module
    - function modules have the following naming convention :

        f_name_prefix + ... + f_name_suffix

        currently :
    
        f_name_prefix = class.__name__ + "_"
        f_name_suffix = ".py"
   
    - the __all__ variable in each function module, is used as list of functions to be added to target class
    """
    
    f_name_prefix = t_class.__name__ + "_"
    f_name_suffix = ".py"
    
    file_names = glob(f_name_prefix + '*' + f_name_suffix) # the function is used in class definition, should be in same dir
  
    for f_name in file_names:
      
        submod_name = f_name[:-len(f_name_suffix)]

        f, tmp_filename, description = find_module(submod_name, [getcwd()]) # Argh, see http://bugs.python.org/issue6448 https://hg.python.org/cpython/rev/b28dadd20d9b/ 
        
        try:
            mod_mod = load_module(submod_name, f, tmp_filename, description)
    
            for func_name in mod_mod.__all__: # __all__ should be defined in each module, lists functions to be imported in class
                setattr(t_class, func_name, mod_mod.__dict__[func_name])
            
        except ImportError, err:
            print('ImportError:', err)
            
        finally:
            f.close()

        