#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.0639171600341796875 * v0 + 0.1471168994903564453125 * v1 + -0.1946094036102294921875 * v2 + -0.0696659088134765625 * v3 + -0.173511981964111328125 * v4 + 0.25 * v5 + -0.697756290435791015625 * v6 + 0.1709110736846923828125 * v7 + -0.53635883331298828125 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 134044*v0>> 18;
	// Computation of c1*v1 in r1
	r1 = 617053*v1>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -816251*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -146100*v3>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -363881*v4>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 1048576*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -1463301*v6>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 716853*v7>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -1124826*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<18,10,true> SoP_ac_fixed(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true,AC_TRN> c0 = 0.0639171600341796875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,-1,true,AC_TRN> c1 = 0.1471168994903564453125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-1,true,AC_TRN> c2 = -0.1946094036102294921875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,-2,true,AC_TRN> c3 = -0.0696659088134765625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,-1,true,AC_TRN> c4 = -0.173511981964111328125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,0,true,AC_TRN> c5 = 0.25;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,1,true,AC_TRN> c6 = -0.697756290435791015625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,-1,true,AC_TRN> c7 = 0.1709110736846923828125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,1,true,AC_TRN> c8 = -0.53635883331298828125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
