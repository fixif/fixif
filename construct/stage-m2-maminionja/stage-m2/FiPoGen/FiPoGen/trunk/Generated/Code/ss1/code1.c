#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.0632369518280029296875 * v3 + -0.04792308807373046875 * v4 + 0.259254634380340576171875 * v1 + 0.000148773193359375 * v6 + -0.27274334430694580078125 * v2 + 0.01005458831787109375 * v5 + -0.86855566501617431640625 * v0 + 0.8806438446044921875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7)
{
    // Registers declaration
	int32_t r0, r1, r2, r3;
	// Computation of c3*v3 in r0
	r0 = -265235*v3>> 14;
	// Computation of c4*v4 in r1
	r1 = -201004*v4>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 4349571*v1>> 20;
	// Computation of c6*v6 in r2
	r2 = 39*v6>> 7;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -2287937*v2>> 17;
	// Computation of c5*v5 in r2
	r2 = 10543*v5>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -14571946*v0>> 19;
	// Computation of c8*v8 in r3
	r3 = 923422*v8>> 17;
	// Computation of r2+r3 in r2
	r2 = r2 + r3;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<20,13,true> SoP_ac_fixed(ac_fixed<14,11,true,AC_TRN> v3,ac_fixed<15,11,true,AC_TRN> v4,ac_fixed<20,13,true,AC_TRN> v1,ac_fixed<7,7,true,AC_TRN> v6,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<19,13,true,AC_TRN> v0,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,13,true> sd = 0;
	ac_fixed<20,13,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<20,-2,true,AC_TRN> c3 = -0.0632369518280029296875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,-3,true,AC_TRN> c4 = -0.04792308807373046875;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<24,0,true,AC_TRN> c1 = 0.259254634380340576171875;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<7,-11,true,AC_TRN> c6 = 0.000148773193359375;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true,AC_TRN> c2 = -0.27274334430694580078125;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<15,-5,true,AC_TRN> c5 = 0.01005458831787109375;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<25,1,true,AC_TRN> c0 = -0.86855566501617431640625;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<21,1,true,AC_TRN> c8 = 0.8806438446044921875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
