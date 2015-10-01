#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.068359375 * v6 + 0.125 * v7 + -0.007568359375 * v5;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c6*v6 in r0
	r0 = 70*v6>> 7;
	// Computation of c7*v7 in r1
	r1 = 8*v7>> 2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -31*v5>> 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<2,3,true> SoP_ac_fixed(ac_fixed<7,7,true,AC_TRN> v6,ac_fixed<2,3,true,AC_TRN> v7,ac_fixed<11,9,true,AC_TRN> v5)
{
	//Declaration of sums sd and s
	ac_fixed<6,3,true> sd = 0;
	ac_fixed<2,3,true> s = 0;

	//Computation of c6*v6 in sd
	ac_fixed<8,-2,true,AC_TRN> c6 = 0.068359375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<5,-1,true,AC_TRN> c7 = 0.125;
	sd = sd + c7*v7;
	//Computation of c5*v5 in sd
	ac_fixed<6,-6,true,AC_TRN> c5 = -0.007568359375;
	sd = sd + c5*v5;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
