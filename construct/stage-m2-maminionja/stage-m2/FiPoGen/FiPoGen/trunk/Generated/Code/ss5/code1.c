#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.3270552158355712890625 * v0 + -0.07829749584197998046875 * v1 + 0.07365143299102783203125 * v2 + 0.6519358158111572265625 * v3 + 0.3743097782135009765625 * v4 + -0.25785219669342041015625 * v5 + 0.04083156585693359375 * v6 + 0.0938603878021240234375 * v7 + 0.6831510066986083984375 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 2743538*v0>> 20;
	// Computation of c1*v1 in r1
	r1 = -1313614*v1>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 617833*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 5468834*v3>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 1569969*v4>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -2163021*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 342520*v6>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 1574716*v7>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = 2865343*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<20,11,true> SoP_ac_fixed(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,0,true,AC_TRN> c0 = 0.3270552158355712890625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,-2,true,AC_TRN> c1 = -0.07829749584197998046875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true,AC_TRN> c2 = 0.07365143299102783203125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<24,1,true,AC_TRN> c3 = 0.6519358158111572265625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true,AC_TRN> c4 = 0.3743097782135009765625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = -0.25785219669342041015625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-3,true,AC_TRN> c6 = 0.04083156585693359375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.0938603878021240234375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = 0.6831510066986083984375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
