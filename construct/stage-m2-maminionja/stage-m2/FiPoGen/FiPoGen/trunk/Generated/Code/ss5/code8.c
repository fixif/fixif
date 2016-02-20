#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 4.6474456787109375 * v0 + -7.513275146484375 * v1 + -0.47011566162109375 * v2 + -6.68109130859375 * v3 + 3.53643798828125 * v4 + 8.1562652587890625 * v5 + -4.7039031982421875 * v6 + 2.925533294677734375 * v7 + -0.11029052734375 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 609150*v0>> 20;
	// Computation of c1*v1 in r1
	r1 = -1969560*v1>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -61619*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -875704*v3>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 231764*v4>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 1069058*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -616550*v6>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 766911*v7>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -7228*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<17,14,true> SoP_ac_fixed(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,4,true,AC_TRN> c0 = 4.6474456787109375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,4,true,AC_TRN> c1 = -7.513275146484375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<17,0,true,AC_TRN> c2 = -0.47011566162109375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,4,true,AC_TRN> c3 = -6.68109130859375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,3,true,AC_TRN> c4 = 3.53643798828125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,5,true,AC_TRN> c5 = 8.1562652587890625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,4,true,AC_TRN> c6 = -4.7039031982421875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,3,true,AC_TRN> c7 = 2.925533294677734375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true,AC_TRN> c8 = -0.11029052734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
