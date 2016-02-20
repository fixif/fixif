#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.292980194091796875 * v3 + 0.1953983306884765625 * v4 + 0.2727434635162353515625 * v1 + -0.0008544921875 * v6 + -0.44718170166015625 * v2 + -0.025897979736328125 * v5 + -0.0488278865814208984375 * v0 + -1.697429656982421875 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7)
{
    // Registers declaration
	int32_t r0, r1, r2, r3;
	// Computation of c3*v3 in r0
	r0 = 307212*v3>> 14;
	// Computation of c4*v4 in r1
	r1 = 204890*v4>> 15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 1143969*v1>> 20;
	// Computation of c6*v6 in r2
	r2 = -56*v6>> 7;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -937808*v2>> 17;
	// Computation of c5*v5 in r2
	r2 = -6789*v5>> 11;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -204799*v0>> 19;
	// Computation of c8*v8 in r3
	r3 = -444971*v8>> 17;
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

ac_fixed<17,12,true> SoP_ac_fixed(ac_fixed<14,11,true,AC_TRN> v3,ac_fixed<15,11,true,AC_TRN> v4,ac_fixed<20,13,true,AC_TRN> v1,ac_fixed<7,7,true,AC_TRN> v6,ac_fixed<17,12,true,AC_TRN> v2,ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<19,13,true,AC_TRN> v0,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<20,0,true,AC_TRN> c3 = 0.292980194091796875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,-1,true,AC_TRN> c4 = 0.1953983306884765625;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true,AC_TRN> c1 = 0.2727434635162353515625;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<7,-9,true,AC_TRN> c6 = -0.0008544921875;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<21,0,true,AC_TRN> c2 = -0.44718170166015625;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<14,-4,true,AC_TRN> c5 = -0.025897979736328125;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<19,-3,true,AC_TRN> c0 = -0.0488278865814208984375;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<20,2,true,AC_TRN> c8 = -1.697429656982421875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
