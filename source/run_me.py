# App launcher and initializer
# Contexts of launch
# - standalone app with runtime arguments
# - standalone app with file-contained args
# - webapp run with web-input parameters

# Run as Standalone

# Parse arguments and catch errors
# https://docs.python.org/2/library/argparse.html

import sys

# Adding source folders to PYTHONPATH
sys.path.append("./source/class")
sys.path.append("./source/func_math")
sys.path.append("./source/func_run")
sys.path.append("./source/meth")

# TEMP
# Manual override
is_run_as_cli = False
is_run_as_webapp = False
is_run_as_standalone = True

# Parse command line args

if (__name__ == "__main__"):
    print("FiPoGen running in standalone mode (parameters as file)")
    load_global_options("file",path_file)
elif is_run_as_cli:
    print("FiPoGen running in CLI mode (parameters as CL")
    load_global_options("CLI")
elif is_run_as_webapp:
    # Print nothing, debug
    print("FiPoGen runnin in webapp mode, waiting for parameters input in web UI")
    load_global_options("webapp")
    

    
