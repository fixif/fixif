#include <stdio.h>
#include "std_log2c.h"
#include "amd_iss_c.h"

void amd_run( Amd_port *port)
//Amd_out amd_run( Amd_in *in)
	{
	static unsigned int ram[16] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
	static unsigned int accu = 15;
	static int temps = 36;

	unsigned int r, s, alu_out;
	//Amd_out out;

	unsigned int a = std2ui( port->a, 4);
	unsigned int b = std2ui( port->b, 4);
	unsigned int d = std2ui( port->d, 4);
	unsigned int i = std2ui( port->i, 9);
	unsigned int cin = std2ui( &(port->cin), 1);

	unsigned int q0;
	unsigned int r0;
	unsigned int q3;
	unsigned int r3;

	unsigned int pi;
	unsigned int gi;

	switch (i & 0x7)
		{
		case 0 :
			r = ram[a];
			s = accu;
			break;
		case 1 :
			r = ram[a];
			s = ram[b];
			break;
		case 2 :
			r = 0;
			s = accu;
			break;
		case 3 :
			r = 0;
			s = ram[b];
			break;
		case 4 :
			r = 0;
			s = ram[a];
			break;
		case 5 :
			r = d;
			s = ram[a];
			break;
		case 6 :
			r = d;
			s = accu;
			break;
		case 7 :
			r = d;
			s = 0;
		}

	// alu_out
	switch ((i >> 3) & 0x7)
		{
		case 0 :
			alu_out = r + s + cin;
			port->cout = (alu_out & 0x10)? STD_1 : STD_0;
			break;
		case 1 :
			alu_out = (cin)? s - r : s - r - 1;
			port->cout = (alu_out & 0x10)? STD_0 : STD_1;
			break;
		case 2 :
			alu_out = (cin)? r - s : r - s - 1;
			port->cout = (alu_out & 0x10)? STD_0 : STD_1;
			break;
		case 3 :
			alu_out = r | s;
			break;
		case 4 :
			alu_out = r & s;
			break;
		case 5 :
			alu_out = (~r) & s;
			break;
		case 6 :
			alu_out = r ^ s;
			break;
		case 7 :
			alu_out = ~(r ^ s);
		}
	//Flags
	//np
	switch ((i >> 3) & 0x7)
		{
		case 0 :
			pi = (r | s) & 0xF;
			port->np = (pi == 0xf)? STD_0 : STD_1;
			gi = (r & s) & 0xF;
			port->ng = ((gi & 8) ||
						((gi & 4) && (pi & 8) ) ||
						((gi & 2) && (pi & 8) && (pi & 4)) ||
						((gi & 1) && (pi & 8) && (pi & 4) && (pi & 2)))? STD_0 : STD_1;
			port->ovr = (((r & 8) == (s & 8)) && ((alu_out & 8) != (r & 8)))? STD_1 : STD_0;
			break;
		case 1 :
			pi = ((~r) | s) & 0xF;
			port->np = (pi == 0xf)? STD_0 : STD_1;
			gi = ((~r) & s) & 0xF;
			port->ng = ((gi & 8) ||
						((gi & 4) && (pi & 8) ) ||
						((gi & 2) && (pi & 8) && (pi & 4)) ||
						((gi & 1) && (pi & 8) && (pi & 4) && (pi & 2)))? STD_0 : STD_1;
			port->ovr = ((((~r) & 8) == (s & 8)) && ((alu_out & 8) != (s & 8)))? STD_1 : STD_0;
			break;
		case 2 :
			pi = (r | (~s)) & 0xF;
			port->np = (pi == 0xf)? STD_0 : STD_1;
			gi = (r & (~s)) & 0xF;
			port->ng = ((gi & 8) ||
						((gi & 4) && (pi & 8) ) ||
						((gi & 2) && (pi & 8) && (pi & 4)) ||
						((gi & 1) && (pi & 8) && (pi & 4) && (pi & 2)))? STD_0 : STD_1;
			port->ovr = (((r & 8) == ((~s) & 8)) && ((alu_out & 8) != (r & 8)))? STD_1 : STD_0;
			break;
		case 3 :
			pi = (r | s) & 0xF;
			port->np = STD_0;
			port->ng = (pi == 0xf)? STD_1 : STD_0;
			port->cout = ((!(pi == 0xf)) || cin)? STD_1 : STD_0;
			port->ovr = ((!(pi == 0xf)) || cin)? STD_1 : STD_0;
			break;
		case 4 :
			port->np = STD_0;
			gi = (r & s) & 0xF;
			port->ng = (gi) ? STD_0 : STD_1;
			port->cout = (gi || cin)? STD_1 : STD_0;
			port->ovr = ((gi == 0) || !cin)? STD_1 : STD_0;
			break;
		case 5 :
			port->np = STD_0;
			gi = ((~r) & s) & 0xF;
			port->ng = (gi) ? STD_0 : STD_1;
			port->cout = (gi || cin)? STD_1 : STD_0;
			port->ovr = ((gi == 0) || !cin)? STD_1 : STD_0;
			break;
		case 6 :
			pi = ((~r) | s) & 0xF;
			gi = ((~r) & s) & 0xF;
			port->np = (gi) ? STD_1 : STD_0;
			port->ng = (((gi & 8) && (pi & 8)) ||
						((gi & 4) && (pi & 8) && (pi & 4)) ||
						((gi & 2) && (pi & 8) && (pi & 4) && (pi & 2)) ||
						((pi & 8) && (pi & 4) && (pi & 2) && (pi & 1))) ? STD_1 : STD_0;
			port->cout = (((gi & 8) && (pi & 8)) ||
						((gi & 4) && (pi & 8) && (pi & 4)) ||
						((gi & 2) && (pi & 8) && (pi & 4) && (pi & 2)) ||
						((pi & 8) && (pi & 4) && (pi & 2) && (pi & 1) && ( (gi & 1) || !cin))) ? STD_1 : STD_0;
			port->ovr = (port->cout == STD_0)? STD_1 : STD_0;
			break;
		case 7 :
			pi = (r | s) & 0xF;
			gi = (r & s) & 0xF;
			port->np = (gi) ? STD_1 : STD_0;
			port->ng = (((gi & 8) && (pi & 8)) ||
						((gi & 4) && (pi & 8) && (pi & 4)) ||
						((gi & 2) && (pi & 8) && (pi & 4) && (pi & 2)) ||
						((pi & 8) && (pi & 4) && (pi & 2) && (pi & 1))) ? STD_1 : STD_0;
			port->cout = (((gi & 8) && (pi & 8)) ||
						((gi & 4) && (pi & 8) && (pi & 4)) ||
						((gi & 2) && (pi & 8) && (pi & 4) && (pi & 2)) ||
						((pi & 8) && (pi & 4) && (pi & 2) && (pi & 1) && ( (gi & 1) || !cin))) ? STD_1 : STD_0;
			port->ovr = (port->cout == STD_0)? STD_1 : STD_0;
		}
	alu_out &= 0xF;


	// Signe

	port->sign = (alu_out & 8)? STD_1 : STD_0;

	// Zero

	port->zero = (alu_out)? STD_0 : STD_1;

	

	if (port->noe == STD_1) slv_setv(port->y, 4, "%s", "ZZZZ");
	else
		{
		if (((i >> 6) & 0x7) == 2) slv_setv(port->y, 4, "%u", ram[a]);
		else slv_setv(port->y, 4, "%u", alu_out);
		}

	switch ((i >> 6) & 0x7)
		{
		case 0 :
			accu = alu_out;
			break;
		case 2 :
		case 3 :
			ram[b] = alu_out;
			break;
		case 4 :
			q3 = std2ui( &(port->q3), 1);
			r3 = std2ui( &(port->r3), 1);
			port->q0 = (accu & 1)? STD_1 : STD_0;
			port->r0 = (alu_out & 1)? STD_1 : STD_0;
			accu = ((accu >> 1) | (q3 << 3)) & 0xf;
			ram[b] = ((alu_out >> 1) | (r3 << 3)) & 0xf;
			break;
		case 5 :
			r3 = std2ui( &(port->r3), 1);
			port->q0 = (accu & 1)? STD_1 : STD_0;
			port->r0 = (alu_out & 1)? STD_1 : STD_0;
			ram[b] = ((alu_out >> 1) | (r3 << 3)) & 0xf;
			break;
		case 6 :
			q0 = std2ui( &(port->q0), 1);
			r0 = std2ui( &(port->r0), 1);
			port->q3 = (accu & 8)? STD_1 : STD_0;
			port->r3 = (alu_out & 8)? STD_1 : STD_0;
			accu = ((accu << 1) | q0) & 0xf;
			ram[b] = ((alu_out << 1) | r0) & 0xf;
			break;
		case 7 :
			r0 = std2ui( &(port->r0), 1);
			port->q3 = (accu & 8)? STD_1 : STD_0;
			port->r3 = (alu_out & 8)? STD_1 : STD_0;
			ram[b] = ((alu_out << 1) | r0) & 0xf;
		}
	//return out;
	//printf("accu = %x\n",accu);
	printf("%d : ram[12] = %x \t ram[7] = %x \taccu = %x\n", temps+=4,ram[12],ram[7], accu);
	}
