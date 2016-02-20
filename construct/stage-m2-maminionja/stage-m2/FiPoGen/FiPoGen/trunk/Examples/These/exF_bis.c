#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


double double_DFI(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8,double v9,double v10,double v11,double v12,double v13,double v14,double v15,double v16)
{
    double r;
    r = -0.03118419647216796875 * v7 + 0.0363025665283203125 * v8 + 0.006961822509765625 * v15 + -0.005564212799072265625 * v16 + 0.18310546875 * v4 + 0.2921142578125 * v2 + 0.2704315185546875 * v5 + -0.2965545654296875 * v6 + -0.94012451171875 * v0 + -0.693145751953125 * v3 + -0.089813232421875 * v12 + 0.07305145263671875 * v14 + 1.04327392578125 * v1 + -0.17235565185546875 * v13 + -1.95404052734375 * v10 + 1.046142578125 * v11 + 2.0692138671875 * v9;
	return r; 
}



int16_t C_int_DFI(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8,int16_t v9,int16_t v10,int16_t v11,int16_t v12,int16_t v13,int16_t v14,int16_t v15,int16_t v16)
{
	int32_t r0, r1;
	r0 = -32699*v7;
	r1 = 19033*v8;
	r0 = r0 >>1;
	r0 = r0 + r1;
	r1 = 29200*v15;
	r0 = r0 + r1;
	r1 = -23338*v16;
	r0 = r0 + r1;
	r1 = 24000*v4;
	r0 = r0 >>2;
	r0 = r0 + r1;
	r1 = 19144*v2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 17723*v5;
	r0 = r0 + r1;
	r1 = -19435*v6;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -30806*v0;
	r0 = r0 + r1;
	r1 = -22713*v3;
	r0 = r0 + r1;
	r1 = -23544*v12;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 19150*v14;
	r1 = r1 >> 1; // a voir
	r0 = r0 + r1;
	r1 = 17093*v1;
	r0 = r0 + r1;
	r1 = -22591*v13;
	r0 = r0 + r1;
	r1 = -32015*v10;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 17140*v11;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 16951*v9;
	r1 = r1 << 3;
	r0 = r0 + r1;
	return r0 >> 16;
}


int16_t C_int_ss1_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = 26871*v7;
	// Computation of c6*v6 in r1
	r1 = -25771*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -19897*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 16687*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 4;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 32485*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -20653*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -27909*v8;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -20999*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 31274*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 4;
	r1 = r1 <<1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}


int16_t C_int_ss1_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c8*v8 in r0
	r0 = -30684*v8;
	// Computation of c2*v2 in r1
	r1 = 18959*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -20999*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 20382*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 19212*v7;
	// Computation of c6*v6 in r2
	r2 = -19504*v6;
	// Computation of r1+r2 in r1
	r1 = r1 >> 5;
	r1 = r1 + r2;
	// Computation of c5*v5 in r2
	r2 = 21475*v5;
	// Computation of r1+r2 in r1
	r1 = r1 >> 5;
	r1 = r1 + r2;
	// Computation of c4*v4 in r2
	r2 = 22525*v4;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = 22902*v1;
	// Computation of r1+r2 in r1
	r1 = r1 >> 3;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}



int16_t C_int_ss1_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = -25797*v7;
	// Computation of c6*v6 in r1
	r1 = 25199*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -25218*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -26524*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = 23339*v8;
	// Computation of r0+r1 in r0
	r0 = r0 >> 4;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -31106*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 20653*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 22195*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -18959*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}



int16_t C_int_ss1_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = 21463*v7;
	// Computation of c6*v6 in r1
	r1 = -28926*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 27601*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 6;
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -22026*v8;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -19819*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 28458*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -31106*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -20382*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -32485*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}



int16_t C_int_ss1_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = 19455*v7;
	// Computation of c6*v6 in r1
	r1 = -18809*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 25218*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -19897*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -31013*v8;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 22525*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >>1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 18736*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >>3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 16792*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -28458*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}



int16_t C_int_ss1_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = 24348*v7;
	// Computation of c6*v6 in r1
	r1 = -25837*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >>5;
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -22586*v8;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -21475*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -26524*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -25661*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -16687*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -18736*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -19819*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}


int16_t C_int_ss1_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -18105*v8;
	// Computation of c2*v2 in r1
	r1 = -25199*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -19504*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -25771*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -20263*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -26280*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 28926*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 25837*v5;
	// Computation of r0+r1 in r0
	r1 = r1 <<1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -18809*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}



int16_t C_int_ss1_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 24057*v8;
	// Computation of c2*v2 in r1
	r1 = 25797*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 19212*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 26871*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -21463*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 19455*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -24348*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 23766*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -20263*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss1_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = -24057*v7;
	// Computation of c6*v6 in r1
	r1 = 18105*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 31013*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 7;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -22586*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -22026*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c8*v8 in r1
	r1 = -30806*v8;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 23339*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 30684*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 27909*v0;
	// Computation of r0+r1 in r0
	r1 = r1 <<1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}


int16_t C_int_ss2_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -18808*v8;
	// Computation of c0*v0 in r1
	r1 = -16578*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 23378*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -30639*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 <<3;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 25172*v2;
	// Computation of r0+r1 in r0
	r1 = r1 <<3;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -26479*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 29291*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 25084*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -27708*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 25625*v8;
	// Computation of c7*v7 in r1
	r1 = 26343*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r1 = r1 <<4;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 22438*v1;
	// Computation of r0+r1 in r0
	r1 = r1 <<4;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 20401*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 20311*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 20063*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 20323*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 29097*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 32709*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -29470*v8;
	// Computation of c0*v0 in r1
	r1 = -22237*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -16983*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 <<4;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -17147*v1;
	// Computation of r0+r1 in r0
	r1 = r1 <<4;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -16432*v6;
	// Computation of r0+r1 in r0
	r1 = r1 <<3;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -24868*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -29919*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -19761*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -18080*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 16607*v8;
	// Computation of c1*v1 in r1
	r1 = -22235*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -19004*v7;
	// Computation of r0+r1 in r0
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -20174*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -17578*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -20253*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -22756*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -21496*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -24813*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 24706*v8;
	// Computation of c7*v7 in r1
	r1 = -24151*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 6;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -31389*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 6;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -26400*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -18548*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -28256*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -24830*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -22245*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -17380*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 22379*v8;
	// Computation of c7*v7 in r1
	r1 = 17249*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >>4;
	r1 = r1 <<6;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 27509*v1;
	// Computation of r0+r1 in r0
	r1 = r1 <<6;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 17769*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 20599*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 18202*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 31972*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 27383*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 31716*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -17004*v8;
	// Computation of c5*v5 in r1
	r1 = 27826*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 20498*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 22345*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 19208*v7;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 21715*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 17340*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 20044*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 24854*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -31213*v8;
	// Computation of c2*v2 in r1
	r1 = -28387*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 28370*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -31271*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -27013*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -20709*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -24890*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -31647*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -18476*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss2_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30806*v8;
	// Computation of c7*v7 in r1
	r1 = 22654*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 6;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 21348*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 6;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 23177*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 19566*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 5;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 18772*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 4;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 27139*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 18808*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 26035*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 3;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -19640*v8;
	// Computation of c5*v5 in r1
	r1 = -28221*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 29196*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 25837*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -17654*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 20338*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -21759*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -24095*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 30635*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -28034*v8;
	// Computation of c3*v3 in r1
	r1 = 17342*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 21979*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 26015*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 25325*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 16422*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -27551*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -17380*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -31510*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30531*v8;
	// Computation of c7*v7 in r1
	r1 = 19797*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 29342*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 18692*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -23651*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 28951*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -17205*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -20541*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -29328*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 21520*v7;
	// Computation of c8*v8 in r1
	r1 = -23123*v8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 18614*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 18116*v0;
	// Computation of c6*v6 in r2
	r2 = 22622*v6;
	// Computation of r1+r2 in r1
	r1 = r1 >> 6; //doute
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 19552*v3;
	// Computation of c5*v5 in r2
	r2 = 24714*v5;
	// Computation of r1+r2 in r1
	r1 = r1 << 1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -17892*v1;
	// Computation of r1+r2 in r1
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -20277*v2;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 28695*v8;
	// Computation of c3*v3 in r1
	r1 = -20990*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 25641*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -27203*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -18823*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -25245*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -26787*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 20470*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -29627*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -31245*v8;
	// Computation of c4*v4 in r1
	r1 = 22451*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -21056*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -24238*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 28765*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 27340*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r0 = r0 >> 1;
	// Computation of c0*v0 in r1
	r1 = -18261*v0;
	r1 = r1 >> 2; //gros doute
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 29949*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 27877*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c2*v2 in r0
	r0 = 21435*v2;
	// Computation of c7*v7 in r1
	r1 = 20320*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 31384*v1;
	// Computation of c4*v4 in r2
	r2 = -18350*v4;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c8*v8 in r2
	r2 = -29905*v8;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c3*v3 in r2
	r2 = -18917*v3;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -26338*v0;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 17016*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 30937*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -23152*v5;
	// Computation of c7*v7 in r1
	r1 = 30463*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 17375*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -17031*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 31355*v3;
	// Computation of c4*v4 in r2
	r2 = 17271*v4;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of c8*v8 in r2
	r2 = -28241*v8;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 18876*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 21387*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss3_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 27891*v7;
	// Computation of c0*v0 in r1
	r1 = 17313*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 23632*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -25755*v6;
	// Computation of c5*v5 in r2
	r2 = 26431*v5;
	// Computation of r1+r2 in r1
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -20813*v2;
	// Computation of c4*v4 in r2
	r2 = 25254*v4;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c8*v8 in r2
	r2 = -30806*v8;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c3*v3 in r2
	r2 = 22303*v3;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -28752*v8;
	// Computation of c6*v6 in r1
	r1 = -31230*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -22226*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -22856*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -18162*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -21874*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -25730*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -17005*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -22249*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 27112*v8;
	// Computation of c7*v7 in r1
	r1 = 16937*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 20024*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 18988*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -19965*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -28144*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 19691*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -19787*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 32356*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -24993*v8;
	// Computation of c7*v7 in r1
	r1 = -25018*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -18959*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 21818*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -31794*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 20793*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 26553*v0;
	r1 = r1 >> 1; 
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -21698*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -26689*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 30430*v7;
	// Computation of c0*v0 in r1
	r1 = 16384*v0;
	// Computation of r0+r1 in r0
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 28556*v6;
	// Computation of c8*v8 in r2
	r2 = -16521*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c4*v4 in r2
	r2 = 30746*v4;
	// Computation of r1+r2 in r1
	r2 = r2 >> 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 31695*v5;
	// Computation of c3*v3 in r2
	r2 = 19085*v3;
	// Computation of r1+r2 in r1
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = 32685*v2;
	// Computation of r1+r2 in r1
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = 23135*v1;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c6*v6 in r0
	r0 = -19521*v6;
	// Computation of c2*v2 in r1
	r1 = -31423*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -18857*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -31094*v4;
	// Computation of c8*v8 in r2
	r2 = 16570*v8;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -22202*v5;
	// Computation of c7*v7 in r2
	r2 = -18465*v7;
	// Computation of r1+r2 in r1
	r1 = r1 <<1;
	r2 = r2 << 3;
	r1 = r1 + r2;
	// Computation of c3*v3 in r2
	r2 = -20666*v3;
	// Computation of r1+r2 in r1
	r2 = r2 << 3;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -19686*v0;
	// Computation of r1+r2 in r1
	r2 = r2 << 3;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 21970*v8;
	// Computation of c7*v7 in r1
	r1 = 20206*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 20717*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 32232*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 22230*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 19553*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 25657*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 17810*v6;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 29892*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 31733*v7;
	// Computation of c8*v8 in r1
	r1 = -30202*v8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 24297*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -31857*v2;
	// Computation of c6*v6 in r2
	r2 = -17131*v6;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 3;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -23296*v3;
	// Computation of c4*v4 in r2
	r2 = -24759*v4;
	// Computation of r1+r2 in r1
	r1 = r1 << 1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -31196*v0;
	// Computation of r1+r2 in r1
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = -27839*v1;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 28644*v8;
	// Computation of c5*v5 in r1
	r1 = -26962*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 16393*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 28104*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 27474*v4;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -19193*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -18141*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -18951*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -16443*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss4_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30806*v8;
	// Computation of c7*v7 in r1
	r1 = 21898*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 23183*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 19532*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 27988*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 19333*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 23045*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 22094*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 18510*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -22787*v8;
	// Computation of c5*v5 in r1
	r1 = -19593*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -17780*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = -23950*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -18227*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -26978*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -28676*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -16809*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -17503*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c6*v6 in r0
	r0 = -29344*v6;
	// Computation of c7*v7 in r1
	r1 = -21602*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -28744*v1;
	// Computation of c8*v8 in r2
	r2 = 22075*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1; //(7,-24)
	r1 = -24472*v3;
	r2 = -30858*v5;
	r1 = r1 + r2; //(7,-24)
	r0 = r0 >> 1; //(8,-23)
	r1 = r1 >> 1; //(8,-23)
	r0 = r0 + r1;
	r1 = 20382*v4;
	r2 = -19162*v2;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = -20329*v0;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c7*v7 in r0
	r0 = -16999*v7;
	// Computation of c8*v8 in r1
	r1 = -25276*v8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 30718*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -19056*v6;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -19856*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 31736*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -16842*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -28298*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 19253*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -28913*v8;
	// Computation of c0*v0 in r1
	r1 = 20084*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 18653*v7;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 22646*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 24504*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 31678*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 27278*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 27862*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 31590*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = -30309*v7;
	// Computation of c3*v3 in r1
	r1 = -17691*v3;
	// Computation of r0+r1 in r0
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -32756*v4;
	// Computation of c8*v8 in r2
	r2 = 23359*v8;
	// Computation of r1+r2 in r1
	r1 = r1 >> 5;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -28597*v5;
	// Computation of c2*v2 in r2
	r2 = -19366*v2;
	// Computation of r1+r2 in r1
	r1 = r1 << 1;
	r2 = r2 << 3;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -27183*v6;
	// Computation of c1*v1 in r2
	r2 = -17958*v1;
	// Computation of r1+r2 in r1
	r2 = r2 << 3;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -16676*v0;
	// Computation of r1+r2 in r1
	r2 = r2 << 3;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 19439*v8;
	// Computation of c5*v5 in r1
	r1 = 19249*v5;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 19052*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 23736*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 20664*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 29941*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 24643*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 30571*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 28115*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c8*v8 in r0
	r0 = -19511*v8;
	// Computation of c5*v5 in r1
	r1 = -30500*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -22849*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -26322*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 27745*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 23573*v6;
	// Computation of c7*v7 in r2
	r2 = 29452*v7;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of c4*v4 in r2
	r2 = -21432*v4;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -32768*v0;
	// Computation of r1+r2 in r1
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = -16636*v7;
	// Computation of c1*v1 in r1
	r1 = -23187*v1;
	// Computation of r0+r1 in r0
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 22759*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 23510*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -19325*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 28011*v6;
	// Computation of c8*v8 in r2
	r2 = 17085*v8;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = 19530*v0;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -26478*v2;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss5_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30806*v8;
	// Computation of c1*v1 in r1
	r1 = 21578*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 19560*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 21814*v7;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 28601*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 22938*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 22649*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 18317*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 19334*v4;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30607*v8;
	// Computation of c7*v7 in r1
	r1 = -25537*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -27148*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -18821*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -19579*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -20201*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -24888*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -30454*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -21641*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 29871*v7;
	// Computation of c4*v4 in r1
	r1 = 24876*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 23383*v3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 30422*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -31370*v6;
	// Computation of c8*v8 in r2
	r2 = 27018*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c5*v5 in r2
	r2 = -22373*v5;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = -19042*v0;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -19871*v2;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c3*v3 in r0
	r0 = 32018*v3;
	// Computation of c6*v6 in r1
	r1 = -17357*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 32191*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -31286*v2;
	// Computation of c8*v8 in r2
	r2 = -31667*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c7*v7 in r2
	r2 = -22863*v7;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = -25643*v5;
	// Computation of c4*v4 in r2
	r2 = -17493*v4;
	// Computation of r1+r2 in r1
	r2 = r2 << 1;
	r1 = r1 + r2;
	// Computation of c1*v1 in r2
	r2 = 23118*v1;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	//r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c6*v6 in r0
	r0 = 25671*v6;
	// Computation of c8*v8 in r1
	r1 = -19180*v8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -23970*v4;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 31100*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 31947*v5;
	// Computation of c7*v7 in r2
	r2 = 18094*v7;
	// Computation of r1+r2 in r1
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of c3*v3 in r2
	r2 = 23774*v3;
	// Computation of r1+r2 in r1
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = 16973*v2;
	// Computation of r1+r2 in r1
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of c0*v0 in r2
	r2 = 21117*v0;
	// Computation of r1+r2 in r1
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c5*v5 in r0
	r0 = -16858*v5;
	// Computation of c3*v3 in r1
	r1 = -26172*v3;
	// Computation of r0+r1 in r0
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -22467*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -24342*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -25003*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -22666*v4;
	// Computation of c8*v8 in r2
	r2 = 19866*v8;
	// Computation of r1+r2 in r1
	r1 = r1 + r2;
	// Computation of c6*v6 in r2
	r2 = -32343*v6;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r1 = r1 + r2;
	// Computation of c7*v7 in r2
	r2 = -24051*v7;
	// Computation of r1+r2 in r1
	r1 = r1 >> 1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 21939*v8;
	// Computation of c1*v1 in r1
	r1 = 20693*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 32099*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 23227*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 32071*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 27247*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 21480*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 27870*v7;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 27686*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1, r2;
	// Computation of c7*v7 in r0
	r0 = 31438*v7;
	// Computation of c8*v8 in r1
	r1 = -30788*v8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = -27431*v6;
	// Computation of c5*v5 in r2
	r2 = 29050*v5;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of c2*v2 in r2
	r2 = -26830*v2;
	// Computation of r1+r2 in r1
	r1 = r1 >> 2;
	r1 = r1 + r2;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -20852*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = -29604*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -26772*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -29840*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = 23856*v8;
	// Computation of c0*v0 in r1
	r1 = -19267*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c7*v7 in r1
	r1 = 29707*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 20848*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 26339*v5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = -26925*v3;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -19436*v2; // doute
	r1 = r1 >> 1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 24674*v4;
	// Computation of r0+r1 in r0
	//r0 = r0 % 8589934592;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -32768*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_ss6_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c8*v8 in r0
	r0 = -30806*v8;
	// Computation of c7*v7 in r1
	r1 = 21900*v7;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c3*v3 in r1
	r1 = 23226*v3;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 21909*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 19514*v0;
	// Computation of r0+r1 in r0
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c5*v5 in r1
	r1 = 27919*v5;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c4*v4 in r1
	r1 = 19214*v4;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 23709*v2;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c6*v6 in r1
	r1 = 18402*v6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_t1(int16_t v0,int16_t v1)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c1*v1 in r0
	r0 = -30806*v1;
	// Computation of c0*v0 in r1
	r1 = 21746*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_t2(int16_t v0)
{
	int32_t r0;
	r0 = 24168*v0; 
	//r0 << 1;
	return r0 >> 14; //?
}

int16_t C_int_rho_t3(int16_t v0)
{
	int32_t r0;
	r0 = 23528*v0;
	//r0 << 1;
	return r0 >> 15;//?
}

int16_t C_int_rho_t4(int16_t v0)
{
	int32_t r0;
	r0 = 28953*v0;
	//r0 << 2;
	return r0 >> 15;//?
}

int16_t C_int_rho_t5(int16_t v0)
{
	int32_t r0;
	r0 = 23578*v0; 
	//r0 << 1;
	return r0 >> 14;//?
}

int16_t C_int_rho_t6(int16_t v0)
{
	int32_t r0;
	r0 = 25005*v0; 
	//r0 << 1;
	return r0 >> 14;//?
}

int16_t C_int_rho_t7(int16_t v0)
{
	int32_t r0;
	r0 = 24945*v0; 
	//r0 << 1;
	return r0 >> 14;//?
}

int16_t C_int_rho_t8(int16_t v0)
{
	int32_t r0;
	r0 = 17186*v0; 
	//r0 << 2;
	return r0 >> 14;//?
}

int16_t C_int_rho_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -28352*v3;
	// Computation of c2*v2 in r1
	r1 = 32728*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -25868*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = 20713*v3;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 11;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 19309*v2;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -17815*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = 32565*v3;
	// Computation of c2*v2 in r1
	r1 = 24663*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 3;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -28488*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -18280*v3;
	// Computation of c2*v2 in r1
	r1 = 26448*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 4;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 16872*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = 29455*v3;
	// Computation of c2*v2 in r1
	r1 = 26603*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >>2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 16467*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -21392*v3;
	// Computation of c0*v0 in r1
	r1 = 22575*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >>4;
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 28136*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -31568*v3;
	// Computation of c2*v2 in r1
	r1 = 25292*v2;
	// Computation of r0+r1 in r0
	r0 = r0 >> 2;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = 17585*v0;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 16384*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_x8(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c2*v2 in r0
	r0 = -25474*v2;
	// Computation of c0*v0 in r1
	r1 = 17329*v0;
	// Computation of r0+r1 in r0
	r0 = r0 >>2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 25767*v1;
	// Computation of r0+r1 in r0
	r0 = r0 >>1;
	r1 = r1 <<1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_rho_y(int16_t v0)
{	return v0;	}




int16_t C_int_LGS_t2(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -22528*v0;
	r1 = 16384*v1;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16; //(10,-5)
}

int16_t C_int_LGS_t10(int16_t v0)
{
	int32_t r0;
	r0 = 32528*v0;
	return r0 >> 15; //(10,-5)
}

int16_t C_int_LGS_t19(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -22731*v0;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(10,-5)
}

int16_t C_int_LGS_t27(int16_t v0)
{
	int32_t r0;
	r0 = 29272*v0;
	return r0 >> 15; // (10,-5)
}

int16_t C_int_LGS_t36(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -27152*v0;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(10,-5)
}

int16_t C_int_LGS_t44(int16_t v0)
{
	int32_t r0;
	r0 = 28411*v0;
	return r0 >> 15; //(10,-5)
}

int16_t C_int_LGS_t53(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -31715*v0;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t61(int16_t v0)
{
	int32_t r0;
	r0 = 27237*v0;
	return r0 >> 15; // (10,-5)
}

int16_t C_int_LGS_t70(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = -21261*v0;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t78(int16_t v0)
{
	int32_t r0;
	r0 = 24274*v0; 	
	return r0 >> 14; //(10,-5)
}

int16_t C_int_LGS_t87(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = -18572*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t95(int16_t v0)
{
    int32_t r0;
	r0 = 16789*v0; 	
	return r0 >> 14; //(10,-5)
}

int16_t C_int_LGS_t104(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = -23644*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t112(int16_t v0)
{
	int32_t r0;
	r0 = 25019*v0;
	return r0 >> 15; //(8,-7)
}

int16_t C_int_LGS_t119(int16_t v0,int16_t v1)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c1*v1 in r0
	r0 = 24228*v1;
	// Computation of c0*v0 in r1
	r1 = 32768*v0;
	// Computation of r0+r1 in r0
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_LGS_t126(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 27515*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
} 

int16_t C_int_LGS_t133(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 17673*v1;
	r1 = 32768*v0;
	r0 = r0 << 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(9,-6)
}

int16_t C_int_LGS_t140(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 27499*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t147(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 24256*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t154(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 22565*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t161(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 22528*v1;
	r1 = 32768*v0;
	r0 = r0 >> 3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t169(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 22528*v1;
	r1 = 32768*v0;
	r0 = r0 >> 3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t170(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c2*v2 in r0
	r0 = 22731*v2;
	// Computation of c1*v1 in r1
	r1 = 32768*v1;
	// Computation of r0+r1 in r0
	r1 = r1 << 1;
	r0 = r0 + r1;
	// Computation of c0*v0 in r1
	r1 = -22528*v0;
	// Computation of r0+r1 in r0
	r1 = r1 >> 1;
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_LGS_t171(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 27152*v2;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -22731*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t172(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 31715*v2;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -27152*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t173(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = 21261*v2;
	r0 = r0 << 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -31715*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t174(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = 18572*v2;
	r0 = r0 << 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -21261*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t175(int16_t v0,int16_t v1,int16_t v2)
{
    // Registers declaration
	int32_t r0, r1;
	// Computation of c2*v2 in r0
	r0 = 23644*v2;
	// Computation of c0*v0 in r1
	r1 = -18572*v0;
	// Computation of r0+r1 in r0
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 32768*v1;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_LGS_t176(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -17243*v1;
	r1 = -23644*v0;
	r0 = r0 << 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x1(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 22493*v1;
	r1 = 16384*v0;
	r0 = r0 >> 11;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x2(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32717*v1;
	r1 = 16384*v0;
	r0 = r0 >> 7;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x3(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 23756*v1;
	r1 = 16384*v0;
	r0 = r0 >> 5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x4(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32093*v1;
	r1 = 16384*v0;
	r0 = r0 >> 4;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x5(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 19121*v1;
	r1 = 16384*v0;
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x6(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 17727*v1;
	r1 = 16384*v0;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x7(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 21111*v1;
	r1 = 16384*v0;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x8(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 28553*v1;
	r1 = 16384*v0;
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -19562*v6;
	r1 = -20301*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -23392*v5;
	r0 = r0 + r1;

	r1 = -27484*v4;
	r2 = -30806*v8;
	r1 = r1 + r2;
	r2 = -20625*v7;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r2 = 25004*v3;
	r1 = r1 + r2;
	r2 = 23617*v2;
	r1 = r1 >> 1;
	r2 = r2 >> 1;
	r1 = r1 + r2;
	r2 = 20025*v1;
	r2 = r2 >> 1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

double Dt2(double v0,double v1)
{	return -0.0859375 * v0 + v1;	}

double Dt10(double v0)
{	return 0.99267578125 * v0;	}

double Dt19(double v0,double v1)
{	return -0.3468475341796875 * v0 + v1;	}

double Dt27(double v0)
{	return 0.893310546875 * v0;	}

double Dt36(double v0,double v1)
{	return -0.414306640625 * v0 + v1;	}

double Dt44(double v0)
{	return 0.867034912109375 * v0;	}

double Dt53(double v0,double v1)
{	return -0.4839324951171875 * v0 + v1;	}

double Dt61(double v0)
{	return 0.831207275390625 * v0;	}

double Dt70(double v0,double v1)
{	return v1 - 0.648834228515625 * v0;	}

double Dt78(double v0)
{	return 0.74078369140625 * v0;	}

double Dt87(double v0,double v1)
{	return v1 - 1.133544921875 * v0;	}

double Dt95(double v0)
{	return 0.512359619140625 * v0;	}

double Dt104(double v0,double v1)
{	return v1 - 2.88623046875 * v0;	}

double Dt112(double v0)
{	return 0.095439910888671875 * v0;	}

double Dt119(double v0,double v1)
{	return v0 + 1.478759765625 * v1;	}

double Dt126(double v0,double v1)
{	return 0.839691162109375 * v1 + v0;	}

double Dt133(double v0,double v1)
{	return 0.539337158203125 * v1 + v0;	}

double Dt140(double v0,double v1)
{	return 0.4196014404296875 * v1 + v0;	}

double Dt147(double v0,double v1)
{	return 0.3701171875 * v1 + v0;	}

double Dt154(double v0,double v1)
{	return 0.3443145751953125 * v1 + v0;	}

double Dt161(double v0,double v1)
{	return 0.0859375 * v1 + v0;	}

double Dt169(double v0,double v1)
{	return 0.0859375 * v1 + v0;	}

double Dt170(double v0,double v1,double v2)
{	return v1 + 0.3468475341796875 * v2 - 0.0859375 * v0;	}

double Dt171(double v0,double v1,double v2)
{	return 0.414306640625 * v2 + v1 - 0.3468475341796875 * v0;	}

double Dt172(double v0,double v1,double v2)
{	return 0.4839324951171875 * v2 + v1 - 0.414306640625 * v0;	}

double Dt173(double v0,double v1,double v2)
{	return v1 + 0.648834228515625 * v2 - 0.4839324951171875 * v0;	}

double Dt174(double v0,double v1,double v2)
{	return v1 + 1.133544921875 * v2 - 0.648834228515625 * v0;	}

double Dt175(double v0,double v1,double v2)
{	return v1 + 2.88623046875 * v2 - 1.133544921875 * v0;	}

double Dt176(double v0,double v1)
{	return -4.209716796875 * v1 - 2.88623046875 * v0;	}

double DLx1f(double v0,double v1)
{	return 0.001340687274932861328125 * v1 + 1 * v0;	}

double DLx2f(double v0,double v1)
{	return 0.015600681304931640625 * v1 + 1 * v0;	}

double DLx3f(double v0,double v1)
{	return 0.04531097412109375 * v1 + 1 * v0;	}

double DLx4f(double v0,double v1)
{	return 0.122425079345703125 * v1 + 1 * v0;	}

double DLx5f(double v0,double v1)
{	return 0.2917633056640625 * v1 + 1 * v0;	}

double DLx6f(double v0,double v1)
{	return 0.540985107421875 * v1 + 1 * v0;	}

double DLx7f(double v0,double v1)
{	return 0.644256591796875 * v1 + 1 * v0;	}

double DLx8f(double v0,double v1)
{	return 0.4356842041015625 * v1 + 1 * v0;	}

double DLyf(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{	return -0.59698486328125 * v6 + -0.619537353515625 * v0 + -0.7138671875 * v5 + -0.209686279296875 * v4 + -0.94012451171875 * v8 + -0.3147125244140625 * v7 + 0.38153076171875 * v3 + 0.3603668212890625 * v2 + 0.3055572509765625 * v1;}



double impulse()
{
	double X=( rand()/(double)RAND_MAX ) * (20) +490;
	return 500*powf(2,6);
}

double 
impulse2(int c)
{
  // int32_t X = (rand()%(0x00006800<<1+1))-0x6800;
  float x1 = sinf(0.001*c*2*3.1416*20);
  float x2 = sinf(0.001*c*2*3.1416);
  float x3 = (x1+2*x2)*250-100;
  return x3*powf(2,7);
}

int main(void)
{
	srand(time(NULL));

	double imp = impulse(1);
	int16_t u = (int16_t)imp,
		DFIy = 0, DFIy1 = 0, DFIy2 = 0, DFIy3 = 0, DFIy4 = 0, DFIy5 = 0, DFIy6 = 0, DFIy7 = 0, DFIy8 = 0, 
		DFIu1 = 0, DFIu2 = 0, DFIu3 = 0, DFIu4 = 0, DFIu5 = 0, DFIu6 = 0, DFIu7 = 0, DFIu8 = 0/*, 
		x11 = 0, x12 = 0, x13 = 0, x14 = 0, x15 = 0, x16 = 0, x17 = 0, x18 = 0, y1 = 0,
		xp11 = 0, xp12 = 0, xp13 = 0, xp14 = 0, xp15 = 0, xp16 = 0, xp17 = 0, xp18 = 0,
		x21 = 0, x22 = 0, x23 = 0, x24 = 0, x25 = 0, x26 = 0, x27 = 0, x28 = 0, y2 = 0,
		xp21 = 0, xp22 = 0, xp23 = 0, xp24 = 0, xp25 = 0, xp26 = 0, xp27 = 0, xp28 = 0,
		x31 = 0, x32 = 0, x33 = 0, x34 = 0, x35 = 0, x36 = 0, x37 = 0, x38 = 0, y3 = 0,
		xp31 = 0, xp32 = 0, xp33 = 0, xp34 = 0, xp35 = 0, xp36 = 0, xp37 = 0, xp38 = 0,
		x41 = 0, x42 = 0, x43 = 0, x44 = 0, x45 = 0, x46 = 0, x47 = 0, x48 = 0, y4 = 0,
		xp41 = 0, xp42 = 0, xp43 = 0, xp44 = 0, xp45 = 0, xp46 = 0, xp47 = 0, xp48 = 0,
		x51 = 0, x52 = 0, x53 = 0, x54 = 0, x55 = 0, x56 = 0, x57 = 0, x58 = 0, y5 = 0,
		xp51 = 0, xp52 = 0, xp53 = 0, xp54 = 0, xp55 = 0, xp56 = 0, xp57 = 0, xp58 = 0,
		x61 = 0, x62 = 0, x63 = 0, x64 = 0, x65 = 0, x66 = 0, x67 = 0, x68 = 0, y6 = 0,
		xp61 = 0, xp62 = 0, xp63 = 0, xp64 = 0, xp65 = 0, xp66 = 0, xp67 = 0, xp68 = 0,
		xR1 = 0, xR2 = 0, xR3 = 0, xR4 = 0, xR5 = 0, xR6 = 0, xR7 = 0, xR8 = 0, yR = 0,
		tpR1 = 0, tpR2 = 0, tpR3 = 0, tpR4 = 0, tpR5 = 0, tpR6 = 0, tpR7 = 0, tpR8 = 0,
		xpR1 = 0, xpR2 = 0, xpR3 = 0, xpR4 = 0, xpR5 = 0, xpR6 = 0, xpR7 = 0, xpR8 = 0,
		tpL2 = 0, tpL10 = 0, tpL19 = 0, tpL27 = 0, tpL36 = 0, tpL44 = 0, tpL53 = 0, tpL61 = 0,
		tpL70 = 0, tpL78 = 0, tpL87 = 0, tpL95 = 0, tpL104 = 0, tpL112 = 0, tpL119 = 0, tpL126 = 0,
		tpL133 = 0, tpL140 = 0, tpL147 = 0, tpL154 = 0, tpL161 = 0,
		tpL169 = 0, tpL170 = 0, tpL171 = 0, tpL172 = 0, tpL173 = 0, tpL174 = 0, tpL175 = 0, tpL176 = 0,
		xpL1 = 0, xpL2 = 0, xpL3 = 0, xpL4 = 0, xpL5 = 0, xpL6 = 0, xpL7 = 0, xpL8 = 0,
		xL1 = 0, xL2 = 0, xL3 = 0, xL4 = 0, xL5 = 0, xL6 = 0, xL7 = 0, xL8 = 0, yL=0*/;

	double Du = imp*powf(2,-6),
		Du1 = 0, Du2 = 0, Du3 = 0, Du4 = 0, Du5 = 0, Du6 = 0, Du7 = 0, Du8 = 0, 
		Dy = 0, Dy1 = 0, Dy2 = 0, Dy3 = 0, Dy4 = 0, Dy5 = 0, Dy6 = 0, Dy7 = 0, Dy8 = 0,
		/*DLx1 = 0, DLx2 = 0, DLx3 = 0, DLx4 = 0, DLx5 = 0, DLx6 = 0, DLx7 = 0, DLx8 = 0, DLy = 0,
		DLxp1 = 0, DLxp2 = 0, DLxp3 = 0, DLxp4 = 0, DLxp5 = 0, DLxp6 = 0, DLxp7 = 0, DLxp8 = 0,
		DtpL2 = 0, DtpL10 = 0, DtpL19 = 0, DtpL27 = 0, DtpL36 = 0, DtpL44 = 0, DtpL53 = 0, DtpL61 = 0,
		DtpL70 = 0, DtpL78 = 0, DtpL87 = 0, DtpL95 = 0, DtpL104 = 0, DtpL112 = 0, DtpL119 = 0, DtpL126 = 0,
		DtpL133 = 0, DtpL140 = 0, DtpL147 = 0, DtpL154 = 0, DtpL161 = 0,
		DtpL169 = 0, DtpL170 = 0, DtpL171 = 0, DtpL172 = 0, DtpL173 = 0, DtpL174 = 0, DtpL175 = 0, DtpL176 = 0,*/
		miny = 1000,maxy=-1000,
		maxEy1=-10000,minEy1=10000,
		maxEy2=-10000,minEy2=10000,
		maxEy3=-10000,minEy3=10000,
		maxEy4=-10000,minEy4=10000,
		maxEy5=-10000,minEy5=10000,
		maxEy6=-10000,minEy6=10000,
		maxEyL=-10000,minEyL=10000,
		maxEyR=-10000,minEyR=10000,
		maxEyDFI=-10000,minEyDFI=10000;

	int cpt = 1;
	while(cpt<160){


		DFIy = C_int_DFI(u,DFIu1,DFIu2,DFIu3,DFIu4,DFIu5,DFIu6,DFIu7,DFIu8, DFIy1,DFIy2,DFIy3,DFIy4,DFIy5,DFIy6,DFIy7,DFIy8);
		DFIu8 = DFIu7; DFIu7 = DFIu6; DFIu6 = DFIu5; DFIu5 = DFIu4; DFIu4 = DFIu3; DFIu3 = DFIu2; DFIu2 = DFIu1; DFIu1=u;
		DFIy8 = DFIy7; DFIy7 = DFIy6; DFIy6 = DFIy5; DFIy5 = DFIy4; DFIy4 = DFIy3; DFIy3 = DFIy2; DFIy2 = DFIy1; DFIy1=DFIy;

		/*xp11 = C_int_ss1_x1(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp12 = C_int_ss1_x2(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp13 = C_int_ss1_x3(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp14 = C_int_ss1_x4(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp15 = C_int_ss1_x5(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp16 = C_int_ss1_x6(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp17 = C_int_ss1_x7(x11, x12, x13, x14, x15, x16, x17, x18,u);
		xp18 = C_int_ss1_x8(x11, x12, x13, x14, x15, x16, x17, x18,u);
		y1 = C_int_ss1_y(x11, x12, x13, x14, x15, x16, x17, x18,u);
		x11 = xp11; x12 = xp12; x13 = xp13; x14 = xp14; x15 = xp15; x16 = xp16; x17 = xp17; x18 = xp18;

		xp21 = C_int_ss2_x1(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp22 = C_int_ss2_x2(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp23 = C_int_ss2_x3(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp24 = C_int_ss2_x4(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp25 = C_int_ss2_x5(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp26 = C_int_ss2_x6(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp27 = C_int_ss2_x7(x21, x22, x23, x24, x25, x26, x27, x28,u);
		xp28 = C_int_ss2_x8(x21, x22, x23, x24, x25, x26, x27, x28,u);
		y2 = C_int_ss2_y(x21, x22, x23, x24, x25, x26, x27, x28,u);
		x21 = xp21; x22 = xp22; x23 = xp23; x24 = xp24; x25 = xp25; x26 = xp26; x27 = xp27; x28 = xp28;

		xp31 = C_int_ss3_x1(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp32 = C_int_ss3_x2(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp33 = C_int_ss3_x3(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp34 = C_int_ss3_x4(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp35 = C_int_ss3_x5(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp36 = C_int_ss3_x6(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp37 = C_int_ss3_x7(x31, x32, x33, x34, x35, x36, x37, x38,u);
		xp38 = C_int_ss3_x8(x31, x32, x33, x34, x35, x36, x37, x38,u);
		y3 = C_int_ss3_y(x31, x32, x33, x34, x35, x36, x37, x38,u);
		x31 = xp31; x32 = xp32; x33 = xp33; x34 = xp34; x35 = xp35; x36 = xp36; x37 = xp37; x38 = xp38;

		xp41 = C_int_ss4_x1(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp42 = C_int_ss4_x2(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp43 = C_int_ss4_x3(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp44 = C_int_ss4_x4(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp45 = C_int_ss4_x5(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp46 = C_int_ss4_x6(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp47 = C_int_ss4_x7(x41, x42, x43, x44, x45, x46, x47, x48,u);
		xp48 = C_int_ss4_x8(x41, x42, x43, x44, x45, x46, x47, x48,u);
		y4 = C_int_ss4_y(x41, x42, x43, x44, x45, x46, x47, x48,u);
		x41 = xp41; x42 = xp42; x43 = xp43; x44 = xp44; x45 = xp45; x46 = xp46; x47 = xp47; x48 = xp48;

		xp51 = C_int_ss5_x1(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp52 = C_int_ss5_x2(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp53 = C_int_ss5_x3(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp54 = C_int_ss5_x4(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp55 = C_int_ss5_x5(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp56 = C_int_ss5_x6(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp57 = C_int_ss5_x7(x51, x52, x53, x54, x55, x56, x57, x58,u);
		xp58 = C_int_ss5_x8(x51, x52, x53, x54, x55, x56, x57, x58,u);
		y5 = C_int_ss5_y(x51, x52, x53, x54, x55, x56, x57, x58,u);
		x51 = xp51; x52 = xp52; x53 = xp53; x54 = xp54; x55 = xp55; x56 = xp56; x57 = xp57; x58 = xp58;

		xp61 = C_int_ss6_x1(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp62 = C_int_ss6_x2(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp63 = C_int_ss6_x3(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp64 = C_int_ss6_x4(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp65 = C_int_ss6_x5(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp66 = C_int_ss6_x6(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp67 = C_int_ss6_x7(x61, x62, x63, x64, x65, x66, x67, x68,u);
		xp68 = C_int_ss6_x8(x61, x62, x63, x64, x65, x66, x67, x68,u);
		y6 = C_int_ss6_y(x61, x62, x63, x64, x65, x66, x67, x68,u);
		x61 = xp61; x62 = xp62; x63 = xp63; x64 = xp64; x65 = xp65; x66 = xp66; x67 = xp67; x68 = xp68;

		tpR1 = C_int_rho_t1(xR1,u);
		tpR2 = C_int_rho_t2(xR2);
		tpR3 = C_int_rho_t3(xR3);
		tpR4 = C_int_rho_t4(xR4);
		tpR5 = C_int_rho_t5(xR5);
		tpR6 = C_int_rho_t6(xR6);
		tpR7 = C_int_rho_t7(xR7);
		tpR8 = C_int_rho_t8(xR8);
		xpR1 = C_int_rho_x1(tpR1, tpR2, xR1, u);
		xpR2 = C_int_rho_x2(tpR1, tpR3, xR2, u);
		xpR3 = C_int_rho_x3(tpR1, tpR4, xR3, u);
		xpR4 = C_int_rho_x4(tpR1, tpR5, xR4, u);
		xpR5 = C_int_rho_x5(tpR1, tpR6, xR5, u);
		xpR6 = C_int_rho_x6(tpR1, tpR7, xR6, u);
		xpR7 = C_int_rho_x7(tpR1, tpR8, xR7, u);
		xpR8 = C_int_rho_x8(tpR1, xR8, u);
		yR   = tpR1;
		xR1 = xpR1; xR2 = xpR2; xR3 = xpR3; xR4 = xpR4; xR5 = xpR5; xR6 = xpR6; xR7 = xpR7; xR8 = xpR8; 

		

		

		tpL2 = C_int_LGS_t2(xL1, xL2);
		tpL10 = C_int_LGS_t10(tpL2);
		tpL19 = C_int_LGS_t19(tpL10, xL3);
		tpL27 = C_int_LGS_t27(tpL19);
		tpL36 = C_int_LGS_t36(tpL27, xL4);
		tpL44 = C_int_LGS_t44(tpL36);
		tpL53 = C_int_LGS_t53(tpL44, xL5);
		tpL61 = C_int_LGS_t61(tpL53);
		tpL70 = C_int_LGS_t70(tpL61, xL6);
		tpL78 = C_int_LGS_t78(tpL70);
		tpL87 = C_int_LGS_t87(tpL78, xL7); 
		tpL95 = C_int_LGS_t95(tpL87); 
		tpL104 = C_int_LGS_t104(tpL95, xL8);
		tpL112 = C_int_LGS_t112(tpL104);
		tpL119 = C_int_LGS_t119(tpL95, tpL112);
		tpL126 = C_int_LGS_t126(tpL78, tpL119);
		tpL133 = C_int_LGS_t133(tpL61, tpL126);
		tpL140 = C_int_LGS_t140(tpL44, tpL133);
		tpL147 = C_int_LGS_t147(tpL27, tpL140);
		tpL154 = C_int_LGS_t154(tpL10, tpL147);
		tpL161 = C_int_LGS_t161(xL1, tpL154);
		tpL169 = C_int_LGS_t169(tpL161, tpL154); 
		tpL170 = C_int_LGS_t170(tpL161, tpL154, tpL147); 
		tpL171 = C_int_LGS_t171(tpL154, tpL147, tpL140); 
		tpL172 = C_int_LGS_t172(tpL147, tpL140, tpL133);
		tpL173 = C_int_LGS_t173(tpL140, tpL133, tpL126); 
		tpL174 = C_int_LGS_t174(tpL133, tpL126, tpL119); 
		tpL175 = C_int_LGS_t175(tpL126, tpL119, tpL112); 
		tpL176 = C_int_LGS_t176(tpL119, tpL112);
		
		xpL1 = C_int_LGS_x1(tpL169,u); xpL2 = C_int_LGS_x2(tpL170,u); xpL3 = C_int_LGS_x3(tpL171,u); xpL4 = C_int_LGS_x4(tpL172,u);
		xpL5 = C_int_LGS_x5(tpL173,u); xpL6 = C_int_LGS_x6(tpL174,u); xpL7 = C_int_LGS_x7(tpL175,u); xpL8 = C_int_LGS_x8(tpL176,u);
		yL = C_int_LGS_y(xL1,xL2,xL3,xL4,xL5,xL6,xL7,xL8,u);
		xL1 = xpL1; xL2 = xpL2; xL3 = xpL3; xL4 = xpL4; xL5 = xpL5; xL6 = xpL6; xL7 = xpL7; xL8 = xpL8; 


		DtpL2 = Dt2(DLx1,DLx2);
		DtpL10 = Dt10(DtpL2);
		DtpL19 = Dt19(DtpL10,DLx3);
		DtpL27 = Dt27(DtpL19);
		DtpL36 = Dt36(DtpL27,DLx4);
		DtpL44 = Dt44(DtpL36);
		DtpL53 = Dt53(DtpL44,DLx5);
		DtpL61 = Dt61(DtpL53);
		DtpL70 = Dt70(DtpL61,DLx6);
		DtpL78 = Dt78(DtpL70);
		DtpL87 = Dt87(DtpL78,DLx7); 
		DtpL95 = Dt95(DtpL87); 
		DtpL104 = Dt104(DtpL95,DLx8);
		DtpL112 = Dt112(DtpL104);
		DtpL119 = Dt119(DtpL95,DtpL112);
		DtpL126 = Dt126(DtpL78, DtpL119);
		DtpL133 = Dt133(DtpL61, DtpL126);
		DtpL140 = Dt140(DtpL44, DtpL133);
		DtpL147 = Dt147(DtpL27, DtpL140);
		DtpL154 = Dt154(DtpL10, DtpL147);
		DtpL161 = Dt161(DLx1, DtpL154);
		DtpL169 = Dt169(DtpL161,DtpL154); 
		DtpL170 = Dt170(DtpL161,DtpL154,DtpL147); 
		DtpL171 = Dt171(DtpL154,DtpL147,DtpL140); 
		DtpL172 = Dt172(DtpL147,DtpL140,DtpL133);
		DtpL173 = Dt173(DtpL140,DtpL133,DtpL126); 
		DtpL174 = Dt174(DtpL133,DtpL126,DtpL119); 
		DtpL175 = Dt175(DtpL126,DtpL119,DtpL112); 
		DtpL176 = Dt176(DtpL119,DtpL112);

		DLxp1 = DLx1f(DtpL169,Du); DLxp2 = DLx2f(DtpL170,Du); DLxp3 = DLx3f(DtpL171,Du); DLxp4 = DLx4f(DtpL172,Du);
		DLxp5 = DLx5f(DtpL173,Du); DLxp6 = DLx6f(DtpL174,Du); DLxp7 = DLx7f(DtpL175,Du); DLxp8 = DLx8f(DtpL176,Du);
		DLy = DLyf(DLx1,DLx2,DLx3,DLx4,DLx5,DLx6,DLx7,DLx8,Du);
		DLx1 = DLxp1; DLx2 = DLxp2; DLx3 = DLxp3; DLx4 = DLxp4; DLx5 = DLxp5; DLx6 = DLxp6; DLx7 = DLxp7; DLx8 = DLxp8; */



		Dy = double_DFI(Du,Du1, Du2, Du3, Du4, Du5, Du6, Du7, Du8,Dy1, Dy2, Dy3, Dy4, Dy5, Dy6, Dy7, Dy8);
		Du8 = Du7; Du7 = Du6; Du6 = Du5; Du5 = Du4; Du4 = Du3; Du3 = Du2; Du2 = Du1; Du1=Du;
		Dy8 = Dy7; Dy7 = Dy6; Dy6 = Dy5; Dy5 = Dy4; Dy4 = Dy3; Dy3 = Dy2; Dy2 = Dy1; Dy1=Dy;

		/*if(y1*powf(2,-2)-Dy >maxEy1) maxEy1=y1*powf(2,-2)-Dy;
		if(y1*powf(2,-2)-Dy<minEy1) minEy1=y1*powf(2,-2)-Dy;
		if(y2*powf(2,-2)-Dy >maxEy2) maxEy2=y2*powf(2,-2)-Dy;
		if(y2*powf(2,-2)-Dy<minEy2) minEy2=y2*powf(2,-2)-Dy;
		if(y3*powf(2,-2)-Dy >maxEy3) maxEy3=y3*powf(2,-2)-Dy;
		if(y3*powf(2,-2)-Dy<minEy3) minEy3=y3*powf(2,-2)-Dy;
		if(y4*powf(2,-2)-Dy >maxEy4) maxEy4=y4*powf(2,-2)-Dy;
		if(y4*powf(2,-2)-Dy<minEy4) minEy4=y4*powf(2,-2)-Dy;
		if(y5*powf(2,-2)-Dy >maxEy5) maxEy5=y5*powf(2,-2)-Dy;
		if(y5*powf(2,-2)-Dy<minEy5) minEy5=y5*powf(2,-2)-Dy;
		if(y6*powf(2,-2)-Dy >maxEy6) maxEy6=y6*powf(2,-2)-Dy;
		if(y6*powf(2,-2)-Dy<minEy6) minEy6=y6*powf(2,-2)-Dy;
		if(yR*powf(2,-2)-Dy >maxEyR) maxEyR=yR*powf(2,-2)-Dy;
		if(yR*powf(2,-2)-Dy<minEyR) minEyR=yR*powf(2,-2)-Dy;
		if(yL*powf(2,-2)-Dy >maxEyL) maxEyL=yL*powf(2,-2)-Dy;
		if(yL*powf(2,-2)-Dy<minEyL) minEyL=yL*powf(2,-2)-Dy;*/
		if(DFIy*powf(2,-4)-Dy >maxEyDFI) maxEyDFI=DFIy*powf(2,-4)-Dy;
		if(DFIy*powf(2,-4)-Dy<minEyDFI) minEyDFI=DFIy*powf(2,-4)-Dy;

		if(Dy >maxy) maxy=Dy;
		if(Dy<miny) miny=Dy;
		
		//printf("%d %g %g %g %g %g %g %g %g %g %g\n",cpt, imp*powf(2,-2), y1*powf(2,-2)-Dy, y2*powf(2,-2)-Dy, y3*powf(2,-2)-Dy, y4*powf(2,-2)-Dy, y5*powf(2,-2)-Dy, y6*powf(2,-2)-Dy, yR*powf(2,-2)-Dy, yL*powf(2,-2)-DLy, DFIy*powf(2,-2)-Dy);

		//printf("%d %g %g %g %g %g \n",cpt, Dy, (int32_t)y3*powf(2,-2), yR*powf(2,-2), yL*powf(2,-2), DFIy*powf(2,-2));

		//printf("%d %g %g %g %g %g %g %g %g %g\n",cpt, DFIy*powf(2,-4)-Dy, y1*powf(2,-4)-Dy,y2*powf(2,-4)-Dy, y3*powf(2,-4)-Dy, y4*powf(2,-4)-Dy, y5*powf(2,-4)-Dy, y6*powf(2,-4)-Dy, yR*powf(2,-4)-Dy, yL*powf(2,-4)-DLy);
		printf("%d %g %g %g\n",cpt, /*DFIy*powf(2,-3)-*/Dy, -2649.37929503, -2506.09162439);
		cpt++;
		imp = impulse(cpt);
		u = (int16_t) imp;
		Du =imp*powf(2,-6);
  	}
  	//printf(" %g ; %g\n", minDy,maxDy);
  	/*printf(" %g ; %g", miny,maxy);
  	printf("dSS1 = [ %.6g ; %.6g ]\n", minEy1, maxEy1);
	printf("dSS2 = [ %.6g ; %.6g ]\n", minEy2, maxEy2);
	printf("dSS3 = [ %.6g ; %.6g ]\n", minEy3, maxEy3);
	printf("dSS4 = [ %.6g ; %.6g ]\n", minEy4, maxEy4);
	printf("dSS5 = [ %.6g ; %.6g ]\n", minEy5, maxEy5);
	printf("dSS6 = [ %.6g ; %.6g ]\n", minEy6, maxEy6);
	printf("dSSL = [ %.6g ; %.6g ]\n", minEyL, maxEyL);
	printf("dSSR = [ %.6g ; %.6g ]\n", minEyR, maxEyR);
	printf("dSSDFI = [ %.6g ; %.6g ]\n", minEyDFI, maxEyDFI);*/
  return 0;
}

