#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 4.898258507251739501953125 * v5 + 2.4793329536914825439453125 * v6 + 3.5518662929534912109375 * v0 + 4.9808134734630584716796875 * v3 + 0.7820050716400146484375 * v8 + 2.48081505298614501953125 * v4 + 6.43144161999225616455078125 * v7 + 0.9982068836688995361328125 * v2 + 5.4780856668949127197265625 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = 82179141*v5>> 22;
	// Computation of c6*v6 in r1
	r1 = 83192609*v6>> 22;
	// Computation of r0+r1 in r0
	r0 = r0 % 1048576;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 119180856*v0>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 167128367*v3>> 21;
	// Computation of c8*v8 in r2
	r2 = 3279967*v8>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 % 1048576;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 83242340*v4>> 20;
	// Computation of c7*v7 in r2
	r2 = 431606741*v7>> 22;
	// Computation of r1+r2 in r1
	r1 = r1 % 1048576;
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = 33494265*v2>> 19;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = 367628106*v1>> 22;
	// Computation of r1+r2 in r1
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 4;
}

ac_fixed<22,13,true> SoP_ac_fixed(ac_fixed<22,11,true,AC_TRN> v5,ac_fixed<22,12,true,AC_TRN> v6,ac_fixed<19,12,true,AC_TRN> v0,ac_fixed<21,12,true,AC_TRN> v3,ac_fixed<15,9,true,AC_TRN> v8,ac_fixed<20,12,true,AC_TRN> v4,ac_fixed<22,13,true,AC_TRN> v7,ac_fixed<19,12,true,AC_TRN> v2,ac_fixed<22,13,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<26,13,true> sd = 0;
	ac_fixed<22,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<28,4,true,AC_TRN> c5 = 4.898258507251739501953125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,3,true,AC_TRN> c6 = 2.4793329536914825439453125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<28,3,true,AC_TRN> c0 = 3.5518662929534912109375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<29,4,true,AC_TRN> c3 = 4.9808134734630584716796875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = 0.7820050716400146484375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<28,3,true,AC_TRN> c4 = 2.48081505298614501953125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<30,4,true,AC_TRN> c7 = 6.43144161999225616455078125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,1,true,AC_TRN> c2 = 0.9982068836688995361328125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<30,4,true,AC_TRN> c1 = 5.4780856668949127197265625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
