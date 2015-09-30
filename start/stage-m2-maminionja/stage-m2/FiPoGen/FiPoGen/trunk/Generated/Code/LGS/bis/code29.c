#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1)
{
    /*      TP_Float_sop        */
    double r;
    r = 1 * v0 + 0.0013408660888671875 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 4194304*v0>> 21;
	// Computation of c1*v1 in r1
	r1 = 703*v1>> 13;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 1;
}

ac_fixed<21,12,true> SoP_ac_fixed(ac_fixed<21,12,true,AC_TRN> v0,ac_fixed<13,9,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,2,true,AC_TRN> c0 = 1;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<11,-8,true,AC_TRN> c1 = 0.0013408660888671875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
