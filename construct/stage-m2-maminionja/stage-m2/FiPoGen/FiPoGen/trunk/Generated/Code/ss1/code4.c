#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.3220920562744140625 * v3 + 0.6896762847900390625 * v4 + 0.04792308807373046875 * v1 + -0.003387451171875 * v6 + 0.1953983306884765625 * v2 + 0.19020843505859375 * v5 + -0.036738872528076171875 * v0 + -0.16170501708984375 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7)
{
    // Registers declaration
	int32_t r0, r1, r2, r3;
	// Computation of c3*v3 in r0
	r0 = -168869*v3>> 14;
	// Computation of c4*v4 in r1
	r1 = 361589*v4>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 100502*v1>> 20;
	// Computation of c6*v6 in r2
	r2 = -111*v6>> 7;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 204890*v2>> 17;
	// Computation of c5*v5 in r2
	r2 = 24931*v5>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -77047*v0>> 19;
	// Computation of c8*v8 in r3
	r3 = -21195*v8>> 17;
	// Computation of r2+r3 in r2
	r2 = r2 + r3;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<15,11,true> SoP_ac_fixed(ac_fixed<14,11,true,AC_TRN> v3,ac_fixed<15,11,true,AC_TRN> v4,ac_fixed<20,13,true,AC_TRN> v1,ac_fixed<7,7,true,AC_TRN> v6,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<19,13,true,AC_TRN> v0,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<15,11,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<19,0,true,AC_TRN> c3 = -0.3220920562744140625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,1,true,AC_TRN> c4 = 0.6896762847900390625;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<18,-3,true,AC_TRN> c1 = 0.04792308807373046875;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<8,-7,true,AC_TRN> c6 = -0.003387451171875;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<19,-1,true,AC_TRN> c2 = 0.1953983306884765625;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<16,-1,true,AC_TRN> c5 = 0.19020843505859375;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<18,-3,true,AC_TRN> c0 = -0.036738872528076171875;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<16,-1,true,AC_TRN> c8 = -0.16170501708984375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
