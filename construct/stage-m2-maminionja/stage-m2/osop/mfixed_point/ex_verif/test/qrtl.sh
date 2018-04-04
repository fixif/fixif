#!/bin/bash
quartus_map top_level --analysis_and_elaboration
#quartus_cmd -f quartus.tcl 
#quartus_sh -g  top_level
quartus_sh --tcl_eval set_global_assignment -name FAMILY "Cyclone IV GX"
quartus_sh --tcl_eval set_global_assignment -name DEVICE auto
quartus_sh --tcl_eval set_global_assignment -name TOP_LEVEL_ENTITY top_level
quartus_sh --tcl_eval set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
quartus_sh --tcl_eval set_global_assignment -name SEARCH_PATH /soc/alliance/cells/sxlib


# adding source files to project
for file in  $(ls *.vhd)
	do
		quartus_sh --tcl_eval set_global_assignment -name VHDL_FILE $file
		echo "adding $file to project"
	done



quartus_sh --clean top_level
quartus_map --read_settings_files=on --write_settings_files=off top_level -c top_level --analysis_and_elaboration

