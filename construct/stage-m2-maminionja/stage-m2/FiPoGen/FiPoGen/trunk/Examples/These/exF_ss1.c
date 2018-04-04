#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


double double_x1(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
	double r;
	r = 1.058913767337799072265625e-05 * v7 + 0.00015039741992950439453125 * v6 + 0.0056154727935791015625 * v5 + -0.036739349365234375 * v4 + -0.0527477264404296875 * v3 + -0.048828125 * v2 + 1.1151123046875 * v8 + 0.868560791015625 * v1 + 0.38116455078125 * v0;
	//r = 1.05891865371e-05 * v7 + 0.000150397542172 * v6 + 0.00561554356397 * v5 -0.0367389413626 * v4 -0.0527471294178 * v3 -0.0488278986357 * v2 + 1.11511478422 * v8 + 0.868555641483 * v1 + 0.381165836221 * v0;
	return r; 
}

double double_x2(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = 1.420266926288604736328125e-05 * v7 + 0.00014705955982208251953125 * v6 + 0.01005458831787109375 * v5 + -0.047924041748046875 * v4 + -0.063236236572265625 * v3 + 0.880645751953125 * v8 + -0.2727508544921875 * v2 + -0.868560791015625 * v0 + 0.2592620849609375 * v1;
	//r = 1.42027697884e-05 * v7 + 0.000147058719827 * v6 + 0.0100547381296 * v5 -0.0479230882972 * v4 -0.0632368860274 * v3 + 0.880644285426 * v8 -0.272743349014 * v2 -0.868555641483 * v0 + 0.25925465753 * v1;
	return r;
}

double double_x3(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = -5.500577390193939208984375e-05 * v7 + -0.0008521974086761474609375 * v6 + -0.02589893341064453125 * v5 + 0.19539642333984375 * v4 + -0.048828125 * v0 + -1.69744873046875 * v8 + 0.2929840087890625 * v3 + 0.2727508544921875 * v1 + -0.447174072265625 * v2;
	//r= -0.0488278986357*v0 + 0.272743349014*v1 -0.447181676721*v2 +0.292980118324*v3 + 0.19539834565*v4 -0.0258986481392*v5 -0.000852193375464*v6 -5.50063896085e-05 *v7 - 1.69742788388*v8
	return r; 
}

double double_x4(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = -6.86533749103546142578125e-05 * v7 + 0.00148594379425048828125 * v6 + 0.17205047607421875 * v8 + -0.1504364013671875 * v5 + 0.0527477264404296875 * v0 + -0.643646240234375 * v3 + -0.2929840087890625 * v2 + 0.3220977783203125 * v4 + -0.063236236572265625 * v1;
	return r; 
}

double double_x5(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = 2.7538277208805084228515625e-05 * v7 + -0.0033867359161376953125 * v6 + -0.16170501708984375 * v8 + 0.19020843505859375 * v5 + 0.047924041748046875 * v1 + -0.036739349365234375 * v0 + 0.689666748046875 * v4 + -0.3220977783203125 * v3 + 0.19539642333984375 * v2;
	return r; 
}

double double_x6(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = 0.007668972015380859375 * v7 + 0.025909423828125 * v5 + 0.0537700653076171875 * v8 + 0.19751739501953125 * v6 + 0.0056154727935791015625 * v0 + -0.02589893341064453125 * v2 + -0.01005458831787109375 * v1 + 0.19020843505859375 * v4 + 0.1504364013671875 * v3;
	return r; 
}

double double_x7(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = -0.000146798789501190185546875 * v8 + 0.0684661865234375 * v7 + 0.00014705955982208251953125 * v1 + -0.00015039741992950439453125 * v0 + 0.00148594379425048828125 * v3 + 0.0008521974086761474609375 * v2 + 0.0033867359161376953125 * v4 + -0.19751739501953125 * v5 + -0.4504547119140625 * v6;
	return r; 
}

double double_x8(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = -5.1058828830718994140625e-05 * v8 + -2.7538277208805084228515625e-05 * v4 + 1.420266926288604736328125e-05 * v1 + -1.058913767337799072265625e-05 * v0 + -6.86533749103546142578125e-05 * v3 + 5.500577390193939208984375e-05 * v2 + 0.1318511962890625 * v7 + 0.0684661865234375 * v6 + -0.007668972015380859375 * v5;
	return r; 
}

double double_y(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{
    double r;
    r = -5.1058828830718994140625e-05 * v7 + -0.000146798789501190185546875 * v6 + -0.0537700653076171875 * v5 + -0.11029052734375 * v8 + 0.16170501708984375 * v4 + 0.17205047607421875 * v3 + -1.1151123046875 * v0 + 1.69744873046875 * v2 + 0.880645751953125 * v1;
	return r; 
}


int16_t C_int_DFI(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8,int16_t v9,int16_t v10,int16_t v11,int16_t v12,int16_t v13,int16_t v14,int16_t v15,int16_t v16)
{
	int32_t r0, r1;
	r0 = -24188*v8;
	r1 = 25906*v7;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -29144*v16;
	r0 = r0 + r1;
	r1 = -28912*v0;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -26267*v15;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -16944*v2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -21946*v4;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 21865*v6;
	r0 = r0 + r1;
	r1 = 25571*v5;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -28011*v9;
	r0 = r0 + r1;
	r1 = 32515*v12;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -27480*v1;
	r0 = r0 + r1;
	r1 = -28000*v3;

	r0 = r0 + r1;
	r1 = 25244*v14;
	r0 = r0 + r1;
	r1 = -31131*v10;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -17435*v11;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 20664*v13;
	r0 = r0 + r1;
	return r0 >> 16;
}


int16_t C_int_ss1_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 22740*v7;
	r1 = 20186*v6;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = 23553*v5;
	r0 = r0 >> 7;
	r0 = r0 + r1;
	r1 = -19262*v4;
	r0 = r0 >> 5;
	r0 = r0 + r1;
	r1 = -27655*v3;
	r0 = r0 + r1;
	r1 = -25600*v2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 18270*v8;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 28461*v1;
	r0 = r0 >> 2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 24980*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}


int16_t C_int_ss1_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 30500*v7;
	r1 = 19738*v6;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = 21086*v5;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = -25126*v4;
	r0 = r0 >> 4;
	r0 = r0 + r1;
	r1 = -16577*v3;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 28857*v8;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -17875*v2;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -28461*v0;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 16991*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}



int16_t C_int_ss1_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -29531*v7;
	r1 = -28595*v6;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = -27157*v5;
	r0 = r0 >> 7;
	r0 = r0 + r1;
	r1 = 25611*v4;
	r0 = r0 >> 5;
	r0 = r0 + r1;
	r1 = -25600*v0;
	r0 = r0 + r1;
	r1 = -27811*v8;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 19201*v3;
	r0 = r0 + r1;
	r1 = 17875*v1;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -29306*v2;
	r0 = r0 + r1;
	return r0 >> 16;
}



int16_t C_int_ss1_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -18429*v7;
	r1 = 24930*v6;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = 22551*v8;
	r0 = r0 >> 9;
	r0 = r0 + r1;
	r1 = -19718*v5;
	r0 = r0 + r1;
	r1 = 27655*v0;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -21091*v3;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -19201*v2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 21109*v4;
	r0 = r0 + r1;
	r1 = -16577*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}



int16_t C_int_ss1_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 29569*v7;
	r1 = -28410*v6;
	r0 = r0 >> 9;
	r0 = r0 + r1;
	r1 = -21195*v8;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = 24931*v5;
	r0 = r0 + r1;
	r1 = 25126*v1;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -19262*v0;
	r0 = r0 + r1;
	r1 = 22599*v4;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -21109*v3;
	r0 = r0 + r1;
	r1 = 25611*v2;
	r0 = r0 + r1;
	return r0 >> 16;
}



int16_t C_int_ss1_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 32166*v7;
	r1 = 27168*v5;
	r0 = r0 >> 8;
	r0 = r0 + r1;
	r1 = 28191*v8;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 25889*v6;
	r0 = r0 + r1;
	r1 = 23553*v0;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -27157*v2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -21086*v1;
	r0 = r0 + r1;
	r1 = 24931*v4;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 19718*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}


int16_t C_int_ss1_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -19703*v8;
	r1 = 17948*v7;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = 19738*v1;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -20186*v0;
	r0 = r0 + r1;
	r1 = 24930*v3;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 28595*v2;
	r0 = r0 + r1;
	r1 = 28410*v4;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -25889*v5;
	r0 = r0 >> 3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -29521*v6;
	r0 = r0 + r1;
	return r0 >> 16;
}



int16_t C_int_ss1_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -27412*v8;
	r1 = -29569*v4;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 30500*v1;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -22740*v0;
	r0 = r0 + r1;
	r1 = -18429*v3;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 29531*v2;
	r0 = r0 + r1;
	r1 = 17282*v7;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = 17948*v6;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -32166*v5;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss1_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -27412*v7;
	r1 = -19703*v6;
	r0 = r0 >> 6;
	r0 = r0 + r1;
	r1 = -28191*v5;
	r0 = r0 >> 10;
	r0 = r0 + r1;
	r1 = -28912*v8;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 21195*v4;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = 22551*v3;
	r0 = r0 + r1;
	r1 = -18270*v0;
	r0 = r0 >> 4;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 27811*v2;
	r0 = r0 + r1;
	r1 = 28857*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}


int16_t C_int_ss2_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -17317*v8;
	r1 = 23614*v2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -28879*v1;
	r0 = r0 + r1;
	r1 = 32275*v5;
	r2 = 30350*v6;
	r1 = r1 << 2;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r0 = r0 + r1;
	r1 = 21482*v7;
	r2 = 30564*v4;
	r1 = r1 << 1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = -19922*v3;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = 23539*v0;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 19067*v8;
	r1 = 23986*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -22826*v2;
	r1 = r1 >> 3;
	r0 = r0 + r1;
	r1 = -23978*v5;
	r2 = -27205*v6;
	r1 = r1 << 2;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r0 = r0 + r1;
	r1 = -28923*v7;
	r2 = -20714*v4;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = -21600*v0;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = -27687*v1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 26020*v8;
	r1 = -23378*v6;
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = -16766*v0;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = -29314*v5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -31454*v4;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -18108*v3;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -22991*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -18607*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -22713*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -17544*v8;
	r1 = 32698*v6;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 17255*v4;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 18864*v0;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 31186*v5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 29539*v3;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 18018*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 28326*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 25113*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -18981*v8;
	r1 = 29800*v6;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 19942*v5;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 19497*v4;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 21436*v2;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 20714*v0;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 24843*v3;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 16759*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 25627*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -27748*v7;
	r1 = -23994*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -31581*v1;
	r2 = 24618*v8;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -18401*v3;
	r2 = -32175*v6;
	r1 = r1 << 3;
	r2 = r2 << 3;
	r1 = r1 + r2;
	r0 = r0 + r1;
	r1 = -25458*v5;
	r2 = -21177*v2;
	r1 = r1 << 2;
	r2 = r2 << 3;
	r1 = r1 + r2;
	r2 = -30778*v4;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 27713*v8;
	r1 = -23532*v6;
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = -24931*v5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -27168*v4;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -24545*v3;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -20619*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -19805*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -28931*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -20672*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -22876*v8;
	r1 = 18320*v2;
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 16526*v5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 20911*v4;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 26734*v3;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 25678*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 28586*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 18976*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 29094*v6;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss2_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -28912*v8;
	r1 = 30212*v2;
	r0 = r0 >> 6;
	r0 = r0 + r1;
	r1 = -17915*v6;
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = -31210*v3;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 17765*v5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -26452*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 20801*v4;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 24015*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 24171*v7;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 23558*v8;
	r1 = 28252*v7;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 21182*v2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 17846*v4;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 27738*v6;
	r0 = r0 >> 2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 32053*v5;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -30344*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -30023*v1;
	r0 = r0 + r1;
	r1 = -26909*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 18537*v5;
	r1 = 28353*v8;
	r0 = r0 + r1;
	r1 = 19320*v2;
	r2 = 18960*v7;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	r1 = 29329*v0;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 30364*v4;
	r2 = -23196*v6;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 30057*v3;
	r1 = r1 + r2;
	r2 = 17633*v1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -31164*v8;
	r1 = 30416*v7;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -21217*v2;
	r0 = r0 + r1;
	r1 = 21398*v0;
	r0 = r0 + r1;
	r1 = 28999*v1;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 16882*v6;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -30178*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 26074*v5;
	r0 = r0 + r1;
	r1 = -19126*v4;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 26821*v8;
	r1 = 26375*v7;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -23627*v2;
	r0 = r0 + r1;
	r1 = 20992*v6;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 22694*v4;
	r0 = r0 + r1;
	r1 = 28293*v3;
	r0 = r0 >> 1;
	r1 = r1 >> 1; // doute
	r0 = r0 + r1;
	r1 = 27011*v0;
	//r0 = r0 >> 1; // doute
	r0 = r0 + r1;
	r1 = 20334*v5;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 18247*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -31486*v8;
	r1 = -19582*v7;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -16471*v0;
	r0 = r0 + r1;
	r1 = 21480*v6;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 24895*v2;
	r0 = r0 + r1;
	r0 = r0 >> 1;
	r1 = -24155*v1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 16958*v5;
	//r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -23899*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -20015*v4;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -30897*v4;
	r1 = 25589*v7;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 23700*v1;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 21724*v8;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r0 = r0 >> 1;
	r1 = 28597*v0;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -32636*v5;
	//r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -16730*v2;
	r0 = r0 + r1;
	r1 = -21837*v6;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -31747*v3;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 21401*v4;
	r1 = 17320*v8;
	r0 = r0 + r1;
	r1 = 31959*v1;
	r2 = -29496*v7;
	r1 = r1 + r2;
	r2 = 23168*v2;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 16602*v0;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -19670*v3;
	r2 = 30723*v6;
	r1 = r1 + r2;
	r2 = 25082*v5;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 26121*v5;
	r1 = 19233*v7;
	r0 = r0 + r1;
	r1 = -31940*v3;
	r2 = -23606*v4;
	r1 = r1 + r2;
	r2 = 20530*v2;
	r2 = r2 >> 1;
	r1 = r1 + r2;
	r2 = -32192*v8;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -19653*v6;
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 21476*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 21112*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss3_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -28912*v8;
	r1 = -25892*v2;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = 26532*v7;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 29865*v5;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 27719*v4;
	r0 = r0 + r1;
	r0 = r0 >> 1; // doute
	r1 = 26515*v0;
	r1 = r1 >> 1; // doute
	r0 = r0 + r1;
	r1 = -21211*v6;
	//r0 = r0 >> 1; // doute
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 17838*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -21453*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 18762*v7;
	r1 = -16683*v8;
	r0 = r0 + r1;
	r1 = -31014*v0;
	r0 = r0 + r1;
	r1 = 23660*v4;
	r2 = -28553*v6;
	r1 = r1 + r2;
	r2 = -19698*v2;
	r1 = r1 >> 2;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 16744*v5;
	r2 = -26787*v1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = -24553*v3;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 18941*v7;
	r1 = 21203*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 28316*v6;
	r2 = -18419*v5;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r2 = 30211*v4;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r2 = 19239*v2;
	r1 = r1 + r2;
	r2 = 19884*v8;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r2 = 32143*v1;
	r1 = r1 + r2;
	r2 = 28295*v0;
	r1 = r1 >> 1;
	r2 = r2 >> 1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -26825*v4;
	r1 = 19740*v6;
	r0 = r0 + r1;
	r1 = 23885*v1;
	r0 = r0 + r1;
	r1 = -30032*v2;
	r2 = -23130*v8;
	r1 = r1 >> 3;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -17614*v3;
	r2 = -17571*v7;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = -18991*v5;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = -27295*v0;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 29476*v7;
	r1 = -23939*v8;
	r0 = r0 + r1;
	r1 = 24188*v0;
	r0 = r0 + r1;
	r0 = r0 >> 1;
	r1 = -20596*v3;
	r2 = 21742*v4;
	r1 = r1 + r2;
	r2 = -28170*v2;
	r1 = r1 + r2;
	r1 = r1 >> 2;
	r0 = r0 + r1;	
	r1 = 18757*v6;
	r2 = 27208*v1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 32415*v5;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 22040*v8;
	r1 = -18767*v4;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 16605*v0;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 20108*v1;
	r0 = r0 >> 1;
	r1 = r1 << 3;
	r0 = r0 + r1;
	r1 = 22000*v5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 30007*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 17453*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 26311*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 23455*v6;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 20413*v8;
	r1 = -20017*v3;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -32768*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -24596*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -17530*v6;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -22610*v5;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -19311*v2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -18853*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -19459*v4;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -32279*v7;
	r1 = -29503*v3;
	r1 = r1 << 1; 
	r0 = r0 + r1;
	r1 = 19683*v0;
	r0 = r0 + r1;
	r1 = 30012*v6;
	r2 = 30510*v8;
	r1 = r1 + r2;
	r2 = 16490*v4;
	r1 = r1 >> 1; 
	r2 = r2 >> 1;
	r1 = r1 + r2;
	r2 = 23432*v5;
	r1 = r1 + r2;
	r2 = -19891*v2;
	r1 = r1 + r2;
	r2 = -28327*v1;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 20199*v4;
	r1 = -20031*v8;
	r0 = r0 + r1;
	r1 = -16397*v2;
	r2 = -25447*v6;
	r1 = r1 >> 6;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 27794*v0;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 18197*v3;
	r2 = 21042*v7;
	r1 = r1 << 1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 24936*v1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 26361*v5;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss4_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -28912*v8;
	r1 = -29873*v2;
	r0 = r0 >> 4;
	r0 = r0 + r1;
	r1 = 28926*v4;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -22585*v6;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 32717*v0;
	r0 = r0 + r1;
	r1 = -30445*v1;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 26352*v7;
	r0 = r0 + r1;
	r1 = 32584*v5;
	r0 = r0 + r1;
	r1 = -23667*v3;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -21491*v6;
	r1 = -27968*v8;
	r0 = r0 + r1;
	r1 = 25762*v2;
	r2 = -29040*v0;
	r1 = r1 >> 2;
	r1 = r1 + r2;
	r0 = r0 + r1;
	r1 = -25139*v3;
	r2 = 16512*v4;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 31777*v5;
	r2 = -20850*v1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 31450*v7;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 21407*v6;
	r1 = 19307*v2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 24605*v7;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 24531*v4;
	r0 = r0 + r1;
	r1 = -20525*v1;
	r0 = r0 + r1;
	r1 = 22385*v8;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -16899*v5;
	r0 = r0 + r1;
	r1 = 21434*v0;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 21363*v3;
	//r0 = r0 % 8589934592;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -29935*v4;
	r1 = -18620*v8;
	r0 = r0 + r1;
	r1 = 23047*v2;
	r2 = 17178*v3;
	r1 = r1 >> 2;
	r1 = r1 + r2;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	r1 = -24806*v7;
	r2 = 20864*v1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = -32216*v0;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 20493*v6;
	r2 = -18036*v5;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 31153*v7;
	r1 = 19447*v6;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 17386*v0;
	r0 = r0 + r1;
	r1 = -18732*v2;
	r2 = 28781*v4;
	r1 = r1 + r2;
	r2 = -23814*v8;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 31272*v5;
	r2 = 22912*v1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = 26668*v3;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -17206*v4;
	r1 = -26836*v8;
	r0 = r0 + r1;
	r1 = -20447*v0;
	r2 = 24529*v3;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	r1 = 30016*v6;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 26888*v2;
	r2 = 20364*v5;
	r1 = r1 << 1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r2 = 27720*v1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 20805*v7;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = 29639*v8;
	r1 = -17164*v6;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -28894*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -24887*v7;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -27839*v5;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -32768*v3;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -18444*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -20103*v4;
	r0 = r0 + r1;
	r1 = -30965*v2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 26736*v5;
	r1 = 23097*v6;
	r0 = r0 + r1;
	r1 = -26566*v1;
	r0 = r0 + r1;
	r1 = 21224*v0;
	r0 = r0 + r1;
	r1 = 23913*v2;
	r2 = 18750*v4;
	r1 = r1 + r2;
	r2 = 17000*v8;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r2 = -31369*v7;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -29025*v3;
	//r0 = r0 % 8589934592;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 19478*v4;
	r1 = -22589*v6;
	r0 = r0 + r1;
	r1 = 32355*v2;
	r1 = r1 >> 3;
	r0 = r0 + r1;
	r1 = 25377*v3;
	r2 = -23971*v8;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 28533*v5;
	r2 = 17117*v7;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 23086*v1;
	r1 = r1 + r2;
	r2 = 24870*v0;
	r1 = r1 + r2;
	//r0 = r0 % 8589934592;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss5_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -28912*v8;
	r1 = -30810*v2;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = 28971*v4;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 16704*v5;
	r0 = r0 >> 2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -30774*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 23966*v7;
	r0 = r0 + r1;
	r1 = -19267*v6;
	r0 = r0 + r1;
	r1 = -27366*v3;
	r0 = r0 + r1;
	r1 = 19036*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -19573*v6;
	r1 = -16811*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 19615*v1;
	r0 = r0 + r1;
	r1 = 20313*v4;
	r2 = -22853*v8;
	r1 = r1 >> 3;
	r1 = r1 + r2;
	r2 = 22361*v2;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 22395*v5;
	r2 = 23575*v7;
	r1 = r1 << 1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 29989*v3;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -28907*v5;
	r1 = 27705*v8;
	r0 = r0 + r1;
	r1 = -20743*v2;
	r2 = -31430*v6;
	r1 = r1 + r2;
	r2 = 31875*v0;
	r2 = r2 >> 1;
	r1 = r1 + r2;
	r2 = 28418*v4;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 17762*v1;
	r2 = 18388*v7;
	r1 = r1 + r2;
	r2 = 30030*v3;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -32695*v3;
	r1 = -32231*v7;
	r0 = r0 + r1;
	r1 = 19734*v0;
	r2 = -25578*v4;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -20732*v2;
	r2 = -21631*v8;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 28822*v6;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 25616*v1;
	r2 = -32768*v5;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 19039*v2;
	r1 = 22915*v7;
	r0 = r0 + r1;
	r1 = 30527*v6;
	r0 = r0 + r1;
	r1 = 20900*v1;
	r2 = 20968*v5;
	r1 = r1 << 1;
	r2 = r2 << 2;
	r1 = r1 + r2;
	r0 = r0 + r1;
	r1 = 20825*v4;
	r2 = -27773*v8;
	r1 = r1 + r2;
	r2 = 21085*v3;
	r1 = r1 + r2;
	r2 = 22094*v0;
	r1 = r1 >> 1;
	r2 = r2 >> 2;
	r1 = r1 + r2;
	//r1 = r1 % 8589934592;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 19703*v7;
	r1 = -27979*v8;
	r0 = r0 + r1;
	r1 = -31415*v4;
	r0 = r0 + r1;
	r1 = -26652*v0;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -27163*v6;
	r2 = -24610*v1;
	r1 = r1 >> 3;
	r1 = r1 + r2;
	r2 = 32208*v3;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 3;
	r0 = r0 + r1;
	r1 = 17673*v5;
	//r0 = r0 % 8589934592;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 32338*v2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -18523*v4;
	r1 = 24596*v8;
	r0 = r0 + r1;
	r1 = -29078*v0;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -31710*v1;
	r2 = -20131*v3;
	r1 = r1 << 1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -18660*v2;
	r2 = -20174*v7;
	r1 = r1 + r2;
	r2 = -27576*v6;
	r1 = r1 + r2;
	r2 = -31340*v5;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = 26188*v5;
	r1 = 21371*v8;
	r0 = r0 + r1;
	r1 = -21318*v2;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	r1 = -21231*v3;
	r2 = -18533*v7;
	r1 = r1 << 1;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 27719*v4;
	r2 = 21085*v6;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = 26000*v0;
	r2 = r2 << 1;
	r1 = r1 + r2;
	r2 = -19185*v1;
	r1 = r1 + r2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_x8(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1, r2;
	r0 = -25508*v2;
	r1 = 23753*v7;
	r0 = r0 + r1;
	r1 = 20632*v1;
	r0 = r0 + r1;
	r1 = 22598*v0;
	r2 = -18251*v3;
	r1 = r1 + r2;
	r2 = -20368*v4;
	r1 = r1 >> 1;
	r1 = r1 + r2;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = -23380*v6;
	r2 = -17315*v8;
	r1 = r1 + r2;
	r2 = 16718*v5;
	r1 = r1 + r2;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_ss6_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -28912*v8;
	r1 = -23985*v2;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 18811*v4;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = 30636*v7;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -22385*v6;
	r0 = r0 + r1;
	r1 = -16697*v3;
	r0 = r0 + r1;
	r1 = 17598*v0;
	r0 = r0 >> 1;
	r1 = r1 >> 1;
	r0 = r0 + r1;
	r1 = 16623*v5;
	//r0 = r0 % 8589934592;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -30834*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_t1(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -28912*v1;
	r0 = r0 >> 7;
	r1 = 22646*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_t2(int16_t v0)
{
	int32_t r0;
	r0 = 27090*v0; 
	//r0 << 1;
	return r0 >> 15;
}

int16_t C_int_rho_t3(int16_t v0)
{
	int32_t r0;
	r0 = 32416*v0;
	//r0 << 1;
	return r0 >> 15;
}

int16_t C_int_rho_t4(int16_t v0)
{
	int32_t r0;
	r0 = 17262*v0;
	//r0 << 2;
	return r0 >> 14;
}

int16_t C_int_rho_t5(int16_t v0)
{
	int32_t r0;
	r0 = 30040*v0; 
	//r0 << 1;
	return r0 >> 15;
}

int16_t C_int_rho_t6(int16_t v0)
{
	int32_t r0;
	r0 = 29499*v0; 
	//r0 << 1;
	return r0 >> 15;
}

int16_t C_int_rho_t7(int16_t v0)
{
	int32_t r0;
	r0 = 23957*v0; 
	//r0 << 1;
	return r0 >> 15;
}

int16_t C_int_rho_t8(int16_t v0)
{
	int32_t r0;
	r0 = 16968*v0; 
	//r0 << 2;
	return r0 >> 14;
}

int16_t C_int_rho_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1;
	r0 = -20619*v3;
	r0 = r0 >> 1;
	r1 = 17005*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 16384*v1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -28011*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x2(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1;
	r0 = 19839*v2;
	r1 = -32228*v3;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 16384*v1;
	r0 = r0 >> 4;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -28564*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x3(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1;
	r0 = -18532*v2;
	r1 = -25063*v3;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 16384*v1;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -16572*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x4(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1;
	r0 = -16958*v2;
	r1 = -29456*v3;
	r0 = r0 >> 4;
	r0 = r0 + r1;
	r1 = 25536*v0;
	r0 = r0 + r1;
	r1 = 16384*v1;
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x5(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1;
	r0 = 23292*v2;
	r1 = 21738*v3;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 19218*v0;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = 16384*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x6(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1;
	r0 = 24426*v2;
	r1 = 16384*v1;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = 26081*v3;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = 32102*v0;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x7(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{
	int32_t r0, r1, r2;
	r0 = 31941*v3;
	r1 = 16384*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = 27472*v2;
	r2 = -26118*v0;
	r1 = r1 >> 2;
	r1 = r1 + r2;
	r1 = r1 >> 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_x8(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 27509*v1;
	r1 = -29988*v2;
	r0 = r0 >> 3;
	r0 = r0 + r1;
	r1 = -20621*v0;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_rho_y(int16_t v0)
{	return v0;	}

int16_t C_int_LGS_t2(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -29486*v0;
	r1 = 16384*v1;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t10(int16_t v0)
{
	int32_t r0;
	r0 = 27252*v0;
	return r0 >> 14; //(10,-5)
}

int16_t C_int_LGS_t19(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -16434*v0;
	r1 = 32768*v1;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t27(int16_t v0)
{
	int32_t r0;
	r0 = 27099*v0;
	return r0 >> 14; //doute (10,-5)
}

int16_t C_int_LGS_t36(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -25080*v0;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(10,-5)
}

int16_t C_int_LGS_t44(int16_t v0)
{
	int32_t r0;
	r0 = 29228*v0;
	return r0 >> 15; //(10,-5)
}

int16_t C_int_LGS_t53(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -25729*v0;
	r1 = 32768*v1;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t61(int16_t v0)
{
	int32_t r0;
	r0 = 21142*v0;
	return r0 >> 14; // (10,-5)
}

int16_t C_int_LGS_t70(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = -22159*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t78(int16_t v0)
{
	int32_t r0;
	r0 = 30061*v0; 	
	return r0 >> 15; //(10,-5)
}

int16_t C_int_LGS_t87(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = -16872*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16; //(11,-4)
}

int16_t C_int_LGS_t95(int16_t v0)
{
    int32_t r0;
	r0 = 22249*v0; 	
	return r0 >> 14; //(9,-6)
}

int16_t C_int_LGS_t104(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = -17760*v0;
	r0 = r0 >> 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16; //(12,-3)
}

int16_t C_int_LGS_t112(int16_t v0)
{
	int32_t r0;
	r0 = 17785*v0;
	return r0 >> 14; //(8,-7)
}

int16_t C_int_LGS_t119(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 32768*v0;
	r1 = 24117*v1;
	r0 = r0 << 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(9,-6)
}

int16_t C_int_LGS_t126(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 30955*v1;
	r1 = 32768*v0;
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;//(9,-6)
} 

int16_t C_int_LGS_t133(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 28593*v1;
	r1 = 32768*v0;
	r0 = r0 << 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;//(9,-6)
}

int16_t C_int_LGS_t140(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 22950*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t147(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 20741*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t154(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 27335*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t161(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 29486*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;//(10,-5)
}

int16_t C_int_LGS_t169(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 29486*v1;
	r1 = 32768*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t170(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = 16434*v2;
	r0 = r0 << 1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -29486*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t171(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 25080*v2;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -16434*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t172(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 25729*v2;
	r1 = 32768*v1;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -25080*v0;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t173(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = 22159*v2;
	r1 = r1 << 1;
	r0 = r0 + r1;
	r1 = -25729*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t174(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = 16872*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -22159*v0;
	r1 = r1 << 1;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t175(int16_t v0,int16_t v1,int16_t v2)
{
	int32_t r0, r1;
	r0 = 32768*v1;
	r1 = 17760*v2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	r1 = -16872*v0;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_t176(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = -26038*v1;
	r1 = -17760*v0;
	r0 = r0 << 2;
	r1 = r1 << 3;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x1(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 19478*v1;
	r1 = 16384*v0;
	r0 = r0 >> 6;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x2(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 21647*v1;
	r1 = 16384*v0;
	r0 = r0 >> 5;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x3(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 25949*v1;
	r1 = 16384*v0;
	r0 = r0 >> 4;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x4(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 20498*v1;
	r1 = 16384*v0;
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x5(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 29267*v1;
	r1 = 16384*v0;
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x6(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 16770*v1;
	r1 = 16384*v0;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x7(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 17752*v1;
	r1 = 16384*v0;
	r0 = r0 >> 1;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_x8(int16_t v0,int16_t v1)
{
	int32_t r0, r1;
	r0 = 24120*v1;
	r1 = 16384*v0;
	r0 = r0 >> 2;
	r1 = r1 << 2;
	r0 = r0 + r1;
	return r0 >> 16;
}

int16_t C_int_LGS_y(int16_t v0,int16_t v1,int16_t v2,int16_t v3,int16_t v4,int16_t v5,int16_t v6,int16_t v7,int16_t v8)
{
	int32_t r0, r1;
	r0 = -28912*v8;
	r1 = -31532*v4;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -17495*v3;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -27570*v7;
	r0 = r0 >> 2;
	r0 = r0 + r1;
	r1 = -26756*v5;
	r0 = r0 + r1;
	r1 = 17824*v0;
	r0 = r0 + r1;
	r1 = -20649*v6;
	r0 = r0 >> 1;
	r0 = r0 + r1;
	r1 = -23723*v2;
	r0 = r0 + r1;
	r1 = -24658*v1;
	r0 = r0 + r1;
	return r0 >> 16;
}

double Dt2(double v0,double v1)
{	return -0.449920654296875 * v0 + v1;	}

double Dt10(double v0)
{	return 0.8316650390625 * v0;	}

double Dt19(double v0,double v1)
{	return -0.50152587890625 * v0 + v1;	}

double Dt27(double v0)
{	return 0.826995849609375 * v0;	}

double Dt36(double v0,double v1)
{	return -0.3826904296875 * v0 + v1;	}

double Dt44(double v0)
{	return 0.8919677734375 * v0;	}

double Dt53(double v0,double v1)
{	return -0.785186767578125 * v0 + v1;	}

double Dt61(double v0)
{	return 0.64520263671875 * v0;	}

double Dt70(double v0,double v1)
{	return v1 - 1.35247802734375 * v0;	}

double Dt78(double v0)
{	return 0.4586944580078125 * v0;	}

double Dt87(double v0,double v1)
{	return v1 - 2.0595703125 * v0;	}

double Dt95(double v0)
{	return 0.3394927978515625 * v0;	}

double Dt104(double v0,double v1)
{	return v1 - 4.3359375 * v0;	}

double Dt112(double v0)
{	return 0.067844390869140625 * v0;	}

double Dt119(double v0,double v1)
{	return v0 + 1.47198486328125 * v1;	}

double Dt126(double v0,double v1)
{	return 0.944671630859375 * v1 + v0;	}

double Dt133(double v0,double v1)
{	return 0.872589111328125 * v1 + v0;	}

double Dt140(double v0,double v1)
{	return 0.70037841796875 * v1 + v0;	}

double Dt147(double v0,double v1)
{	return 0.3164825439453125 * v1 + v0;	}

double Dt154(double v0,double v1)
{	return 0.4170989990234375 * v1 + v0;	}

double Dt161(double v0,double v1)
{	return 0.449920654296875 * v1 + v0;	}

double Dt169(double v0,double v1)
{	return 0.449920654296875 * v1 + v0;	}

double Dt170(double v0,double v1,double v2)
{	return v1 + 0.50152587890625 * v2 - 0.449920654296875 * v0;	}

double Dt171(double v0,double v1,double v2)
{	return 0.3826904296875 * v2 + v1 - 0.50152587890625 * v0;	}

double Dt172(double v0,double v1,double v2)
{	return 0.785186767578125 * v2 + v1 - 0.3826904296875 * v0;	}

double Dt173(double v0,double v1,double v2)
{	return v1 + 1.35247802734375 * v2 - 0.785186767578125 * v0;	}

double Dt174(double v0,double v1,double v2)
{	return v1 + 2.0595703125 * v2 - 1.35247802734375 * v0;	}

double Dt175(double v0,double v1,double v2)
{	return v1 + 4.3359375 * v2 - 2.0595703125 * v0;	}

double Dt176(double v0,double v1)
{	return -6.35693359375 * v1 - 4.3359375 * v0;	}

double DLx1f(double v0,double v1)
{	return 0.0185756683349609375 * v1 + 1 * v0;	}

double DLx2f(double v0,double v1)
{	return 0.0412883758544921875 * v1 + 1 * v0;	}

double DLx3f(double v0,double v1)
{	return 0.098987579345703125 * v1 + 1 * v0;	}

double DLx4f(double v0,double v1)
{	return 0.312774658203125 * v1 + 1 * v0;	}

double DLx5f(double v0,double v1)
{	return 0.4465789794921875 * v1 + 1 * v0;	}

double DLx6f(double v0,double v1)
{	return 0.51177978515625 * v1 + 1 * v0;	}

double DLx7f(double v0,double v1)
{	return 0.541748046875 * v1 + 1 * v0;	}

double DLx8f(double v0,double v1)
{	return 0.3680419921875 * v1 + 1 * v0;	}

double DLyf(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8)
{	return -0.11029052734375 * v8 + -0.1202850341796875 * v4 + -0.2669525146484375 * v3 + -1.6827392578125 * v7 + -1.633056640625 * v5 + 1.087890625 * v0 + -2.5206298828125 * v6 + -2.8958740234375 * v2 + -3.010009765625 * v1;	}



double impulse()
{
	double X=( rand()/(double)RAND_MAX ) * (399) -237;
	return X*powf(2,7);
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
		DFIu1 = 0, DFIu2 = 0, DFIu3 = 0, DFIu4 = 0, DFIu5 = 0, DFIu6 = 0, DFIu7 = 0, DFIu8 = 0, 
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
		xL1 = 0, xL2 = 0, xL3 = 0, xL4 = 0, xL5 = 0, xL6 = 0, xL7 = 0, xL8 = 0, yL=0;

	double Du = imp*powf(2,-7),
		Dx1 = 0, Dx2 = 0, Dx3 = 0, Dx4 = 0, Dx5 = 0, Dx6 = 0, Dx7 = 0, Dx8 = 0, Dy = 0,
		Dxp1 = 0, Dxp2 = 0, Dxp3 = 0, Dxp4 = 0, Dxp5 = 0, Dxp6 = 0, Dxp7 = 0, Dxp8 = 0,
		DLx1 = 0, DLx2 = 0, DLx3 = 0, DLx4 = 0, DLx5 = 0, DLx6 = 0, DLx7 = 0, DLx8 = 0, DLy = 0,
		DLxp1 = 0, DLxp2 = 0, DLxp3 = 0, DLxp4 = 0, DLxp5 = 0, DLxp6 = 0, DLxp7 = 0, DLxp8 = 0,
		DtpL2 = 0, DtpL10 = 0, DtpL19 = 0, DtpL27 = 0, DtpL36 = 0, DtpL44 = 0, DtpL53 = 0, DtpL61 = 0,
		DtpL70 = 0, DtpL78 = 0, DtpL87 = 0, DtpL95 = 0, DtpL104 = 0, DtpL112 = 0, DtpL119 = 0, DtpL126 = 0,
		DtpL133 = 0, DtpL140 = 0, DtpL147 = 0, DtpL154 = 0, DtpL161 = 0,
		DtpL169 = 0, DtpL170 = 0, DtpL171 = 0, DtpL172 = 0, DtpL173 = 0, DtpL174 = 0, DtpL175 = 0, DtpL176 = 0,
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
	while(cpt<100000){


		DFIy = C_int_DFI(u,DFIu1,DFIu2,DFIu3,DFIu4,DFIu5,DFIu6,DFIu7,DFIu8, DFIy1,DFIy2,DFIy3,DFIy4,DFIy5,DFIy6,DFIy7,DFIy8);
		DFIu8 = DFIu7; DFIu7 = DFIu6; DFIu6 = DFIu5; DFIu5 = DFIu4; DFIu4 = DFIu3; DFIu3 = DFIu2; DFIu2 = DFIu1; DFIu1=u;
		DFIy8 = DFIy7; DFIy7 = DFIy6; DFIy6 = DFIy5; DFIy5 = DFIy4; DFIy4 = DFIy3; DFIy3 = DFIy2; DFIy2 = DFIy1; DFIy1=DFIy;

		xp11 = C_int_ss1_x1(x11, x12, x13, x14, x15, x16, x17, x18,u);
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

		
		/*tpL1 = xL1; tpL2 = C_int_LGS_t2(xL1,xL2); tpL3 = xL3; tpL4 = xL4; tpL5 = xL5; tpL6 = xL6; tpL7 = xL7; tpL8 = xL8;
		tpL9 = -tpL1; tpL10 = C_int_LGS_t10(tpL2); tpL11 = -tpL3; tpL12 = -tpL4; tpL13 = -tpL5; tpL14 = -tpL6; tpL15 = -tpL7; tpL16 = -tpL8;
		tpL17 = -tpL9; tpL18 = -tpL10; tpL19 = C_int_LGS_t19(tpL10,tpL11); tpL20 = -tpL12; tpL21 = -tpL13; tpL22 = -tpL14; tpL23 = -tpL15; tpL24 = -tpL16;
		tpL25 = -tpL17; tpL26 = -tpL18; tpL27 = C_int_LGS_t27(tpL19); tpL28 = -tpL20; tpL29 = -tpL21; tpL30 = -tpL22; tpL31 = -tpL23; tpL32 = -tpL24;
		tpL33 = -tpL25; tpL34 = -tpL26; tpL35 = -tpL27; tpL36 = C_int_LGS_t36(tpL27,tpL28); tpL37 = -tpL29; tpL38 = -tpL30; tpL39 = -tpL31; tpL40 = -tpL32;
		tpL41 = -tpL33; tpL42 = -tpL34; tpL43 = -tpL35; tpL44 = C_int_LGS_t44(tpL36); tpL45 = -tpL37; tpL46 = -tpL38; tpL47 = -tpL39; tpL48 = -tpL40;
		tpL49 = -tpL41; tpL50 = -tpL42; tpL51 = -tpL43; tpL52 = -tpL44; tpL53 = C_int_LGS_t53(tpL44,tpL45); tpL54 = -tpL46; tpL55 = -tpL47; tpL56 = -tpL48;
		tpL57 = -tpL49; tpL58 = -tpL50; tpL59 = -tpL51; tpL60 = -tpL52; tpL61 = C_int_LGS_t61(tpL53); tpL62 = -tpL54; tpL63 = -tpL55; tpL64 = -tpL56;
		tpL65 = -tpL57; tpL66 = -tpL58; tpL67 = -tpL59; tpL68 = -tpL60; tpL69 = -tpL61; tpL70 = C_int_LGS_t70(tpL61,tpL62); tpL71 = -tpL63; tpL72 = -tpL64;
		tpL73 = -tpL65; tpL74 = -tpL66; tpL75 = -tpL67; tpL76 = -tpL68; tpL77 = -tpL69; tpL78 = C_int_LGS_t78(tpL70); tpL79 = -tpL71; tpL80 = -tpL72;
		tpL81 = -tpL73; tpL82 = -tpL74; tpL88 = -tpL75; tpL84 = -tpL76; tpL85 = -tpL77; tpL86 = -tpL78; tpL87 = C_int_LGS_t87(tpL78,tpL79); tpL88 = -tpL80;
		tpL89 = -tpL81; tpL90 = -tpL82; tpL91 = -tpL83; tpL92 = -tpL84; tpL93 = -tpL85; tpL94 = -tpL86; tpL95 = C_int_LGS_t95(tpL87); tpL96 = -tpL88;
		tpL97 = -tpL89; tpL98 = -tpL90; tpL99 = -tpL91; tpL100 = -tpL92; tpL101 = -tpL93; tpL102 = -tpL94; tpL103 = -tpL95; tpL104 = C_int_LGS_t104(tpL95,tpL96);
		tpL105 = -tpL97; tpL106 = -tpL98; tpL107 = -tpL99; tpL108 = -tpL100; tpL109 = -tpL101; tpL110 = -tpL102; tpL111 = -tpL103; tpL112 = C_int_LGS_t112(tpL104);
		tpL113 = -tpL105; tpL114 = -tpL106; tpL115 = -tpL107; tpL116 = -tpL108; tpL117 = -tpL109; tpL118 = -tpL110; tpL119 = C_int_LGS_t119(tpL111,tpL112); tpL120 = -tpL112;
		tpL121 = -tpL113; tpL122 = -tpL114; tpL123 = -tpL115; tpL124 = -tpL116; tpL125 = -tpL117; tpL126 = C_int_LGS_t126(tpL118, tpL119); tpL127 = -tpL119; tpL128 = -tpL120;
		tpL129 = -tpL121; tpL130 = -tpL122; tpL131 = -tpL123; tpL132 = -tpL124; tpL133 = C_int_LGS_t133(tpL125, tpL126); tpL134 = -tpL126; tpL135 = -tpL127; tpL136 = -tpL128;
		tpL137 = -tpL129; tpL138 = -tpL130; tpL139 = -tpL131; tpL140 = C_int_LGS_t140(tpL132, tpL133); tpL141 = -tpL133; tpL142 = -tpL134; tpL143 = -tpL135; tpL144 = -tpL136;
		tpL145 = -tpL137; tpL146 = -tpL138; tpL147 = C_int_LGS_t147(tpL139, tpL140); tpL148 = -tpL140; tpL149 = -tpL141; tpL150 = -tpL142; tpL151 = -tpL143; tpL152 = -tpL144;
		tpL153 = -tpL145; tpL154 = C_int_LGS_t154(tpL146, tpL147); tpL155 = -tpL147; tpL156 = -tpL148; tpL157 = -tpL149; tpL158 = -tpL150; tpL159 = -tpL151; tpL160 = -tpL152;
		tpL161 = C_int_LGS_t161(tpL153, tpL154); tpL162 = -tpL154; tpL163 = -tpL155; tpL164 = -tpL156; tpL165 = -tpL157; tpL166 = -tpL158; tpL167 = -tpL159; tpL168 = -tpL160;
		tpL169 = C_int_LGS_t169(tpL161,tpL162); tpL170 = C_int_LGS_t170(tpL161,tpL162,tpL163); tpL171 = C_int_LGS_t171(tpL162,tpL163,tpL164); tpL172 = C_int_LGS_t172(tpL163,tpL164,tpL165);
		tpL173 = C_int_LGS_t173(tpL164,tpL165,tpL166); tpL174 = C_int_LGS_t174(tpL165,tpL166,tpL167); tpL175 = C_int_LGS_t175(tpL166,tpL167,tpL168); tpL176 = C_int_LGS_t176(tpL167,tpL168);*/
		

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
		DLx1 = DLxp1; DLx2 = DLxp2; DLx3 = DLxp3; DLx4 = DLxp4; DLx5 = DLxp5; DLx6 = DLxp6; DLx7 = DLxp7; DLx8 = DLxp8; 



		Dxp1 = double_x1(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp2 = double_x2(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp3 = double_x3(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp4 = double_x4(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp5 = double_x5(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp6 = double_x6(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp7 = double_x7(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dxp8 = double_x8(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dy = double_y(Dx1, Dx2, Dx3, Dx4, Dx5, Dx6, Dx7, Dx8, Du);
		Dx1 = Dxp1; Dx2 = Dxp2; Dx3 = Dxp3; Dx4 = Dxp4; Dx5 = Dxp5; Dx6 = Dxp6; Dx7 = Dxp7; Dx8 = Dxp8;

		if(y1*powf(2,-2)-Dy >maxEy1) maxEy1=y1*powf(2,-2)-Dy;
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
		if(yL*powf(2,-2)-Dy<minEyL) minEyL=yL*powf(2,-2)-Dy;
		if(DFIy*powf(2,-2)-Dy >maxEyDFI) maxEyDFI=DFIy*powf(2,-2)-Dy;
		if(DFIy*powf(2,-2)-Dy<minEyDFI) minEyDFI=DFIy*powf(2,-2)-Dy;

		if(Dy >maxy) maxy=Dy;
		if(Dy<miny) miny=Dy;
		
		//printf("%d %g %g %g %g %g %g %g %g %g %g\n",cpt, imp*powf(2,-2), y1*powf(2,-2)-Dy, y2*powf(2,-2)-Dy, y3*powf(2,-2)-Dy, y4*powf(2,-2)-Dy, y5*powf(2,-2)-Dy, y6*powf(2,-2)-Dy, yR*powf(2,-2)-Dy, yL*powf(2,-2)-DLy, DFIy*powf(2,-2)-Dy);

		//printf("%d %g %g %g %g %g \n",cpt, Dy, (int32_t)y3*powf(2,-2), yR*powf(2,-2), yL*powf(2,-2), DFIy*powf(2,-2));

		//printf("%d %g \n",cpt, yL*powf(2,-2)-DLy);
		cpt++;
		imp = impulse(cpt);
		u = (int16_t) imp;
		Du =imp*powf(2,-7);
  	}
  	//printf(" %g ; %g\n", minDy,maxDy);
  	printf(" %g ; %g", miny,maxy);
  	printf("dSS1 = [ %.6g ; %.6g ]\n", minEy1, maxEy1);
	printf("dSS2 = [ %.6g ; %.6g ]\n", minEy2, maxEy2);
	printf("dSS3 = [ %.6g ; %.6g ]\n", minEy3, maxEy3);
	printf("dSS4 = [ %.6g ; %.6g ]\n", minEy4, maxEy4);
	printf("dSS5 = [ %.6g ; %.6g ]\n", minEy5, maxEy5);
	printf("dSS6 = [ %.6g ; %.6g ]\n", minEy6, maxEy6);
	printf("dSSL = [ %.6g ; %.6g ]\n", minEyL, maxEyL);
	printf("dSSR = [ %.6g ; %.6g ]\n", minEyR, maxEyR);
	printf("dSSDFI = [ %.6g ; %.6g ]\n", minEyDFI, maxEyDFI);
  return 0;
}

