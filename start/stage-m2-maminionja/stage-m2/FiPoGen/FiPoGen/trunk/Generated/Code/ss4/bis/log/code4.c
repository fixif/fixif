#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -1.19146728515625 * v6 + -1.91790771484375 * v2 + -4.603759765625 * v1 + -0.059307098388671875 * v4 + 0.252838134765625 * v8 + -1.3551025390625 * v5 + -4.508056640625 * v7 + -5.04541015625 * v3 + -4.80615234375 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c6*v6 in r0
	r0 = -19521*v6;
	// Computation of c2*v2 in r1
	r1 = -31423*v2;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -18857*v1;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -31094*v4;
	// Computation of c8*v8 in r2
	r2 = 16570*v8;
	// Computation of r1+r2 in r1
	r1 = r1 % 17179869184;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 % 8589934592;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -22202*v5;
	// Computation of c7*v7 in r2
	r2 = -18465*v7;
	// Computation of r1+r2 in r1
	r1 = r1 % 2147483648;
	r2 = r2 % 536870912;
	r1 = r1 + r2;
	// Computation of c3*v3 in r2
	r2 = -20666*v3;
	// Computation of r1+r2 in r1
	r2 = r2 % 536870912;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -19686*v0;
	// Computation of r1+r2 in r1
	r2 = r2 % 536870912;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,10,true> SoP_ac_fixed(ac_fixed<16,8,true,AC_TRN> v6,ac_fixed<16,10,true,AC_TRN> v2,ac_fixed<16,8,true,AC_TRN> v1,ac_fixed<16,10,true,AC_TRN> v4,ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,9,true,AC_TRN> v5,ac_fixed<16,9,true,AC_TRN> v7,ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,9,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<32,10,true> sd = 0;
	ac_fixed<16,10,true> s = 0;

	//Computation of c6*v6 in register r0
	ac_fixed<16,2,true,AC_TRN> c6 = -1.19146728515625;
	ac_fixed<32,10,true,AC_TRN> r0 = c6*v6;

	//Computation of c2*v2 in register r1
	ac_fixed<16,2,true,AC_TRN> c2 = -1.91790771484375;
	ac_fixed<32,12,true,AC_TRN> r1 = c2*v2;


	//Computation of r0+r1 in register r2
	ac_fixed<32,10,true,AC_TRN> r2 = r0 + r1;
	//Computation of c1*v1 in register r3
	ac_fixed<16,4,true,AC_TRN> c1 = -4.603759765625;
	ac_fixed<32,12,true,AC_TRN> r3 = c1*v1;


	//Computation of r2+r3 in register r4
	ac_fixed<32,10,true,AC_TRN> r4 = r2 + r3;
	//Computation of c4*v4 in register r5
	ac_fixed<16,-3,true,AC_TRN> c4 = -0.059307098388671875;
	ac_fixed<32,7,true,AC_TRN> r5 = c4*v4;

	//Computation of c8*v8 in register r6
	ac_fixed<16,0,true,AC_TRN> c8 = 0.252838134765625;
	ac_fixed<32,9,true,AC_TRN> r6 = c8*v8;


	//Computation of r5+r6 in register r7
	ac_fixed<32,9,true,AC_TRN> r7 = r5 + r6;

	//Computation of r4+r7 in register r8
	ac_fixed<32,10,true,AC_TRN> r8 = r4 + r7;
	//Computation of c5*v5 in register r9
	ac_fixed<16,2,true,AC_TRN> c5 = -1.3551025390625;
	ac_fixed<32,11,true,AC_TRN> r9 = c5*v5;

	//Computation of c7*v7 in register r10
	ac_fixed<16,4,true,AC_TRN> c7 = -4.508056640625;
	ac_fixed<32,13,true,AC_TRN> r10 = c7*v7;


	//Computation of r9+r10 in register r11
	ac_fixed<32,10,true,AC_TRN> r11 = r9 + r10;
	//Computation of c3*v3 in register r12
	ac_fixed<16,4,true,AC_TRN> c3 = -5.04541015625;
	ac_fixed<32,13,true,AC_TRN> r12 = c3*v3;


	//Computation of r11+r12 in register r13
	ac_fixed<32,10,true,AC_TRN> r13 = r11 + r12;
	//Computation of c0*v0 in register r14
	ac_fixed<16,4,true,AC_TRN> c0 = -4.80615234375;
	ac_fixed<32,13,true,AC_TRN> r14 = c0*v0;


	//Computation of r13+r14 in register r15
	ac_fixed<32,10,true,AC_TRN> r15 = r13 + r14;

	//Computation of r8+r15 in register r16
	ac_fixed<32,10,true,AC_TRN> r16 = r8 + r15;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
