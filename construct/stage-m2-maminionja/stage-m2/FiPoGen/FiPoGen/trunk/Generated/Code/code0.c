#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0,double v1,double v2,double v3)
{
    /*      TP_Float_sop        */
    double r;
    r = -0.003797054290771484375 * v3 + 17.0458984375 * v0 + 39.744140625 * v1 + 28.3779296875 * v2;
	return r; 
}

int16_t C_int(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -31852*v3;
	// Computation of c0*v0 in r1
	r1 = 17455*v0;
	// Computation of r0+r1 in r0
	r0 = r0 % 34359738368;
	r1 = r1 % 67108864;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 20349*v1;
	// Computation of r0+r1 in r0
	r1 = r1 % 2097152;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 29059*v2;
	// Computation of r0+r1 in r0
	r1 = r1 % 2097152;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

/* double SoP_ac_fixed(float tab[int16_t v0,int16_t v1,int16_t v2,int16_t v3])
{
          TP_Float        
    
	float L3 = tab[3]*pow(2,-10);
	float L0 = tab[0]*pow(2,-14);
	float L1 = tab[1]*pow(2,-10);
	float L2 = tab[2]*pow(2,-9);

    
          TP_Float        

	//Computation of c3*v3 in register r0
	ac_fixed<16,-7,true,AC_TRN> c3 = -0.003797054290771484375;
	ac_fixed<16,6,true,AC_TRN> v3 = L3;
	ac_fixed<32,-1,true,AC_TRN> r0 = c3*v3;


	//Computation of c0*v0 in register r1
	ac_fixed<16,6,true,AC_TRN> c0 = 17.0458984375;
	ac_fixed<16,2,true,AC_TRN> v0 = L0;
	ac_fixed<32,8,true,AC_TRN> r1 = c0*v0;


	//Computation of r0+r1 in register r2
	ac_fixed<32,1,true,AC_TRN> r2 = r0 + r1;

	//Computation of c1*v1 in register r3
	ac_fixed<16,7,true,AC_TRN> c1 = 39.744140625;
	ac_fixed<16,6,true,AC_TRN> v1 = L1;
	ac_fixed<32,13,true,AC_TRN> r3 = c1*v1;


	//Computation of r2+r3 in register r4
	ac_fixed<32,1,true,AC_TRN> r4 = r2 + r3;

	//Computation of c2*v2 in register r5
	ac_fixed<16,6,true,AC_TRN> c2 = 28.3779296875;
	ac_fixed<16,7,true,AC_TRN> v2 = L2;
	ac_fixed<32,13,true,AC_TRN> r5 = c2*v2;


	//Computation of r4+r5 in register r6
	ac_fixed<32,1,true,AC_TRN> r6 = r4 + r5;

	//Computation of the final right shift
	ac_fixed<16,2,true,AC_TRN> r7 = r6;
	double res = r7.to_double();
	return res;
}*/
