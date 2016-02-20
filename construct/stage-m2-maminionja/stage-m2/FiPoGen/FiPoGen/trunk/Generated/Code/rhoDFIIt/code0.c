#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1)
{
    /*      TP_Float_sop        */
    double r;
    r = 5.528835296630859375 * v0 + -0.11029052734375 * v1;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c0*v0 in r0
	r0 = 1449351*v0>> 19;
	// Computation of c1*v1 in r1
	r1 = -7228*v1>> 18;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 1;
}

/* double SoP_ac_fixed(float tab[int16_t v0,int16_t v1])
{
          TP_Float        
    
	float L0 = tab[0]*pow(2,-8);
	float L1 = tab[1]*pow(2,-9);

    
          TP_Float        

	//Computation of c0*v0 in register r0
	ac_fixed<22,4,true,AC_TRN> c0 = 5.528835296630859375;
	ac_fixed<19,11,true,AC_TRN> v0 = L0;
	ac_fixed<21,14,true,AC_TRN> r0 = c0*v0;


	//Computation of c1*v1 in register r1
	ac_fixed<14,-2,true,AC_TRN> c1 = -0.11029052734375;
	ac_fixed<18,9,true,AC_TRN> v1 = L1;
	ac_fixed<13,6,true,AC_TRN> r1 = c1*v1;


	//Computation of r0+r1 in register r2
	ac_fixed<21,14,true,AC_TRN> r2 = r0 + r1;

	//Computation of the final right shift
	ac_fixed<20,14,true,AC_TRN> r3 = r2;
	double res = r3.to_double();
	return res;
}*/
