#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.223876953125 * v6 + -0.1648101806640625 * v7 + -0.109649658203125 * v1 + 0.084209442138671875 * v8 + -0.3734130859375 * v3 + -0.2354278564453125 * v5 + 0.311004638671875 * v4 + -0.292388916015625 * v2 + -0.620391845703125 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c6*v6 in r0
	r0 = -29344*v6;
	// Computation of c7*v7 in r1
	r1 = -21602*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -28744*v1;
	// Computation of c8*v8 in r2
	r2 = 22075*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r1 = r1 % 8589934592;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -24472*v3;
	// Computation of c5*v5 in r2
	r2 = -30858*v5;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 % 17179869184;
	r1 = r1 % 8589934592;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 20382*v4;
	// Computation of c2*v2 in r2
	r2 = -19162*v2;
	// Computation of r1+r2 in r1
	r2 = r2 % 2147483648;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -20329*v0;
	// Computation of r1+r2 in r1
	r2 = r2 % 2147483648;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,9,true> SoP_ac_fixed(ac_fixed<16,8,true,AC_TRN> v6,ac_fixed<16,8,true,AC_TRN> v7,ac_fixed<16,9,true,AC_TRN> v1,ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,8,true,AC_TRN> v3,ac_fixed<16,9,true,AC_TRN> v5,ac_fixed<16,9,true,AC_TRN> v4,ac_fixed<16,10,true,AC_TRN> v2,ac_fixed<16,9,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<32,9,true> sd = 0;
	ac_fixed<16,9,true> s = 0;

	//Computation of c6*v6 in register r0
	ac_fixed<16,-1,true,AC_TRN> c6 = -0.223876953125;
	ac_fixed<32,7,true,AC_TRN> r0 = c6*v6;

	//Computation of c7*v7 in register r1
	ac_fixed<16,-1,true,AC_TRN> c7 = -0.1648101806640625;
	ac_fixed<32,7,true,AC_TRN> r1 = c7*v7;


	//Computation of r0+r1 in register r2
	ac_fixed<32,7,true,AC_TRN> r2 = r0 + r1;
	//Computation of c1*v1 in register r3
	ac_fixed<16,-2,true,AC_TRN> c1 = -0.109649658203125;
	ac_fixed<32,7,true,AC_TRN> r3 = c1*v1;

	//Computation of c8*v8 in register r4
	ac_fixed<16,-2,true,AC_TRN> c8 = 0.084209442138671875;
	ac_fixed<32,7,true,AC_TRN> r4 = c8*v8;


	//Computation of r3+r4 in register r5
	ac_fixed<32,7,true,AC_TRN> r5 = r3 + r4;

	//Computation of r2+r5 in register r6
	ac_fixed<32,7,true,AC_TRN> r6 = r2 + r5;
	//Computation of c3*v3 in register r7
	ac_fixed<16,0,true,AC_TRN> c3 = -0.3734130859375;
	ac_fixed<32,8,true,AC_TRN> r7 = c3*v3;

	//Computation of c5*v5 in register r8
	ac_fixed<16,-1,true,AC_TRN> c5 = -0.2354278564453125;
	ac_fixed<32,8,true,AC_TRN> r8 = c5*v5;


	//Computation of r7+r8 in register r9
	ac_fixed<32,8,true,AC_TRN> r9 = r7 + r8;

	//Computation of r6+r9 in register r10
	ac_fixed<32,8,true,AC_TRN> r10 = r6 + r9;
	//Computation of c4*v4 in register r11
	ac_fixed<16,0,true,AC_TRN> c4 = 0.311004638671875;
	ac_fixed<32,9,true,AC_TRN> r11 = c4*v4;

	//Computation of c2*v2 in register r12
	ac_fixed<16,0,true,AC_TRN> c2 = -0.292388916015625;
	ac_fixed<32,10,true,AC_TRN> r12 = c2*v2;


	//Computation of r11+r12 in register r13
	ac_fixed<32,9,true,AC_TRN> r13 = r11 + r12;
	//Computation of c0*v0 in register r14
	ac_fixed<16,1,true,AC_TRN> c0 = -0.620391845703125;
	ac_fixed<32,10,true,AC_TRN> r14 = c0*v0;


	//Computation of r13+r14 in register r15
	ac_fixed<32,9,true,AC_TRN> r15 = r13 + r14;

	//Computation of r10+r15 in register r16
	ac_fixed<32,9,true,AC_TRN> r16 = r10 + r15;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
