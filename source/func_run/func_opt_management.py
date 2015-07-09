# This file regroups functions for option management
from __builtin__ import file
def load_global_options(source, path):
    "This function loads fipogen global options and parameters from different data sources, depending on user choice"
    " - file loads params from file "
    " - CLI loads args from CLI"
    " - webapp loads args from webpage"
     
    # Check args consistence
    if ( is not(( source == "file"   ) or
                ( source == "webapp" ) or
                ( source == "CLI"    )):
        print("load_global_options : arg error"))
    
# Dirty hardcoded definitions for global opts until other parts are complete

    