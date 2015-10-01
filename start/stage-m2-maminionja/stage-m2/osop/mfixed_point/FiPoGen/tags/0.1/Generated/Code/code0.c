#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(int16_t x0,int16_t x1)
{
    /*      TP_Float_sop        */
    double r;
    (1 * x0*pow(2,-9) + 0.4678955078125 * x1*pow(2,-11))
	return r*powf(2.f,-9); ;
}

int16_t SoP_int(int16_t x0,int16_t x1)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
	int16 c, x;
	int32 r0, r1, r2, r3;

	//Computation of c0*x0 in register r0
	c = 16384;
	r0 = c*x0;

	//Computation of c1*x1 in register r1
	c = 30664;
	r1 = c*x1;

	//Computation of r0+r1 in register r2
	r2= ( r0 << 2 ) + ( r1 >> 2 );

	//Computation of the final right shift
	r3= r2 >> 16 ;
	return r3;
}

/* double SoP_ac_fixed(float tab[int16_t x0,int16_t x1])
{
          TP_Float        
    
	float L0 = tab[0]*pow(2,-9);
	float L1 = tab[1]*pow(2,-11);

    
          TP_Float        

	//Computation of c0*x0 in register r0
	ac_fixed<16,2,true,AC_TRN> c0 = 1;
	ac_fixed<16,7,true,AC_TRN> x0 = L0;
	ac_fixed<32,9,true,AC_TRN> r0 = c0*x0;


	//Computation of c1*x1 in register r1
	ac_fixed<16,0,true,AC_TRN> c1 = 0.4678955078125;
	ac_fixed<16,5,true,AC_TRN> x1 = L1;
	ac_fixed<32,5,true,AC_TRN> r1 = c1*x1;


	//Computation of r0+r1 in register r2
	ac_fixed<32,7,true,AC_TRN> r2 = r0 + r1;

	//Computation of the final right shift
	ac_fixed<16,7,true,AC_TRN> r3 = r2;
	double res = r3.to_double();
	return res;
}*/
