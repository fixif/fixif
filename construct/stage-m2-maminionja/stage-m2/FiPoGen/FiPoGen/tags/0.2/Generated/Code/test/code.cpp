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

double SoP_float(float tab[9])
{
    /*      TP_Float_sop        */
    double r;
    r = (((((0.015244686904602972737921007251316 * tab[2]*pow(2,-11) + 0.010163124603068649648429655485415 * tab[3]*pow(2,-11)) + ((0.0025407811507671619784265448771521 * tab[0]*pow(2,-11) + 0.0025407811507671619784265448771521 * tab[4]*pow(2,-11)) + 0.010163124603068649648429655485415 * tab[1]*pow(2,-11))) + -0.25124988761024086292295010025555 * tab[8]*pow(2,-11)) + 1.345585149455075013591454080597 * tab[7]*pow(2,-11)) + (2.6440237193486328948210939415731 * tab[5]*pow(2,-11) + -2.779011479605740575493655342143 * tab[6]*pow(2,-11))) ;
    return r;
}

double SoP_int(float tab[9])
{
    /*      TP_Int_dec        */
    
	float L2 = tab[2];
	float L3 = tab[3];
	float L0 = tab[0];
	float L4 = tab[4];
	float L1 = tab[1];
	float L8 = tab[8];
	float L7 = tab[7];
	float L5 = tab[5];
	float L6 = tab[6];

    
    /*      TP_Int_sop        */
	int16 c, x;
	int32 r0, r1, r2, r3;

	//Computation of c2*x2 in register r0
	c = 31970;
	x = L2;
	r0 = c*x;

	//Computation of c3*x3 in register r1
	c = 21314;
	x = L3;
	r1 = c*x;

	//Computation of r0+r1 in register r2
	r2= ( r0 >> 1 ) + ( r1 >> 1 );

	//Computation of c0*x0 in register r0
	c = 21314;
	x = L0;
	r0 = c*x;

	//Computation of c4*x4 in register r1
	c = 21314;
	x = L4;
	r1 = c*x;

	//Computation of r0+r1 in register r3
	r3= ( r0 >> 1 ) + ( r1 >> 1 );

	//Computation of c1*x1 in register r0
	c = 21314;
	x = L1;
	r0 = c*x;

	//Computation of r3+r0 in register r1
	r1= ( r3 >> 2 ) + ( r0 >> 1 );

	//Computation of r2+r1 in register r0
	r0= ( r2 >> 1 ) + ( r1 >> 1 );

	//Computation of c8*x8 in register r1
	c = -16466;
	x = L8;
	r1 = c*x;

	//Computation of r0+r1 in register r2
	r2= ( r0 >> 4 ) + ( r1 >> 1 );

	//Computation of c7*x7 in register r0
	c = 22046;
	x = L7;
	r0 = c*x;

	//Computation of r2+r0 in register r1
	r1= ( r2 >> 2 ) + ( r0 >> 1 );

	//Computation of c5*x5 in register r0
	c = 21660;
	x = L5;
	r0 = c*x;

	//Computation of c6*x6 in register r2
	c = -22766;
	x = L6;
	r2 = c*x;

	//Computation of r0+r2 in register r3
	r3= ( r0 >> 1 ) + ( r2 >> 1 );

	//Computation of r1+r3 in register r0
	r0= ( r1 >> 1 ) + r3 ;
	double res = ((long)r0)*pow(2,-23);
	return res;
}

double SoP_ac_fixed(float tab[9])
{
    /*      TP_Float        */
    
	float L2 = tab[2];
	float L3 = tab[3];
	float L0 = tab[0];
	float L4 = tab[4];
	float L1 = tab[1];
	float L8 = tab[8];
	float L7 = tab[7];
	float L5 = tab[5];
	float L6 = tab[6];

    
    /*      TP_Float        */

	//Computation of c2*x2 in register r0
	ac_fixed<16,-5,true> c2 = 0.01524448394775390625;
	ac_fixed<16,5,true> x2 = L2*pow(2,-11);
	ac_fixed<32,0,true> r0 = c2*x2;


	//Computation of c3*x3 in register r1
	ac_fixed<16,-5,true> c3 = 0.01016330718994140625;
	ac_fixed<16,5,true> x3 = L3*pow(2,-11);
	ac_fixed<32,0,true> r1 = c3*x3;


	//Computation of r0+r1 in register r2
	ac_fixed<32,1,true> r2 = r0 + r1;

	//Computation of c0*x0 in register r3
	ac_fixed<16,-7,true> c0 = 0.0025408267974853515625;
	ac_fixed<16,5,true> x0 = L0*pow(2,-11);
	ac_fixed<32,-2,true> r3 = c0*x0;


	//Computation of c4*x4 in register r4
	ac_fixed<16,-7,true> c4 = 0.0025408267974853515625;
	ac_fixed<16,5,true> x4 = L4*pow(2,-11);
	ac_fixed<32,-2,true> r4 = c4*x4;


	//Computation of r3+r4 in register r5
	ac_fixed<32,-1,true> r5 = r3 + r4;

	//Computation of c1*x1 in register r6
	ac_fixed<16,-5,true> c1 = 0.01016330718994140625;
	ac_fixed<16,5,true> x1 = L1*pow(2,-11);
	ac_fixed<32,0,true> r6 = c1*x1;


	//Computation of r5+r6 in register r7
	ac_fixed<32,1,true> r7 = r5 + r6;

	//Computation of r2+r7 in register r8
	ac_fixed<32,2,true> r8 = r2 + r7;

	//Computation of c8*x8 in register r9
	ac_fixed<16,0,true> c8 = -0.251251220703125;
	ac_fixed<16,5,true> x8 = L8*pow(2,-11);
	ac_fixed<32,5,true> r9 = c8*x8;


	//Computation of r8+r9 in register r10
	ac_fixed<32,6,true> r10 = r8 + r9;

	//Computation of c7*x7 in register r11
	ac_fixed<16,2,true> c7 = 1.3455810546875;
	ac_fixed<16,5,true> x7 = L7*pow(2,-11);
	ac_fixed<32,7,true> r11 = c7*x7;


	//Computation of r10+r11 in register r12
	ac_fixed<32,8,true> r12 = r10 + r11;

	//Computation of c5*x5 in register r13
	ac_fixed<16,3,true> c5 = 2.64404296875;
	ac_fixed<16,5,true> x5 = L5*pow(2,-11);
	ac_fixed<32,8,true> r13 = c5*x5;


	//Computation of c6*x6 in register r14
	ac_fixed<16,3,true> c6 = -2.779052734375;
	ac_fixed<16,5,true> x6 = L6*pow(2,-11);
	ac_fixed<32,8,true> r14 = c6*x6;


	//Computation of r13+r14 in register r15
	ac_fixed<32,9,true> r15 = r13 + r14;

	//Computation of r12+r15 in register r16
	ac_fixed<32,9,true> r16 = r12 + r15;
	double res = r16.to_double();
	return res;
}


int main()
{
    ac_fixed<16,-5,true> c1 = 0.01524448394775390625;
	ac_fixed<16,5,true> x1 = 17592.0*pow(2,-11);
	ac_fixed<32,0,true> r1 = c1*x1;

	ac_fixed<16,-5,true> c2 = 0.015244686904602972737921007251316;
	ac_fixed<16,5,true> x2 = 17592.0*pow(2,-11);
	ac_fixed<32,0,true> r2 = c2*x2;
    cout<<setprecision(30)<<r1<<endl;
    cout<<r2<<endl;
    return 0;
}