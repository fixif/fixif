#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -1.028922557830810546875 * v5 + -0.9870395660400390625 * v6 + -3.0521240234375 * v0 + -3.19485950469970703125 * v3 + 0.151564121246337890625 * v8 + -0.0864632129669189453125 * v4 + -2.935951709747314453125 * v7 + -1.3712866306304931640625 * v2 + -2.9714145660400390625 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -2157807*v5>> 20;
	// Computation of c6*v6 in r1
	r1 = -1034986*v6>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -6400768*v0>> 16;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -6700106*v3>> 19;
	// Computation of c8*v8 in r2
	r2 = 317853*v8>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 % 1048576;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -362653*v4>> 18;
	// Computation of c7*v7 in r2
	r2 = -6157137*v7>> 18;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -5751593*v2>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -6231508*v1>> 18;
	// Computation of r1+r2 in r1
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<18,10,true> SoP_ac_fixed(ac_fixed<20,9,true,AC_TRN> v5,ac_fixed<17,8,true,AC_TRN> v6,ac_fixed<16,9,true,AC_TRN> v0,ac_fixed<19,9,true,AC_TRN> v3,ac_fixed<15,9,true,AC_TRN> v8,ac_fixed<18,10,true,AC_TRN> v4,ac_fixed<18,9,true,AC_TRN> v7,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,2,true,AC_TRN> c5 = -1.028922557830810546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,1,true,AC_TRN> c6 = -0.9870395660400390625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,3,true,AC_TRN> c0 = -3.0521240234375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,3,true,AC_TRN> c3 = -3.19485950469970703125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-1,true,AC_TRN> c8 = 0.151564121246337890625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<20,-2,true,AC_TRN> c4 = -0.0864632129669189453125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<24,3,true,AC_TRN> c7 = -2.935951709747314453125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<24,2,true,AC_TRN> c2 = -1.3712866306304931640625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<24,3,true,AC_TRN> c1 = -2.9714145660400390625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
