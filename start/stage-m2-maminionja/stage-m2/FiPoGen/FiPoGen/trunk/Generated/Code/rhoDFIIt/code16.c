#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0)
{
    /*      TP_Float_sop        */
    double r;
    r = 1 * v0;
	return r; 
}

int16_t C_int(int16_t v0)
{
    // Registers declaration
	// Computation of c0*v0 in r0
	r0 = 16384*v0;
	// The result is returned 	return r0;
}

/* double SoP_ac_fixed(float tab[int16_t v0])
{
          TP_Float        
    
	float L0 = tab[0]*pow(2,-2);

    
          TP_Float        

	//Computation of c0*v0 in register r0
	ac_fixed<16,2,true,AC_TRN> c0 = 1;
	ac_fixed<16,14,true,AC_TRN> v0 = L0;
	ac_fixed<32,16,true,AC_TRN> r0 = c0*v0;


}*/
