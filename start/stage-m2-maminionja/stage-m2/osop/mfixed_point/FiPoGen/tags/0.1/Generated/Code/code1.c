#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(int16_t x0,int16_t x1,int16_t x2,int16_t x3)
{
    /*      TP_Float_sop        */
    double r;
    ((-1.35546875 * x1*pow(2,-11) + 1 * x3*pow(2,-10)) + (-0.12236785888671875 * x0*pow(2,-9) + -0.00029146671295166015625 * x2*pow(2,-9)))
	return r*powf(2.f,-9); ;
}

int16_t SoP_int(int16_t x0,int16_t x1,int16_t x2,int16_t x3)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
	int16 c, x;
	int32 r0, r1, r2, r3, r4;

	//Computation of c1*x1 in register r0
	c = -22208;
	r0 = c*x1;

	//Computation of c3*x3 in register r1
	c = 16384;
	r1 = c*x3;

	//Computation of r0+r1 in register r2
	r2= r0 + ( r1 << 1 );

	//Computation of c0*x0 in register r0
	c = -32078;
	r0 = c*x0;

	//Computation of c2*x2 in register r1
	c = -19560;
	r1 = c*x2;

	//Computation of r0+r1 in register r3
	r3= r0 + ( r1 >> 8 );

	//Computation of r2+r3 in register r0
	r0= r2 + ( r3 >> 2 );

	//Computation of the final right shift
	r1= r0 >> 16 ;
	return r1;
}

/* double SoP_ac_fixed(float tab[int16_t x0,int16_t x1,int16_t x2,int16_t x3])
{
          TP_Float        
    
	float L1 = tab[1]*pow(2,-11);
	float L3 = tab[3]*pow(2,-10);
	float L0 = tab[0]*pow(2,-9);
	float L2 = tab[2]*pow(2,-9);

    
          TP_Float        

	//Computation of c1*x1 in register r0
	ac_fixed<16,2,true,AC_TRN> c1 = -1.35546875;
	ac_fixed<16,5,true,AC_TRN> x1 = L1;
	ac_fixed<32,7,true,AC_TRN> r0 = c1*x1;


	//Computation of c3*x3 in register r1
	ac_fixed<16,2,true,AC_TRN> c3 = 1;
	ac_fixed<16,6,true,AC_TRN> x3 = L3;
	ac_fixed<32,8,true,AC_TRN> r1 = c3*x3;


	//Computation of r0+r1 in register r2
	ac_fixed<32,7,true,AC_TRN> r2 = r0 + r1;

	//Computation of c0*x0 in register r3
	ac_fixed<16,-2,true,AC_TRN> c0 = -0.12236785888671875;
	ac_fixed<16,7,true,AC_TRN> x0 = L0;
	ac_fixed<32,5,true,AC_TRN> r3 = c0*x0;


	//Computation of c2*x2 in register r4
	ac_fixed<16,-10,true,AC_TRN> c2 = -0.00029146671295166015625;
	ac_fixed<16,7,true,AC_TRN> x2 = L2;
	ac_fixed<32,-3,true,AC_TRN> r4 = c2*x2;


	//Computation of r3+r4 in register r5
	ac_fixed<32,5,true,AC_TRN> r5 = r3 + r4;

	//Computation of r2+r5 in register r6
	ac_fixed<32,7,true,AC_TRN> r6 = r2 + r5;

	//Computation of the final right shift
	ac_fixed<16,7,true,AC_TRN> r7 = r6;
	double res = r7.to_double();
	return res;
}*/
