#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.040802001953125 * v3 + 0.086116790771484375 * v0 + 0.21466064453125 * v2 + 1 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -21392*v3;
	// Computation of c0*v0 in r1
	r1 = 22575*v0;
	// Computation of r0+r1 in r0
	r0 = r0 % 68719476736;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 28136*v2;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,12,true> SoP_ac_fixed(ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,12,true,AC_TRN> v0,ac_fixed<16,12,true,AC_TRN> v2,ac_fixed<16,11,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<32,12,true> sd = 0;
	ac_fixed<16,12,true> s = 0;

	//Computation of c3*v3 in register r0
	ac_fixed<16,-3,true,AC_TRN> c3 = -0.040802001953125;
	ac_fixed<32,6,true,AC_TRN> r0 = c3*v3;

	//Computation of c0*v0 in register r1
	ac_fixed<16,-2,true,AC_TRN> c0 = 0.086116790771484375;
	ac_fixed<32,10,true,AC_TRN> r1 = c0*v0;


	//Computation of r0+r1 in register r2
	ac_fixed<32,10,true,AC_TRN> r2 = r0 + r1;
	//Computation of c2*v2 in register r3
	ac_fixed<16,-1,true,AC_TRN> c2 = 0.21466064453125;
	ac_fixed<32,11,true,AC_TRN> r3 = c2*v2;


	//Computation of r2+r3 in register r4
	ac_fixed<32,11,true,AC_TRN> r4 = r2 + r3;
	//Computation of c1*v1 in register r5
	ac_fixed<16,2,true,AC_TRN> c1 = 1;
	ac_fixed<32,13,true,AC_TRN> r5 = c1*v1;


	//Computation of r4+r5 in register r6
	ac_fixed<32,12,true,AC_TRN> r6 = r4 + r5;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
