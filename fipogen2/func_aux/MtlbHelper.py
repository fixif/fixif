#coding=utf8

import numpy.testing as npt

from numpy import where

from scipy.io import loadmat, savemat
import os, sys


# use matlab from python
# note : this should be transient and removed when published on internet
# http://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
# installed it in user folder with user
# cd "matlabroot\extern\engines\python"
# python setup.py install --user

import matlab.engine

class MtlbHelper(object):
    
    @staticmethod
    def _quoted(string):
        
        return "\'" + string + "\'"
       
    @staticmethod
    def _quoted_list(string_list):
        
        return ["\'" + string + "\'" for string in string_list]
    
    def __init__(self, target_folder = None):
    
        self.eng = matlab.engine.start_matlab()
        #self.debug_mat = True
        
        # current location of target functions to test
        abs_fwr_dir = os.path.join(os.getcwd(),"Structures","test","FWRToolbox","")
        self.eng.addpath(abs_fwr_dir, nargout=0)
        
        #print('==================================================')
        #print('Adding the following path to matlab engine : ')
        #print(abs_fwr_dir)
        #print('==================================================')
        
        if target_folder is None :
            target_folder = "tmp_mat"
        
        self.path_mat = os.path.join(os.getcwd(), target_folder, "")
        
        try:
            os.makedirs(self.path_mat)
        except OSError:
            if not os.path.isdir(self.path_mat): #don't complain if dir exists
                raise

    def _save(self, var):
    
        """
        saves var variable in var.mat file
        easier for debug purposes
        """
    
        fmt = "\'-v7\'" # we don't want hdf5 format
        
        filename = var + ".mat"
        
        abspath_filename = self._quoted(os.path.join(self.path_mat, filename))
    
        str_save = 'save(' + abspath_filename + "," + self._quoted(var) + "," + fmt + ');'
        
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
    
        abspath_filename = os.path.join(self.path_mat, filename)
    
        h = loadmat(abspath_filename)
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
    
        name_tmp = 'mtlb_inject'
    
        abspath_tmp = os.path.join(self.path_mat, name_tmp)

        savemat(abspath_tmp, tmp_dict)
    
        abspath_tmp += ".mat"

        cmd = "load(" + self._quoted(abspath_tmp) + ")"
    
        self.eng.eval(cmd, nargout=0)

    
        
    def compare(self, mtlb_code, varz, local_varz_dict, decim = 10):

        """
        Compare value stored in local_varz_dict with matlab values for a given executed code (mtlb_code)
        """
    
        is_debug = False
    
        def _reshape_1dto2d(var_dict): #could be replaced by atleast2d() ???
        
            for key in var_dict.keys():
                
#                print(key)
#                print(type(var_dict[key]))
                
                if var_dict[key].shape == (1,):
                    var_dict[key] = var_dict[key].reshape(1,1)
                
            return var_dict
    
        local_varz_dict = _reshape_1dto2d(local_varz_dict)
    
        tmp_dict = {}
    
        #print(mtlb_code)
    
        self.pushCmdGetVar(mtlb_code, varz, tmp_dict)
    
#         for var in varz:

#             print('+++++++++++++++')            
#             print('+++++++++++++++')
#             print(var)
#             print('+++++++++++++++')            
#             print('Matlab variable')
#             print('+++++++++++++++')
#             print(str(tmp_dict[var]))
#             print('+++++++++++++++')
#             print('Python variable')
#             print('+++++++++++++++')
#             print(str(local_varz_dict[var]))

        for var in varz:
        
            #print("Shape of tmp_dict[" + var + "]")
            #print(str(tmp_dict[var].shape))
            #print("Shape of local_varz_dict["+ var +"]")
            #print(str(local_varz_dict[var].shape))
        
            if is_debug:
                print("Comparing " + var)
            
            try:
                npt.assert_almost_equal(tmp_dict[var], local_varz_dict[var], decimal=decim)
            except AssertionError as e:
                
                print('+++++++++++++++ {0:12} mismatch'.format(var))

                
                if is_debug:

                    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    print(var)
                    print('+++++++++++++++')            
                    print('Matlab variable')
                    print('+++++++++++++++')
                    print(tmp_dict[var])
                    print('+++++++++++++++')
                    print('Python variable')
                    print('+++++++++++++++')
                    print(local_varz_dict[var])     
                    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')  

                if var in {'OP_dlk_dZ', 'CP_dlbk_dZ'}:
                    
                    print('warning (false positive) : discrepancy could be due to different order of eigenvalues')
                    print('if norm is the same, it is a strong indication of the former source of discrepancy')
                    
                else:
                	
 			    	print(e)               	
                    
#                     tmp_var_mtlb = tmp_dict[var]
#                     tmp_var_pyth = local_varz_dict[var]
#                     
#                     diff_mat = []
#                     
#                     for k in xrange(0, tmp_var_mtlb.shape[2]):
#                         diff_mat = tmp_var_mtlb[:,:,k] - tmp_var_pyth[:,:,k]
#                     
#                         for row, col in zip(*where(diff_mat >= 1.e-5)):
#                             print('{} , {} : {} / {}'.format(row, col, tmp_var_mtlb[row,col,k], tmp_var_pyth[row,col,k]))
                    