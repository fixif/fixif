#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.04531097412109375 * v1 + 1 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c1*v1 in r0
	r0 = 23756*v1;
	// Computation of c0*v0 in r1
	r1 = 16384*v0;
	// Computation of r0+r1 in r0
	r0 = r0 % 137438953472;
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,11,true> SoP_ac_fixed(ac_fixed<16,9,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<32,11,true> sd = 0;
	ac_fixed<16,11,true> s = 0;

	//Computation of c1*v1 in register r0
	ac_fixed<16,-3,true,AC_TRN> c1 = 0.04531097412109375;
	ac_fixed<32,6,true,AC_TRN> r0 = c1*v1;

	//Computation of c0*v0 in register r1
	ac_fixed<16,2,true,AC_TRN> c0 = 1;
	ac_fixed<32,13,true,AC_TRN> r1 = c0*v0;


	//Computation of r0+r1 in register r2
	ac_fixed<32,11,true,AC_TRN> r2 = r0 + r1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
