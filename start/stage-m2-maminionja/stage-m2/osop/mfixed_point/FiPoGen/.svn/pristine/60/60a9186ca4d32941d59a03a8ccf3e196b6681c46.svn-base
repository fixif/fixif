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

double SoP_float(float tab[$TP_Size])
{
    /*      TP_Float_sop        */
    double r;
    r = $TP_Float_sop ;
    return r;
}

double SoP_int(float tab[$TP_Size])
{
    /*      TP_Int_dec        */
    
$TP_Int_dec
    
    /*      TP_Int_sop        */
$TP_Int_sop
}

/* double SoP_ac_fixed(float tab[$TP_Size])
{
          TP_Float        
    
$TP_acf_dec
    
          TP_Float        
$TP_acf_sop
}*/
