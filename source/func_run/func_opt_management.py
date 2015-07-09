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
    # This file gathers constants, options and parameters related to the run
    # To maintain consistency, options defined here should NOT vary during the run
    # Consistency in norm calculations, etc...


    # EPSILON for SST verification
    global GLOB_EPSILON ;
    
    GLOB_EPSILON = 1.e-8 ;
    
    # norms
    global GLOB_NORRM_OPT_L1, GLOB_OPT_NORM_L2 ;
    
    GLOB_OPT_NORM_L1 = "basic" ;
    GLOB_OPT_NORM_L2 = "basic" ;

    # SST description
    # 'direct','formII','rho1','rho2'
    # Different methods can be used
    global OPT_SST_DESC ;
    
    OPT_SST_DESC = ['direct' 'formII'] ;

    # Parameters for realization selection / SOFTWARE
    global OPT_PRM_SW, OPT_PRM_SW_WEIGHT ;
    
    OPT_PRM_SW        = [['norm_l2' 'norm_l1'],['norm_l2'],['#ops']] ;
    OPT_PRM_SW_WEIGHT = [[0.4 0.6],[1],[1]] ;

    # Parameters for realization selection / HARDWARE
    # Sum of weights should be verified when parameters are imported, etc
    # Parameter list
    # elec_power, circuit_size, op_num

    # list with alldefault_options parameters for all runs (example with 2 runs)

    global OPT_PRM_HW, OPT_PRM_HW_WEIGHT ;
    
    OPT_PRM_HW        = [['elec_power' 'circuit_size'], ['circuit_size']] ;
    OPT_PRM_HW_WEIGHT = [[0.5 0.5],                     [1]] ;

    # Parameters for target architecture
    # 'virtual' : virtual architecture with no constraint on bit lengths etc
    # 'virtex1' : example arch
    # Optimization can be done at the same time with array def

    global OPT_ARCH_TYPE ;

    OPT_ARCH_TYPE = ['virtual' 'virtual' 'virtex2' 'xilinx2000'] ;

    # if the architecture is virtual the machine does not know what we want
    
    global OPT_FPO_LENGTH
    OPT_FPO_LENGTH = [16 8] ;

    # This could be done otherwise if we define a class with all relevant info for architectures
    # TBD / Thibault

    # Database of current known artchitectures with known constraints

