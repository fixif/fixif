#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.062830448150634765625 * v0 + -0.184285640716552734375 * v1 + 0.37986850738525390625 * v2 + -0.3646709918975830078125 * v3 + -0.30541229248046875 * v4 + 0.5175302028656005859375 * v5 + 0.081939697265625 * v6 + -0.14939594268798828125 * v7 + -0.06005382537841796875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = -131765*v0>> 17;
	// Computation of c1*v1 in r1
	r1 = -386475*v1>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 398321*v2>> 14;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -1529541*v3>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -640496*v4>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 2170679*v5>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 343680*v6>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -156653*v7>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -62971*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<17,10,true> SoP_ac_fixed(ac_fixed<17,10,true,AC_TRN> v0,ac_fixed<17,10,true,AC_TRN> v1,ac_fixed<14,9,true,AC_TRN> v2,ac_fixed<18,11,true,AC_TRN> v3,ac_fixed<17,10,true,AC_TRN> v4,ac_fixed<18,11,true,AC_TRN> v5,ac_fixed<19,11,true,AC_TRN> v6,ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true,AC_TRN> c0 = -0.062830448150634765625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,-1,true,AC_TRN> c1 = -0.184285640716552734375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true,AC_TRN> c2 = 0.37986850738525390625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = -0.3646709918975830078125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,0,true,AC_TRN> c4 = -0.30541229248046875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,1,true,AC_TRN> c5 = 0.5175302028656005859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-2,true,AC_TRN> c6 = 0.081939697265625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true,AC_TRN> c7 = -0.14939594268798828125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<17,-3,true,AC_TRN> c8 = -0.06005382537841796875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
