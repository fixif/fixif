#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -7.1567547321319580078125 * v5 + -2.853803455829620361328125 * v6 + -4.093217372894287109375 * v0 + -1.105220794677734375 * v3 + 3.17626094818115234375 * v8 + -3.8396055698394775390625 * v4 + -2.7725617885589599609375 * v7 + -1.403257548809051513671875 * v2 + -2.2713954448699951171875 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -30017605*v5>> 20;
	// Computation of c6*v6 in r1
	r1 = -47878877*v6>> 22;
	// Computation of r0+r1 in r0
	r0 = r0 % 4194304;
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -34336396*v0>> 21;
	// Computation of r0+r1 in r0
	r1 = r1 % 4194304;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -18542528*v3>> 22;
	// Computation of c8*v8 in r2
	r2 = 3330551*v8>> 17;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -32208946*v4>> 21;
	// Computation of c7*v7 in r2
	r2 = -11628967*v7>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 % 4194304;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -23542755*v2>> 20;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -19053846*v1>> 21;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<20,13,true> SoP_ac_fixed(ac_fixed<20,11,true,AC_TRN> v5,ac_fixed<22,13,true,AC_TRN> v6,ac_fixed<21,12,true,AC_TRN> v0,ac_fixed<22,13,true,AC_TRN> v3,ac_fixed<17,9,true,AC_TRN> v8,ac_fixed<21,12,true,AC_TRN> v4,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<20,13,true,AC_TRN> v2,ac_fixed<21,12,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<24,13,true> sd = 0;
	ac_fixed<20,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<26,4,true,AC_TRN> c5 = -7.1567547321319580078125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,3,true,AC_TRN> c6 = -2.853803455829620361328125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<27,4,true,AC_TRN> c0 = -4.093217372894287109375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,2,true,AC_TRN> c3 = -1.105220794677734375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,3,true,AC_TRN> c8 = 3.17626094818115234375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,3,true,AC_TRN> c4 = -3.8396055698394775390625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,3,true,AC_TRN> c7 = -2.7725617885589599609375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,2,true,AC_TRN> c2 = -1.403257548809051513671875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<26,3,true,AC_TRN> c1 = -2.2713954448699951171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s.to_double();
}
