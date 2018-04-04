#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1)
{
    /*      TP_Float_sop        */
    double r;
    r = 4.335906982421875 * v0 + 6.35687255859375 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 1136632*v0>> 6;
	// Computation of c1*v1 in r1
	r1 = 833208*v1>> 5;
	// Computation of r0+r1 in r0
	r0 = r0 % 4194304;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 1;
}

ac_fixed<18,11,true> SoP_ac_fixed(ac_fixed<5,9,true,AC_TRN> v0,ac_fixed<5,9,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,4,true,AC_TRN> c0 = 4.335906982421875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,4,true,AC_TRN> c1 = 6.35687255859375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
