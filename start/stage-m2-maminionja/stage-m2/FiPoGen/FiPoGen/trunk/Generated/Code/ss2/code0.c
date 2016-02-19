#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 3.93980872631072998046875 * v5 + 0.92621038854122161865234375 * v6 + 1.4366941750049591064453125 * v0 + -0.60798163712024688720703125 * v3 + -2.113919734954833984375 * v8 + 1.8654798567295074462890625 * v4 + 1.31116139888763427734375 * v7 + 0.3603222668170928955078125 * v2 + -0.440654933452606201171875 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = 66099022*v5>> 20;
	// Computation of c6*v6 in r1
	r1 = 62156927*v6>> 22;
	// Computation of r0+r1 in r0
	r0 = r0 % 4194304;
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 48207457*v0>> 21;
	// Computation of r0+r1 in r0
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -40800957*v3>> 22;
	// Computation of c8*v8 in r2
	r2 = -8866422*v8>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 62595117*v4>> 21;
	// Computation of c7*v7 in r2
	r2 = 21997638*v7>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 % 4194304;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = 24180818*v2>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -14785926*v1>> 21;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<21,12,true> SoP_ac_fixed(ac_fixed<20,11,true,AC_TRN> v5,ac_fixed<22,13,true,AC_TRN> v6,ac_fixed<21,12,true,AC_TRN> v0,ac_fixed<22,13,true,AC_TRN> v3,ac_fixed<17,9,true,AC_TRN> v8,ac_fixed<21,12,true,AC_TRN> v4,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<20,13,true,AC_TRN> v2,ac_fixed<21,12,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<27,3,true,AC_TRN> c5 = 3.93980872631072998046875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,1,true,AC_TRN> c6 = 0.92621038854122161865234375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<27,2,true,AC_TRN> c0 = 1.4366941750049591064453125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<27,1,true,AC_TRN> c3 = -0.60798163712024688720703125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<25,3,true,AC_TRN> c8 = -2.113919734954833984375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<27,2,true,AC_TRN> c4 = 1.8654798567295074462890625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<26,2,true,AC_TRN> c7 = 1.31116139888763427734375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,0,true,AC_TRN> c2 = 0.3603222668170928955078125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<25,0,true,AC_TRN> c1 = -0.440654933452606201171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s.to_double();
}
