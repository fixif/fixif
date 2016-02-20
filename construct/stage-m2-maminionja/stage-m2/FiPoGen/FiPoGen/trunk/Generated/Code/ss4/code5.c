#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.57534277439117431640625 * v0 + -1 * v1 + -0.58932578563690185546875 * v2 + -1.2217237949371337890625 * v3 + -0.5938303470611572265625 * v4 + -0.69000327587127685546875 * v5 + -1.0699279308319091796875 * v6 + -0.375308573246002197265625 * v7 + 0.3114802837371826171875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = -4826325*v0>> 19;
	// Computation of c1*v1 in r1
	r1 = -16777216*v1>> 20;
	// Computation of r0+r1 in r0
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -4943623*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -10248562*v3>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -2490705*v4>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -5788167*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -4487603*v6>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -6296633*v7>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = 1306443*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<19,10,true> SoP_ac_fixed(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true,AC_TRN> c0 = -0.57534277439117431640625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = -1;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<24,1,true,AC_TRN> c2 = -0.58932578563690185546875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true,AC_TRN> c3 = -1.2217237949371337890625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<23,1,true,AC_TRN> c4 = -0.5938303470611572265625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = -0.69000327587127685546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<24,2,true,AC_TRN> c6 = -1.0699279308319091796875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true,AC_TRN> c7 = -0.375308573246002197265625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = 0.3114802837371826171875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
