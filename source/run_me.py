# App launcher and initializer
# Contexts of launch
# - standalone app with runtime arguments
# - standalone app with file-contained args
# - webapp run with web-input parameters

import sys

# Adding source folders to PYTHONPATH
sys.path.append("./class");
sys.path.append("./func_math");
sys.path.append("./func_run");
sys.path.append("./meth");

#print(sys.path);

from func_opt_management import load_global_opt, set_global_default ;

# TEMP
# Manual override
is_run_as_cli = False ;
is_run_as_webapp = False ;
is_run_as_standalone = True ;

# Default value for conf file
path_file = "./conf_fipogen.py" ;

set_global_default();

# Parse arguments and catch errors
# https://docs.python.org/2/library/argparse.html

if (__name__ == "__main__"):
    print("FiPoGen running in standalone mode (parameters as file)")
    load_global_opt("file",path_file) ;
elif is_run_as_cli:
    print("FiPoGen running in CLI mode (CL parameters")
    # Verify and parse args
    load_global_opt("CLI");
elif is_run_as_webapp:
    # Print nothing, debug
    print("FiPoGen running in webapp mode, waiting for parameters input in web UI")
    # Wait for keyboard-chair interface
    # func_load_webserver ;
    # func_setup_webserver ;
    load_global_opt("webapp") ;
    

    

    
