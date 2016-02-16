#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.04080212116241455078125 * v1 + 0.2146587371826171875 * v2 + 0.0861148834228515625 * v0 + 1 * v3;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c1*v1 in r0
	r0 = -342273*v1>> 21;
	// Computation of c2*v2 in r1
	r1 = 112543*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 45149*v0>> 17;
	// Computation of c3*v3 in r2
	r2 = 2048*v3>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 2;
}

ac_fixed<17,12,true> SoP_ac_fixed(ac_fixed<16,11,true,AC_TRN> v1,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<17,12,true,AC_TRN> v0,ac_fixed<16,9,true,AC_TRN> v3)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,-3,true,AC_TRN> c1 = -0.04080212116241455078125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<18,-1,true,AC_TRN> c2 = 0.2146587371826171875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<17,-2,true,AC_TRN> c0 = 0.0861148834228515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<13,2,true,AC_TRN> c3 = 1;
	sd = sd + c3*v3;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
