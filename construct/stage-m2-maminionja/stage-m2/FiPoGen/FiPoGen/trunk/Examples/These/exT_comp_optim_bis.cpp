#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include "ac_fixed.h"

using namespace std;

double double_DFI(double v0,double v1,double v2,double v3,double v4,double v5,double v6,double v7,double v8,double v9,double v10,double v11,double v12,double v13,double v14,double v15,double v16)
{
    double r;
    r = -0.03118419647216796875 * v7 + 0.0363025665283203125 * v8 + 0.006961822509765625 * v15 + -0.005564212799072265625 * v16 + 0.18310546875 * v4 + 0.2921142578125 * v2 + 0.2704315185546875 * v5 + -0.2965545654296875 * v6 + -0.94012451171875 * v0 + -0.693145751953125 * v3 + -0.089813232421875 * v12 + 0.07305145263671875 * v14 + 1.04327392578125 * v1 + -0.17235565185546875 * v13 + -1.95404052734375 * v10 + 1.046142578125 * v11 + 2.0692138671875 * v9;
	return r; 
}


ac_fixed<20,12,true> code_fixed_DFI(ac_fixed<20,9,true,AC_TRN> v0,
	ac_fixed<20,9,true,AC_TRN> v1,ac_fixed<20,9,true,AC_TRN> v2,
	ac_fixed<20,9,true,AC_TRN> v3,ac_fixed<20,9,true,AC_TRN> v4,
	ac_fixed<20,9,true,AC_TRN> v5,ac_fixed<20,9,true,AC_TRN> v6,
	ac_fixed<20,9,true,AC_TRN> v7,ac_fixed<20,9,true,AC_TRN> v8,
	ac_fixed<20,12,true,AC_TRN> v9,ac_fixed<20,12,true,AC_TRN> v10,
	ac_fixed<20,12,true,AC_TRN> v11,ac_fixed<20,12,true,AC_TRN> v12,
	ac_fixed<20,12,true,AC_TRN> v13,ac_fixed<20,12,true,AC_TRN> v14,
	ac_fixed<20,12,true,AC_TRN> v15,ac_fixed<20,12,true,AC_TRN> v16)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<20,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<23,1,true,AC_TRN> c0 = -0.9401397705078125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<24,2,true,AC_TRN> c1 = 1.043252468109130859375;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,0,true,AC_TRN> c2 = 0.2921078205108642578125;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<23,1,true,AC_TRN> c3 = -0.6931591033935546875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true,AC_TRN> c4 = 0.18310546875;
	sd = sd + c4*v4;
	//Computation of c5*v5 in sd
	ac_fixed<22,0,true,AC_TRN> c5 = 0.2704293727874755859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true,AC_TRN> c6 = -0.29655361175537109375;
	sd = sd + c6*v6;
	//Computation of c7*v7 in sd
	ac_fixed<18,-4,true,AC_TRN> c7 = -0.031183719635009765625;
	sd = sd + c7*v7;
	//Computation of c8*v8 in sd
	ac_fixed<19,-3,true,AC_TRN> c8 = 0.036302089691162109375;
	sd = sd + c8*v8;
	//Computation of c9*v9 in sd
	ac_fixed<28,3,true,AC_TRN> c9 = 2.069251537322998046875;
	sd = sd + c9*v9;
	//Computation of c10*v10 in sd
	ac_fixed<27,2,true,AC_TRN> c10 = -1.9540421664714813232421875;
	sd = sd + c10*v10;
	//Computation of c11*v11 in sd
	ac_fixed<27,2,true,AC_TRN> c11 = 1.0461590290069580078125;
	sd = sd + c11*v11;
	//Computation of c12*v12 in sd
	ac_fixed<23,-2,true,AC_TRN> c12 = -0.089812457561492919921875;
	sd = sd + c12*v12;
	//Computation of c13*v13 in sd
	ac_fixed<24,-1,true,AC_TRN> c13 = -0.1723540723323822021484375;
	sd = sd + c13*v13;
	//Computation of c14*v14 in sd
	ac_fixed<23,-2,true,AC_TRN> c14 = 0.073051869869232177734375;
	sd = sd + c14*v14;
	//Computation of c15*v15 in sd
	ac_fixed<19,-6,true,AC_TRN> c15 = 0.00696194171905517578125;
	sd = sd + c15*v15;
	//Computation of c16*v16 in sd
	ac_fixed<19,-6,true,AC_TRN> c16 = -0.0055642426013946533203125;
	sd = sd + c16*v16;

	//Computation of the final right shift
	s = s + sd;
	return s;
}



ac_fixed<17,12,true> code_fixed_rho_t1(ac_fixed<18,12,true> v0,ac_fixed<16,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<18,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,2,true> c0 = 1.327266693115234375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<16,1,true> c1 = -0.94012451171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,11,true> code_fixed_rho_t2(ac_fixed<18,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<17,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.737548828125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<18,12,true> code_fixed_rho_t3(ac_fixed<17,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.718006134033203125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_rho_t4(ac_fixed<18,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.88358306884765625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,11,true> code_fixed_rho_t5(ac_fixed<17,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<17,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.71953582763671875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_rho_t6(ac_fixed<17,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,1,true> c0 = 0.7630977630615234375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<16,11,true> code_fixed_rho_t7(ac_fixed<17,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<16,11,true> sd = 0;
	ac_fixed<16,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,1,true> c0 = 0.7612762451171875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<16,11,true> code_fixed_rho_t8(ac_fixed<18,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<16,11,true> sd = 0;
	ac_fixed<16,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,1,true> c0 = 0.52446746826171875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_rho_x1(ac_fixed<17,12,true> v0,
	ac_fixed<17,11,true> v1,ac_fixed<18,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<20,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<21,2,true> c1 = 1;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<19,-1,true> c2 = 0.24969387054443359375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true> c0 = -0.1973590850830078125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<18,1,true> c3 = -0.865234375;
	sd = sd + c3*v3;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_rho_x2(ac_fixed<17,12,true> v0,
	ac_fixed<18,12,true> v1,ac_fixed<18,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<20,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c2 = 0.2946319580078125;
	sd = sd + c2*v2;
	//Computation of c2*v2 in sd
	ac_fixed<20,2,true> c1 = 1;
	sd = sd + c1*v1;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = -0.27183437347412109375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<9,-8,true> c3 = 0.0012359619140625;
	sd = sd + c3*v3;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,12,true> code_fixed_rho_x3(ac_fixed<17,12,true> v0,
	ac_fixed<18,12,true> v1,ac_fixed<17,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<21,-1,true> c3 = 0.248450756072998046875;
	sd = sd + c3*v3;
	//Computation of c2*v2 in sd
	ac_fixed<18,-1,true> c2 = 0.188159942626953125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<18,-1,true> c0 = -0.217350006103515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<15,2,true> c1 = 1;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_rho_x4(ac_fixed<17,12,true> v0,
	ac_fixed<17,11,true> v1,ac_fixed<18,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<20,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<21,-2,true> c3 = -0.069734096527099609375;
	sd = sd + c3*v3;
	//Computation of c2*v2 in sd
	ac_fixed<19,-1,true> c2 = 0.20178127288818359375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = 0.2574462890625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<15,2,true> c1 = 1;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,12,true> code_fixed_rho_x5(ac_fixed<17,12,true> v0,
	ac_fixed<18,11,true> v1,ac_fixed<17,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,0,true> c3 = 0.44944667816162109375;
	sd = sd + c3*v3;
	//Computation of c2*v2 in sd
	ac_fixed<18,-1,true> c2 = 0.202960968017578125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<18,-1,true> c0 = 0.1256313323974609375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<16,2,true> c1 = 1;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,12,true> code_fixed_rho_x6(ac_fixed<17,12,true> v0,
	ac_fixed<16,11,true> v1,ac_fixed<17,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,-3,true> c3 = -0.04080212116241455078125;
	sd = sd + c3*v3;
	//Computation of c2*v2 in sd
	ac_fixed<18,-1,true> c2 = 0.2146587371826171875;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<17,-2,true> c0 = 0.0861148834228515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<13,2,true> c1= 1;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,12,true> code_fixed_rho_x7(ac_fixed<17,12,true> v0,
	ac_fixed<16,11,true> v1,ac_fixed<17,12,true> v2,
	ac_fixed<16,9,true> v3)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,0,true> c3 = -0.4816837310791015625;
	sd = sd + c3*v3;
	//Computation of c2*v2 in sd
	ac_fixed<18,-1,true> c2 = 0.1929645538330078125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<18,-1,true> c0 = 0.134159088134765625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<16,2,true> c1 = 1;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_rho_x8(ac_fixed<17,12,true> v0,
	ac_fixed<18,12,true> v1,ac_fixed<16,9,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<20,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<21,0,true> c2 = -0.38869762420654296875;
	sd = sd + c2*v2;
	//Computation of c2*v2 in sd
	ac_fixed<17,1,true> c1 = 0.786346435546875;
	sd = sd + c1*v1;
	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true> c0 = 0.1322078704833984375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<19,13,true> code_fixed_ss1_x1(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,13,true> sd = 0;
	ac_fixed<19,13,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<17,-3,true,AC_TRN> c3 = 0.06196117401123046875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<10,-9,true,AC_TRN> c4 = -0.0005931854248046875;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<19,-1,true,AC_TRN> c1 = -0.1602115631103515625;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<7,-9,true,AC_TRN> c6 = -0.000762939453125;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<17,-4,true,AC_TRN> c2 = -0.01969623565673828125;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<14,-5,true,AC_TRN> c5 = 0.00795745849609375;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<24,1,true,AC_TRN> c0 = 0.9543926715850830078125;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<19,0,true,AC_TRN> c8 = -0.4258556365966796875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<13,10,true> code_fixed_ss1_x2(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<17,10,true> sd = 0;
	ac_fixed<13,10,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<17,0,true,AC_TRN> c3 = 0.311004638671875;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<12,-4,true,AC_TRN> c4 = 0.021484375;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<15,-2,true,AC_TRN> c1 = 0.08736419677734375;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<7,-6,true,AC_TRN> c6 = -0.004638671875;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<19,1,true,AC_TRN> c2 = 0.578594207763671875;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<12,-4,true,AC_TRN> c5 = 0.020477294921875;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true,AC_TRN> c0 = -0.1602115631103515625;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true,AC_TRN> c8 = -0.9363861083984375;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<16,11,true> code_fixed_ss1_x3(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<16,11,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<18,-1,true,AC_TRN> c3 = -0.2373199462890625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<11,-7,true,AC_TRN> c4 = -0.0030059814453125;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true,AC_TRN> c1 = -0.5785961151123046875;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<8,-7,true,AC_TRN> c6 = 0.00299072265625;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<21,1,true,AC_TRN> c2 = 0.67735195159912109375;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<14,-4,true,AC_TRN> c5 = -0.025295257568359375;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<18,-4,true,AC_TRN> c0 = 0.0196964740753173828125;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<18,0,true,AC_TRN> c8 = 0.3561248779296875;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<13,10,true> code_fixed_ss1_x4(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<17,10,true> sd = 0;
	ac_fixed<13,10,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<14,-3,true,AC_TRN> c3 = 0.052642822265625;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<16,0,true,AC_TRN> c4 = 0.434234619140625;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<17,0,true,AC_TRN> c1 = -0.311004638671875;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<8,-5,true,AC_TRN> c6 = -0.0137939453125;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<17,-1,true,AC_TRN> c2 = -0.2373199462890625;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<16,0,true,AC_TRN> c5 = -0.3024139404296875;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<17,-3,true,AC_TRN> c0 = -0.06196117401123046875;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<15,-1,true,AC_TRN> c8 = -0.1680450439453125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<12,9,true> code_fixed_ss1_x5(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<16,9,true> sd = 0;
	ac_fixed<12,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<17,1,true,AC_TRN> c5 = 0.5717620849609375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<10,-3,true,AC_TRN> c6 = -0.035888671875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<11,-9,true,AC_TRN> c0 = -0.0005931854248046875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<17,0,true,AC_TRN> c3 = -0.43422698974609375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<12,-4,true,AC_TRN> c8 = -0.029571533203125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<17,1,true,AC_TRN> c4 = 0.512451171875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<5,-7,true,AC_TRN> c7 = 0.002197265625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<11,-7,true,AC_TRN> c2 = 0.0030059814453125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<13,-4,true,AC_TRN> c1 = 0.021484375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<11,9,true> code_fixed_ss1_x6(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<15,9,true> sd = 0;
	ac_fixed<11,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<14,-1,true,AC_TRN> c5 = -0.195770263671875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<10,-2,true,AC_TRN> c6 = -0.0986328125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<14,-5,true,AC_TRN> c0 = -0.00795745849609375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<16,0,true,AC_TRN> c3 = -0.3024139404296875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<12,-3,true,AC_TRN> c8 = -0.0430908203125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<16,1,true,AC_TRN> c4 = -0.57177734375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<5,-6,true,AC_TRN> c7 = 0.005859375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<13,-4,true,AC_TRN> c2 = -0.02529144287109375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<12,-4,true,AC_TRN> c1 = -0.020477294921875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<5,6,true> code_fixed_ss1_x7(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<9,6,true> sd = 0;
	ac_fixed<5,6,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<10,-2,true,AC_TRN> c5 = 0.0986328125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<8,-1,true,AC_TRN> c6 = -0.201171875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<7,-9,true,AC_TRN> c0 = -0.000762939453125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<8,-5,true,AC_TRN> c3 = 0.0137939453125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<4,-9,true,AC_TRN> c8 = -0.0009765625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<9,-3,true,AC_TRN> c4 = -0.035888671875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<8,0,true,AC_TRN> c7 = -0.30859375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<7,-7,true,AC_TRN> c2 = -0.00299072265625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<7,-6,true,AC_TRN> c1 = -0.004638671875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<3,5,true> code_fixed_ss1_x8(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<7,5,true> sd = 0;
	ac_fixed<3,5,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<5,-6,true,AC_TRN> c5 = -0.005859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<8,0,true,AC_TRN> c6 = -0.30859375;
	sd = sd + c6*v6;
	//Computation of c4*v4 in sd
	ac_fixed<4,-7,true,AC_TRN> c4 = 0.00244140625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<6,-1,true,AC_TRN> c7 = 0.1796875;
	sd = sd + c7*v7;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,12,true> code_fixed_ss1_y(ac_fixed<19,13,true,AC_TRN> v0,
	ac_fixed<13,10,true,AC_TRN> v1,ac_fixed<16,11,true,AC_TRN> v2,
	ac_fixed<13,10,true,AC_TRN> v3,ac_fixed<12,9,true,AC_TRN> v4,
	ac_fixed<11,9,true,AC_TRN> v5,ac_fixed<5,6,true,AC_TRN> v6,
	ac_fixed<3,5,true,AC_TRN> v7,ac_fixed<15,9,true,AC_TRN> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c3*v3 in sd
	ac_fixed<16,-1,true,AC_TRN> c3 = -0.1680450439453125;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<12,-4,true,AC_TRN> c4 = 0.029571533203125;
	sd = sd + c4*v4;
	//Computation of c1*v1 in sd
	ac_fixed<18,1,true,AC_TRN> c1 = 0.9363861083984375;
	sd = sd + c1*v1;
	//Computation of c6*v6 in sd
	ac_fixed<5,-8,true,AC_TRN> c6 = 0.0010986328125;
	sd = sd + c6*v6;
	//Computation of c2*v2 in sd
	ac_fixed<18,0,true,AC_TRN> c2 = 0.3561248779296875;
	sd = sd + c2*v2;
	//Computation of c5*v5 in sd
	ac_fixed<13,-3,true,AC_TRN> c5 = -0.0430755615234375;
	sd = sd + c5*v5;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true,AC_TRN> c0 = 0.42585659027099609375;
	sd = sd + c0*v0;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true,AC_TRN> c8 = -0.9401397705078125;
	sd = sd + c8*v8;

	//Computation of the final right shift
	s = s + sd;
	return s;
}






ac_fixed<19,12,true> code_fixed_ss2_x1(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,12,true> sd = 0;
	ac_fixed<19,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,1,true> c5 = -0.845585346221923828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<24,1,true> c6 = 0.76550638675689697265625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,-2,true> c0 = -0.063240528106689453125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true> c3 = -1.616137981414794921875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,0,true> c8 = -0.2869853973388671875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,-1,true> c4 = 0.17836344242095947265625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<26,2,true> c7 = -1.870077788829803466796875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,3,true> c2 = 3.07279884815216064453125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<25,1,true> c1 = 0.8939001560211181640625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<22,13,true> code_fixed_ss2_x2(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<26,13,true> sd = 0;
	ac_fixed<22,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<28,4,true> c5 = 4.898258507251739501953125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,3,true> c6 = 2.4793329536914825439453125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<28,3,true> c0 = 3.5518662929534912109375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<29,4,true> c3 = 4.9808134734630584716796875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true> c8 = 0.7820050716400146484375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<28,3,true> c4 = 2.48081505298614501953125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<30,4,true> c7 = 6.43144161999225616455078125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,1,true> c2 = 0.9982068836688995361328125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<30,4,true> c1 = 5.4780856668949127197265625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,12,true> code_fixed_ss2_x3(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,12,true> sd = 0;
	ac_fixed<19,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<25,3,true> c5 = -3.035640239715576171875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<26,3,true> c6 = -2.005886554718017578125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<22,-1,true> c0 = -0.16965329647064208984375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true> c3 = -1.2060902118682861328125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,0,true> c8 = -0.44967937469482421875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<25,2,true> c4 = -1.82608807086944580078125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<27,3,true> c7 = -2.07306659221649169921875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<25,2,true> c2 = -1.1034967899322509765625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<27,3,true> c1 = -2.093114435672760009765625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_ss2_x4(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<25,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<25,1,true> c5 = -0.757243335247039794921875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,3,true> c6 = -2.4723255932331085205078125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<29,4,true> c0 = -4.29140007495880126953125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<28,3,true> c3 = -2.7778887450695037841796875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true> c8 = 0.5067918300628662109375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<26,1,true> c4 = -0.6560055315494537353515625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<29,3,true> c7 = -2.3198604881763458251953125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<29,4,true> c2 = -4.9252796471118927001953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<30,4,true> c1 = -5.4284845292568206787109375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,12,true> code_fixed_ss2_x5(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,12,true> sd = 0;
	ac_fixed<20,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<27,4,true> c5 = -5.43100082874298095703125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,4,true> c6 = -6.06197845935821533203125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<29,5,true> c0 = -13.79710137844085693359375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<29,5,true> c3 = -12.890563786029815673828125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<22,1,true> c8 = 0.753965854644775390625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<27,3,true> c4 = -2.121588051319122314453125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<30,5,true> c7 = -11.792387545108795166015625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<29,5,true> c2 = -9.056646049022674560546875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<30,5,true> c1 = -15.3266203105449676513671875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<22,11,true> code_fixed_ss2_x6(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<26,11,true> sd = 0;
	ac_fixed<22,11,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<29,3,true> c5 = 3.34263980388641357421875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<30,3,true> c6 = 3.90282692015171051025390625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<31,4,true> c0 = 4.443961732089519500732421875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<31,4,true> c3 = 4.338144905865192413330078125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<22,-2,true> c8 = 0.085370957851409912109375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<29,2,true> c4 = 1.9357912838459014892578125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<32,4,true> c7 = 4.2111686281859874725341796875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<31,4,true> c2 = 5.029105700552463531494140625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<32,4,true> c1 = 6.716135554015636444091796875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<22,12,true> code_fixed_ss2_x7(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<26,12,true> sd = 0;
	ac_fixed<22,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<25,0,true> c5 = 0.424597442150115966796875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<28,2,true> c6 = 1.223392486572265625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<29,3,true> c0 = 2.11671493947505950927734375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<28,2,true> c3 = 1.5169831812381744384765625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<24,1,true> c8 = -0.51890742778778076171875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<25,-1,true> c4 = 0.156383991241455078125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<29,2,true> c7 = 1.1723602116107940673828125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<29,3,true> c2 = 2.65080974996089935302734375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<30,3,true> c1 = 2.727642543613910675048828125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<22,13,true> code_fixed_ss2_x8(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<26,13,true> sd = 0;
	ac_fixed<22,13,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<27,3,true> c5 = -3.038344323635101318359375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<27,2,true> c6 = -1.2639661133289337158203125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<25,0,true> c0 = 0.43289005756378173828125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,1,true> c3 = -0.563853323459625244140625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<23,1,true> c8 = -0.9525587558746337890625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<27,2,true> c4 = -1.9315639436244964599609375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<28,2,true> c7 = -1.90865238010883331298828125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<25,0,true> c2 = -0.4331484138965606689453125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<28,2,true> c1 = -1.64873488247394561767578125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,12,true> code_fixed_ss2_y(ac_fixed<19,12,true> v0,
	ac_fixed<22,13,true> v1,ac_fixed<19,12,true> v2,
	ac_fixed<21,12,true> v3, ac_fixed<20,12,true> v4,
	ac_fixed<22,11,true> v5,ac_fixed<22,12,true> v6,
	ac_fixed<22,13,true> v7,ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,4,true> c5 = 6.62574005126953125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,4,true> c6 = 4.583095550537109375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,5,true> c0 = 9.5538997650146484375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,5,true> c3 = 11.31696319580078125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true> c8 = -0.9401397705078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,3,true> c4 = 2.29593658447265625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,5,true> c7 = 11.06137561798095703125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<22,3,true> c2 = 3.1781139373779296875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<25,5,true> c1 = 10.4239597320556640625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<15,10,true> code_fixed_ss3_x1(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,10,true> sd = 0;
	ac_fixed<15,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<14,-6,true> c5 = -0.00672817230224609375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<18,-2,true> c6 = -0.06734371185302734375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<19,0,true> c0 = 0.4674587249755859375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<19,1,true> c3 = -0.735332489013671875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<13,-5,true> c8 = -0.009365081787109375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<14,-4,true> c4 = 0.027843475341796875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,1,true> c7 = -0.664020538330078125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<17,-1,true> c2 = 0.19712066650390625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<18,0,true> c1 = 0.310337066650390625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,9,true> code_fixed_ss3_x2(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,9,true> sd = 0;
	ac_fixed<15,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<19,-2,true> c5 = -0.105099201202392578125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,-2,true> c6 = 0.06264591217041015625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true> c0 = -0.240398406982421875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<18,-1,true> c3 = 0.1323070526123046875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,-2,true> c8 = -0.10694122314453125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<20,1,true> c4 = 0.7939243316650390625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true> c7 = 0.19321727752685546875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<19,0,true> c2 = -0.2651958465576171875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<18,-1,true> c1 = 0.167690277099609375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,9,true> code_fixed_ss3_x3(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,9,true> sd = 0;
	ac_fixed<15,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<19,-2,true> c5 = 0.07130336761474609375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-1,true> c6 = 0.223862171173095703125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<19,-1,true> c0 = -0.2237567901611328125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<19,0,true> c3 = 0.441753387451171875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<16,-3,true> c8 = -0.0582332611083984375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<19,0,true> c4 = -0.3608875274658203125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<17,-3,true> c7 = 0.03775882720947265625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<19,0,true> c2 = -0.2625331878662109375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<19,0,true> c1 = -0.31343841552734375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,9,true> code_fixed_ss3_x4(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,9,true> sd = 0;
	ac_fixed<15,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,-1,true> c5 = 0.188554286956787109375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<17,-4,true> c6 = 0.0215740203857421875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<11,-9,true> c0 = 0.0005397796630859375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<20,1,true> c3 = 0.59668731689453125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<18,-1,true> c8 = -0.1764163970947265625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<18,-1,true> c4 = 0.1420154571533203125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<18,-2,true> c7 = 0.08209323883056640625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<19,0,true> c2 = -0.30939483642578125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = -0.5460262298583984375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,9,true> code_fixed_ss3_x5(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,9,true> sd = 0;
	ac_fixed<15,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,0,true> c5 = 0.3912525177001953125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-1,true> c6 = -0.207538604736328125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = -0.3852100372314453125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<17,-2,true> c3 = -0.0800685882568359375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<16,-3,true> c8 = 0.0547313690185546875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<19,0,true> c4 = 0.312343597412109375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true> c7 = -0.2043704986572265625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,1,true> c2 = -0.57442474365234375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<19,0,true> c1 = -0.4520778656005859375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_ss3_x6(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,0,true> c5 = 0.4253699779510498046875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true> c6 = 0.4569835662841796875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,-1,true> c0 = -0.139317035675048828125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<20,0,true> c3 = -0.369842529296875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,-3,true> c8 = -0.0595951080322265625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<18,-2,true> c4 = 0.08564281463623046875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-1,true> c7 = -0.16064739227294921875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true> c2 = 0.43892002105712890625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<20,0,true> c1 = 0.4171733856201171875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_ss3_x7(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,0,true> c5 = 0.4720642566680908203125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,-1,true> c6 = 0.1298201084136962890625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true> c0 = -0.100472927093505859375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<19,-1,true> c3 = -0.144329071044921875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<18,-2,true> c8 = -0.11407756805419921875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<17,-3,true> c4 = -0.034999847412109375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-1,true> c7 = 0.15502643585205078125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true> c2 = 0.32707691192626953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<16,-4,true> c1 = 0.02993011474609375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<16,10,true> code_fixed_ss3_x8(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<20,10,true> sd = 0;
	ac_fixed<16,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<19,-2,true> c5 = -0.088316440582275390625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,1,true> c6 = 0.5760498046875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = 0.326335906982421875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<14,-5,true> c3 = 0.0149517059326171875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<18,-1,true> c8 = -0.215465545654296875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<16,-3,true> c4 = 0.0329418182373046875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true> c7 = 0.2324161529541015625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<19,0,true> c2 = 0.26512908935546875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<19,0,true> c1 = -0.2598667144775390625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,12,true> code_fixed_ss3_y(ac_fixed<15,10,true> v0,
	ac_fixed<15,9,true> v1, ac_fixed<15,9,true> v2,
	ac_fixed<15,9,true> v3, ac_fixed<15,9,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<18,11,true> v6,
	ac_fixed<16,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,2,true> c5 = 1.61322784423828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,1,true> c6 = -0.785984039306640625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,3,true> c0 = 2.1134033203125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<18,2,true> c3 = 1.36126708984375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true> c8 = -0.9401397705078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<16,0,true> c4 = 0.385345458984375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<19,2,true> c7 = 1.70235443115234375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<16,0,true> c2 = -0.3175811767578125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<19,3,true> c1 = 2.884765625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<16,9,true> code_fixed_ss4_x1(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<20,9,true> sd = 0;
	ac_fixed<16,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,0,true> c5 = -0.392608642578125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,0,true> c6 = -0.476531982421875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,1,true> c0 = -0.667552947998046875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,2,true> c3 = -1.395000457763671875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<14,-6,true> c8 = -0.006855010986328125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<20,-1,true> c4 = -0.129737377166748046875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<22,2,true> c7 = -1.356586456298828125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,0,true> c2 = -0.277133464813232421875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = -0.67897796630859375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,8,true> code_fixed_ss4_x2(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,-1,true> c5 = -0.2147190570831298828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,0,true> c6 = -0.304637908935546875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,-1,true> c0 = 0.2468593120574951171875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<23,1,true> c3 = 0.611095905303955078125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<16,-6,true> c8 = 0.0064640045166015625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<21,-2,true> c4 = 0.075115680694580078125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<23,1,true> c7 = 0.51686954498291015625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true> c2 = -0.07548296451568603515625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 0.579477787017822265625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss4_x3(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,1,true> c5 = -0.66218090057373046875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,1,true> c6 = -0.578578948974609375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = 0.4051647186279296875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<20,0,true> c3 = 0.33291721343994140625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,-3,true> c8 = -0.04766941070556640625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<21,0,true> c4 = -0.407238483428955078125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,0,true> c7 = -0.3817386627197265625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,-1,true> c2 = -0.242565155029296875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = 0.6345615386962890625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss4_x4(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,0,true> c5 = 0.4836237430572509765625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,0,true> c6 = 0.435732364654541015625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,2,true> c0 = 1;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,2,true> c3 = 1.164875030517578125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true> c8 = -0.12604618072509765625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<19,-4,true> c4 = 0.0293219089508056640625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<23,1,true> c7 = 0.928656101226806640625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true> c2 = 0.49872601032257080078125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 0.70601367950439453125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,10,true> code_fixed_ss4_x5(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,2,true> c5 = -1.35511875152587890625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,2,true> c6 = -1.19145488739013671875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<25,4,true> c0 = -4.806136608123779296875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<25,4,true> c3 = -5.045399188995361328125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<21,0,true> c8 = 0.25283145904541015625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<19,-3,true> c4 = -0.059306621551513671875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,4,true> c7 = -4.508141040802001953125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<24,2,true> c2 = -1.9179141521453857421875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<24,4,true> c1 = -4.60383319854736328125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,9,true> code_fixed_ss4_x6(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,9,true> sd = 0;
	ac_fixed<20,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<26,2,true> c5 = 1.2644636631011962890625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<25,2,true> c6 = 1.08701038360595703125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<26,2,true> c0 = 1.565958917140960693359375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<26,2,true> c3 = 1.967296183109283447265625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<21,-3,true> c8 = 0.041903555393218994140625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<25,0,true> c4 = 0.456110179424285888671875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<26,2,true> c7 = 1.233251631259918212890625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<26,1,true> c2 = 0.6784044802188873291015625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<26,3,true> c1 = 2.3867800235748291015625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,8,true> code_fixed_ss4_x7(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,-2,true> c5 = 0.092687129974365234375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<18,-3,true> c6 = -0.032674312591552734375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<22,0,true> c0 = -0.476015567779541015625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true> c3 = -0.3554713726043701171875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-2,true> c8 = -0.1152133941650390625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,-1,true> c4 = -0.18889367580413818359375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-2,true> c7 = 0.121052265167236328125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<18,-5,true> c2 = -0.0151908397674560546875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<21,0,true> c1 = -0.424787044525146484375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,9,true> code_fixed_ss4_x8(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,9,true> sd = 0;
	ac_fixed<19,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,-3,true> c5 = -0.05142629146575927734375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,-1,true> c6 = 0.2144186496734619140625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = -0.57834279537200927734375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,1,true> c3 = -0.58572065830230712890625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<19,-4,true> c8 = 0.02731668949127197265625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,-2,true> c4 = 0.10480368137359619140625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<21,-2,true> c7 = 0.06253349781036376953125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<23,-1,true> c2 = -0.125448286533355712890625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<24,2,true> c1 = -1.10722827911376953125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,12,true> code_fixed_ss4_y(ac_fixed<16,10,true> v0,
	ac_fixed<17,9,true> v1, ac_fixed<17,9,true> v2,
	ac_fixed<18,9,true> v3, ac_fixed<18,9,true> v4,
	ac_fixed<20,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<19,10,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,4,true> c5 = 6.8329315185546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,4,true> c6 = 4.51910400390625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,5,true> c0 = 9.537261962890625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<21,5,true> c3 = 11.31988525390625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true> c8 = -0.9401397705078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<20,3,true> c4 = 2.36002349853515625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<21,5,true> c7 = 10.692535400390625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,3,true> c2 = 2.8130645751953125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<20,5,true> c1 = 10.787994384765625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}	





ac_fixed<17,9,true> code_fixed_ss5_x1(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,9,true> sd = 0;
	ac_fixed<17,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,1,true> c5 = -0.597916126251220703125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,1,true> c6 = -0.55623912811279296875;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,0,true> c0 = -0.267075061798095703125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<21,1,true> c3 = -0.87513256072998046875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<19,-2,true> c8 = -0.086926937103271484375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<21,0,true> c4 = -0.411656856536865234375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<21,1,true> c7 = -0.73088741302490234375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,-1,true> c2 = -0.1282417774200439453125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = -0.542592525482177734375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss5_x2(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,-1,true> c5 = -0.235429286956787109375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,-1,true> c6 = -0.22387790679931640625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = -0.620391368865966796875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<21,0,true> c3 = -0.3734188079833984375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-2,true> c8 = 0.084208011627197265625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true> c4 = 0.3109991550445556640625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-1,true> c7 = -0.164807796478271484375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true> c2 = -0.292396068572998046875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<20,-2,true> c1 = -0.1096515655517578125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,10,true> code_fixed_ss5_x3(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,2,true> c5 = -1.02798366546630859375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,0,true> c6 = -0.2907657623291015625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,-1,true> c0 = -0.151487827301025390625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<19,-1,true> c3 = 0.23436260223388671875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<18,-3,true> c8 = -0.048210620880126953125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,1,true> c4 = -0.863583087921142578125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<18,-2,true> c7 = -0.0648479461669921875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,-1,true> c2 = 0.242127895355224609375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 0.587543010711669921875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,8,true> code_fixed_ss5_x4(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,1,true> c5 = 0.691113948822021484375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,0,true> c6 = 0.425144195556640625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,2,true> c0 = 1.2258260250091552734375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<23,2,true> c3 = 1.495610713958740234375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-2,true> c8 = -0.1102955341339111328125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<21,-1,true> c4 = 0.241015911102294921875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<23,2,true> c7 = 1.1385097503662109375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true> c2 = 0.4833700656890869140625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<23,1,true> c1 = 0.8324515819549560546875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,9,true> code_fixed_ss5_x5(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,9,true> sd = 0;
	ac_fixed<17,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,1,true> c5 = -0.87270259857177734375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,1,true> c6 = -0.82956027984619140625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,3,true> c0 = -2.03562259674072265625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<23,3,true> c3 = -2.15955257415771484375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<19,-2,true> c8 = 0.08910846710205078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<14,-7,true> c4 = -0.003904819488525390625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<22,2,true> c7 = -1.8498935699462890625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<24,2,true> c2 = -1.1819827556610107421875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<24,3,true> c1 = -2.192136287689208984375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,9,true> code_fixed_ss5_x6(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,9,true> sd = 0;
	ac_fixed<19,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<25,2,true> c5 = 1.174879550933837890625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<23,1,true> c6 = 0.932959079742431640625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = 0.9137384891510009765625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,2,true> c3 = 1.2612340450286865234375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<21,-2,true> c8 = 0.074152469635009765625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<23,0,true> c4 = 0.429005146026611328125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<23,1,true> c7 = 0.7520391941070556640625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<25,1,true> c2 = 0.581430375576019287109375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<25,2,true> c1 = 1.4487221240997314453125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,8,true> code_fixed_ss5_x7(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,0,true> c5 = -0.4653873443603515625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<18,-3,true> c6 = 0.044962406158447265625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = -1;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<21,0,true> c3 = -0.401638031005859375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<21,-1,true> c8 = -0.1488564014434814453125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<23,1,true> c4 = -0.654040813446044921875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-1,true> c7 = 0.22469806671142578125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true> c2 = 0.1058385372161865234375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c1 = -0.3486545085906982421875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,8,true> code_fixed_ss5_x8(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<22,0,true> c5 = 0.3472690582275390625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<18,-3,true> c6 = 0.053427219390869140625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<19,-3,true> c0 = 0.037250518798828125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,1,true> c3 = -0.589764118194580078125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<19,-3,true> c8 = 0.03258800506591796875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,0,true> c4 = 0.3587396144866943359375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<22,1,true> c7 = -0.50769805908203125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<23,0,true> c2 = -0.40401709079742431640625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<23,1,true> c1 = -0.707618236541748046875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,12,true> code_fixed_ss5_y(ac_fixed<17,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<18,10,true> v2,
	ac_fixed<17,8,true> v3, ac_fixed<17,9,true> v4,
	ac_fixed<19,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<17,8,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,4,true> c5 = 6.98260498046875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,4,true> c6 = 4.472015380859375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,5,true> c0 = 9.55084228515625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<20,5,true> c3 = 11.200286865234375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true> c8 = -0.9401397705078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<19,3,true> c4 = 2.360076904296875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,5,true> c7 = 10.651458740234375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,3,true> c2 = 2.76476287841796875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<21,5,true> c1 = 10.5360565185546875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}


ac_fixed<16,9,true> code_fixed_ss6_x1(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<20,9,true> sd = 0;
	ac_fixed<16,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,1,true> c5 = -0.5974979400634765625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,1,true> c6 = -0.6604251861572265625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,1,true> c0 = -0.9293975830078125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,2,true> c3 = -1.65697002410888671875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<15,-5,true> c8 = -0.01459407806396484375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<21,0,true> c4 = -0.308237552642822265625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<22,2,true> c7 = -1.5586261749267578125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,0,true> c2 = -0.379761219024658203125;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,2,true> c1 = -1.148738861083984375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss6_x2(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,-2,true> c5 = -0.0853478908538818359375;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,-2,true> c6 = -0.1196651458740234375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,-2,true> c0 = -0.07264041900634765625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true> c3 = 0.356800556182861328125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<19,-3,true> c8 = 0.051532745361328125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<23,0,true> c4 = 0.37957286834716796875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<22,0,true> c7 = 0.4557883739471435546875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true> c2 = -0.07580125331878662109375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c1 = 0.464209079742431640625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,10,true> code_fixed_ss6_x3(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,10,true> sd = 0;
	ac_fixed<17,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,1,true> c5 = -0.7825565338134765625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<20,1,true> c6 = -0.52968597412109375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = 0.49120235443115234375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<20,0,true> c3 = 0.48855686187744140625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,-3,true> c8 = -0.0604000091552734375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,1,true> c4 = -0.533857822418212890625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<19,-1,true> c7 = -0.17443370819091796875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<17,-4,true> c2 = -0.0298366546630859375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 0.7054901123046875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,9,true> code_fixed_ss6_x4(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<23,9,true> sd = 0;
	ac_fixed<19,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,0,true> c5 = 0.4874660968780517578125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<22,0,true> c6 = 0.3917086124420166015625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<25,2,true> c0 = 1.288856983184814453125;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<25,2,true> c3 = 1.451045989990234375;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<22,-1,true> c8 = -0.14632833003997802734375;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<21,-3,true> c4 = -0.045719206333160400390625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<25,2,true> c7 = 1.10436379909515380859375;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<25,1,true> c2 = 0.517961025238037109375;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<24,1,true> c1 = 0.94910919666290283203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,10,true> code_fixed_ss6_x5(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<23,2,true> c5 = -1.028922557830810546875;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,1,true> c6 = -0.9870395660400390625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<24,3,true> c0 = -3.0521240234375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<24,3,true> c3 = -3.19485950469970703125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-1,true> c8 = 0.151564121246337890625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<20,-2,true> c4 = -0.0864632129669189453125;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<24,3,true> c7 = -2.935951709747314453125;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<24,2,true> c2 = -1.3712866306304931640625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<24,3,true> c1 = -2.9714145660400390625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,9,true> code_fixed_ss6_x6(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<24,9,true> sd = 0;
	ac_fixed<20,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<25,1,true> c5 = 0.979584991931915283203125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<24,1,true> c6 = 0.8449132442474365234375;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<25,1,true> c0 = 0.65552580356597900390625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<25,1,true> c3 = 0.978725254535675048828125;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<22,-2,true> c8 = 0.083691418170928955078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<25,0,true> c4 = 0.3544174134731292724609375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<24,0,true> c7 = 0.42526590824127197265625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<25,0,true> c2 = 0.4157597124576568603515625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<26,2,true> c1 = 1.263010323047637939453125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,8,true> code_fixed_ss6_x7(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<21,8,true> sd = 0;
	ac_fixed<17,8,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<17,-5,true> c5 = 0.0138523578643798828125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<15,-6,true> c6 = -0.0065402984619140625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<23,1,true> c0 = -0.6363646984100341796875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<22,0,true> c3 = -0.4085009098052978515625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<20,-2,true> c8 = -0.117447376251220703125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,-1,true> c4 = -0.2258586883544921875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<20,-2,true> c7 = 0.11992645263671875;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<19,-4,true> c2 = -0.0255870819091796875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c1 = -0.4553165435791015625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,9,true> code_fixed_ss6_x8(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<22,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<21,-1,true> c5 = 0.200946807861328125;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<21,0,true> c6 = 0.318109989166259765625;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<20,-2,true> c0 = -0.073497295379638671875;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<21,-1,true> c3 = -0.2054183483123779296875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,-5,true> c8 = 0.0113756656646728515625;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<22,-1,true> c4 = 0.18824446201324462890625;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<21,-1,true> c7 = 0.2266485691070556640625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<21,-2,true> c2 = -0.07414424419403076171875;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<22,0,true> c1 = -0.5;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<15,12,true> code_fixed_ss6_y(ac_fixed<16,9,true> v0,
	ac_fixed<18,9,true> v1, ac_fixed<17,10,true> v2,
	ac_fixed<19,9,true> v3, ac_fixed<18,10,true> v4,
	ac_fixed<20,9,true> v5, ac_fixed<17,8,true> v6,
	ac_fixed<18,9,true> v7, ac_fixed<15,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<15,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<20,4,true> c5 = 6.8160552978515625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<19,4,true> c6 = 4.492706298828125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<21,5,true> c0 = 9.528228759765625;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<21,5,true> c3 = 11.340728759765625;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<17,1,true> c8 = -0.9401397705078125;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<20,3,true> c4 = 2.34548187255859375;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<21,5,true> c7 = 10.6934967041015625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<20,3,true> c2 = 2.8941802978515625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<21,5,true> c1 = 10.6976776123046875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}














ac_fixed<18,11,true> code_fixed_LGS_t2(ac_fixed<21,12,true> v0,ac_fixed<18,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<18,-2,true> c0 = -0.0859375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,2,true> c1 = 1;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t10(ac_fixed<18,11,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.99266815185546875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t19(ac_fixed<18,11,true> v0,ac_fixed<18,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,0,true> c0 = -0.3468532562255859375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,2,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t27(ac_fixed<18,11,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.893314361572265625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t36(ac_fixed<18,11,true> v0,ac_fixed<18,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,0,true> c0 = -0.41431427001953125;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t44(ac_fixed<18,11,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.867046356201171875;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t53(ac_fixed<18,11,true> v0,ac_fixed<18,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,0,true> c0 = -0.4839382171630859375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t61(ac_fixed<18,11,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = 0.83121490478515625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_LGS_t70(ac_fixed<18,11,true> v0,ac_fixed<18,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,1,true> c0 = -0.648845672607421875;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t78(ac_fixed<18,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,1,true> c0 = 0.7407741546630859375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,12,true> code_fixed_LGS_t87(ac_fixed<18,11,true> v0,ac_fixed<17,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,12,true> sd = 0;
	ac_fixed<18,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,2,true> c0 = -1.13352203369140625;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t95(ac_fixed<18,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,1,true> c0 = 0.512348175048828125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,12,true> code_fixed_LGS_t104(ac_fixed<18,11,true> v0,ac_fixed<17,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<18,12,true> sd = 0;
	ac_fixed<17,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,3,true> c0 = -2.8862152099609375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<19,1,true> c1 = 1;
	sd = sd + v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<20,9,true> code_fixed_LGS_t112(ac_fixed<17,12,true> v0)
{
	//Declaration of sums sd and s
	ac_fixed<18,9,true> sd = 0;
	ac_fixed<18,9,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true> c0 = 0.09544086456298828125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,10,true> code_fixed_LGS_t119(ac_fixed<18,11,true> v0,ac_fixed<18,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,10,true> sd = 0;
	ac_fixed<18,10,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,2,true> c1 = 1.478748321533203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t126(ac_fixed<18,11,true> v0,ac_fixed<18,10,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = 0.8396816253662109375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t133(ac_fixed<18,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<21,1,true> c1 = 0.53932857513427734375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t140(ac_fixed<18,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,0,true> c1 = 0.4195957183837890625;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t147(ac_fixed<18,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,0,true> c1 = 0.370113372802734375;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<19,11,true> code_fixed_LGS_t154(ac_fixed<18,11,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<19,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<22,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,0,true> c1 = 0.344310760498046875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_LGS_t161(ac_fixed<21,12,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<19,-2,true> c1 = 0.085937976837158203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_LGS_t169(ac_fixed<21,12,true> v0,ac_fixed<19,11,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,1,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<19,-2,true> c1 = 0.085937976837158203125;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t170(ac_fixed<21,12,true> v0, ac_fixed<19,11,true> v1,ac_fixed<19,11,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true> c2 = 0.3468532562255859375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<19,-2,true> c0 = -0.085937976837158203125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t171(ac_fixed<19,11,true> v0, ac_fixed<19,11,true> v1, ac_fixed<19,11,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true> c2 = 0.41431427001953125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = -0.3468532562255859375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t172(ac_fixed<19,11,true> v0, ac_fixed<19,11,true> v1, ac_fixed<19,11,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,0,true> c2 = 0.48393726348876953125;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = -0.41431427001953125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t173(ac_fixed<19,11,true> v0, ac_fixed<19,11,true> v1,ac_fixed<19,11,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,1,true> c2 = 0.6488437652587890625;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c0 = -0.48393726348876953125;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_t174(ac_fixed<19,11,true> v0, ac_fixed<19,11,true> v1,ac_fixed<18,10,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<20,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<22,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<21,2,true> c2 = 1.1335201263427734375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<21,1,true> c0 = -0.6488437652587890625;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,11,true> code_fixed_LGS_t175(ac_fixed<19,11,true> v0, ac_fixed<18,10,true> v1,ac_fixed<18,9,true> v2)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c1*v1 in sd
	ac_fixed<20,1,true> c1 = 1;
	sd = sd + v1;
	//Computation of c2*v2 in sd
	ac_fixed<20,3,true> c2 = 2.8862152099609375;
	sd = sd + c2*v2;
	//Computation of c0*v0 in sd
	ac_fixed<21,2,true> c0 = -1.1335201263427734375;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,11,true> code_fixed_LGS_t176(ac_fixed<18,10,true>v0,ac_fixed<18,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,3,true> c0 = -2.8862152099609375;
	sd = sd + c0*v0;
	//Computation of c1*v1 in sd
	ac_fixed<20,4,true> c1 = -4.209686279296875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<21,12,true> code_fixed_LGS_x1(ac_fixed<21,12,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<22,12,true> sd = 0;
	ac_fixed<21,12,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<24,2,true> c0 = 1;
	sd = sd + v0;
	//Computation of c1*v1 in sd
	ac_fixed<11,-8,true> c1 = 0.0013408660888671875;
	sd = sd + c1*v1;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_x2(ac_fixed<18,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,-5,true> c1 = 0.0156008899211883544921875;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<12,2,true> c0= 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_x3(ac_fixed<18,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,-3,true> c1 = 0.045310497283935546875;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<14,2,true> c0= 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_x4(ac_fixed<18,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,-2,true> c1 = 0.1224234104156494140625;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<15,2,true> c0= 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_x5(ac_fixed<18,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,0,true> c1 = 0.2917652130126953125;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<17,2,true> c0 = 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<18,11,true> code_fixed_LGS_x6(ac_fixed<18,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<19,11,true> sd = 0;
	ac_fixed<18,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<21,1,true> c1 = 0.54097843170166015625;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<18,2,true> c0 = 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,11,true> code_fixed_LGS_x7(ac_fixed<17,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,1,true> c1 = 0.6442661285400390625;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<17,2,true> c0 = 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<17,11,true> code_fixed_LGS_x8(ac_fixed<17,11,true> v0,ac_fixed<13,9,true> v1)
{
	//Declaration of sums sd and s
	ac_fixed<18,11,true> sd = 0;
	ac_fixed<17,11,true> s = 0;

	//Computation of c0*v0 in sd
	ac_fixed<20,0,true> c1 = 0.43568325042724609375;
	sd = sd + c1*v1;
	//Computation of c1*v1 in sd
	ac_fixed<16,2,true> c0 = 1;
	sd = sd + c0*v0;

	//Computation of the final right shift
	s = s + sd;
	return s;
}

ac_fixed<13,12,true> code_fixed_LGS_y(ac_fixed<21,12,true> v0,
	ac_fixed<18,11,true> v1, ac_fixed<18,11,true> v2,
	ac_fixed<18,11,true> v3,ac_fixed<18,11,true> v4,
	ac_fixed<18,11,true> v5, ac_fixed<17,11,true> v6,
	ac_fixed<17,11,true> v7,ac_fixed<13,9,true> v8)
{
	//Declaration of sums sd and s
	ac_fixed<17,12,true> sd = 0;
	ac_fixed<13,12,true> s = 0;

	//Computation of c5*v5 in sd
	ac_fixed<17,1,true> c5 = -0.7138824462890625;
	sd = sd + c5*v5;
	//Computation of c6*v6 in sd
	ac_fixed<17,1,true> c6 = -0.59698486328125;
	sd = sd + c6*v6;
	//Computation of c0*v0 in sd
	ac_fixed<18,1,true> c0 = -0.61952972412109375;
	sd = sd + c0*v0;
	//Computation of c3*v3 in sd
	ac_fixed<16,0,true> c3 = 0.38153076171875;
	sd = sd + c3*v3;
	//Computation of c8*v8 in sd
	ac_fixed<15,1,true> c8 = -0.94012451171875;
	sd = sd + c8*v8;
	//Computation of c4*v4 in sd
	ac_fixed<15,-1,true> c4 = -0.209686279296875;
	sd = sd + c4*v4;
	//Computation of c7*v7 in sd
	ac_fixed<16,0,true> c7 = -0.3147125244140625;
	sd = sd + c7*v7;
	//Computation of c2*v2 in sd
	ac_fixed<16,0,true> c2 = 0.3603668212890625;
	sd = sd + c2*v2;
	//Computation of c1*v1 in sd
	ac_fixed<16,0,true> c1 = 0.3055572509765625;
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
	double Du = imp*powf(2,-7),
		Du1 = 0, Du2 = 0, Du3 = 0, Du4 = 0, Du5 = 0, Du6 = 0, Du7 = 0, Du8 = 0, 
		Dy = 0, Dy1 = 0, Dy2 = 0, Dy3 = 0, Dy4 = 0, Dy5 = 0, Dy6 = 0, Dy7 = 0, Dy8 = 0,
		maxDy=-1000,minDy=1000,
		maxy=-1000,miny=1000;

	ac_fixed<18,9,true> u=imp;

	ac_fixed<20,9,true> DFIu1=0,DFIu2=0,DFIu3=0,DFIu4=0,DFIu5=0,DFIu6=0,DFIu7=0,DFIu8=0;
	ac_fixed<20,12,true> DFIy = 0, DFIy1 = 0, DFIy2 = 0, DFIy3 = 0, DFIy4 = 0, DFIy5 = 0, DFIy6 = 0, DFIy7 = 0, DFIy8 = 0;


	ac_fixed<17,12,true> Rt1=0, Rx3=0,Rxp3=0,  Rx5=0,Rxp5=0, Rx6=0,Rxp6=0, Rx7=0,Rxp7=0;
	ac_fixed<17,11,true> Rt2=0, Rt5=0; 
	ac_fixed<18,12,true> Rt3=0, Rt4=0, Rx1=0,Rxp1=0, Rx2=0,Rxp2=0, Rx4=0,Rxp4=0, Rx8=0,Rxp8=0;
	ac_fixed<18,11,true> Rt6=0;
	ac_fixed<16,11,true> Rt7=0, Rt8=0;
	ac_fixed<16,12,true> Ry=0;

	ac_fixed<15,10,true> x31=0, xp31=0;
	ac_fixed<15,9,true> x34=0, xp34=0, x32=0, xp32=0,x35=0, xp35=0,x33=0,xp33=0;
	ac_fixed<18,11,true> x36=0, xp36=0, x37=0, xp37=0;
	ac_fixed<16,10,true> x38=0, xp38=0;
	ac_fixed<15,12,true> y3=0;

	ac_fixed<19,13,true,AC_TRN>   x11 =0, xp11 =0;
	ac_fixed<13,10,true,AC_TRN>   x12 =0, xp12 =0;
	ac_fixed<16,11,true,AC_TRN>   x13 =0, xp13 =0;
	ac_fixed<13,10,true,AC_TRN>   x14 =0, xp14 =0;
	ac_fixed<12,9,true,AC_TRN>   x15 =0, xp15 =0;
	ac_fixed<11,9,true,AC_TRN>   x16 =0, xp16 =0;
	ac_fixed<5,6,true,AC_TRN>   x17 =0, xp17 =0;
	ac_fixed<3,5,true,AC_TRN>   x18 =0, xp18 =0;
	ac_fixed<15,9,true,AC_TRN>  y1 =0;

	ac_fixed<19,12,true> x21=0, xp21=0, x23=0, xp23=0;
	ac_fixed<22,13,true> x22=0,xp22=0, x28=0,xp28=0;
	ac_fixed<21,12,true> x24=0, xp24=0;
	ac_fixed<20,12,true> x25=0,xp25=0;
	ac_fixed<22,11,true> x26=0, xp26=0;
	ac_fixed<22,12,true> x27=0,xp27=0;
	ac_fixed<15,12,true> y2=0;

	ac_fixed<16,10,true> x41=0, xp41=0;
	ac_fixed<17,9,true> x42=0, xp42=0;
	ac_fixed<17,9,true> x43=0, xp43=0;
	ac_fixed<18,9,true> x44=0, xp44=0;
	ac_fixed<18,9,true> x45=0, xp45=0;
	ac_fixed<20,11,true> x46=0, xp46=0;
	ac_fixed<17,11,true> x47=0, xp47=0;
	ac_fixed<19,10,true> x48=0, xp48=0;
	ac_fixed<15,12,true> y4=0;

	ac_fixed<17,9,true> x51 =0, xp51 =0;
	ac_fixed<18,9,true>  x52 =0, xp52 =0;
	ac_fixed<18,10,true> x53 =0, xp53 =0;
	ac_fixed<17,8,true>  x54 =0, xp54 =0;
	ac_fixed<17,9,true> x55 =0, xp55 =0;
	ac_fixed<19,9,true>  x56 =0, xp56 =0;
	ac_fixed<17,8,true> x57 =0, xp57 =0;
	ac_fixed<17,8,true>  x58 =0, xp58 =0;
	ac_fixed<15,14,true> y5 = 0;


	ac_fixed<16,9,true> x61 =0, xp61 =0;
	ac_fixed<18,9,true>  x62 =0, xp62 =0;
	ac_fixed<17,10,true> x63 =0, xp63 =0;
	ac_fixed<19,9,true>  x64 =0, xp64 =0;
	ac_fixed<18,10,true> x65 =0, xp65 =0;
	ac_fixed<20,9,true>  x66 =0, xp66 =0;
	ac_fixed<17,8,true> x67 =0, xp67 =0;
	ac_fixed<18,9,true>  x68 =0, xp68 =0;
	ac_fixed<15,14,true> y6=0;



	ac_fixed<18,11,true>  xL6=0, xpL6=0,xL5=0, xpL5=0,xL4=0, xpL4=0, xL3=0, xpL3=0,xL2=0, xpL2=0,
		tL174=0, tL173=0,tL171=0, tL172=0,tL170=0,
		tL2=0, tL10=0,tL19=0, tL27=0, tL36=0, tL44=0, tL53=0,tL61=0,tL78=0,tL95=0;
	ac_fixed<18,12,true>  tL70=0, tL87=0;
	ac_fixed<17,12,true> tL104=0;
	ac_fixed<18,9,true> tL112=0;
	ac_fixed<18,10,true> tL119=0;
	ac_fixed<19,11,true> tL126=0,tL140=0,tL147=0, tL133=0, tL154=0;
	ac_fixed<21,12,true> xL1=0, xpL1=0,tL169=0,tL161=0;
	ac_fixed<17,11,true> xL8=0, xpL8=0, xL7=0, xpL7=0,tL176=0,tL175=0;
	ac_fixed<13,12,true> yL=0;

	Du = u.to_double();


	int cpt = 1;
	while(cpt<=1000){

		Dy = double_DFI(Du,Du1, Du2, Du3, Du4, Du5, Du6, Du7, Du8,Dy1, Dy2, Dy3, Dy4, Dy5, Dy6, Dy7, Dy8);
		Du8 = Du7; Du7 = Du6; Du6 = Du5; Du5 = Du4; Du4 = Du3; Du3 = Du2; Du2 = Du1; Du1=Du;
		Dy8 = Dy7; Dy7 = Dy6; Dy6 = Dy5; Dy5 = Dy4; Dy4 = Dy3; Dy3 = Dy2; Dy2 = Dy1; Dy1=Dy;
		

		DFIy = code_fixed_DFI(u,DFIu1,DFIu2,DFIu3,DFIu4,DFIu5,DFIu6,DFIu7,DFIu8, DFIy1,DFIy2,DFIy3,DFIy4,DFIy5,DFIy6,DFIy7,DFIy8);
		DFIu8 = DFIu7; DFIu7 = DFIu6; DFIu6 = DFIu5; DFIu5 = DFIu4; DFIu4 = DFIu3; DFIu3 = DFIu2; DFIu2 = DFIu1; DFIu1=u;
		DFIy8 = DFIy7; DFIy7 = DFIy6; DFIy6 = DFIy5; DFIy5 = DFIy4; DFIy4 = DFIy3; DFIy3 = DFIy2; DFIy2 = DFIy1; DFIy1=DFIy;

		Rt1 = code_fixed_rho_t1(Rx1,u);
		Rt2 = code_fixed_rho_t2(Rx2);
		Rt3 = code_fixed_rho_t3(Rx3);
		Rt4 = code_fixed_rho_t4(Rx4);
		Rt5 = code_fixed_rho_t5(Rx5);
		Rt6 = code_fixed_rho_t6(Rx6);
		Rt7 = code_fixed_rho_t7(Rx7);
		Rt8 = code_fixed_rho_t8(Rx8);
		Rxp1 = code_fixed_rho_x1(Rt1, Rt2, Rx1, u);
		Rxp2 = code_fixed_rho_x2(Rt1, Rt3, Rx2, u);
		Rxp3 = code_fixed_rho_x3(Rt1, Rt4, Rx3, u);
		Rxp4 = code_fixed_rho_x4(Rt1, Rt5, Rx4, u);
		Rxp5 = code_fixed_rho_x5(Rt1, Rt6, Rx5, u);
		Rxp6 = code_fixed_rho_x6(Rt1, Rt7, Rx6, u);
		Rxp7 = code_fixed_rho_x7(Rt1, Rt8, Rx7, u);
		Rxp8 = code_fixed_rho_x8(Rt1, Rx8, u);
		Ry = Rt1;
		Rx1 = Rxp1; Rx2 = Rxp2; Rx3 = Rxp3; Rx4 = Rxp4; Rx5 = Rxp5; Rx6 = Rxp6; Rx7 = Rxp7; Rx8 = Rxp8; 

		

		xp11 = code_fixed_ss1_x1(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp12 = code_fixed_ss1_x2(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp13 = code_fixed_ss1_x3(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp14 = code_fixed_ss1_x4(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp15 = code_fixed_ss1_x5(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp16 = code_fixed_ss1_x6(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp17 = code_fixed_ss1_x7(x11, x12, x13, x14, x15, x16, x17, x18, u);
		xp18 = code_fixed_ss1_x8(x11, x12, x13, x14, x15, x16, x17, x18, u);
		y1 = code_fixed_ss1_y(x11, x12, x13, x14, x15, x16, x17, x18, u);
		x11 = xp11; x12 = xp12; x13 = xp13; x14 = xp14; x15 = xp15; x16 = xp16; x17 = xp17; x18 = xp18; 

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
		

		//cout << cpt<<" "<< DFIy.to_double()-Dy << " "<< Ry.to_double()-Dy  << " "<< y2.to_double()-Dy   << " "<< y3.to_double()-Dy   << " "<< y4.to_double()-Dy<< " "<< y5.to_double()-Dy   << " "<< y6.to_double()-Dy   << " "<< yL.to_double()-Dy << endl;
		cout << cpt <<" "<< DFIy.to_double()-Dy<<" "<< Ry.to_double()-Dy << " "<< y2.to_double()-Dy << " "<< y3.to_double()-Dy << " "<< y4.to_double()-Dy<< " "<< y5.to_double()-Dy << " "<< y6.to_double()-Dy << " "<< yL.to_double()-Dy << endl;


		imp = impulse();
		u = imp;
		Du =u.to_double();
		cpt++;
  	}
  	//printf(" %g ; %g\n", minDy,maxDy);
  	//printf(" %g ; %g", miny,maxy);
  return 0;
}