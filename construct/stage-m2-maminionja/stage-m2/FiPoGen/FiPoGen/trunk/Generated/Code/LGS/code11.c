#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.33949184417724609375 * v0;
	return r; 
}

int16_t C_int(int16_t v0)
{
    // Registers declaration
	// Computation of c0*v0 in r0
	r0 = -711966*v0>> 19;
	// The result is returned 	return r0;
}

ac_fixed<19,10,true> SoP_ac_fixed(ac_fixed<19,12,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<19,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = -0.33949184417724609375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
