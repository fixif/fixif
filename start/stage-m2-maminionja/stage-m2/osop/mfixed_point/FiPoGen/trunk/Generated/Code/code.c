#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
    /*      TP_Float_sop        */
    double r;
    ((((2.87109375 * x5*pow(2,-10) + -3.208251953125 * x6*pow(2,-10)) + 0.001327991485595703125 * x0*pow(2,-11)) + (0.0053119659423828125 * x3*pow(2,-11) + -0.3187103271484375 * x8*pow(2,-10))) + (((0.001327991485595703125 * x4*pow(2,-11) + 1.63458251953125 * x7*pow(2,-10)) + 0.00796794891357421875 * x2*pow(2,-11)) + 0.0053119659423828125 * x1*pow(2,-11)))
	return r*powf(2.f,-10); ;
}

int16_t SoP_int(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
	int32_t r0, r1, r2, r3, r4;

	//Computation of c5*x5 in register r23_0
	c = 23520;
	r0 = c*x5>> 9;

	//Computation of c6*x6 in register r23_1
	c = -26282;
	r1 = c*x6>> 9;

	//Computation of r0+r1 in register r2
	r0 = r0 % 131072;
	r1 = r1 % 131072;
	r2 = r0 + r1;

	//Computation of c0*x0 in register r11_0
	c = 22280;
	r0 = c*x0>> 21;

	//Computation of r2+r0 in register r1
	r1 = r2 + r0;

	//Computation of c3*x3 in register r13_0
	c = 22280;
	r0 = c*x3>> 19;

	//Computation of c8*x8 in register r20_2
	c = -20887;
	r2 = c*x8>> 12;

	//Computation of r0+r2 in register r3
	r3 = r0 + r2;

	//Computation of r1+r3 in register r0
	r0 = r1 + r3;

	//Computation of c4*x4 in register r11_1
	c = 22280;
	r1 = c*x4>> 21;

	//Computation of c7*x7 in register r22_2
	c = 26781;
	r2 = c*x7>> 10;

	//Computation of r1+r2 in register r3
	r2 = r2 % 262144;
	r3 = r1 + r2;

	//Computation of c2*x2 in register r14_1
	c = 16710;
	r1 = c*x2>> 18;

	//Computation of r3+r1 in register r2
	r2 = r3 + r1;

	//Computation of c1*x1 in register r13_1
	c = 22280;
	r1 = c*x1>> 19;

	//Computation of r2+r1 in register r3
	r3 = r2 + r1;

	//Computation of r0+r3 in register r1
	r1 = r0 + r3;

	//Computation of the final right shift
	r20_2= r20_1 >> 4 ;
	return r20_2;
}

/* double SoP_ac_fixed(float tab[int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8])
{
          TP_Float        
    
	float L5 = tab[5]*pow(2,-10);
	float L6 = tab[6]*pow(2,-10);
	float L0 = tab[0]*pow(2,-11);
	float L3 = tab[3]*pow(2,-11);
	float L8 = tab[8]*pow(2,-10);
	float L4 = tab[4]*pow(2,-11);
	float L7 = tab[7]*pow(2,-10);
	float L2 = tab[2]*pow(2,-11);
	float L1 = tab[1]*pow(2,-11);

    
          TP_Float        

	//Computation of c5*x5 in register r0
	ac_fixed<16,3,true,AC_TRN> c5 = 2.87109375;
	ac_fixed<16,6,true,AC_TRN> x5 = L5;
	ac_fixed<23,9,true,AC_TRN> r0 = c5*x5;


	//Computation of c6*x6 in register r1
	ac_fixed<16,3,true,AC_TRN> c6 = -3.208251953125;
	ac_fixed<16,6,true,AC_TRN> x6 = L6;
	ac_fixed<23,9,true,AC_TRN> r1 = c6*x6;


	//Computation of r0+r1 in register r2
	ac_fixed<20,5,true,AC_TRN> r2 = r0 + r1;

	//Computation of c0*x0 in register r3
	ac_fixed<16,-8,true,AC_TRN> c0 = 0.001327991485595703125;
	ac_fixed<16,5,true,AC_TRN> x0 = L0;
	ac_fixed<11,-3,true,AC_TRN> r3 = c0*x0;


	//Computation of r2+r3 in register r4
	ac_fixed<20,5,true,AC_TRN> r4 = r2 + r3;

	//Computation of c3*x3 in register r5
	ac_fixed<16,-6,true,AC_TRN> c3 = 0.0053119659423828125;
	ac_fixed<16,5,true,AC_TRN> x3 = L3;
	ac_fixed<13,-1,true,AC_TRN> r5 = c3*x3;


	//Computation of c8*x8 in register r6
	ac_fixed<16,0,true,AC_TRN> c8 = -0.3187103271484375;
	ac_fixed<16,6,true,AC_TRN> x8 = L8;
	ac_fixed<20,6,true,AC_TRN> r6 = c8*x8;


	//Computation of r5+r6 in register r7
	ac_fixed<20,5,true,AC_TRN> r7 = r5 + r6;

	//Computation of r4+r7 in register r8
	ac_fixed<20,5,true,AC_TRN> r8 = r4 + r7;

	//Computation of c4*x4 in register r9
	ac_fixed<16,-8,true,AC_TRN> c4 = 0.001327991485595703125;
	ac_fixed<16,5,true,AC_TRN> x4 = L4;
	ac_fixed<11,-3,true,AC_TRN> r9 = c4*x4;


	//Computation of c7*x7 in register r10
	ac_fixed<16,2,true,AC_TRN> c7 = 1.63458251953125;
	ac_fixed<16,6,true,AC_TRN> x7 = L7;
	ac_fixed<22,8,true,AC_TRN> r10 = c7*x7;


	//Computation of r9+r10 in register r11
	ac_fixed<20,5,true,AC_TRN> r11 = r9 + r10;

	//Computation of c2*x2 in register r12
	ac_fixed<16,-5,true,AC_TRN> c2 = 0.00796794891357421875;
	ac_fixed<16,5,true,AC_TRN> x2 = L2;
	ac_fixed<14,0,true,AC_TRN> r12 = c2*x2;


	//Computation of r11+r12 in register r13
	ac_fixed<20,5,true,AC_TRN> r13 = r11 + r12;

	//Computation of c1*x1 in register r14
	ac_fixed<16,-6,true,AC_TRN> c1 = 0.0053119659423828125;
	ac_fixed<16,5,true,AC_TRN> x1 = L1;
	ac_fixed<13,-1,true,AC_TRN> r14 = c1*x1;


	//Computation of r13+r14 in register r15
	ac_fixed<20,5,true,AC_TRN> r15 = r13 + r14;

	//Computation of r8+r15 in register r16
	ac_fixed<20,5,true,AC_TRN> r16 = r8 + r15;

	//Computation of the final right shift
	ac_fixed<16,6,true,AC_TRN> r17 = r16;
	double res = r17.to_double();
	return res;
}*/
