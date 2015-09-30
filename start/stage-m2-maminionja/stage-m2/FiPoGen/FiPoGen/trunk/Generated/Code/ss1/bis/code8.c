#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.1680450439453125 * v3 + 0.029571533203125 * v4 + 0.9363861083984375 * v1 + 0.0010986328125 * v6 + 0.3561248779296875 * v2 + -0.0430755615234375 * v5 + 0.42585659027099609375 * v0 + -0.9401397705078125 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7)
{
    // Registers declaration
	int32_t r0, r1, r2, r3;
	// Computation of c3*v3 in r0
	r0 = -22026*v3>> 13;
	// Computation of c4*v4 in r1
	r1 = 1938*v4>> 12;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 122734*v1>> 13;
	// Computation of c6*v6 in r2
	r2 = 9*v6>> 5;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 93356*v2>> 16;
	// Computation of c5*v5 in r2
	r2 = -2823*v5>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = 446543*v0>> 19;
	// Computation of c8*v8 in r3
	r3 = -61613*v8>> 15;
	// Computation of r2+r3 in r2
	r2 = r2 + r3;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<15,12,true> SoP_ac_fixed(ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<5,6,true,AC_TRN> v6,ac_fixed<16,11,true,AC_TRN> v2,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<19,13,true,AC_TRN> v0,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<16,-1,true,AC_TRN> c3 = -0.1680450439453125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<12,-4,true,AC_TRN> c4 = 0.029571533203125;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<18,1,true,AC_TRN> c1 = 0.9363861083984375;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<5,-8,true,AC_TRN> c6 = 0.0010986328125;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<18,0,true,AC_TRN> c2 = 0.3561248779296875;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<13,-3,true,AC_TRN> c5 = -0.0430755615234375;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true,AC_TRN> c0 = 0.42585659027099609375;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true,AC_TRN> c8 = -0.9401397705078125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
