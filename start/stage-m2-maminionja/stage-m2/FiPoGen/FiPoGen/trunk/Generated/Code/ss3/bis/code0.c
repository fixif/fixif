#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.00672817230224609375 * v5 + -0.06734371185302734375 * v6 + 0.4674587249755859375 * v0 + -0.735332489013671875 * v3 + -0.009365081787109375 * v8 + 0.027843475341796875 * v4 + -0.664020538330078125 * v7 + 0.19712066650390625 * v2 + 0.310337066650390625 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -7055*v5>> 18;
	// Computation of c6*v6 in r1
	r1 = -70615*v6>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 245083*v0>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -192763*v3>> 15;
	// Computation of c8*v8 in r2
	r2 = -2455*v8>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 7299*v4>> 15;
	// Computation of c7*v7 in r2
	r2 = -348138*v7>> 16;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = 51674*v2>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = 81353*v1>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<15,10,true> SoP_ac_fixed(ac_fixed<18,11,true,AC_TRN> v5,ac_fixed<18,11,true,AC_TRN> v6,ac_fixed<15,10,true,AC_TRN> v0,ac_fixed<15,9,true,AC_TRN> v3,ac_fixed<15,9,true,AC_TRN> v8,ac_fixed<15,9,true,AC_TRN> v4,ac_fixed<16,10,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v2,ac_fixed<15,9,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,10,true> sd = 0;
	ac_fixed<15,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<14,-6,true,AC_TRN> c5 = -0.00672817230224609375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<18,-2,true,AC_TRN> c6 = -0.06734371185302734375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<19,0,true,AC_TRN> c0 = 0.4674587249755859375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<19,1,true,AC_TRN> c3 = -0.735332489013671875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<13,-5,true,AC_TRN> c8 = -0.009365081787109375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<14,-4,true,AC_TRN> c4 = 0.027843475341796875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,1,true,AC_TRN> c7 = -0.664020538330078125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<17,-1,true,AC_TRN> c2 = 0.19712066650390625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<18,0,true,AC_TRN> c1 = 0.310337066650390625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
