#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.0138523578643798828125 * v5 + -0.0065402984619140625 * v6 + -0.6363646984100341796875 * v0 + -0.4085009098052978515625 * v3 + -0.117447376251220703125 * v8 + -0.2258586883544921875 * v4 + 0.11992645263671875 * v7 + -0.0255870819091796875 * v2 + -0.4553165435791015625 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = 58101*v5>> 20;
	// Computation of c6*v6 in r1
	r1 = -13716*v6>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -2669107*v0>> 16;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -1713377*v3>> 19;
	// Computation of c8*v8 in r2
	r2 = -492610*v8>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -1894640*v4>> 18;
	// Computation of c7*v7 in r2
	r2 = 503008*v7>> 18;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -214640*v2>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -1909736*v1>> 18;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<17,8,true> SoP_ac_fixed(ac_fixed<20,9,true,AC_TRN> v5,ac_fixed<17,8,true,AC_TRN> v6,ac_fixed<16,9,true,AC_TRN> v0,ac_fixed<19,9,true,AC_TRN> v3,ac_fixed<15,9,true,AC_TRN> v8,ac_fixed<18,10,true,AC_TRN> v4,ac_fixed<18,9,true,AC_TRN> v7,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<17,-5,true,AC_TRN> c5 = 0.0138523578643798828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<15,-6,true,AC_TRN> c6 = -0.0065402984619140625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<23,1,true,AC_TRN> c0 = -0.6363646984100341796875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = -0.4085009098052978515625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-2,true,AC_TRN> c8 = -0.117447376251220703125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,-1,true,AC_TRN> c4 = -0.2258586883544921875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-2,true,AC_TRN> c7 = 0.11992645263671875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<19,-4,true,AC_TRN> c2 = -0.0255870819091796875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true,AC_TRN> c1 = -0.4553165435791015625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
