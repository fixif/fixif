#coding=utf8

"""
Get data (TS/SS) from existing source on hard drive or if not exists, create some
"""

__author__ = "Joachim Kruithof"
__copyright__ = "Copyright 2015, FIPOgen Project, LIP6"
__credits__ = ["Joachim Kruithof"]

__license__ = "CECILL-C"
__version__ = "1.0a"
__maintainer__ = "Joachim Kruithof"
__email__ = "joachim.kruithof@lip6.fr"
__status__ = "Beta"

from glob import glob
import os
import sys
import pickle

from gen_data import gen_data

def gen_data_files(data_type, data_source, opt, file_basename, file_suffix):
        
    # get list of objects
    list_obj = gen_data(data_type, data_source, opt)
        
    i = 0
        
    # save obj to file
    for obj in list_obj:
            
        with open(file_basename + str(i) + file_suffix, 'wb') as pfile:
            pickle.dump(obj, pfile, protocol=0) # use human-readable format
            
        i += 1
        
def load_data_files(files_current):
        
    list_obj = []
        
    for file in files_current:
        with open(file, 'r') as pfile:
            list_obj.append(pickle.load(pfile))
        
    return list_obj        

def get_data(data_type, data_source, opt="", dir_data=None, is_refresh=False):

    list_obj = [] # dTF or dSS list
    dir_start = os.getcwd()
    
    default_folder = "test_data"
    file_sep = "_"
    file_basename = data_type + file_sep
    file_suffix = ".fip"
    
    if dir_data is None:
        dir_data = os.path.join(os.getcwd(), default_folder)
        
    dir_data = os.path.join(dir_data, data_source, opt)

    # http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
    try: 
        os.makedirs(dir_data)
    except OSError:
        if not os.path.isdir(dir_data):
            raise
            print('Could not create directory for fipogen data')

    os.chdir(dir_data)

    # check if some data already exists
    files_current = glob(file_basename + "*" + file_suffix)
    
    if is_refresh:
        
        for file in files_current:
            
            try:
                os.remove(file)
            except OSError:
                print("Could not delete file " + file)
            
        files_current = []
    
    if not files_current:
        gen_data_files(data_type, data_source, opt, file_basename, file_suffix)
        files_current = glob(file_basename + "*")
    
    list_obj = load_data_files(files_current)
    
    os.chdir(dir_start)
    
    return list_obj
    