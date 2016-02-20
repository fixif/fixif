#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.00975000858306884765625 * v0 + 0.21148622035980224609375 * v1 + 0.41028118133544921875 * v2 + 0.02339231967926025390625 * v3 + -0.13127040863037109375 * v4 + 0.62147486209869384765625 * v5 + 0.22900259494781494140625 * v6 + 0.07936370372772216796875 * v7 + -0.2047405242919921875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = -81789*v0>> 20;
	// Computation of c1*v1 in r1
	r1 = 3548150*v1>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 3441688*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 196229*v3>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -550588*v4>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 5213309*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 1921013*v6>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 1331502*v7>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -858744*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<18,9,true> SoP_ac_fixed(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,-5,true,AC_TRN> c0 = -0.00975000858306884765625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,-1,true,AC_TRN> c1 = 0.21148622035980224609375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true,AC_TRN> c2 = 0.41028118133544921875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,-4,true,AC_TRN> c3 = 0.02339231967926025390625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = -0.13127040863037109375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = 0.62147486209869384765625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,-1,true,AC_TRN> c6 = 0.22900259494781494140625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.07936370372772216796875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true,AC_TRN> c8 = -0.2047405242919921875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
