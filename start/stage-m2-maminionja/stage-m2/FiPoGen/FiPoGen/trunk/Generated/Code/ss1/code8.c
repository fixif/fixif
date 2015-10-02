#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.172054290771484375 * v3 + 0.16170501708984375 * v4 + 0.8806438446044921875 * v1 + -0.11029052734375 * v8 + 1.6974277496337890625 * v2 + -0.05377197265625 * v5 + -1.11511516571044921875 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c3*v3 in r0
	r0 = 45103*v3>> 14;
	// Computation of c4*v4 in r1
	r1 = 42390*v4>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 923422*v1>> 20;
	// Computation of c8*v8 in r2
	r2 = -7228*v8>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 889941*v2>> 17;
	// Computation of c5*v5 in r2
	r2 = -3524*v5>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -1169283*v0>> 19;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<17,14,true> SoP_ac_fixed(ac_fixed<14,11,true,AC_TRN> v3,ac_fixed<15,11,true,AC_TRN> v4,ac_fixed<20,13,true,AC_TRN> v1,ac_fixed<17,9,true,AC_TRN> v8,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<19,13,true,AC_TRN> v0)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<17,-1,true,AC_TRN> c3 = 0.172054290771484375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<17,-1,true,AC_TRN> c4 = 0.16170501708984375;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true,AC_TRN> c1 = 0.8806438446044921875;
	sd = sd + c1*v1;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true,AC_TRN> c8 = -0.11029052734375;
	sd = sd + c8*v8;
	//Computation of c2*v2 in sd
	ac_fixed<21,2,true,AC_TRN> c2 = 1.6974277496337890625;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<13,-3,true,AC_TRN> c5 = -0.05377197265625;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<22,2,true,AC_TRN> c0 = -1.11511516571044921875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
