#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include "ac_fixed.h"

using namespace std;

double double_t1(double v0,double v1)
{
    double r;
    r = 5.528835296630859375 * v0 + -0.11029052734375 * v1;
	return r; 
}

double double_t2(double v0)
{
    double r;
    r = 0.826725006103515625 * v0;
	return r; 
}

double double_t3(double v0)
{
    double r;
    r = 0.9892597198486328125 * v0;
	return r; 
}

double double_t4(double v0)
{
    double r;
    r = 0.52680206298828125 * v0;
	return r; 
}

double double_t5(double v0)
{
    double r;
    r = 0.91674041748046875 * v0;
	return r; 
}

double double_t6(double v0)
{
    double r;
    r = 0.450115203857421875 * v0;
	return r; 
}

double double_t7(double v0)
{
    double r;
    r = 0.0913848876953125 * v0;
	return r; 
}

double double_t8(double v0)
{
    double r;
    r = 0.2589111328125 * v0;
	return r; 
}

double double_x1(double v0,double v1,double v2,double v3)
{
    double r;
    r = 1 * v1 + 1.037916660308837890625 * v2 + -0.21370983123779296875 * v0 + -0.6292400360107421875 * v3;
	return r; 
}

double double_x2(double v0,double v1,double v2,double v3)
{
    double r;
    r = 0.009459972381591796875 * v2 + 1 * v1 + -0.054480850696563720703125 * v0 + -0.1229400634765625 * v3;
	return r; 
}

double double_x3(double v0,double v1,double v2,double v3)
{
    double r;
    r = -0.764850616455078125 * v3 + -0.035347461700439453125 * v2 + -0.063218891620635986328125 * v0 + 1 * v1;
	return r; 
}

double double_x4(double v0,double v1,double v2,double v3)
{
    double r;
    r = -0.449459075927734375 * v3 + -0.004043102264404296875 * v2 + 0.01217663288116455078125 * v0 + 1 * v1;
	return r; 
}

double double_x5(double v0,double v1,double v2,double v3)
{
    double r;
    r = 0.6634063720703125 * v3 + 0.04442596435546875 * v2 + 0.1466238498687744140625 * v0 + 1 * v1;
	return r; 
}

double double_x6(double v0,double v1,double v2,double v3)
{
    double r;
    r = 0.795928955078125 * v3 + 0.023296356201171875 * v2 + 0.12245845794677734375 * v0 + 1 * v1;
	return r; 
}

double double_x7(double v0,double v1,double v2,double v3)
{
    double r;
    r = 0.9747314453125 * v3 + 0.02618408203125 * v2 + -0.0062255859375 * v0 + 1 * v1;
	return r; 
}

double double_x8(double v0,double v1,double v2)
{
    double r;
    r = -0.9150390625 * v2 + 0.0262451171875 * v1 + -0.0786590576171875 * v0;
	return r; 
}

double double_y(double v0)
{
    double r;
    r = 1 * v0;
	return r; 
}


ac_fixed<16,14,true> code_fixed_DFI(ac_fixed<16,9,true,AC_TRN> v0,ac_fixed<16,9,true,AC_TRN> v1,ac_fixed<16,9,true,AC_TRN> v2,ac_fixed<16,9,true,AC_TRN> v3,ac_fixed<16,9,true,AC_TRN> v4,ac_fixed<16,9,true,AC_TRN> v5,ac_fixed<16,9,true,AC_TRN> v6,ac_fixed<16,9,true,AC_TRN> v7,ac_fixed<16,9,true,AC_TRN> v8,ac_fixed<16,14,true,AC_TRN> v9,ac_fixed<16,14,true,AC_TRN> v10,ac_fixed<16,14,true,AC_TRN> v11,ac_fixed<16,14,true,AC_TRN> v12,ac_fixed<16,14,true,AC_TRN> v13,ac_fixed<16,14,true,AC_TRN> v14,ac_fixed<16,14,true,AC_TRN> v15,ac_fixed<16,14,true,AC_TRN> v16)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<16,14,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<14,-2,true,AC_TRN> c0 = -0.11029052734375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<19,3,true,AC_TRN> c1 = -3.3545379638671875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<16,0,true,AC_TRN> c2 = -0.258544921875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,3,true,AC_TRN> c3 = -3.417938232421875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<17,1,true,AC_TRN> c4 = -0.66973876953125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<18,2,true,AC_TRN> c5 = 1.5607452392578125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<17,1,true,AC_TRN> c6 = 0.667266845703125;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<13,-3,true,AC_TRN> c7 = 0.049407958984375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<12,-4,true,AC_TRN> c8 = -0.0230712890625;
	sd = sd + c8*v8;
	//Computation of c9*v9 in sd
	ac_fixed<18,-3,true,AC_TRN> c9 = -0.053426265716552734375;
	sd = sd + c9*v9;
	//Computation of c10*v10 in sd
	ac_fixed<20,-1,true,AC_TRN> c10 = -0.2375087738037109375;
	sd = sd + c10*v10;
	//Computation of c11*v11 in sd
	ac_fixed<21,0,true,AC_TRN> c11 = -0.26603794097900390625;
	sd = sd + c11*v11;
	//Computation of c12*v12 in sd
	ac_fixed<18,-3,true,AC_TRN> c12 = 0.06201839447021484375;
	sd = sd + c12*v12;
	//Computation of c13*v13 in sd
	ac_fixed<21,0,true,AC_TRN> c13 = 0.315310955047607421875;
	sd = sd + c13*v13;
	//Computation of c14*v14 in sd
	ac_fixed<19,-2,true,AC_TRN> c14 = 0.09629726409912109375;
	sd = sd + c14*v14;
	//Computation of c15*v15 in sd
	ac_fixed<15,-6,true,AC_TRN> c15 = -0.006262302398681640625;
	sd = sd + c15*v15;
	//Computation of c16*v16 in sd
	ac_fixed<13,-8,true,AC_TRN> c16 = -0.001737117767333984375;
	sd = sd + c16*v16;

	//Computation of the final right shift
	s = s + sd;
	return s;
}



ac_fixed<20,14,true> code_fixed_t1(ac_fixed<19,11,true> v0, ac_fixed<18,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<20,14,true> s = 0;
	//Computation of c0*v0 in register r0
	ac_fixed<22,4,true> c0 = 5.528835296630859375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in register r1
	ac_fixed<14,-2,true> c1 = -0.11029052734375;
	sd = sd + c1*v1;
	s=s+sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_t2(ac_fixed<19,11,true> v0)
{ 	
	//Computation of c0*v0 in register r0
	ac_fixed<20,1,true> c0 = 0.826725006103515625;
	ac_fixed<19,11,true> r0 = c0*v0;
	return r0;
}

ac_fixed<19,11,true> code_fixed_t3(ac_fixed<19,11,true> v0)
{   
	//Computation of c0*v0 in register r0
	ac_fixed<20,1,true> c0 = 0.9892597198486328125;
	ac_fixed<19,11,true> r0 = c0*v0;
	return r0;
}

ac_fixed<18,10,true> code_fixed_t4(ac_fixed<19,11,true> v0)
{
	//Computation of c0*v0 in register r0
	ac_fixed<20,1,true> c0 = 0.52680206298828125;
	ac_fixed<18,10,true> r0 = c0*v0;
	return r0;
}

ac_fixed<18,11,true> code_fixed_t5(ac_fixed<18,11,true> v0)
{
	//Computation of c0*v0 in register r0
	ac_fixed<19,1,true> c0 = 0.91674041748046875;
	ac_fixed<18,11,true> r0 = c0*v0;
	return r0;
}

ac_fixed<17,10,true> code_fixed_t6(ac_fixed<16,11,true> v0)
{
	//Computation of c0*v0 in register r0
	ac_fixed<18,0,true> c0 = 0.450115203857421875;
	ac_fixed<17,10,true> r0 = c0*v0;
	return r0;
}

ac_fixed<13,7,true> code_fixed_t7(ac_fixed<12,10,true> v0)
{
	//Computation of c0*v0 in register r0
	ac_fixed<14,-2,true> c0 = 0.0913848876953125;
	ac_fixed<13,7,true> r0 = c0*v0;
	return r0;
}

ac_fixed<11,9,true> code_fixed_t8(ac_fixed<11,11,true> v0)
{
	//Computation of c0*v0 in register r0
	ac_fixed<13,0,true> c0 = 0.2589111328125;
	ac_fixed<11,9,true> r0 = c0*v0;
	return r0;
}

ac_fixed<19,11,true> code_fixed_x1(ac_fixed<20,14,true> v0, ac_fixed<19,11,true> v1,
	ac_fixed<19,11,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<23,2,true> c1 = 1;
	sd = sd + c1*v1;
	//Computation of c2*v2 in register r1
	ac_fixed<23,2,true> c2 = 1.037916660308837890625;
	sd = sd + c2*v2;
	//Computation of r0+r1 in register r2
	//Computation of c0*v0 in register r3
	ac_fixed<23,-1,true> c0 = -0.21370983123779296875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in register r4
	ac_fixed<20,1,true> c3 = -0.6292400360107421875;
	sd = sd + c3*v3;
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_x2(ac_fixed<20,14,true> v0, ac_fixed<19,11,true> v1,
	ac_fixed<19,11,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;
	ac_fixed<16,-5,true> c2 = 0.009459972381591796875;
	sd = sd + c2*v2;
	ac_fixed<23,2,true> c1 = 1;
	sd = sd + c1*v1;
	ac_fixed<21,-3,true> c0 = -0.054480850696563720703125;
	sd = sd + c0*v0;
	ac_fixed<17,-2,true> c3 = -0.1229400634765625;
	sd = sd + c3*v3;
	s=s+sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_x3(ac_fixed<20,14,true> v0, ac_fixed<18,10,true> v1,
	ac_fixed<19,11,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<20,1,true> c3 = -0.764850616455078125;
	sd = sd + c3*v3;
	//Computation of c2*v2 in register r1
	ac_fixed<18,-3,true> c2 = -0.035347461700439453125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in register r3
	ac_fixed<22,-2,true> c0 = -0.063218891620635986328125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in register r4
	ac_fixed<22,2,true> c1 = 1;
	sd = sd + c1*v1;
	s=s+sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_x4(ac_fixed<20,14,true> v0, ac_fixed<18,11,true> v1,
	ac_fixed<19,11,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<19,0,true> c3 = -0.449459075927734375;
	sd = sd + c3*v3;
	//Computation of c2*v2 in register r1
	ac_fixed<15,-6,true> c2 = -0.004043102264404296875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in register r3
	ac_fixed<19,-5,true> c0 = 0.01217663288116455078125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in register r4
	ac_fixed<23,2,true> c1 = 1;
	sd = sd + c1*v1;
	s=s+sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_x5(ac_fixed<20,14,true> v0, ac_fixed<17,10,true> v1,
	ac_fixed<18,11,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<19,1,true> c3 = 0.6634063720703125;
	sd = sd + c3*v3;
	//Computation of c2*v2 in register r1
	ac_fixed<17,-3,true> c2 = 0.04442596435546875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in register r3
	ac_fixed<22,-1,true> c0 = 0.1466238498687744140625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in register r4
	ac_fixed<21,2,true> c1 = 1;
	sd = sd + c1*v1;
	s=s+sd;
	return s;
}

ac_fixed<16,11,true> code_fixed_x6(ac_fixed<20,14,true> v0, ac_fixed<13,7,true> v1,
	ac_fixed<16,11,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<16,11,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<17,1,true> c3 = 0.795928955078125;
	sd = sd + c3*v3;
	//Computation of c2*v2 in register r1
	ac_fixed<14,-4,true> c2 = 0.023296356201171875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in register r3
	ac_fixed<19,-2,true> c0 = 0.12245845794677734375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in register r4
	ac_fixed<16,2,true> c1 = 1;
	sd = sd + c1*v1;
	s=s+sd;
	return s;
}

ac_fixed<12,10,true> code_fixed_x7(ac_fixed<20,14,true> v0, ac_fixed<11,9,true> v1,
	ac_fixed<12,10,true> v2, ac_fixed<18,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<14,10,true> sd = 0;
	ac_fixed<12,10,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<14,1,true> c3 = 0.9747314453125;
	sd = sd + c3*v3;
	//Computation of c2*v2 in register r1
	ac_fixed<10,-4,true> c2 = 0.02618408203125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in register r3
	ac_fixed<12,-6,true> c0 = -0.0062255859375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in register r4
	ac_fixed<15,2,true> c1 = 1;
	sd = sd + c1*v1;
	s=s+sd;
	return s;
}

ac_fixed<11,11,true> code_fixed_x8(ac_fixed<20,14,true> v0, ac_fixed<11,11,true> v1,
	ac_fixed<18,9,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<13,11,true> sd = 0;
	ac_fixed<11,11,true> s = 0;
	//Computation of c1*v1 in register r0
	ac_fixed<12,1,true> c2 = -0.9150390625;
	sd = sd + c2*v2;
	//Computation of c2*v2 in register r1
	ac_fixed<9,-4,true> c1 = 0.0262451171875;
	sd = sd + c1*v1;
	//Computation of c0*v0 in register r3
	ac_fixed<14,-2,true> c0 = -0.0786590576171875;
	sd = sd + c0*v0;
	s=s+sd;
	return s;
}


ac_fixed<21,12,true> code_fixed_ss2_x1(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3,	ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<27,3,true> c5 = 3.93980872631072998046875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,1,true> c6 = 0.92621038854122161865234375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<27,2,true> c0 = 1.4366941750049591064453125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<27,1,true> c3 = -0.60798163712024688720703125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<25,3,true> c8 = -2.113919734954833984375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<27,2,true> c4 = 1.8654798567295074462890625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<26,2,true> c7 = 1.31116139888763427734375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,0,true> c2 = 0.3603222668170928955078125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<25,0,true> c1 = -0.440654933452606201171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_ss2_x2(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<27,3,true> c5 = -2.9270560741424560546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,1,true> c6 = -0.8302190303802490234375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<27,2,true> c0 = -1.318378984928131103515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,0,true> c3 = 0.3660008609294891357421875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<25,3,true> c8 = 2.3274757862091064453125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<27,2,true> c4 = -1.264290332794189453125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,1,true> c7 = -0.882656753063201904296875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<22,-4,true> c2 = -0.02176861464977264404296875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<25,0,true> c1 = -0.42246568202972412109375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,13,true> code_fixed_ss2_x3(ac_fixed<21,12,true> v0, 
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,13,true> sd = 0;
	ac_fixed<20,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<26,4,true> c5 = -7.1567547321319580078125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,3,true> c6 = -2.853803455829620361328125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<27,4,true> c0 = -4.093217372894287109375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,2,true> c3 = -1.105220794677734375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,3,true> c8 = 3.17626094818115234375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,3,true> c4 = -3.8396055698394775390625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,3,true> c7 = -2.7725617885589599609375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,2,true> c2 = -1.403257548809051513671875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<26,3,true> c1 = -2.2713954448699951171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<22,13,true> code_fixed_ss2_x4(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<26,13,true> sd = 0;
	ac_fixed<22,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<28,4,true> c5 = 7.6138370037078857421875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<29,3,true> c6 = 3.9915024340152740478515625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<29,4,true> c0 = 4.605542838573455810546875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<28,2,true> c3 = 1.8029229640960693359375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<26,4,true> c8 = -4.2833006381988525390625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<29,4,true> c4 = 4.21262657642364501953125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<27,3,true> c7 = 3.0655066967010498046875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<28,2,true> c2 = 1.09973002970218658447265625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<28,3,true> c1 = 3.45780098438262939453125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_ss2_x5(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<28,4,true> c5 = 4.8687078952789306640625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,2,true> c6 = 1.8188438713550567626953125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<28,3,true> c0 = 2.5286175906658172607421875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<27,1,true> c3 = 0.75814153254032135009765625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<25,3,true> c8 = -2.3170688152313232421875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<28,3,true> c4 = 2.379960477352142333984375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<26,2,true> c7 = 1.564164221286773681640625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<28,2,true> c2 = 1.30833549797534942626953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<27,2,true> c1 = 1.0229103565216064453125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_ss2_x6(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<26,2,true> c5 = -1.553825438022613525390625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,1,true> c6 = -0.9819056689739227294921875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<26,1,true> c0 = -0.7322327196598052978515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<27,1,true> c3 = -0.56156308948993682861328125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true> c8 = 0.751278400421142578125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,1,true> c4 = -0.9392834007740020751953125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true> c7 = -0.423393428325653076171875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<27,1,true> c2 = -0.64628143608570098876953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<23,-2,true> c1 = -0.12047290802001953125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<22,13,true> code_fixed_ss2_x7(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<26,13,true> sd = 0;
	ac_fixed<22,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<28,4,true> c5 = -6.086655557155609130859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<29,3,true> c6 = -2.87255020439624786376953125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<28,3,true> c0 = -3.5316387116909027099609375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<28,2,true> c3 = -1.49808232486248016357421875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<25,3,true> c8 = 3.382912158966064453125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<28,3,true> c4 = -3.3163668811321258544921875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<27,3,true> c7 = -2.52347469329833984375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<28,2,true> c2 = -1.2584867179393768310546875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<28,3,true> c1 = -2.4176125824451446533203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_ss2_x8(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<26,2,true> c5 = 1.0086538791656494140625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<25,-1,true> c6 = 0.2219680249691009521484375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<26,1,true> c0 = 0.8723606765270233154296875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,0,true> c3 = 0.4079312980175018310546875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true> c8 = -0.69810771942138671875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,1,true> c4 = 0.6381544768810272216796875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,1,true> c7 = 0.57909524440765380859375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<27,1,true> c2 = 0.5590752661228179931640625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<26,1,true> c1 = 0.7836394608020782470703125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,14,true> code_fixed_ss2_y(ac_fixed<21,12,true> v0,
	ac_fixed<21,12,true> v1, ac_fixed<20,13,true> v2,
	ac_fixed<22,13,true> v3, ac_fixed<21,12,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<22,13,true> v6,
	ac_fixed<20,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,5,true> c5 = 8.67453765869140625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<24,4,true> c6 = -4.3738079071044921875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<22,3,true> c0 = 2.931491851806640625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,4,true> c3 = -7.61971950531005859375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true> c8 = -0.11029052734375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,3,true> c4 = 2.53919219970703125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<21,3,true> c7 = 2.95052337646484375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true> c2 = 0.46099853515625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<23,4,true> c1 = -6.4580821990966796875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss3_x1(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = -0.4106044769287109375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,0,true,AC_TRN> c1 = -0.45810699462890625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<17,-3,true,AC_TRN> c2 = 0.040401458740234375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = -0.4630157947540283203125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,-2,true,AC_TRN> c4 = 0.068076610565185546875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,0,true,AC_TRN> c5 = 0.48909282684326171875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = 0.4232485294342041015625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<16,-4,true,AC_TRN> c7 = 0.026943206787109375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<15,-5,true,AC_TRN> c8 = 0.01123332977294921875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss3_x2(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = 0.447527408599853515625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,0,true,AC_TRN> c1 = 0.26905536651611328125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<17,-3,true,AC_TRN> c2 = 0.03685092926025390625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,-1,true,AC_TRN> c3 = 0.2293169498443603515625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,0,true,AC_TRN> c4 = 0.463319301605224609375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<20,-2,true,AC_TRN> c5 = 0.0707118511199951171875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = -0.3539412021636962890625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<18,-2,true,AC_TRN> c7 = 0.0723285675048828125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<20,0,true,AC_TRN> c8 = 0.432636260986328125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<14,9,true> code_fixed_ss3_x3(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<18,9,true> sd = 0;
	ac_fixed<14,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<16,-3,true,AC_TRN> c0 = 0.040813446044921875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<17,-2,true,AC_TRN> c1 = 0.110622406005859375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<16,-2,true,AC_TRN> c2 = -0.080936431884765625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,-1,true,AC_TRN> c3 = -0.230243682861328125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<18,-1,true,AC_TRN> c4 = -0.1459217071533203125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<18,-2,true,AC_TRN> c5 = 0.0994663238525390625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,0,true,AC_TRN> c6 = 0.2576045989990234375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<16,-2,true,AC_TRN> c7 = 0.11602783203125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<14,-4,true,AC_TRN> c8 = -0.029720306396484375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_ss3_x4(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = 0.412161350250244140625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true,AC_TRN> c1 = 0.556848049163818359375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<19,-1,true,AC_TRN> c2 = -0.18026256561279296875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<20,-2,true,AC_TRN> c3 = 0.1079285144805908203125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,-1,true,AC_TRN> c4 = 0.173143863677978515625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,0,true,AC_TRN> c5 = 0.3102734088897705078125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-2,true,AC_TRN> c6 = 0.0800778865814208984375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true,AC_TRN> c7 = 0.2012271881103515625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<17,-3,true,AC_TRN> c8 = 0.0511569976806640625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss3_x5(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true,AC_TRN> c0 = -0.062830448150634765625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,-1,true,AC_TRN> c1 = -0.184285640716552734375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true,AC_TRN> c2 = 0.37986850738525390625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = -0.3646709918975830078125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,0,true,AC_TRN> c4 = -0.30541229248046875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,1,true,AC_TRN> c5 = 0.5175302028656005859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-2,true,AC_TRN> c6 = 0.081939697265625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true,AC_TRN> c7 = -0.14939594268798828125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<17,-3,true,AC_TRN> c8 = -0.06005382537841796875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_ss3_x6(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,-1,true,AC_TRN> c0 = 0.21817493438720703125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<19,-2,true,AC_TRN> c1 = 0.0904083251953125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,1,true,AC_TRN> c2 = -0.51055622100830078125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = -0.4844152927398681640625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<17,-4,true,AC_TRN> c4 = -0.02946567535400390625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<21,-1,true,AC_TRN> c5 = -0.248992919921875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,1,true,AC_TRN> c6 = -0.666427135467529296875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<18,-2,true,AC_TRN> c7 = 0.09761524200439453125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<20,0,true,AC_TRN> c8 = 0.33147907257080078125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_ss3_x7(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,0,true,AC_TRN> c0 = 0.253330707550048828125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<19,-3,true,AC_TRN> c1 = 0.0609569549560546875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,-1,true,AC_TRN> c2 = 0.176759243011474609375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,0,true,AC_TRN> c3 = -0.3001334667205810546875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.1632754802703857421875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = 0.382720947265625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,0,true,AC_TRN> c6 = 0.4687969684600830078125;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<19,-2,true,AC_TRN> c7 = -0.112518310546875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,0,true,AC_TRN> c8 = 0.264287471771240234375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,9,true> code_fixed_ss3_x8(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,9,true> sd = 0;
	ac_fixed<15,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true,AC_TRN> c0 = 0.16107177734375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,0,true,AC_TRN> c1 = 0.32770061492919921875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<15,-4,true,AC_TRN> c2 = 0.0195789337158203125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<16,-5,true,AC_TRN> c3 = -0.0152301788330078125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<16,-4,true,AC_TRN> c4 = -0.0225124359130859375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<18,-3,true,AC_TRN> c5 = 0.049821376800537109375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,1,true,AC_TRN> c6 = -0.59977245330810546875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<18,-1,true,AC_TRN> c7 = 0.146739959716796875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<17,-2,true,AC_TRN> c8 = -0.122802734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<17,14,true> code_fixed_ss3_y(ac_fixed<17,10,true,AC_TRN> v0,
	ac_fixed<17,10,true,AC_TRN> v1, ac_fixed<14,9,true,AC_TRN> v2,
	ac_fixed<18,11,true,AC_TRN> v3, ac_fixed<17,10,true,AC_TRN> v4,
	ac_fixed<18,11,true,AC_TRN> v5, ac_fixed<19,11,true,AC_TRN> v6,
	ac_fixed<15,9,true,AC_TRN> v7, ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,3,true,AC_TRN> c0 = 3.23668670654296875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,4,true,AC_TRN> c1 = -5.237548828125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<17,1,true,AC_TRN> c2 = -0.7901611328125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,4,true,AC_TRN> c3 = 4.355022430419921875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,3,true,AC_TRN> c4 = 3.383697509765625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<20,2,true,AC_TRN> c5 = 1.8227996826171875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,4,true,AC_TRN> c6 = -5.17850494384765625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<19,3,true,AC_TRN> c7 = 3.238739013671875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true,AC_TRN> c8 = -0.11029052734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<19,10,true> code_fixed_ss4_x1(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-1,true,AC_TRN> c0 = -0.23661899566650390625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = -0.817473590373992919921875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,-1,true,AC_TRN> c2 = -0.1502807140350341796875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<24,1,true,AC_TRN> c3 = -0.74930989742279052734375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,-2,true,AC_TRN> c4 = 0.09025669097900390625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = 0.25549995899200439453125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-2,true,AC_TRN> c6 = -0.108922481536865234375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.0715696811676025390625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = -0.254567623138427734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_ss4_x2(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,0,true,AC_TRN> c0 = 0.4317538738250732421875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,-1,true,AC_TRN> c1 = 0.245232105255126953125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,-1,true,AC_TRN> c2 = 0.146778583526611328125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true,AC_TRN> c3 = 1.29412519931793212890625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true,AC_TRN> c4 = 0.460979461669921875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<21,-2,true,AC_TRN> c5 = -0.0702617168426513671875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-2,true,AC_TRN> c6 = 0.1080167293548583984375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true,AC_TRN> c7 = 0.289010584354400634765625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = 0.606799602508544921875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss4_x3(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = -0.41648197174072265625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,-2,true,AC_TRN> c1 = 0.0911147594451904296875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<16,-5,true,AC_TRN> c2 = -0.01432037353515625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,0,true,AC_TRN> c3 = -0.26876735687255859375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,0,true,AC_TRN> c4 = -0.4093151092529296875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,1,true,AC_TRN> c5 = -0.579551219940185546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,0,true,AC_TRN> c6 = 0.3012065887451171875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,0,true,AC_TRN> c7 = -0.2681121826171875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<19,-1,true,AC_TRN> c8 = -0.17646694183349609375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss4_x4(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-1,true,AC_TRN> c0 = 0.18454086780548095703125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<24,0,true,AC_TRN> c1 = 0.415159404277801513671875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true,AC_TRN> c2 = -0.10745918750762939453125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,-2,true,AC_TRN> c3 = -0.07856762409210205078125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.1658799648284912109375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = 0.49462127685546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,1,true,AC_TRN> c6 = 0.572414875030517578125;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.112441003322601318359375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = -0.36528491973876953125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss4_x5(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,-2,true,AC_TRN> c0 = 0.06334221363067626953125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = 0.613640308380126953125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<24,1,true,AC_TRN> c2 = 0.9157526493072509765625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,0,true,AC_TRN> c3 = 0.40147411823272705078125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,-3,true,AC_TRN> c4 = -0.0357959270477294921875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = 0.67137813568115234375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = 0.3578937053680419921875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,-1,true,AC_TRN> c7 = 0.133155643939971923828125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<17,-5,true,AC_TRN> c8 = 0.010509490966796875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss4_x6(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true,AC_TRN> c0 = -0.57534277439117431640625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = -1;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<24,1,true,AC_TRN> c2 = -0.58932578563690185546875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true,AC_TRN> c3 = -1.2217237949371337890625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<23,1,true,AC_TRN> c4 = -0.5938303470611572265625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = -0.69000327587127685546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<24,2,true,AC_TRN> c6 = -1.0699279308319091796875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true,AC_TRN> c7 = -0.375308573246002197265625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = 0.3114802837371826171875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss4_x7(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-1,true,AC_TRN> c0 = 0.15016651153564453125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,-3,true,AC_TRN> c1 = -0.0540292263031005859375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true,AC_TRN> c2 = -0.07587969303131103515625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,0,true,AC_TRN> c3 = -0.4501855373382568359375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,-2,true,AC_TRN> c4 = 0.0629055500030517578125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<21,-2,true,AC_TRN> c5 = 0.08938658237457275390625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-2,true,AC_TRN> c6 = 0.11448574066162109375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = -0.12313306331634521484375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<20,-2,true,AC_TRN> c8 = 0.11638641357421875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_ss4_x8(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true,AC_TRN> c0 = 0.8482043743133544921875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = 0.760990798473358154296875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<16,-7,true,AC_TRN> c2 = -0.00195467472076416015625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true,AC_TRN> c3 = 1.1106853485107421875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<23,1,true,AC_TRN> c4 = 0.6164267063140869140625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = 0.80445992946624755859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = -0.3882887363433837890625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<25,1,true,AC_TRN> c7 = 0.642162621021270751953125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = -0.611294269561767578125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,14,true> code_fixed_ss4_y(ac_fixed<19,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<20,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,3,true,AC_TRN> c0 = 3.993743896484375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,4,true,AC_TRN> c1 = -7.43292236328125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<18,1,true,AC_TRN> c2 = -0.9116668701171875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,4,true,AC_TRN> c3 = -5.7781524658203125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,3,true,AC_TRN> c4 = 3.531036376953125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<21,4,true,AC_TRN> c5 = 7.95502471923828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,4,true,AC_TRN> c6 = -5.5140228271484375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,3,true,AC_TRN> c7 = 3.216796875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true,AC_TRN> c8 = -0.11029052734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
}	


ac_fixed<20,10,true> code_fixed_ss5_x1(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,10,true> sd = 0;
	ac_fixed<20,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-2,true,AC_TRN> c0 = -0.11077821254730224609375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,0,true,AC_TRN> c1 = -0.318149745464324951171875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,-4,true,AC_TRN> c2 = 0.024568974971771240234375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,-1,true,AC_TRN> c3 = -0.191798031330108642578125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<23,0,true,AC_TRN> c4 = 0.25195217132568359375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,0,true,AC_TRN> c5 = 0.484873235225677490234375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,-2,true,AC_TRN> c6 = -0.081983089447021484375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<24,-1,true,AC_TRN> c7 = 0.239941895008087158203125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,-1,true,AC_TRN> c8 = -0.21337544918060302734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_ss5_x2(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,0,true,AC_TRN> c0 = 0.3270552158355712890625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,-2,true,AC_TRN> c1 = -0.07829749584197998046875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true,AC_TRN> c2 = 0.07365143299102783203125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<24,1,true,AC_TRN> c3 = 0.6519358158111572265625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true,AC_TRN> c4 = 0.3743097782135009765625;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = -0.25785219669342041015625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-3,true,AC_TRN> c6 = 0.04083156585693359375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.0938603878021240234375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true,AC_TRN> c8 = 0.6831510066986083984375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss5_x3(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true,AC_TRN> c0 = -0.491579532623291015625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true,AC_TRN> c1 = 0.31836032867431640625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<16,-5,true,AC_TRN> c2 = 0.010989665985107421875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<18,-3,true,AC_TRN> c3 = 0.032764434814453125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,0,true,AC_TRN> c4 = -0.45677089691162109375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,1,true,AC_TRN> c5 = -0.550405979156494140625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,0,true,AC_TRN> c6 = 0.3126926422119140625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,-1,true,AC_TRN> c7 = -0.1892540454864501953125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<20,0,true,AC_TRN> c8 = -0.28411388397216796875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss5_x4(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,0,true,AC_TRN> c0 = 0.265285968780517578125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = 0.699210107326507568359375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true,AC_TRN> c2 = -0.07145512104034423828125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,0,true,AC_TRN> c3 = 0.40692341327667236328125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.219581127166748046875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = 0.4771702289581298828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<24,1,true,AC_TRN> c6 = 0.59348762035369873046875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,-1,true,AC_TRN> c7 = 0.23768079280853271484375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = -0.36336803436279296875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss5_x5(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,-5,true,AC_TRN> c0 = -0.00975000858306884765625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,-1,true,AC_TRN> c1 = 0.21148622035980224609375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true,AC_TRN> c2 = 0.41028118133544921875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,-4,true,AC_TRN> c3 = 0.02339231967926025390625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = -0.13127040863037109375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = 0.62147486209869384765625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,-1,true,AC_TRN> c6 = 0.22900259494781494140625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.07936370372772216796875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true,AC_TRN> c8 = -0.2047405242919921875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss5_x6(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true,AC_TRN> c0 = -0.5628798007965087890625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true,AC_TRN> c1 = -0.881776869297027587890625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true,AC_TRN> c2 = -0.47248470783233642578125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<24,1,true,AC_TRN> c3 = -1;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<23,1,true,AC_TRN> c4 = -0.613500118255615234375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = -0.8495686054229736328125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<25,2,true,AC_TRN> c6 = -1.0476343631744384765625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true,AC_TRN> c7 = -0.379737913608551025390625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = 0.4522535800933837890625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss5_x7(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-1,true,AC_TRN> c0 = 0.16192495822906494140625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,-2,true,AC_TRN> c1 = -0.1013414859771728515625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,-3,true,AC_TRN> c2 = 0.045609951019287109375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,0,true,AC_TRN> c3 = -0.4428832530975341796875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,-2,true,AC_TRN> c4 = 0.071527004241943359375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,-1,true,AC_TRN> c5 = 0.20397698879241943359375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,-1,true,AC_TRN> c6 = 0.176212787628173828125;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = -0.11966168880462646484375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true,AC_TRN> c8 = 0.1296999454498291015625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_ss5_x8(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true,AC_TRN> c0 = 0.75898647308349609375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,0,true,AC_TRN> c1 = 0.35226154327392578125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<19,-3,true,AC_TRN> c2 = 0.061712741851806640625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = 0.3872280120849609375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,1,true,AC_TRN> c4 = 0.59441089630126953125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,1,true,AC_TRN> c5 = 0.87076663970947265625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = -0.344676971435546875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<24,1,true,AC_TRN> c7 = 0.52236270904541015625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,1,true,AC_TRN> c8 = -0.731526851654052734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,14,true> code_fixed_ss5_y(ac_fixed<20,10,true,AC_TRN> v0,ac_fixed<20,11,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<19,10,true,AC_TRN> v3,ac_fixed<18,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<19,10,true,AC_TRN> v6,ac_fixed<19,11,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,4,true,AC_TRN> c0 = 4.6474456787109375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,4,true,AC_TRN> c1 = -7.513275146484375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<17,0,true,AC_TRN> c2 = -0.47011566162109375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,4,true,AC_TRN> c3 = -6.68109130859375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,3,true,AC_TRN> c4 = 3.53643798828125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,5,true,AC_TRN> c5 = 8.1562652587890625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,4,true,AC_TRN> c6 = -4.7039031982421875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,3,true,AC_TRN> c7 = 2.925533294677734375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true,AC_TRN> c8 = -0.11029052734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<18,9,true> code_fixed_ss6_x1(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true,AC_TRN> c0 = -0.5512459278106689453125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,-1,true,AC_TRN> c1 = 0.1545078754425048828125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true,AC_TRN> c2 = 0.0750024318695068359375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true,AC_TRN> c3 = 0.4787662029266357421875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<14,-8,true,AC_TRN> c4 = 0.0009982585906982421875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = 0.35077381134033203125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = -0.345189571380615234375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,0,true,AC_TRN> c7 = 0.37215518951416015625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true,AC_TRN> c8 = -0.1778833866119384765625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss6_x2(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,-4,true,AC_TRN> c0 = 0.0311291217803955078125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,0,true,AC_TRN> c1 = 0.26888096332550048828125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,-3,true,AC_TRN> c2 = -0.05739796161651611328125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,1,true,AC_TRN> c3 = 0.8811562061309814453125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.193104267120361328125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = -0.2615299224853515625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,-1,true,AC_TRN> c6 = -0.15713024139404296875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,0,true,AC_TRN> c7 = 0.27550411224365234375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = 0.4386656284332275390625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss6_x3(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,-2,true,AC_TRN> c0 = 0.06259822845458984375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,0,true,AC_TRN> c1 = 0.419086933135986328125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<19,-2,true,AC_TRN> c2 = -0.086551189422607421875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,-1,true,AC_TRN> c3 = -0.1252803802490234375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<17,-3,true,AC_TRN> c4 = -0.0394496917724609375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,1,true,AC_TRN> c5 = -0.516998291015625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,0,true,AC_TRN> c6 = 0.4429798126220703125;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<18,-3,true,AC_TRN> c7 = -0.048481464385986328125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<19,-1,true,AC_TRN> c8 = -0.1715984344482421875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss6_x4(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,-2,true,AC_TRN> c0 = 0.085312366485595703125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,0,true,AC_TRN> c1 = 0.31562387943267822265625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,-1,true,AC_TRN> c2 = 0.14799726009368896484375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,-1,true,AC_TRN> c3 = 0.1809327602386474609375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.165771961212158203125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<24,1,true,AC_TRN> c5 = 0.65339052677154541015625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = 0.4663894176483154296875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-1,true,AC_TRN> c7 = 0.17997395992279052734375;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true,AC_TRN> c8 = -0.21745014190673828125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,9,true> code_fixed_ss6_x5(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,9,true> sd = 0;
	ac_fixed<19,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-1,true,AC_TRN> c0 = -0.20879650115966796875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,-4,true,AC_TRN> c1 = -0.022257506847381591796875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,-1,true,AC_TRN> c2 = 0.236808598041534423828125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<21,-2,true,AC_TRN> c3 = 0.0780467987060546875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,-1,true,AC_TRN> c4 = -0.2368361949920654296875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<25,1,true,AC_TRN> c5 = 0.556255340576171875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<18,-5,true,AC_TRN> c6 = -0.01327037811279296875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<22,-2,true,AC_TRN> c7 = 0.078604876995086669921875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,-1,true,AC_TRN> c8 = -0.22474014759063720703125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_ss6_x6(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,-1,true,AC_TRN> c0 = -0.2006766796112060546875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<24,1,true,AC_TRN> c1 = -0.96298658847808837890625;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true,AC_TRN> c2 = -0.27959537506103515625;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<24,2,true,AC_TRN> c3 = -1.2434480190277099609375;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true,AC_TRN> c4 = -0.2710349559783935546875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<23,0,true,AC_TRN> c5 = -0.4933955669403076171875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,1,true,AC_TRN> c6 = -0.8279025554656982421875;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,0,true,AC_TRN> c7 = -0.31053245067596435546875;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,0,true,AC_TRN> c8 = 0.3871061801910400390625;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss6_x7(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true,AC_TRN> c0 = 0.8327853679656982421875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,-1,true,AC_TRN> c1 = -0.1480934619903564453125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<15,-8,true,AC_TRN> c2 = 0.00107491016387939453125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,1,true,AC_TRN> c3 = -0.6570446491241455078125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true,AC_TRN> c4 = 0.4440765380859375;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<21,-2,true,AC_TRN> c5 = 0.1142165660858154296875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,1,true,AC_TRN> c6 = 0.693878173828125;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<23,0,true,AC_TRN> c7 = -0.29171192646026611328125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true,AC_TRN> c8 = 0.1623742580413818359375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,10,true> code_fixed_ss6_x8(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true,AC_TRN> c0 = 0.0639171600341796875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,-1,true,AC_TRN> c1 = 0.1471168994903564453125;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,-1,true,AC_TRN> c2 = -0.1946094036102294921875;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,-2,true,AC_TRN> c3 = -0.0696659088134765625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<20,-1,true,AC_TRN> c4 = -0.173511981964111328125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,0,true,AC_TRN> c5 = 0.25;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,1,true,AC_TRN> c6 = -0.697756290435791015625;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<21,-1,true,AC_TRN> c7 = 0.1709110736846923828125;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<22,1,true,AC_TRN> c8 = -0.53635883331298828125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,14,true> code_fixed_ss6_y(ac_fixed<18,9,true,AC_TRN> v0,ac_fixed<19,10,true,AC_TRN> v1,ac_fixed<17,10,true,AC_TRN> v2,ac_fixed<18,9,true,AC_TRN> v3,ac_fixed<19,9,true,AC_TRN> v4,ac_fixed<19,10,true,AC_TRN> v5,ac_fixed<18,9,true,AC_TRN> v6,ac_fixed<18,10,true,AC_TRN> v7,ac_fixed<17,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,4,true,AC_TRN> c0 = 4.193878173828125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,4,true,AC_TRN> c1 = -7.44347381591796875;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<15,-2,true,AC_TRN> c2 = -0.1221771240234375;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<19,3,true,AC_TRN> c3 = -3.9579010009765625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<19,3,true,AC_TRN> c4 = 2.1352081298828125;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,5,true,AC_TRN> c5 = 8.22547149658203125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,4,true,AC_TRN> c6 = -5.5097503662109375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<20,3,true,AC_TRN> c7 = 3.78228759765625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true,AC_TRN> c8 = -0.11029052734375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}














ac_fixed<21,12,true> code_fixed_LGS_t2(ac_fixed<20,11,true> v0,ac_fixed<20,11,true> v1)
{
	ac_fixed<22,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;
	ac_fixed<21,0,true> c0 = -0.449921131134033203125;
	sd = sd + c0*v0;
	ac_fixed<23,2,true> c1 = 1;
	sd = sd + c1*v1;
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t10(ac_fixed<21,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 0.8316497802734375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_LGS_t19(ac_fixed<20,11,true> v0, ac_fixed<20,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = -0.501529693603515625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t27(ac_fixed<21,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 0.827002048492431640625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t36(ac_fixed<20,11,true> v0,ac_fixed<20,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true> c0 = -0.382689952850341796875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<23,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t44(ac_fixed<20,11,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,1,true> c0 = 0.89196872711181640625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,12,true> code_fixed_LGS_t53(ac_fixed<20,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,12,true> sd = 0;
	ac_fixed<20,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,1,true> c0 = -0.78519535064697265625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t61(ac_fixed<20,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 0.645191669464111328125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,12,true> code_fixed_LGS_t70(ac_fixed<20,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,12,true> sd = 0;
	ac_fixed<20,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,2,true> c0 = -1.352451324462890625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,11,true> code_fixed_LGS_t78(ac_fixed<20,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<21,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,0,true> c0 = 0.4586870670318603515625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,12,true> code_fixed_LGS_t87(ac_fixed<21,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,12,true> sd = 0;
	ac_fixed<19,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,3,true> c0 = -2.059520721435546875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_LGS_t95(ac_fixed<19,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<19,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true> c0 = 0.33949184417724609375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,13,true> code_fixed_LGS_t104(ac_fixed<19,10,true> v0,ac_fixed<18,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,13,true> sd = 0;
	ac_fixed<20,13,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,4,true> c0 = -4.335906982421875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,9,true> code_fixed_LGS_t112(ac_fixed<20,13,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<20,9,true> sd = 0;
	ac_fixed<20,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,-2,true> c0 = 0.0678455829620361328125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,10,true> code_fixed_LGS_t119(ac_fixed<19,10,true> v0,ac_fixed<20,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<20,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,2,true> c1 = 1.4720058441162109375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,10,true> code_fixed_LGS_t126(ac_fixed<21,11,true> v0,ac_fixed<20,10,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<20,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 0.944675445556640625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,10,true> code_fixed_LGS_t133(ac_fixed<20,11,true> v0,ac_fixed<20,10,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,10,true> sd = 0;
	ac_fixed<19,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 0.87259006500244140625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t140(ac_fixed<20,11,true> v0,ac_fixed<19,10,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 0.70036983489990234375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,11,true> code_fixed_LGS_t147(ac_fixed<20,11,true> v0,ac_fixed<20,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<21,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c1 = 0.3164851665496826171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,11,true> code_fixed_LGS_t154(ac_fixed<20,11,true> v0,ac_fixed<21,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<21,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c1 = 0.4170970916748046875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t161(ac_fixed<20,11,true> v0,ac_fixed<21,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,0,true> c1 = 0.449921131134033203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t169(ac_fixed<20,11,true> v0,ac_fixed<21,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,0,true> c1 = 0.449921131134033203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t170(ac_fixed<20,11,true> v0,ac_fixed<21,11,true> v1,ac_fixed<21,11,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<24,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,1,true> c2 = 0.501529693603515625;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<22,0,true> c0 = -0.449921131134033203125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t171(ac_fixed<21,11,true> v0,ac_fixed<21,11,true> v1,ac_fixed<20,11,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<24,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,0,true> c2 = 0.3826897144317626953125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = -0.501529693603515625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_t172(ac_fixed<21,11,true> v0,ac_fixed<20,11,true> v1,ac_fixed<19,10,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<24,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,1,true> c2 = 0.785195827484130859375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<22,0,true> c0 = -0.3826897144317626953125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t173(ac_fixed<20,11,true> v0, ac_fixed<19,10,true> v1,ac_fixed<20,10,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,2,true> c2 = 1.352451324462890625;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = -0.785195827484130859375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t174(ac_fixed<19,10,true> v0, ac_fixed<20,10,true> v1,ac_fixed<20,9,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,3,true> c2 = 2.05951976776123046875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<22,2,true> c0 = -1.352451324462890625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t175(ac_fixed<20,10,true> v0, ac_fixed<20,9,true> v1,ac_fixed<20,9,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<23,4,true> c2 = 4.335906982421875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<23,3,true> c0 = -2.05951976776123046875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t176(ac_fixed<20,9,true> v0,ac_fixed<20,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,4,true> c0 = -4.335906982421875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,4,true> c1 = -6.35687255859375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_x1(ac_fixed<20,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,2,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<15,-4,true> c1 = 0.0185756683349609375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_x2(ac_fixed<20,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,-3,true> c1 = 0.0412875115871429443359375;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<16,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_x3(ac_fixed<20,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,-2,true> c1 = 0.098987758159637451171875;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<17,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,11,true> code_fixed_LGS_x4(ac_fixed<20,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<21,11,true> sd = 0;
	ac_fixed<20,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,0,true> c1 = 0.3127720355987548828125;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<19,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_x5(ac_fixed<19,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,0,true> c1 = 0.446581363677978515625;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<18,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_x6(ac_fixed<19,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c1 = 0.51178836822509765625;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<19,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_x7(ac_fixed<19,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c1 = 0.541760921478271484375;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<19,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_x8(ac_fixed<18,11,true> v0,ac_fixed<17,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true> c1 = 0.368042469024658203125;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<17,2,true> c0 = 1;
	sd = sd + v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,14,true> code_fixed_LGS_y(ac_fixed<20,11,true> v0,
	ac_fixed<20,11,true> v1, ac_fixed<20,11,true> v2,
	ac_fixed<20,11,true> v3, ac_fixed<19,11,true> v4,
	ac_fixed<19,11,true> v5, ac_fixed<19,11,true> v6,
	ac_fixed<18,11,true> v7, ac_fixed<17,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,14,true> sd = 0;
	ac_fixed<17,14,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,2,true> c5 = -1.633083343505859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,3,true> c6 = -2.520660400390625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,2,true> c0 = 1.087879180908203125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<18,0,true> c3 = -0.266956329345703125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<14,-2,true> c8 = -0.11029052734375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<16,-2,true> c4 = -0.1202850341796875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,2,true> c7 = -1.682735443115234375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,3,true> c2 = -2.895885467529296875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<21,3,true> c1 = -3.01004791259765625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}






double impulse()
{
	double X=( rand()/(double)RAND_MAX ) * (399) -237;
	return X;
}

int main(void)
{
	srand(time(NULL));

	double imp = impulse();
	/*int16_t u = (int16_t)imp,
		x1 = 0, x2 = 0, x3 = 0, y = 0,
		xp1 = 0, xp2 = 0, xp3 = 0;*/
	double Du = 0,
		Dt1 = 0, Dt2 = 0, Dt3 = 0, Dt4 = 0, Dt5 = 0, Dt6 = 0, Dt7 = 0, Dt8 = 0,
		Dx1 = 0, Dx2 = 0, Dx3 = 0, Dx4 = 0, Dx5 = 0, Dx6 = 0, Dx7 = 0, Dx8 = 0, Dy = 0,
		Dxp1 = 0, Dxp2 = 0, Dxp3 = 0, Dxp4 = 0, Dxp5 = 0, Dxp6 = 0, Dxp7 = 0, Dxp8 = 0,
		maxDy=-1000,minDy=1000,
		maxy=-1000,miny=1000;

	ac_fixed<18,9,true> u=imp;

	ac_fixed<16,9,true> DFIu1=0,DFIu2=0,DFIu3=0,DFIu4=0,DFIu5=0,DFIu6=0,DFIu7=0,DFIu8=0;
	ac_fixed<16,14,true> DFIy = 0, DFIy1 = 0, DFIy2 = 0, DFIy3 = 0, DFIy4 = 0, DFIy5 = 0, DFIy6 = 0, DFIy7 = 0, DFIy8 = 0;


	ac_fixed<20,14,true> Rt1=0;
	ac_fixed<19,11,true> Rt2=0, Rt3=0, Rx1=0,Rx2=0,Rx3=0,Rx4=0,Rxp1=0,Rxp2=0,Rxp3=0,Rxp4=0;
	ac_fixed<18,10,true> Rt4=0;
	ac_fixed<18,11,true> Rt5=0, Rx5=0, Rxp5=0;
	ac_fixed<17,10,true> Rt6=0;
	ac_fixed<13,7,true> Rt7=0;
	ac_fixed<11,9,true> Rt8=0;
	ac_fixed<16,11,true> Rx6=0, Rxp6=0;
	ac_fixed<12,10,true> Rx7=0, Rxp7=0;
	ac_fixed<11,11,true> Rx8=0, Rxp8=0;
	ac_fixed<18,14,true> Ry =0;

	ac_fixed<17,10,true,AC_TRN> x31=0, xp31=0, x32=0, xp32=0,x35=0, xp35=0;
	ac_fixed<14,9,true,AC_TRN> x33=0,xp33=0;
	ac_fixed<18,11,true,AC_TRN> x34=0, xp34=0,x36=0, xp36=0;
	ac_fixed<19,11,true,AC_TRN> x37=0, xp37=0;
	ac_fixed<15,9,true,AC_TRN> x38=0, xp38=0;
	ac_fixed<17,14,true,AC_TRN> y3=0;

	ac_fixed<21,12,true> x21=0, xp21=0, x22=0,xp22=0, x25=0,xp25=0;
	ac_fixed<20,13,true> x23=0, xp23=0;
	ac_fixed<22,13,true> x24=0, xp24=0, x27=0,xp27=0;
	ac_fixed<20,11,true> x26=0, xp26=0, x28=0,xp28=0;
	ac_fixed<17,14,true> y2=0;

	ac_fixed<19,10,true,AC_TRN> x41=0, xp41=0;
	ac_fixed<20,11,true,AC_TRN> x42=0, xp42=0;
	ac_fixed<17,10,true,AC_TRN> x43=0, xp43=0;
	ac_fixed<19,10,true,AC_TRN> x44=0, xp44=0;
	ac_fixed<18,9,true,AC_TRN> x45=0, xp45=0;
	ac_fixed<19,10,true,AC_TRN> x46=0, xp46=0;
	ac_fixed<18,9,true,AC_TRN> x47=0, xp47=0;
	ac_fixed<20,11,true,AC_TRN> x48=0, xp48=0;
	ac_fixed<17,14,true,AC_TRN> y4=0;

	ac_fixed<20,10,true,AC_TRN> x51 =0, xp51 =0;
	ac_fixed<20,11,true,AC_TRN> x52 =0, xp52 =0;
	ac_fixed<17,10,true,AC_TRN> x53 =0, xp53 =0;
	ac_fixed<19,10,true,AC_TRN> x54 =0, xp54 =0;
	ac_fixed<18,9,true,AC_TRN> x55 =0, xp55 =0;
	ac_fixed<19,10,true,AC_TRN> x56 =0, xp56 =0;
	ac_fixed<19,10,true,AC_TRN> x57 =0, xp57 =0;
	ac_fixed<19,11,true,AC_TRN> x58 =0, xp58 =0;
	ac_fixed<17,14,true,AC_TRN> y5 = 0;

	ac_fixed<18,9,true,AC_TRN> x61 =0, xp61 =0;
	ac_fixed<19,10,true,AC_TRN> x62 =0, xp62 =0;
	ac_fixed<17,10,true,AC_TRN> x63 =0, xp63 =0;
	ac_fixed<18,9,true,AC_TRN> x64 =0, xp64 =0;
	ac_fixed<19,9,true,AC_TRN> x65 =0, xp65 =0;
	ac_fixed<19,10,true,AC_TRN> x66 =0, xp66 =0;
	ac_fixed<18,9,true,AC_TRN> x67 =0, xp67 =0;
	ac_fixed<18,10,true,AC_TRN> x68 =0, xp68 =0;
	ac_fixed<17,14,true,AC_TRN> y6=0;


	ac_fixed<21,12,true> tL2=0, tL19=0;
	ac_fixed<20,11,true> tL10=0, tL27=0, tL36=0, tL44=0, tL61=0, tL140=0, tL161=0, tL169=0, tL170=0, tL171=0, tL172=0, xL1=0, xpL1=0,
		xL2=0, xpL2=0, xL3=0, xpL3=0, xL4=0, xpL4=0;
	ac_fixed<20,12,true> tL53=0, tL70=0;
	ac_fixed<21,11,true> tL78=0, tL147=0, tL154=0;
	ac_fixed<19,12,true> tL87=0;
	ac_fixed<19,10,true> tL95=0, tL133=0;
	ac_fixed<20,13,true> tL104=0;
	ac_fixed<20,9,true> tL112=0;
	ac_fixed<20,10,true> tL119=0, tL126=0;
	ac_fixed<19,11,true> tL173=0, tL174=0, tL175=0, xL5=0, xpL5=0, xL6=0, xpL6=0, xL7=0, xpL7=0;
	ac_fixed<18,11,true> tL176=0, xL8=0, xpL8=0;
	ac_fixed<17,14,true> yL=0;

	Du = u.to_double();


	int cpt = 1;
	while(cpt<=100){

		Dt1 = double_t1(Dx1,Du);
		Dt2 = double_t2(Dx2);
		Dt3 = double_t3(Dx3);
		Dt4 = double_t4(Dx4);
		Dt5 = double_t5(Dx5);
		Dt6 = double_t6(Dx6);
		Dt7 = double_t7(Dx7);
		Dt8 = double_t8(Dx8);
		Dxp1 = double_x1(Dt1, Dt2, Dx1, Du);
		Dxp2 = double_x2(Dt1, Dt3, Dx2, Du);
		Dxp3 = double_x3(Dt1, Dt4, Dx3, Du);
		Dxp4 = double_x4(Dt1, Dt5, Dx4, Du);
		Dxp5 = double_x5(Dt1, Dt6, Dx5, Du);
		Dxp6 = double_x6(Dt1, Dt7, Dx6, Du);
		Dxp7 = double_x7(Dt1, Dt8, Dx7, Du);
		Dxp8 = double_x8(Dt1, Dx8, Du);
		Dy = Dt1;
		Dx1 = Dxp1; Dx2 = Dxp2; Dx3 = Dxp3; Dx4 = Dxp4; Dx5 = Dxp5; Dx6 = Dxp6; Dx7 = Dxp7; Dx8 = Dxp8; 
		

		DFIy = code_fixed_DFI(u,DFIu1,DFIu2,DFIu3,DFIu4,DFIu5,DFIu6,DFIu7,DFIu8, DFIy1,DFIy2,DFIy3,DFIy4,DFIy5,DFIy6,DFIy7,DFIy8);
		DFIu8 = DFIu7; DFIu7 = DFIu6; DFIu6 = DFIu5; DFIu5 = DFIu4; DFIu4 = DFIu3; DFIu3 = DFIu2; DFIu2 = DFIu1; DFIu1=u;
		DFIy8 = DFIy7; DFIy7 = DFIy6; DFIy6 = DFIy5; DFIy5 = DFIy4; DFIy4 = DFIy3; DFIy3 = DFIy2; DFIy2 = DFIy1; DFIy1=DFIy;

		Rt1 = code_fixed_t1(Rx1,u);
		Rt2 = code_fixed_t2(Rx2);
		Rt3 = code_fixed_t3(Rx3);
		Rt4 = code_fixed_t4(Rx4);
		Rt5 = code_fixed_t5(Rx5);
		Rt6 = code_fixed_t6(Rx6);
		Rt7 = code_fixed_t7(Rx7);
		Rt8 = code_fixed_t8(Rx8);
		Rxp1 = code_fixed_x1(Rt1, Rt2, Rx1, u);
		Rxp2 = code_fixed_x2(Rt1, Rt3, Rx2, u);
		Rxp3 = code_fixed_x3(Rt1, Rt4, Rx3, u);
		Rxp4 = code_fixed_x4(Rt1, Rt5, Rx4, u);
		Rxp5 = code_fixed_x5(Rt1, Rt6, Rx5, u);
		Rxp6 = code_fixed_x6(Rt1, Rt7, Rx6, u);
		Rxp7 = code_fixed_x7(Rt1, Rt8, Rx7, u);
		Rxp8 = code_fixed_x8(Rt1, Rx8, u);
		Ry = Rt1;
		Rx1 = Rxp1; Rx2 = Rxp2; Rx3 = Rxp3; Rx4 = Rxp4; Rx5 = Rxp5; Rx6 = Rxp6; Rx7 = Rxp7; Rx8 = Rxp8; 

		



		xp21 = code_fixed_ss2_x1(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp22 = code_fixed_ss2_x2(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp23 = code_fixed_ss2_x3(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp24 = code_fixed_ss2_x4(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp25 = code_fixed_ss2_x5(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp26 = code_fixed_ss2_x6(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp27 = code_fixed_ss2_x7(x21, x22, x23, x24, x25, x26, x27, x28, u);
		xp28 = code_fixed_ss2_x8(x21, x22, x23, x24, x25, x26, x27, x28, u);
		y2 = code_fixed_ss2_y(x21, x22, x23, x24, x25, x26, x27, x28, u);
		x21 = xp21; x22 = xp22; x23 = xp23; x24 = xp24; x25 = xp25; x26 = xp26; x27 = xp27; x28 = xp28; 

		xp31 = code_fixed_ss3_x1(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp32 = code_fixed_ss3_x2(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp33 = code_fixed_ss3_x3(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp34 = code_fixed_ss3_x4(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp35 = code_fixed_ss3_x5(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp36 = code_fixed_ss3_x6(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp37 = code_fixed_ss3_x7(x31, x32, x33, x34, x35, x36, x37, x38, u);
		xp38 = code_fixed_ss3_x8(x31, x32, x33, x34, x35, x36, x37, x38, u);
		y3 = code_fixed_ss3_y(x31, x32, x33, x34, x35, x36, x37, x38, u);
		x31 = xp31; x32 = xp32; x33 = xp33; x34 = xp34; x35 = xp35; x36 = xp36; x37 = xp37; x38 = xp38; 

		xp41 = code_fixed_ss4_x1(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp42 = code_fixed_ss4_x2(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp43 = code_fixed_ss4_x3(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp44 = code_fixed_ss4_x4(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp45 = code_fixed_ss4_x5(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp46 = code_fixed_ss4_x6(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp47 = code_fixed_ss4_x7(x41, x42, x43, x44, x45, x46, x47, x48, u);
		xp48 = code_fixed_ss4_x8(x41, x42, x43, x44, x45, x46, x47, x48, u);
		y4   = code_fixed_ss4_y(x41, x42, x43, x44, x45, x46, x47, x48, u);
		x41 = xp41; x42 = xp42; x43 = xp43; x44 = xp44; x45 = xp45; x46 = xp46; x47 = xp47; x48 = xp48; 

		xp51 = code_fixed_ss5_x1(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp52 = code_fixed_ss5_x2(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp53 = code_fixed_ss5_x3(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp54 = code_fixed_ss5_x4(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp55 = code_fixed_ss5_x5(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp56 = code_fixed_ss5_x6(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp57 = code_fixed_ss5_x7(x51, x52, x53, x54, x55, x56, x57, x58, u);
		xp58 = code_fixed_ss5_x8(x51, x52, x53, x54, x55, x56, x57, x58, u);
		y5  = code_fixed_ss5_y(x51, x52, x53, x54, x55, x56, x57, x58, u);
		x51 = xp51; x52 = xp52; x53 = xp53; x54 = xp54; x55 = xp55; x56 = xp56; x57 = xp57; x58 = xp58; 

		xp61 = code_fixed_ss6_x1(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp62 = code_fixed_ss6_x2(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp63 = code_fixed_ss6_x3(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp64 = code_fixed_ss6_x4(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp65 = code_fixed_ss6_x5(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp66 = code_fixed_ss6_x6(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp67 = code_fixed_ss6_x7(x61, x62, x63, x64, x65, x66, x67, x68, u);
		xp68 = code_fixed_ss6_x8(x61, x62, x63, x64, x65, x66, x67, x68, u);
		y6  = code_fixed_ss6_y(x61, x62, x63, x64, x65, x66, x67, x68, u);
		x61 = xp61; x62 = xp62; x63 = xp63; x64 = xp64; x65 = xp65; x66 = xp66; x67 = xp67; x68 = xp68; 




		tL2 = code_fixed_LGS_t2(xL1, xL2);
		tL10 = code_fixed_LGS_t10(tL2);
		tL19 = code_fixed_LGS_t19(tL10, xL3);
		tL27 = code_fixed_LGS_t27(tL19);
		tL36 = code_fixed_LGS_t36(tL27, xL4);
		tL44 = code_fixed_LGS_t44(tL36);
		tL53 = code_fixed_LGS_t53(tL44, xL5);
		tL61 = code_fixed_LGS_t61(tL53);
		tL70 = code_fixed_LGS_t70(tL61, xL6);
		tL78 = code_fixed_LGS_t78(tL70);
		tL87 = code_fixed_LGS_t87(tL78, xL7); 
		tL95 = code_fixed_LGS_t95(tL87); 
		tL104 = code_fixed_LGS_t104(tL95, xL8);
		tL112 = code_fixed_LGS_t112(tL104);
		tL119 = code_fixed_LGS_t119(tL95, tL112);
		tL126 = code_fixed_LGS_t126(tL78, tL119);
		tL133 = code_fixed_LGS_t133(tL61, tL126);
		tL140 = code_fixed_LGS_t140(tL44, tL133);
		tL147 = code_fixed_LGS_t147(tL27, tL140);
		tL154 = code_fixed_LGS_t154(tL10, tL147);
		tL161 = code_fixed_LGS_t161(xL1, tL154);
		tL169 = code_fixed_LGS_t169(tL161, tL154); 
		tL170 = code_fixed_LGS_t170(tL161, tL154, tL147); 
		tL171 = code_fixed_LGS_t171(tL154, tL147, tL140); 
		tL172 = code_fixed_LGS_t172(tL147, tL140, tL133);
		tL173 = code_fixed_LGS_t173(tL140, tL133, tL126); 
		tL174 = code_fixed_LGS_t174(tL133, tL126, tL119); 
		tL175 = code_fixed_LGS_t175(tL126, tL119, tL112); 
		tL176 = code_fixed_LGS_t176(tL119, tL112);
		
		xpL1 = code_fixed_LGS_x1(tL169,u); xpL2 = code_fixed_LGS_x2(tL170,u); xpL3 = code_fixed_LGS_x3(tL171,u); xpL4 = code_fixed_LGS_x4(tL172,u);
		xpL5 = code_fixed_LGS_x5(tL173,u); xpL6 = code_fixed_LGS_x6(tL174,u); xpL7 = code_fixed_LGS_x7(tL175,u); xpL8 = code_fixed_LGS_x8(tL176,u);
		yL = code_fixed_LGS_y(xL1,xL2,xL3,xL4,xL5,xL6,xL7,xL8,u);
		xL1 = xpL1; xL2 = xpL2; xL3 = xpL3; xL4 = xpL4; xL5 = xpL5; xL6 = xpL6; xL7 = xpL7; xL8 = xpL8; 





		if(Dy >maxDy) maxDy=Dy;
		if(Dy<minDy) minDy=Dy;
		if(Ry.to_double() >maxy) maxy=Ry.to_double();
		if(Ry.to_double()<miny) miny=Ry.to_double();
		//printf("%d %d %d %d\n", x1,x2,x3,y);
		//printf("%g %g %g %g\n", Dx1*powf(2,14),Dx2*powf(2,10),Dx3*powf(2,9),Dy*powf(2,10));

		//printf("%d %g %g -0.125 0.125\n",cpt,imp,y.to_double()-Dy);
		cout << cpt<<" "<< DFIy.to_double()-Dy << " "<< Ry.to_double()-Dy  << " "<< y2.to_double()-Dy   << " "<< y3.to_double()-Dy   << " "<< y4.to_double()-Dy<< " "<< y5.to_double()-Dy   << " "<< y6.to_double()-Dy   << " "<< yL.to_double()-Dy << endl;
		
		imp = impulse();
		u = imp;
		Du =u.to_double();
		cpt++;
  	}
  	//printf(" %g ; %g\n", minDy,maxDy);
  	//printf(" %g ; %g", miny,maxy);
  return 0;
}