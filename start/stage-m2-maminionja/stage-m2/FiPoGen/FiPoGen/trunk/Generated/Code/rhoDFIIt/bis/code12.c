#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.44944667816162109375 * v1 + 0.202960968017578125 * v2 + 0.1256313323974609375 * v0 + 1 * v3;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c1*v1 in r0
	r0 = 471279*v1>> 20;
	// Computation of c2*v2 in r1
	r1 = 106410*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 65867*v0>> 17;
	// Computation of c3*v3 in r2
	r2 = 16384*v3>> 14;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 2;
}

ac_fixed<17,12,true> SoP_ac_fixed(ac_fixed<18,11,true,AC_TRN> v1,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<17,12,true,AC_TRN> v0,ac_fixed<16,9,true,AC_TRN> v3)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,0,true,AC_TRN> c1 = 0.44944667816162109375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<18,-1,true,AC_TRN> c2 = 0.202960968017578125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<18,-1,true,AC_TRN> c0 = 0.1256313323974609375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<16,2,true,AC_TRN> c3 = 1;
	sd = sd + c3*v3;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
