import numpy.testing as npt

from scipy.io import loadmat, savemat

# use matlab from python
# note : this should be transient and removed when published on internet
# http://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
# installed it in user folder with user
# cd "matlabroot\extern\engines\python"
# python setup.py install --user

import matlab.engine

class MtlbHelper(object):
    
    def __init__(self):
    
        self.eng = matlab.engine.start_matlab()
        #self.debug_mat = True

    def _save(self, var):
    
        """
        saves var variable in var.mat file
        easier for debug purposes
        """
    
        fmt = "\'-v7\'" # we don't want hdf5 format
        filename = "\'" + var + ".mat\'"
    
        str_save = 'save(' + filename + ",\'" + var + "\'," + fmt + ');'
        
        self.eng.eval(str_save, nargout = 0)
    
    def cleanenv(self):
  
        """
        Clean matlab engine environment
        """
    
        self.eng.eval('clear all ; close all ;', nargout = 0)
    
    def _getVar(self, var):
  
        """
        Get array VAR from mat file VAR.mat storing VAR variable
        """
    
        filename = var + '.mat'
    
        h = loadmat(filename)
        return h[var]
  
    def pushCmdGetVar(self, mtlb_code, varz, local_dict):
  
        """
        Get varz back from mtlb_code, by saving and loading mat files
        """
    
        self.eng.eval(mtlb_code, nargout = 0)
    
        for var in varz:
            self._save(var)
            local_dict[var] = self._getVar(var)

    def setVar(self, varz, varz_dict):
    
        """
        Inject variables in matlab engine environment using temp .mat file
        """
        
        tmp_dict = {}
    
        # force float conversion otherwise matlab will trip on calculations
        # involving integer and float arrays  
    
        for var in varz:
            tmp_dict[var] = varz_dict[var].astype(float)
    
        tmp_name = 'mtlb_inject'
    
        savemat(tmp_name, tmp_dict)
    
        cmd = "load(\'"+tmp_name+".mat\')"
    
        self.eng.eval(cmd, nargout=0)

    
        
    def compare(self, mtlb_code, varz, local_varz_dict, decim = 10):

        """
        Compare value stored in local_varz_dict with matlab values for a given executed code (mtlb_code)
        """
    
        tmp_dict = {}
    
        #print(mtlb_code)
    
        self.pushCmdGetVar(mtlb_code, varz, tmp_dict)
    
        #print("TMP_DICT")
        #print(tmp_dict)
        #print("LOCAL_VARZ_DICT")
        #print(local_varz_dict)
        
        for var in varz:
        
            #print("Shape of tmp_dict[" + var + "]")
            #print(str(tmp_dict[var].shape))
            #print("Shape of local_varz_dict["+ var +"]")
            #print(str(local_varz_dict[var].shape))
        
            print("Comparing "+var)
        
            npt.assert_almost_equal(tmp_dict[var], local_varz_dict[var], decimal=decim)
