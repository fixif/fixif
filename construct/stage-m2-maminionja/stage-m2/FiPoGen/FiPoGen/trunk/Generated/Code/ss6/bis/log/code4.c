#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -1.0289306640625 * v5 + -3.19482421875 * v3 + -1.37127685546875 * v2 + -2.971435546875 * v1 + -3.0521240234375 * v0 + -0.08646392822265625 * v4 + 0.1515655517578125 * v8 + -0.987030029296875 * v6 + -2.9359130859375 * v7;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -16858*v5;
	// Computation of c3*v3 in r1
	r1 = -26172*v3;
	// Computation of r0+r1 in r0
	r0 = r0 % 2147483648;
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -22467*v2;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -24342*v1;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -25003*v0;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -22666*v4;
	// Computation of c8*v8 in r2
	r2 = 19866*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c6*v6 in r2
	r2 = -32343*v6;
	// Computation of r1+r2 in r1
	r1 = r1 % 8589934592;
	r1 = r1 + r2;
	// Computation of c7*v7 in r2
	r2 = -24051*v7;
	// Computation of r1+r2 in r1
	r1 = r1 % 8589934592;
	r2 = r2 % 1073741824;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,10,true> SoP_ac_fixed(ac_fixed<16,9,true,AC_TRN> v5,ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,10,true,AC_TRN> v2,ac_fixed<16,9,true,AC_TRN> v1,ac_fixed<16,9,true,AC_TRN> v0,ac_fixed<16,10,true,AC_TRN> v4,ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,8,true,AC_TRN> v6,ac_fixed<16,9,true,AC_TRN> v7)
{
	//Declaration of sums sd and s
	ac_fixed<32,10,true> sd = 0;
	ac_fixed<16,10,true> s = 0;

	//Computation of c5*v5 in register r0
	ac_fixed<16,2,true,AC_TRN> c5 = -1.0289306640625;
	ac_fixed<32,11,true,AC_TRN> r0 = c5*v5;

	//Computation of c3*v3 in register r1
	ac_fixed<16,3,true,AC_TRN> c3 = -3.19482421875;
	ac_fixed<32,12,true,AC_TRN> r1 = c3*v3;


	//Computation of r0+r1 in register r2
	ac_fixed<32,10,true,AC_TRN> r2 = r0 + r1;
	//Computation of c2*v2 in register r3
	ac_fixed<16,2,true,AC_TRN> c2 = -1.37127685546875;
	ac_fixed<32,12,true,AC_TRN> r3 = c2*v2;


	//Computation of r2+r3 in register r4
	ac_fixed<32,10,true,AC_TRN> r4 = r2 + r3;
	//Computation of c1*v1 in register r5
	ac_fixed<16,3,true,AC_TRN> c1 = -2.971435546875;
	ac_fixed<32,12,true,AC_TRN> r5 = c1*v1;


	//Computation of r4+r5 in register r6
	ac_fixed<32,10,true,AC_TRN> r6 = r4 + r5;
	//Computation of c0*v0 in register r7
	ac_fixed<16,3,true,AC_TRN> c0 = -3.0521240234375;
	ac_fixed<32,12,true,AC_TRN> r7 = c0*v0;


	//Computation of r6+r7 in register r8
	ac_fixed<32,10,true,AC_TRN> r8 = r6 + r7;
	//Computation of c4*v4 in register r9
	ac_fixed<16,-2,true,AC_TRN> c4 = -0.08646392822265625;
	ac_fixed<32,8,true,AC_TRN> r9 = c4*v4;

	//Computation of c8*v8 in register r10
	ac_fixed<16,-1,true,AC_TRN> c8 = 0.1515655517578125;
	ac_fixed<32,8,true,AC_TRN> r10 = c8*v8;


	//Computation of r9+r10 in register r11
	ac_fixed<32,8,true,AC_TRN> r11 = r9 + r10;
	//Computation of c6*v6 in register r12
	ac_fixed<16,1,true,AC_TRN> c6 = -0.987030029296875;
	ac_fixed<32,9,true,AC_TRN> r12 = c6*v6;


	//Computation of r11+r12 in register r13
	ac_fixed<32,9,true,AC_TRN> r13 = r11 + r12;
	//Computation of c7*v7 in register r14
	ac_fixed<16,3,true,AC_TRN> c7 = -2.9359130859375;
	ac_fixed<32,12,true,AC_TRN> r14 = c7*v7;


	//Computation of r13+r14 in register r15
	ac_fixed<32,10,true,AC_TRN> r15 = r13 + r14;

	//Computation of r8+r15 in register r16
	ac_fixed<32,10,true,AC_TRN> r16 = r8 + r15;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
