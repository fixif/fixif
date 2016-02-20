all : adder_tb

adder.o : adder.vhdl
	ghdl -a -v adder.vhdl

adder_tb.o : adder_tb.vhdl adder.o
	ghdl -a -v adder_tb.vhdl
	
bidon.o : bidon.vhdl
	ghdl -a -v bidon.vhdl

bidon_c.o : bidon_c.c
	gcc -Wall -c bidon_c.c

adder_tb : adder.o bidon.o adder_tb.o bidon_c.o
	ghdl -e -v -Wl,bidon_c.o adder_tb

run : adder_tb
	ghdl -r adder_tb --vcd=adder.vcd

clean :
	rm *.o adder_tb
