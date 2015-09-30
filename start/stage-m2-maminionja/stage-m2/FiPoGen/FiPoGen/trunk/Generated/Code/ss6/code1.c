#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.0311291217803955078125 * v0 + 0.26888096332550048828125 * v1 + -0.05739796161651611328125 * v2 + 0.8811562061309814453125 * v3 + 0.193104267120361328125 * v4 + -0.2615299224853515625 * v5 + -0.15713024139404296875 * v6 + 0.27550411224365234375 * v7 + 0.4386656284332275390625 * v8;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 130565*v0>> 18;
	// Computation of c1*v1 in r1
	r1 = 2255537*v1>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -481489*v2>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 3695837*v3>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 809938*v4>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -2193872*v5>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -659052*v6>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 2311096*v7>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = 1839897*v8>> 17;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<19,10,true> SoP_ac_fixed(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,-4,true,AC_TRN> c0 = 0.0311291217803955078125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,0,true,AC_TRN> c1 = 0.26888096332550048828125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,-3,true,AC_TRN> c2 = -0.05739796161651611328125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,1,true,AC_TRN> c3 = 0.8811562061309814453125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.193104267120361328125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = -0.2615299224853515625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,-1,true,AC_TRN> c6 = -0.15713024139404296875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,0,true,AC_TRN> c7 = 0.27550411224365234375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = 0.4386656284332275390625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
