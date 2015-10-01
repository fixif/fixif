#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.64365386962890625 * v3 + 0.322093963623046875 * v4 + -0.06323719024658203125 * v1 + 0.00146484375 * v6 + -0.292980194091796875 * v2 + -0.1504364013671875 * v5 + 0.05274677276611328125 * v0 + 0.17205810546875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7)
{
    // Registers declaration
	int32_t r0, r1, r2, r3;
	// Computation of c3*v3 in r0
	r0 = -168730*v3>> 14;
	// Computation of c4*v4 in r1
	r1 = 84435*v4>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -66309*v1>> 20;
	// Computation of c6*v6 in r2
	r2 = 24*v6>> 7;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -153606*v2>> 17;
	// Computation of c5*v5 in r2
	r2 = -9859*v5>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = 55309*v0>> 19;
	// Computation of c8*v8 in r3
	r3 = 11276*v8>> 17;
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

ac_fixed<14,11,true> SoP_ac_fixed(ac_fixed<14,11,true,AC_TRN> v3,ac_fixed<15,11,true,AC_TRN> v4,ac_fixed<20,13,true,AC_TRN> v1,ac_fixed<7,7,true,AC_TRN> v6,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<19,13,true,AC_TRN> v0,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<14,11,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<19,1,true,AC_TRN> c3 = -0.64365386962890625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<18,0,true,AC_TRN> c4 = 0.322093963623046875;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<18,-2,true,AC_TRN> c1 = -0.06323719024658203125;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<6,-8,true,AC_TRN> c6 = 0.00146484375;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<19,0,true,AC_TRN> c2 = -0.292980194091796875;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<15,-1,true,AC_TRN> c5 = -0.1504364013671875;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<17,-3,true,AC_TRN> c0 = 0.05274677276611328125;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<15,-1,true,AC_TRN> c8 = 0.17205810546875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
