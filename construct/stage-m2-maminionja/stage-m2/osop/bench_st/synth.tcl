set file_list [glob *.vhd]
read_file -format vhdl $file_list
current_design top_cell
compile -exact_map
report_area -nosplit > area.txt
report_timing -path full -delay max -nworst 1 -max_paths 1 -significant_digits 2 -sort_by group > timing.txt
report_power > power.txt
quit
