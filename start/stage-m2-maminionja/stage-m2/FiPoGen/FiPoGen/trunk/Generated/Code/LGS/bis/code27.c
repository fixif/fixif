#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2)
{
    /*      TP_Float_sop        */
    double r;
    r = -1 * v1 + -2.8862152099609375 * v2 + 1.1335201263427734375 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c1*v1 in r0
	r0 = -524288*v1>> 6;
	// Computation of c2*v2 in r1
	r1 = -378302*v2>> 5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 594291*v0>> 5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 2;
}

ac_fixed<17,11,true> SoP_ac_fixed(ac_fixed<5,10,true,AC_TRN> v1,ac_fixed<5,9,true,AC_TRN> v2,ac_fixed<5,11,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,1,true,AC_TRN> c1 = -1;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,3,true,AC_TRN> c2 = -2.8862152099609375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<21,2,true,AC_TRN> c0 = 1.1335201263427734375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
