#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.4586870670318603515625 * v0;
	return r; 
}

int16_t C_int(int16_t v0)
{
    // Registers declaration
	// Computation of c0*v0 in r0
	r0 = -1923873*v0>> 20;
	// The result is returned 	return r0;
}

ac_fixed<21,11,true> SoP_ac_fixed(ac_fixed<20,12,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<21,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,0,true,AC_TRN> c0 = -0.4586870670318603515625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
