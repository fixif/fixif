#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.491579532623291015625 * v0 + 0.31836032867431640625 * v1 + 0.010989665985107421875 * v2 + 0.032764434814453125 * v3 + -0.45677089691162109375 * v4 + -0.550405979156494140625 * v5 + 0.3126926422119140625 * v6 + -0.1892540454864501953125 * v7 + -0.28411388397216796875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = -1030917*v0>> 20;
	// Computation of c1*v1 in r1
	r1 = 1335300*v1>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 23047*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 68712*v3>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -478959*v4>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -1154285*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 655764*v6>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -793789*v7>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -297915*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<17,10,true> SoP_ac_fixed(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = -0.491579532623291015625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true,AC_TRN> c1 = 0.31836032867431640625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<16,-5,true,AC_TRN> c2 = 0.010989665985107421875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<18,-3,true,AC_TRN> c3 = 0.032764434814453125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,0,true,AC_TRN> c4 = -0.45677089691162109375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,1,true,AC_TRN> c5 = -0.550405979156494140625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,0,true,AC_TRN> c6 = 0.3126926422119140625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,-1,true,AC_TRN> c7 = -0.1892540454864501953125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<20,0,true,AC_TRN> c8 = -0.28411388397216796875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
