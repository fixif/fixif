#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.757243335247039794921875 * v5 + -2.4723255932331085205078125 * v6 + -4.29140007495880126953125 * v0 + -2.7778887450695037841796875 * v3 + 0.5067918300628662109375 * v8 + -0.6560055315494537353515625 * v4 + -2.3198604881763458251953125 * v7 + -4.9252796471118927001953125 * v2 + -5.4284845292568206787109375 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -12704435*v5>> 22;
	// Computation of c6*v6 in r1
	r1 = -82957481*v6>> 22;
	// Computation of r0+r1 in r0
	r1 = r1 % 1048576;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -143995492*v0>> 19;
	// Computation of r0+r1 in r0
	r1 = r1 % 1048576;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -93210479*v3>> 21;
	// Computation of c8*v8 in r2
	r2 = 2125639*v8>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 % 1048576;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -22011893*v4>> 20;
	// Computation of c7*v7 in r2
	r2 = -155683202*v7>> 22;
	// Computation of r1+r2 in r1
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -165264961*v2>> 19;
	// Computation of r1+r2 in r1
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -364299430*v1>> 22;
	// Computation of r1+r2 in r1
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<21,12,true> SoP_ac_fixed(ac_fixed<22,11,true,AC_TRN> v5,ac_fixed<22,12,true,AC_TRN> v6,ac_fixed<19,12,true,AC_TRN> v0,ac_fixed<21,12,true,AC_TRN> v3,ac_fixed<15,9,true,AC_TRN> v8,ac_fixed<20,12,true,AC_TRN> v4,ac_fixed<22,13,true,AC_TRN> v7,ac_fixed<19,12,true,AC_TRN> v2,ac_fixed<22,13,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<25,1,true,AC_TRN> c5 = -0.757243335247039794921875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,3,true,AC_TRN> c6 = -2.4723255932331085205078125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<29,4,true,AC_TRN> c0 = -4.29140007495880126953125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<28,3,true,AC_TRN> c3 = -2.7778887450695037841796875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = 0.5067918300628662109375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,1,true,AC_TRN> c4 = -0.6560055315494537353515625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<29,3,true,AC_TRN> c7 = -2.3198604881763458251953125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<29,4,true,AC_TRN> c2 = -4.9252796471118927001953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<30,4,true,AC_TRN> c1 = -5.4284845292568206787109375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
