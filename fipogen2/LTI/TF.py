#coding=utf8

# This class describes a transfer function

from TRK.FIPObject import FIPObject

from numpy import nditer

class TF(FIPObject):
  
    def __init__(self, num, den, father_obj = None, **event_spec):
    
        """
        Define transfer function as
       
        :math:`H(s) = \frac{\sum_i num[i] s^i}{\sum_j den[i] s^i}`
        
        TODO : add ZeroPoleGain representation
        
        """
    
        # create default event if not given as arg
        # default =  generated from user/script input
    
        my_e_type      = event_spec.get('e_type', 'create')
        my_e_subtype   = event_spec.get('e_subtype', 'new')      
        my_e_subclass  = event_spec.get('e_subclass', 'TF')
        my_e_source    = event_spec.get('e_source', 'user_input')
        my_e_subsource = event_spec.get('e_subsource', 'TF.__init__') # optional, could also be ''
        my_e_desc      = event_spec.get('e_desc', '')

        TF_event = {'e_type':my_e_type, 'e_subtype':my_e_subtype, 'e_source':my_e_source, 'e_subsource':my_e_subsource, 'e_desc':my_e_desc, 'e_subclass':my_e_subclass}

        my_father_obj = father_obj
      
        FIPObject.__init__(self, self.__class__.__name__, father_obj=my_father_obj, **TF_event)
        
        if (num.shape[0] is not 1) or (den.shape[0] is not 1):
	    raise('TF : num and den should be 1D matrixes')
        
        self._num = num
        self._den = den

    def __str__(self):
       
        str_num = ''
        elno = 0
        
        for el in nditer(self._num):
	    str_num += str(el) + " s^" + str(elno) + " + "
	    elno += 1
       
        str_num = str_num[0:-3]
       
        str_den = ''
        elno = 0
        
        for el in nditer(self._den):
	    str_den += str(el) + " s^" + str(elno) + " + "
	    elno += 1
       
        str_den = str_den[0:-3]
       
        fraclen = max(len(str_num),len(str_den))
        
        fmt = '{0:7} {1:^' + str(fraclen) + '} \n'
       
        str_tf  = "\n"
        str_tf += fmt.format('',str_num)
        str_tf += fmt.format('H(s) = ','-'*fraclen)
        str_tf += fmt.format('',str_den)
        
        return str_tf
        
         
    
