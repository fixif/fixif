#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.005859375 * v5 + -0.30859375 * v6 + 0.00244140625 * v4 + 0.1796875 * v7;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -12*v5>> 11;
	// Computation of c6*v6 in r1
	r1 = -79*v6>> 5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 5*v4>> 12;
	// Computation of c7*v7 in r2
	r2 = 23*v7>> 3;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<3,5,true> SoP_ac_fixed(ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,ac_fixed<12,9,true,AC_TRN> v4,ac_fixed<3,5,true,AC_TRN> v7)
{
	//Declaration of sums sd and s
	ac_fixed<7,5,true> sd = 0;
	ac_fixed<3,5,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<5,-6,true,AC_TRN> c5 = -0.005859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<8,0,true,AC_TRN> c6 = -0.30859375;
	sd = sd + c6*v6;
	//Computation of c4*v4 in sd
	ac_fixed<4,-7,true,AC_TRN> c4 = 0.00244140625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<6,-1,true,AC_TRN> c7 = 0.1796875;
	sd = sd + c7*v7;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
