#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.9150390625 * v1 + 0.0262451171875 * v2 + -0.0786590576171875 * v0;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c1*v1 in r0
	r0 = -1874*v1>> 18;
	// Computation of c2*v2 in r1
	r1 = 215*v2>> 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -5155*v0>> 20;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 2;
}

/* double SoP_ac_fixed(float tab[int16_t v0,int16_t v1,int16_t v2])
{
          TP_Float        
    
	float L1 = tab[1]*pow(2,-9);
	float L2 = tab[2]*pow(2,0);
	float L0 = tab[0]*pow(2,-6);

    
          TP_Float        

	//Computation of c1*v1 in register r0
	ac_fixed<12,1,true,AC_TRN> c1 = -0.9150390625;
	ac_fixed<18,9,true,AC_TRN> v1 = L1;
	ac_fixed<11,9,true,AC_TRN> r0 = c1*v1;


	//Computation of c2*v2 in register r1
	ac_fixed<9,-4,true,AC_TRN> c2 = 0.0262451171875;
	ac_fixed<11,11,true,AC_TRN> v2 = L2;
	ac_fixed<7,5,true,AC_TRN> r1 = c2*v2;


	//Computation of r0+r1 in register r2
	ac_fixed<11,9,true,AC_TRN> r2 = r0 + r1;

	//Computation of c0*v0 in register r3
	ac_fixed<14,-2,true,AC_TRN> c0 = -0.0786590576171875;
	ac_fixed<20,14,true,AC_TRN> v0 = L0;
	ac_fixed<12,10,true,AC_TRN> r3 = c0*v0;


	//Computation of r2+r3 in register r4
	ac_fixed<12,10,true,AC_TRN> r4 = r2 + r3;

	//Computation of the final right shift
	ac_fixed<11,11,true,AC_TRN> r5 = r4;
	double res = r5.to_double();
	return res;
}*/
