import numpy.testing as npt

from scipy.io import loadmat

def mtlb_save(eng, var):
    
    """
    saves var variable in var.mat file
    easier for debug purposes
    """
    
    fmt = "\'-v7\'" # we don't want hdf5 format
    filename = "\'" + var + ".mat\'"
    
    str_save = 'save(' + filename + ",\'" + var + "\'," + fmt + ');'
    
    print(str_save)
    eng.eval(str_save,nargout=0)
    
def mtlb_cleanenv(eng):
  
    """
    Clean matlab engine environment
    """
    
    eng.eval('clear all ; close all ;',nargout=0)
    
def mtlb_getArray(target_var):
  
    """
    Get array VAR from mat file VAR.mat storing VAR variable
    """
    
    filename = target_var + '.mat'
    
    h = loadmat(filename)
    return h[target_var]
  
def mtlb_pushCmdGetVar(mtlb_eng, mtlb_code, varz, local_dict):
  
    """
    Get varz back from mtlb_code, by saving and loading mat files
    """
    
    #print(mtlb_code)
    
    mtlb_eng.eval(mtlb_code, nargout=0)
    
    for var in varz:
        mtlb_save(mtlb_eng, var)
        local_dict[var] = mtlb_getArray(var)
        
def mtlb_compare(mtlb_eng, mtlb_code, varz, local_varz_dict, decim = 10):

    """
    Compare value stored in local_varz_dict with matlab values for a given executed code (mtlb_code)
    """
    
    tmp_dict = {}
    
    mtlb_cleanenv(mtlb_eng)
    
    mtlb_pushCmdGetVar(mtlb_eng, mtlb_code, varz, tmp_dict)
    
    for var in varz:
    	
    	#print("Shape of tmp_dict[" + var + "]")
    	#print(str(tmp_dict[var].shape))
    	#print("Shape of local_varz_dict["+ var +"]")
    	#print(str(local_varz_dict[var].shape))
    	
        npt.assert_almost_equal(tmp_dict[var], local_varz_dict[var], decimal=decim)
