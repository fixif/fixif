# This file regroups functions for option management

def load_global_opt(source, path):
    "This function loads fipogen global options and parameters from different data sources, depending on user choice"
    " - file loads params from file "
    " - CLI loads args from CLI"
    " - webapp loads args from webpage"
     
    # Check args consistence
    if ( not( source == "file" or  source == "webapp" or  source == "CLI" )):
        print("load_global_options : arg error")
        exit()
# Dirty hardcoded definitions for global opts until other parts are complete

def set_global_default():
    "This functions sets default global parameters for the FiPoGen current run"