#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.718017578125 * v0;
	return r; 
}

int16_t C_int(int16_t v0)
{
    // Registers declaration
	// Computation of c0*v0 in r0
	r0 = 23528*v0;
	// The result is returned 	return r0;
}

ac_fixed<32,13,true> SoP_ac_fixed(ac_fixed<16,12,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<32,13,true> sd = 0;
	ac_fixed<32,13,true> s = 0;

	//Computation of c0*v0 in register r0
	ac_fixed<16,1,true,AC_TRN> c0 = 0.718017578125;
	ac_fixed<32,13,true,AC_TRN> r0 = c0*v0;


	//Computation of the final right shift
	s = s + sd;
	return s;
}
