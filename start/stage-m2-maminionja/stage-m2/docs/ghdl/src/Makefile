all : amd_tb

amd2901.o : amd2901.vhdl
	ghdl -a -v amd2901.vhdl

amd_iss.o : amd_iss.vhdl
	ghdl -a -v amd_iss.vhdl

amd_tb.o : amd_tb.vhdl
	ghdl -a -v amd_tb.vhdl

std_log2c.o : std_log2c.c
	gcc -Wall -c  std_log2c.c

amd_iss_c.o : amd_iss_c.c
	gcc -Wall -c  amd_iss_c.c

amd_tb : amd_iss.o amd_tb.o amd2901.o amd_iss_c.o std_log2c.o
	ghdl -e -v -Wl,amd_iss_c.o -Wl,std_log2c.o amd_tb

run : amd_tb
	ghdl -r amd_tb --vcd=amd_tb.vcd

clean :
	rm *.o amd_tb
