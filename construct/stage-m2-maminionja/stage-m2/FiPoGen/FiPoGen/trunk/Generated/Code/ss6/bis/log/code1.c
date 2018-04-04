#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.4557952880859375 * v7 + 0.37957763671875 * v4 + 0.3567962646484375 * v3 + 0.464202880859375 * v1 + -0.11966705322265625 * v6 + 0.051532745361328125 * v8 + -0.085346221923828125 * v5 + -0.07263946533203125 * v0 + -0.075801849365234375 * v2;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 29871*v7;
	// Computation of c4*v4 in r1
	r1 = 24876*v4;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 23383*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 30422*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -31370*v6;
	// Computation of c8*v8 in r2
	r2 = 27018*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c5*v5 in r2
	r2 = -22373*v5;
	// Computation of r1+r2 in r1
	r1 = r1 % 8589934592;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -19042*v0;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -19871*v2;
	// Computation of r1+r2 in r1
	r1 = r1 % 8589934592;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 % 8589934592;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,9,true> SoP_ac_fixed(ac_fixed<16,9,true,AC_TRN> v7,ac_fixed<16,10,true,AC_TRN> v4,ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,9,true,AC_TRN> v1,ac_fixed<16,8,true,AC_TRN> v6,ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,9,true,AC_TRN> v5,ac_fixed<16,9,true,AC_TRN> v0,ac_fixed<16,10,true,AC_TRN> v2)
{
	//Declaration of sums sd and s
	ac_fixed<32,9,true> sd = 0;
	ac_fixed<16,9,true> s = 0;

	//Computation of c7*v7 in register r0
	ac_fixed<16,0,true,AC_TRN> c7 = 0.4557952880859375;
	ac_fixed<32,9,true,AC_TRN> r0 = c7*v7;

	//Computation of c4*v4 in register r1
	ac_fixed<16,0,true,AC_TRN> c4 = 0.37957763671875;
	ac_fixed<32,10,true,AC_TRN> r1 = c4*v4;


	//Computation of r0+r1 in register r2
	ac_fixed<32,9,true,AC_TRN> r2 = r0 + r1;
	//Computation of c3*v3 in register r3
	ac_fixed<16,0,true,AC_TRN> c3 = 0.3567962646484375;
	ac_fixed<32,9,true,AC_TRN> r3 = c3*v3;


	//Computation of r2+r3 in register r4
	ac_fixed<32,9,true,AC_TRN> r4 = r2 + r3;
	//Computation of c1*v1 in register r5
	ac_fixed<16,0,true,AC_TRN> c1 = 0.464202880859375;
	ac_fixed<32,9,true,AC_TRN> r5 = c1*v1;


	//Computation of r4+r5 in register r6
	ac_fixed<32,9,true,AC_TRN> r6 = r4 + r5;
	//Computation of c6*v6 in register r7
	ac_fixed<16,-2,true,AC_TRN> c6 = -0.11966705322265625;
	ac_fixed<32,6,true,AC_TRN> r7 = c6*v6;

	//Computation of c8*v8 in register r8
	ac_fixed<16,-3,true,AC_TRN> c8 = 0.051532745361328125;
	ac_fixed<32,6,true,AC_TRN> r8 = c8*v8;


	//Computation of r7+r8 in register r9
	ac_fixed<32,6,true,AC_TRN> r9 = r7 + r8;
	//Computation of c5*v5 in register r10
	ac_fixed<16,-2,true,AC_TRN> c5 = -0.085346221923828125;
	ac_fixed<32,7,true,AC_TRN> r10 = c5*v5;


	//Computation of r9+r10 in register r11
	ac_fixed<32,7,true,AC_TRN> r11 = r9 + r10;
	//Computation of c0*v0 in register r12
	ac_fixed<16,-2,true,AC_TRN> c0 = -0.07263946533203125;
	ac_fixed<32,7,true,AC_TRN> r12 = c0*v0;


	//Computation of r11+r12 in register r13
	ac_fixed<32,7,true,AC_TRN> r13 = r11 + r12;
	//Computation of c2*v2 in register r14
	ac_fixed<16,-2,true,AC_TRN> c2 = -0.075801849365234375;
	ac_fixed<32,8,true,AC_TRN> r14 = c2*v2;


	//Computation of r13+r14 in register r15
	ac_fixed<32,8,true,AC_TRN> r15 = r13 + r14;

	//Computation of r6+r15 in register r16
	ac_fixed<32,9,true,AC_TRN> r16 = r6 + r15;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
