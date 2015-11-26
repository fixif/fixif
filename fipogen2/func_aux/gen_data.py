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

import LTI

def gen_data(data_type, data_source, opt):
    
    data_dict = {}
    
    is_data_TF = True
    
    ev_source = "func"
    ev_subsource = ""
    
    def gen_data_signal(opt):
      
        """
        Generate TF or SS depending on scipy function used
        """
      
        butter_range_order = range(4, 1, 10)
        butter_range_cut = range(0.05, 0.01, 0.11)
      
        list_obj = []
      
        if opt == "butter":
    
            is_data_TF = True
            ev_subsource = "butter"
    
            for order in butter_range_order:
        
                for cut in butter_range_cut:
          
                    num, den = butter(order,cut)
                    
                    list_obj.append(dTF(num, den, e_source = ev_source, e_subsource = ev_subsource))
        
        return list_obj
     
    def gen_data_random():
    	
    	"""
    	Generate random state spaces
    	"""
    	
    	is_data_TF = False
    	ev_subsource = "random_dSS"
    	
    	# number of state spaces to generate
    	num_ss = 50
    	
    	# range / order of state_space
    	random_n_order = range(1,1,20)
    	#range of inputs
    	random_p_range = range(1,1,5)
    	#range of outputs
    	random_q_range = range(1,1,5)
    	
    	for n in random_n_order:
    		
    		for p in random_p_range:
    			
    			for q in random_q_range:
    				
    				list_obj.append(random_dSS(n, p, q))
    	
        
    if data_source == "signal":
            
        list_obj = gen_data_signal(opt)
            
    elif data_source == "random":

        list_obj = gen_data_random()
    
    
    if data_type == "SS" and is_data_TF: # convert to SS from TF for output
    
        list_obj = [dSS(tf2ss(obj.num, obj.den), e_source = ev_source, e_subsource=ev_subsource) for obj in list_obj]
    
    elif data_type == "TF" and not(is_data_TF): # convert to TF from SS for output
      
        list_obj = [dTF(ss2tf(obj.A, obj.B, obj.C, obj.D), e_source = ev_source, e_subsource=ev_subsource) for obj in list_obj]
      
    else:
      
        raise(ValueError, "data_type not known")
    
    return list_obj
