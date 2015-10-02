#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8,double v9,double v10,double v11,double v12,double v13,double v14,double v15,double v16)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.03118419647216796875 * v7 + 0.0363025665283203125 * v8 + 0.006961822509765625 * v15 + -0.005564212799072265625 * v16 + 0.18310546875 * v4 + 0.2921142578125 * v2 + 0.2704315185546875 * v5 + -0.2965545654296875 * v6 + -0.94012451171875 * v0 + -0.693145751953125 * v3 + -0.089813232421875 * v12 + 0.07305145263671875 * v14 + 1.04327392578125 * v1 + -0.17235565185546875 * v13 + -1.95404052734375 * v10 + 1.046142578125 * v11 + 2.0692138671875 * v9;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8,int16_t v9,int16_t v10,int16_t v11,int16_t v12,int16_t v13,int16_t v14,int16_t v15,int16_t v16)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = -32699*v7;
	// Computation of c8*v8 in r1
	r1 = 19033*v8;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c15*v15 in r1
	r1 = 29200*v15;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c16*v16 in r1
	r1 = -23338*v16;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 24000*v4;
	// Computation of r0+r1 in r0
	r0 = r0 % 17179869184;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 19144*v2;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 17723*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -19435*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -30806*v0;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -22713*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c12*v12 in r1
	r1 = -23544*v12;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c14*v14 in r1
	r1 = 19150*v14;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 17093*v1;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c13*v13 in r1
	r1 = -22591*v13;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c10*v10 in r1
	r1 = -32015*v10;
	// Computation of r0+r1 in r0
	r0 = r0 % 8589934592;
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c11*v11 in r1
	r1 = 17140*v11;
	// Computation of r0+r1 in r0
	r1 = r1 % 1073741824;
	r0 = r0 + r1;
	// Computation of c9*v9 in r1
	r1 = 16951*v9;
	// Computation of r0+r1 in r0
	r1 = r1 % 536870912;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

ac_fixed<16,13,true> SoP_ac_fixed(ac_fixed<16,10,true,AC_TRN> v7,ac_fixed<16,10,true,AC_TRN> v8,ac_fixed<16,13,true,AC_TRN> v15,ac_fixed<16,13,true,AC_TRN> v16,ac_fixed<16,10,true,AC_TRN> v4,ac_fixed<16,10,true,AC_TRN> v2,ac_fixed<16,10,true,AC_TRN> v5,ac_fixed<16,10,true,AC_TRN> v6,ac_fixed<16,10,true,AC_TRN> v0,ac_fixed<16,10,true,AC_TRN> v3,ac_fixed<16,13,true,AC_TRN> v12,ac_fixed<16,13,true,AC_TRN> v14,ac_fixed<16,10,true,AC_TRN> v1,ac_fixed<16,13,true,AC_TRN> v13,ac_fixed<16,13,true,AC_TRN> v10,ac_fixed<16,13,true,AC_TRN> v11,ac_fixed<16,13,true,AC_TRN> v9)
{
	//Declaration of sums sd and s
	ac_fixed<32,13,true> sd = 0;
	ac_fixed<16,13,true> s = 0;

	//Computation of c7*v7 in register r0
	ac_fixed<16,-4,true,AC_TRN> c7 = -0.03118419647216796875;
	ac_fixed<32,6,true,AC_TRN> r0 = c7*v7;

	//Computation of c8*v8 in register r1
	ac_fixed<16,-3,true,AC_TRN> c8 = 0.0363025665283203125;
	ac_fixed<32,7,true,AC_TRN> r1 = c8*v8;


	//Computation of r0+r1 in register r2
	ac_fixed<32,7,true,AC_TRN> r2 = r0 + r1;
	//Computation of c15*v15 in register r3
	ac_fixed<16,-6,true,AC_TRN> c15 = 0.006961822509765625;
	ac_fixed<32,7,true,AC_TRN> r3 = c15*v15;


	//Computation of r2+r3 in register r4
	ac_fixed<32,7,true,AC_TRN> r4 = r2 + r3;
	//Computation of c16*v16 in register r5
	ac_fixed<16,-6,true,AC_TRN> c16 = -0.005564212799072265625;
	ac_fixed<32,7,true,AC_TRN> r5 = c16*v16;


	//Computation of r4+r5 in register r6
	ac_fixed<32,7,true,AC_TRN> r6 = r4 + r5;
	//Computation of c4*v4 in register r7
	ac_fixed<16,-1,true,AC_TRN> c4 = 0.18310546875;
	ac_fixed<32,9,true,AC_TRN> r7 = c4*v4;


	//Computation of r6+r7 in register r8
	ac_fixed<32,9,true,AC_TRN> r8 = r6 + r7;
	//Computation of c2*v2 in register r9
	ac_fixed<16,0,true,AC_TRN> c2 = 0.2921142578125;
	ac_fixed<32,10,true,AC_TRN> r9 = c2*v2;


	//Computation of r8+r9 in register r10
	ac_fixed<32,10,true,AC_TRN> r10 = r8 + r9;
	//Computation of c5*v5 in register r11
	ac_fixed<16,0,true,AC_TRN> c5 = 0.2704315185546875;
	ac_fixed<32,10,true,AC_TRN> r11 = c5*v5;


	//Computation of r10+r11 in register r12
	ac_fixed<32,10,true,AC_TRN> r12 = r10 + r11;
	//Computation of c6*v6 in register r13
	ac_fixed<16,0,true,AC_TRN> c6 = -0.2965545654296875;
	ac_fixed<32,10,true,AC_TRN> r13 = c6*v6;


	//Computation of r12+r13 in register r14
	ac_fixed<32,10,true,AC_TRN> r14 = r12 + r13;
	//Computation of c0*v0 in register r15
	ac_fixed<16,1,true,AC_TRN> c0 = -0.94012451171875;
	ac_fixed<32,11,true,AC_TRN> r15 = c0*v0;


	//Computation of r14+r15 in register r16
	ac_fixed<32,11,true,AC_TRN> r16 = r14 + r15;
	//Computation of c3*v3 in register r17
	ac_fixed<16,1,true,AC_TRN> c3 = -0.693145751953125;
	ac_fixed<32,11,true,AC_TRN> r17 = c3*v3;


	//Computation of r16+r17 in register r18
	ac_fixed<32,11,true,AC_TRN> r18 = r16 + r17;
	//Computation of c12*v12 in register r19
	ac_fixed<16,-2,true,AC_TRN> c12 = -0.089813232421875;
	ac_fixed<32,11,true,AC_TRN> r19 = c12*v12;


	//Computation of r18+r19 in register r20
	ac_fixed<32,11,true,AC_TRN> r20 = r18 + r19;
	//Computation of c14*v14 in register r21
	ac_fixed<16,-2,true,AC_TRN> c14 = 0.07305145263671875;
	ac_fixed<32,11,true,AC_TRN> r21 = c14*v14;


	//Computation of r20+r21 in register r22
	ac_fixed<32,11,true,AC_TRN> r22 = r20 + r21;
	//Computation of c1*v1 in register r23
	ac_fixed<16,2,true,AC_TRN> c1 = 1.04327392578125;
	ac_fixed<32,12,true,AC_TRN> r23 = c1*v1;


	//Computation of r22+r23 in register r24
	ac_fixed<32,12,true,AC_TRN> r24 = r22 + r23;
	//Computation of c13*v13 in register r25
	ac_fixed<16,-1,true,AC_TRN> c13 = -0.17235565185546875;
	ac_fixed<32,12,true,AC_TRN> r25 = c13*v13;


	//Computation of r24+r25 in register r26
	ac_fixed<32,12,true,AC_TRN> r26 = r24 + r25;
	//Computation of c10*v10 in register r27
	ac_fixed<16,2,true,AC_TRN> c10 = -1.95404052734375;
	ac_fixed<32,15,true,AC_TRN> r27 = c10*v10;


	//Computation of r26+r27 in register r28
	ac_fixed<32,13,true,AC_TRN> r28 = r26 + r27;
	//Computation of c11*v11 in register r29
	ac_fixed<16,2,true,AC_TRN> c11 = 1.046142578125;
	ac_fixed<32,15,true,AC_TRN> r29 = c11*v11;


	//Computation of r28+r29 in register r30
	ac_fixed<32,13,true,AC_TRN> r30 = r28 + r29;
	//Computation of c9*v9 in register r31
	ac_fixed<16,3,true,AC_TRN> c9 = 2.0692138671875;
	ac_fixed<32,16,true,AC_TRN> r31 = c9*v9;


	//Computation of r30+r31 in register r32
	ac_fixed<32,13,true,AC_TRN> r32 = r30 + r31;

	//Computation of the final right shift
	s = s + sd;
	return s;
}
