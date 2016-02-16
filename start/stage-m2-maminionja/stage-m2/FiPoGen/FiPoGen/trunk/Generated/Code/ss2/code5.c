#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -1.553825438022613525390625 * v5 + -0.9819056689739227294921875 * v6 + -0.7322327196598052978515625 * v0 + -0.56156308948993682861328125 * v3 + 0.751278400421142578125 * v8 + -0.9392834007740020751953125 * v4 + -0.423393428325653076171875 * v7 + -0.64628143608570098876953125 * v2 + -0.12047290802001953125 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -26068865*v5>> 20;
	// Computation of c6*v6 in r1
	r1 = -65894574*v6>> 22;
	// Computation of r0+r1 in r0
	r0 = r0 % 4194304;
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -24569653*v0>> 21;
	// Computation of r0+r1 in r0
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -37685861*v3>> 22;
	// Computation of c8*v8 in r2
	r2 = 3151090*v8>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 % 4194304;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -31517121*v4>> 21;
	// Computation of c7*v7 in r2
	r2 = -7103363*v7>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 % 4194304;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -43371213*v2>> 20;
	// Computation of r1+r2 in r1
	r2 = r2 % 4194304;
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -4042400*v1>> 21;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<20,11,true> SoP_ac_fixed(ac_fixed<20,11,true,AC_TRN> v5,ac_fixed<22,13,true,AC_TRN> v6,ac_fixed<21,12,true,AC_TRN> v0,ac_fixed<22,13,true,AC_TRN> v3,ac_fixed<17,9,true,AC_TRN> v8,ac_fixed<21,12,true,AC_TRN> v4,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<20,13,true,AC_TRN> v2,ac_fixed<21,12,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<26,2,true,AC_TRN> c5 = -1.553825438022613525390625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,1,true,AC_TRN> c6 = -0.9819056689739227294921875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<26,1,true,AC_TRN> c0 = -0.7322327196598052978515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<27,1,true,AC_TRN> c3 = -0.56156308948993682861328125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = 0.751278400421142578125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,1,true,AC_TRN> c4 = -0.9392834007740020751953125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true,AC_TRN> c7 = -0.423393428325653076171875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<27,1,true,AC_TRN> c2 = -0.64628143608570098876953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<23,-2,true,AC_TRN> c1 = -0.12047290802001953125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s.to_double();
}
