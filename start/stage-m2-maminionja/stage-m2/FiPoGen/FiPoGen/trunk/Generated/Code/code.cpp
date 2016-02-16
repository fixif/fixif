#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

using namespace std;

float RandomFloat(int beta)
{
    float a = pow(2,beta-2)+1;
    float b = pow(2,beta-1)-1;
    float random = ((float) rand()) / (float) RAND_MAX;
    float diff = b - a;
    float r = random * diff;
    return (pow(-1,rand()%2))*(a + r);
}
/*
int RandomInt(int beta)
{
    int r = (pow(-1,rand()%2))*(rand()%((int)pow(2,beta-2)-2)+pow(2,beta-2)+1);
    return r;
    
}
 */

double SoP_float(float tab[2])
{
    /*      TP_Float_sop        */
    double r;
    r = (1 * tab[0]*pow(2,-9) + -1.953369140625 * tab[1]*pow(2,-11)) ;
    return r;
}

double SoP_int(float tab[2])
{
    /*      TP_Int_dec        */
    
	float L0 = tab[0];
	float L1 = tab[1];

    
    /*      TP_Int_sop        */
	int16 c, x;
	int32 r0, r1, r2, r3;

	//Computation of c0*x0 in register r0
	c = 16384;
	x = L0;
	r0 = c*x;

	//Computation of c1*x1 in register r1
	c = -32004;
	x = L1;
	r1 = c*x;

	//Computation of r0+r1 in register r2
	r2= ( r0 >> -1 ) + ( r1 >> 1 );

	//Computation of the final right shift
	r3= r2 >> 16 ;
	double res = ((long)r3)*pow(2,-8);
	return res;
}

/* double SoP_ac_fixed(float tab[2])
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
	ac_fixed<16,2,true,AC_TRN> c1 = -1.953369140625;
	ac_fixed<16,5,true,AC_TRN> x1 = L1;
	ac_fixed<32,7,true,AC_TRN> r1 = c1*x1;


	//Computation of r0+r1 in register r2
	ac_fixed<32,8,true,AC_TRN> r2 = r0 + r1;

	//Computation of the final right shift
	ac_fixed<16,8,true,AC_TRN> r3 = r2;
	double res = r3.to_double();
	return res;
}*/
