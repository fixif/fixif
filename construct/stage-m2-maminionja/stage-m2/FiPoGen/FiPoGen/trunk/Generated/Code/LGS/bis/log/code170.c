#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.414306640625 * v2 + -1 * v1 + 0.3468475341796875 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c2*v2 in r0
	r0 = -27152*v2;
	// Computation of c1*v1 in r1
	r1 = -32768*v1;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 22731*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,11,true> SoP_ac_fixed(ac_fixed<16,11,true,AC_TRN> v2,ac_fixed<16,11,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<32,11,true> sd = 0;
	ac_fixed<16,11,true> s = 0;

	//Computation of c2*v2 in register r0
	ac_fixed<16,0,true,AC_TRN> c2 = -0.414306640625;
	ac_fixed<32,11,true,AC_TRN> r0 = c2*v2;

	//Computation of c1*v1 in register r1
	ac_fixed<16,1,true,AC_TRN> c1 = -1;
	ac_fixed<32,12,true,AC_TRN> r1 = c1*v1;


	//Computation of r0+r1 in register r2
	ac_fixed<32,11,true,AC_TRN> r2 = r0 + r1;
	//Computation of c0*v0 in register r3
	ac_fixed<16,0,true,AC_TRN> c0 = 0.3468475341796875;
	ac_fixed<32,11,true,AC_TRN> r3 = c0*v0;


	//Computation of r2+r3 in register r4
	ac_fixed<32,11,true,AC_TRN> r4 = r2 + r3;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
