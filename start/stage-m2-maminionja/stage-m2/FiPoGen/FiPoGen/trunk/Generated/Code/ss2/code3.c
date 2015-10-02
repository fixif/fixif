#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 7.6138370037078857421875 * v5 + 3.9915024340152740478515625 * v6 + 4.605542838573455810546875 * v0 + 1.8029229640960693359375 * v3 + -4.2833006381988525390625 * v8 + 4.21262657642364501953125 * v4 + 3.0655066967010498046875 * v7 + 1.09973002970218658447265625 * v2 + 3.45780098438262939453125 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = 127738988*v5>> 20;
	// Computation of c6*v6 in r1
	r1 = 267865194*v6>> 22;
	// Computation of r0+r1 in r0
	r0 = r0 % 4194304;
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 154536374*v0>> 21;
	// Computation of r0+r1 in r0
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 120992112*v3>> 22;
	// Computation of c8*v8 in r2
	r2 = -17965465*v8>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 % 4194304;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 141352292*v4>> 21;
	// Computation of c7*v7 in r2
	r2 = 51430668*v7>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 % 4194304;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = 73801633*v2>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = 116024548*v1>> 21;
	// Computation of r1+r2 in r1
	r2 = r2 % 4194304;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<22,13,true> SoP_ac_fixed(ac_fixed<20,11,true,AC_TRN> v5,ac_fixed<22,13,true,AC_TRN> v6,ac_fixed<21,12,true,AC_TRN> v0,ac_fixed<22,13,true,AC_TRN> v3,ac_fixed<17,9,true,AC_TRN> v8,ac_fixed<21,12,true,AC_TRN> v4,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<20,13,true,AC_TRN> v2,ac_fixed<21,12,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<26,13,true> sd = 0;
	ac_fixed<22,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<28,4,true,AC_TRN> c5 = 7.6138370037078857421875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<29,3,true,AC_TRN> c6 = 3.9915024340152740478515625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<29,4,true,AC_TRN> c0 = 4.605542838573455810546875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<28,2,true,AC_TRN> c3 = 1.8029229640960693359375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<26,4,true,AC_TRN> c8 = -4.2833006381988525390625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<29,4,true,AC_TRN> c4 = 4.21262657642364501953125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<27,3,true,AC_TRN> c7 = 3.0655066967010498046875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<28,2,true,AC_TRN> c2 = 1.09973002970218658447265625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<28,3,true,AC_TRN> c1 = 3.45780098438262939453125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s.to_double();
}
