#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.94012451171875 * v8 + 10.6923828125 * v7 + 11.31982421875 * v3 + 9.537109375 * v0 + 6.8330078125 * v5 + 2.3599853515625 * v4 + 2.8131103515625 * v2 + 10.7880859375 * v1 + 4.51904296875 * v6;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30806*v8;
	// Computation of c7*v7 in r1
	r1 = 21898*v7;
	// Computation of r0+r1 in r0
	r0 = r0 % 17179869184;
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 23183*v3;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 19532*v0;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 27988*v5;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 19333*v4;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 23045*v2;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 22094*v1;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 18510*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,12,true> SoP_ac_fixed(ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,9,true,AC_TRN> v7,ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,9,true,AC_TRN> v0,ac_fixed<16,9,true,AC_TRN> v5,ac_fixed<16,10,true,AC_TRN> v4,ac_fixed<16,10,true,AC_TRN> v2,ac_fixed<16,8,true,AC_TRN> v1,ac_fixed<16,8,true,AC_TRN> v6)
{
	//Declaration of sums sd and s
	ac_fixed<32,12,true> sd = 0;
	ac_fixed<16,12,true> s = 0;

	//Computation of c8*v8 in register r0
	ac_fixed<16,1,true,AC_TRN> c8 = -0.94012451171875;
	ac_fixed<32,10,true,AC_TRN> r0 = c8*v8;

	//Computation of c7*v7 in register r1
	ac_fixed<16,5,true,AC_TRN> c7 = 10.6923828125;
	ac_fixed<32,14,true,AC_TRN> r1 = c7*v7;


	//Computation of r0+r1 in register r2
	ac_fixed<32,12,true,AC_TRN> r2 = r0 + r1;
	//Computation of c3*v3 in register r3
	ac_fixed<16,5,true,AC_TRN> c3 = 11.31982421875;
	ac_fixed<32,14,true,AC_TRN> r3 = c3*v3;


	//Computation of r2+r3 in register r4
	ac_fixed<32,12,true,AC_TRN> r4 = r2 + r3;
	//Computation of c0*v0 in register r5
	ac_fixed<16,5,true,AC_TRN> c0 = 9.537109375;
	ac_fixed<32,14,true,AC_TRN> r5 = c0*v0;


	//Computation of r4+r5 in register r6
	ac_fixed<32,12,true,AC_TRN> r6 = r4 + r5;
	//Computation of c5*v5 in register r7
	ac_fixed<16,4,true,AC_TRN> c5 = 6.8330078125;
	ac_fixed<32,13,true,AC_TRN> r7 = c5*v5;


	//Computation of r6+r7 in register r8
	ac_fixed<32,12,true,AC_TRN> r8 = r6 + r7;
	//Computation of c4*v4 in register r9
	ac_fixed<16,3,true,AC_TRN> c4 = 2.3599853515625;
	ac_fixed<32,13,true,AC_TRN> r9 = c4*v4;


	//Computation of r8+r9 in register r10
	ac_fixed<32,12,true,AC_TRN> r10 = r8 + r9;
	//Computation of c2*v2 in register r11
	ac_fixed<16,3,true,AC_TRN> c2 = 2.8131103515625;
	ac_fixed<32,13,true,AC_TRN> r11 = c2*v2;


	//Computation of r10+r11 in register r12
	ac_fixed<32,12,true,AC_TRN> r12 = r10 + r11;
	//Computation of c1*v1 in register r13
	ac_fixed<16,5,true,AC_TRN> c1 = 10.7880859375;
	ac_fixed<32,13,true,AC_TRN> r13 = c1*v1;


	//Computation of r12+r13 in register r14
	ac_fixed<32,12,true,AC_TRN> r14 = r12 + r13;
	//Computation of c6*v6 in register r15
	ac_fixed<16,4,true,AC_TRN> c6 = 4.51904296875;
	ac_fixed<32,12,true,AC_TRN> r15 = c6*v6;


	//Computation of r14+r15 in register r16
	ac_fixed<32,12,true,AC_TRN> r16 = r14 + r15;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
