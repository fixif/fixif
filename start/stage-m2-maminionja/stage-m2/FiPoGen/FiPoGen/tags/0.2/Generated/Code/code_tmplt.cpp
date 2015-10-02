#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include "ac_fixed.h"

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

double SoP_ac_fixed(float tab[$TP_Size])
{
    /*      TP_Float        */
    
$TP_acf_dec
    
    /*      TP_Float        */
$TP_acf_sop
}

/*
int main()
{
    float tab[9] = {27865.97266,
        24230.66602,
        32611.83594,
        24653.33984,
        -27101.1875,
        23106.37109,
        -31828.625,
        -29872.94922,
        -18646.44922};
    cout<<setprecision(30)<<SoP_float(tab)<<endl;
    cout<<SoP_int(tab)<<endl;
    cout<<SoP_ac_fixed(tab)<<endl;
    return 0;
}*/