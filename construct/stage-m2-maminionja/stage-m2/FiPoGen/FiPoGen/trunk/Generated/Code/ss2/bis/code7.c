#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = -3.038344323635101318359375 * v5 + -1.2639661133289337158203125 * v6 + 0.43289005756378173828125 * v0 + -0.563853323459625244140625 * v3 + -0.9525587558746337890625 * v8 + -1.9315639436244964599609375 * v4 + -1.90865238010883331298828125 * v7 + -0.4331484138965606689453125 * v2 + -1.64873488247394561767578125 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -50974959*v5>> 22;
	// Computation of c6*v6 in r1
	r1 = -42411665*v6>> 22;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 14525380*v0>> 19;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -18919778*v3>> 21;
	// Computation of c8*v8 in r2
	r2 = -3995321*v8>> 15;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -64812531*v4>> 20;
	// Computation of c7*v7 in r2
	r2 = -128087493*v7>> 22;
	// Computation of r1+r2 in r1
	r2 = r2 % 1048576;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -14534049*v2>> 19;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -110644725*v1>> 22;
	// Computation of r1+r2 in r1
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
	ac_fixed<27,3,true,AC_TRN> c5 = -3.038344323635101318359375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,2,true,AC_TRN> c6 = -1.2639661133289337158203125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<25,0,true,AC_TRN> c0 = 0.43289005756378173828125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,1,true,AC_TRN> c3 = -0.563853323459625244140625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = -0.9525587558746337890625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<27,2,true,AC_TRN> c4 = -1.9315639436244964599609375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<28,2,true,AC_TRN> c7 = -1.90865238010883331298828125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<25,0,true,AC_TRN> c2 = -0.4331484138965606689453125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<28,2,true,AC_TRN> c1 = -1.64873488247394561767578125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
