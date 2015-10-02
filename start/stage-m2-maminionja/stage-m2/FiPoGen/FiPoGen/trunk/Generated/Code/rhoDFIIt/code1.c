#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double SoP_float(double v0)
{
    /*      TP_Float_sop        */
    double r;
    r = 0.826725006103515625 * v0;
	return r; 
}

int16_t C_int(int16_t v0)
{
    // Registers declaration
	// Computation of c0*v0 in r0
	r0 = 433442*v0>> 19;
	// The result is returned 	return r0;
}

/* double SoP_ac_fixed(float tab[int16_t v0])
{
          TP_Float        
    
	float L0 = tab[0]*pow(2,-8);

    
          TP_Float        

	//Computation of c0*v0 in register r0
	ac_fixed<20,1,true,AC_TRN> c0 = 0.826725006103515625;
	ac_fixed<19,11,true,AC_TRN> v0 = L0;
	ac_fixed<19,11,true,AC_TRN> r0 = c0*v0;


}*/
