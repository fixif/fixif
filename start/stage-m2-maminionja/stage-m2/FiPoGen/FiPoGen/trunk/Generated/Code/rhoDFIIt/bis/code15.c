#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.38869762420654296875 * v1 + 0.786346435546875 * v2 + 0.1322078704833984375 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c1*v1 in r0
	r0 = -815158*v1>> 19;
	// Computation of c2*v2 in r1
	r1 = 51534*v2>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 138630*v0>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 2;
}

ac_fixed<18,12,true> SoP_ac_fixed(ac_fixed<18,12,true,AC_TRN> v1,ac_fixed<16,9,true,AC_TRN> v2,ac_fixed<17,12,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<20,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<21,0,true,AC_TRN> c1 = -0.38869762420654296875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<17,1,true,AC_TRN> c2 = 0.786346435546875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true,AC_TRN> c0 = 0.1322078704833984375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
