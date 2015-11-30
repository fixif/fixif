#coding=utf8

"""
Generate data to compare result between matlab and python routines
"""

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from scipy.signal import butter, tf2ss, ss2tf
from numpy import arange
from LTI import *
from itertools import chain


def gen_data(data_type, data_source, opt):
    
    data_dict = {}
    
    ev_source = "func"
    ev_subsource = ""
    
    def gen_data_signal(opt):
      
        """
        Generate TF or SS depending on scipy function used
        """
      
        butter_range_order = arange(4, 10, 1)
        butter_range_cut   = arange(0.05, 0.11, 0.01)
      
        list_obj = []
      
        if opt == "butter":
    
            is_data_TF = True
            ev_subsource = "butter"
    
            for order in butter_range_order:
        
                for cut in butter_range_cut:
          
                    #print("order = {0} cut = {1}".format(order,cut))
                    num, den = butter(order,cut)
                    list_obj.append(dTF(num, den, e_source = ev_source, e_subsource = ev_subsource))
        
        return list_obj, is_data_TF
     
    def gen_data_random():
        
        """
        Generate random state spaces
        """
        list_obj = []
        is_data_TF = False
        ev_subsource = "random_dSS"
        
        # range / order of state_space
        random_n_order = range(1,20,1)
        #range of inputs
        random_p_range = range(1,5,1)
        #range of outputs
        random_q_range = range(1,5,1)
        
        for n in random_n_order:
            for p in random_p_range:
                for q in random_q_range:
                    
                    list_obj.append(random_dSS(n, p, q)) # TODO add tracking to random_dSS or modify to get dSS(*chain(random_ABCD(n,p,q)), e_source=ev_subsource)
        
        return list_obj, is_data_TF
        
    if data_source == "signal":
        list_obj, is_data_TF = gen_data_signal(opt)
    elif data_source == "random":
        list_obj, is_data_TF = gen_data_random()

    if data_type == "SS" and is_data_TF: # convert to SS from TF for output
        #http://docs.scipy.org/doc/numpy/reference/generated/numpy.matrix.A1.html
        #numpy.matrix.A1 <=> np.asarray(x).ravel
        print('Converting TF to SS')
        
        obj_list = []
        
        for obj in list_obj:
            A, B, C, D = tf2ss(obj.num.A1, ob.den.A1)
            list_obj.append(dSS(A, B, C, D, e_source = ev_source, e_subsource=ev_subsource))
        
        list_obj = obj_list
        
        #list_obj = [dSS(*chain(tf2ss(obj.num.A1, obj.den.A1)), e_source = ev_source, e_subsource=ev_subsource) for obj in list_obj]
    
    elif data_type == "TF" and not(is_data_TF): # convert to TF from SS for output
      
        print("Converting SS to TF NOT IMPLEMENTED")
        
        obj_list = []
        for obj in list_obj:
            
            num, den = ss2tf(obj.A, obj.B, obj.C, obj.D)
            print("********************************************************")
            print('A')
            print(obj.A)
            print('B')
            print(obj.B)
            print('C')
            print(obj.C)
            print('D')
            print(obj.D)
            print('numerator')
            print(num)
            print('denominator')
            print(den)
            print("********************************************************")
            obj_list.append(dTF(num, den, e_source=ev_source, e_subsource=ev_subsource))
        
        list_obj = obj_list
      
    elif data_type == "SS" and not(is_data_TF):
        print("data is SS and we need SS : doing nothing")
    
    elif data_type == "TF" and is_data_TF:
        print("data is TF and we need TF : doing nothing")

    else:  
        raise(ValueError, "data_type not known")
    
    return list_obj
