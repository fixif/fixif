#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.0547313690185546875 * v8 + -0.08007049560546875 * v3 + 0.3912506103515625 * v5 + -0.20754241943359375 * v6 + -0.574432373046875 * v2 + -0.3852081298828125 * v0 + -0.20436859130859375 * v7 + 0.312347412109375 * v4 + -0.4520721435546875 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 28695*v8;
	// Computation of c3*v3 in r1
	r1 = -20990*v3;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 25641*v5;
	// Computation of r0+r1 in r0
	r0 = r0 % 17179869184;
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -27203*v6;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -18823*v2;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -25245*v0;
	// Computation of r0+r1 in r0
	r1 = r1 % 2147483648;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -26787*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 20470*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -29627*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,9,true> SoP_ac_fixed(ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,11,true,AC_TRN> v5,ac_fixed<16,11,true,AC_TRN> v6,ac_fixed<16,9,true,AC_TRN> v2,ac_fixed<16,10,true,AC_TRN> v0,ac_fixed<16,10,true,AC_TRN> v7,ac_fixed<16,9,true,AC_TRN> v4,ac_fixed<16,9,true,AC_TRN> v1)
{
	//Declaration of sums sd and s
	ac_fixed<32,9,true> sd = 0;
	ac_fixed<16,9,true> s = 0;

	//Computation of c8*v8 in register r0
	ac_fixed<16,-3,true,AC_TRN> c8 = 0.0547313690185546875;
	ac_fixed<32,6,true,AC_TRN> r0 = c8*v8;

	//Computation of c3*v3 in register r1
	ac_fixed<16,-2,true,AC_TRN> c3 = -0.08007049560546875;
	ac_fixed<32,7,true,AC_TRN> r1 = c3*v3;


	//Computation of r0+r1 in register r2
	ac_fixed<32,7,true,AC_TRN> r2 = r0 + r1;
	//Computation of c5*v5 in register r3
	ac_fixed<16,0,true,AC_TRN> c5 = 0.3912506103515625;
	ac_fixed<32,11,true,AC_TRN> r3 = c5*v5;


	//Computation of r2+r3 in register r4
	ac_fixed<32,9,true,AC_TRN> r4 = r2 + r3;
	//Computation of c6*v6 in register r5
	ac_fixed<16,-1,true,AC_TRN> c6 = -0.20754241943359375;
	ac_fixed<32,10,true,AC_TRN> r5 = c6*v6;


	//Computation of r4+r5 in register r6
	ac_fixed<32,9,true,AC_TRN> r6 = r4 + r5;
	//Computation of c2*v2 in register r7
	ac_fixed<16,1,true,AC_TRN> c2 = -0.574432373046875;
	ac_fixed<32,10,true,AC_TRN> r7 = c2*v2;


	//Computation of r6+r7 in register r8
	ac_fixed<32,9,true,AC_TRN> r8 = r6 + r7;
	//Computation of c0*v0 in register r9
	ac_fixed<16,0,true,AC_TRN> c0 = -0.3852081298828125;
	ac_fixed<32,10,true,AC_TRN> r9 = c0*v0;


	//Computation of r8+r9 in register r10
	ac_fixed<32,9,true,AC_TRN> r10 = r8 + r9;
	//Computation of c7*v7 in register r11
	ac_fixed<16,-1,true,AC_TRN> c7 = -0.20436859130859375;
	ac_fixed<32,9,true,AC_TRN> r11 = c7*v7;


	//Computation of r10+r11 in register r12
	ac_fixed<32,9,true,AC_TRN> r12 = r10 + r11;
	//Computation of c4*v4 in register r13
	ac_fixed<16,0,true,AC_TRN> c4 = 0.312347412109375;
	ac_fixed<32,9,true,AC_TRN> r13 = c4*v4;


	//Computation of r12+r13 in register r14
	ac_fixed<32,9,true,AC_TRN> r14 = r12 + r13;
	//Computation of c1*v1 in register r15
	ac_fixed<16,0,true,AC_TRN> c1 = -0.4520721435546875;
	ac_fixed<32,9,true,AC_TRN> r15 = c1*v1;


	//Computation of r14+r15 in register r16
	ac_fixed<32,9,true,AC_TRN> r16 = r14 + r15;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
