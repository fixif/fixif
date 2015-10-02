#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.005615234375 * v0 + -0.0100555419921875 * v1 + -0.025897979736328125 * v2 + 0.1504364013671875 * v3 + 0.19020843505859375 * v4 + 0.025909423828125 * v5 + 0.197509765625 * v6 + 0.0078125 * v7 + 0.05377197265625 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 2944*v0>> 19;
	// Computation of c1*v1 in r1
	r1 = -5272*v1>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -6789*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 19718*v3>> 14;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 24931*v4>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 849*v5>> 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 1618*v6>> 7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 2*v7>> 1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = 1762*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<11,9,true> SoP_ac_fixed(ac_fixed<19,13,true,AC_TRN> v0,ac_fixed<20,13,true,AC_TRN> v1,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<14,11,true,AC_TRN> v3,ac_fixed<15,11,true,AC_TRN> v4,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<7,7,true,AC_TRN> v6,ac_fixed<2,3,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<15,9,true> sd = 0;
	ac_fixed<11,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<13,-6,true,AC_TRN> c0 = 0.005615234375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<14,-5,true,AC_TRN> c1 = -0.0100555419921875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<14,-4,true,AC_TRN> c2 = -0.025897979736328125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<16,-1,true,AC_TRN> c3 = 0.1504364013671875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<16,-1,true,AC_TRN> c4 = 0.19020843505859375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<11,-4,true,AC_TRN> c5 = 0.025909423828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<12,-1,true,AC_TRN> c6 = 0.197509765625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<3,-5,true,AC_TRN> c7 = 0.0078125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<12,-3,true,AC_TRN> c8 = 0.05377197265625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
