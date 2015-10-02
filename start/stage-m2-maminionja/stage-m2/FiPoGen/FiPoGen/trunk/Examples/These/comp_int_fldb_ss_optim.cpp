#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include "ac_fixed.h"

using namespace std;

double double_x1(double v1,double v2,double v3,double v4)
{
	double r;
	//r = 17.046156049603884 * v0 + 39.744067440163633 * v1 + 28.378107434473844 * v2 -0.0037970798478361681 * v3;
	//r = 17.0458984375 * v1 + 39.744140625 * v2 + 28.3779296875 * v3 -0.003797054290771484375 * v4;
	ac_fixed<22,6,true> c1 = 17.046156049603884;
	ac_fixed<27,7,true> c2 = 39.744067440163633;
	ac_fixed<27,6,true> c3 = 28.378107434473844;
	ac_fixed<13,-7,true> c4 = -0.0037970798478361681;
	r = c1.to_double() * v1 + c2.to_double() * v2 + c3.to_double() * v3 + c4.to_double() * v4;
	return r;
}

double double_x2(double v1,double v2,double v3,double v4)
{
	double r;
    //r = -298.2602130449506 * v0 + -695.769371652887 * v1 + -496.7940220240763 * v2 -0.0054937169032137729 * v3;
	//r = -298.265625 * v1 + -695.78125 * v2 + -496.796875 * v3 -0.005493640899658203125 * v4;
	ac_fixed<28,10,true> c1 = -298.2602130449506;
	ac_fixed<33,11,true> c2 = -695.769371652887;
	ac_fixed<33,10,true> c3 = -496.7940220240763;
	ac_fixed<16,-6,true> c4 = -0.0054937169032137729;
	r = c1.to_double() * v1 + c2.to_double() * v2 + c3.to_double() * v3 + c4.to_double() * v4;
	return r;
}

double double_x3(double v1,double v2,double v3,double v4)
{
	double r;
    //r = 407.54042536627691 * v0 + 951.00287341471483 * v1 + 679.04108126568019 * v2 + 0.0090279643251138016 * v3;
	//r = 407.546875 * v1 + 951 * v2 + 679.03125 * v3 + 0.009027957916259765625 * v4;
	ac_fixed<26,10,true> c1 = 407.54042536627691;
	ac_fixed<31,11,true> c2 = 951.00287341471483;
	ac_fixed<32,11,true> c3 = 679.04108126568019;
	ac_fixed<15,-5,true> c4 = 0.0090279643251138016;
	r = c1.to_double() * v1 + c2.to_double() * v2 + c3.to_double() * v3 + c4.to_double() * v4;
	return r;
}

double double_y(double v1,double v2,double v3,double v4)
{
	double r;
    //r = 58.710375667234857 * v0 + 67.449296810306308 * v1 + 46.929288054009696 * v2 -0.60253754413295468 * v3;
	//r = 58.7109375 * v1 + 67.44921875 * v2 + 46.9296875 * v3 -0.6025390625 * v4;
	ac_fixed<17,7,true> c1 = 58.710375667234857;
	ac_fixed<22,8,true> c2 = 67.449296810306308;
	ac_fixed<22,7,true> c3 = 46.929288054009696;
	ac_fixed<15,1,true> c4 = -0.60253754413295468;
	r = c1.to_double() * v1 + c2.to_double() * v2 + c3.to_double() * v3 + c4.to_double() * v4;
	return r;
}



ac_fixed<14,2,true> Code_fixed_x1(ac_fixed<14,2,true> v1,
	ac_fixed<20,6,true> v2, ac_fixed<19,7,true> v3,
	ac_fixed<12,6,true> v4)
{
	//Declaration of sums sd and s
	ac_fixed<16,2,true> sd = 0;
	ac_fixed<14,2,true> s = 0;
	//Computation of c1*v1 in sd
	ac_fixed<22,6,true> c1 = 17.046156049603884;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<27,7,true> c2 = 39.744067440163633;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<27,6,true> c3 = 28.378107434473844;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<13,-7,true> c4 = -0.0037970798478361681;
	sd = sd + c4*v4;
	s = s + sd;
	// The result is returned
	return s;
}

ac_fixed<20,6,true> Code_fixed_x2(ac_fixed<14,2,true> v1,
	ac_fixed<20,6,true> v2, ac_fixed<19,7,true> v3,
	ac_fixed<12,6,true> v4)
{
	//Declaration of sums sd and s
	ac_fixed<22,6,true> sd = 0;
	ac_fixed<20,6,true> s = 0;
	//Computation of c1*v1 in sd
	ac_fixed<28,10,true> c1 = -298.2602130449506;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<33,11,true> c2 = -695.769371652887;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<33,10,true> c3 = -496.7940220240763;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<16,-6,true> c4 = -0.0054937169032137729;
	sd = sd + c4*v4;
	s = s + sd;
	// The result is returned
	return s;
}

ac_fixed<19,7,true> Code_fixed_x3(ac_fixed<14,2,true> v1,
	ac_fixed<20,6,true> v2, ac_fixed<19,7,true> v3,
	ac_fixed<12,6,true> v4)
{
	//Declaration of sums sd and s
	ac_fixed<21,7,true> sd = 0;
	ac_fixed<19,7,true> s = 0;
	//Computation of c1*v1 in sd
	ac_fixed<26,10,true> c1 = 407.54042536627691;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<31,11,true> c2 = 951.00287341471483;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<32,11,true> c3 = 679.04108126568019;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<15,-5,true> c4 = 0.0090279643251138016;
	sd = sd + c4*v4;
	s = s + sd;
	// The result is returned
	return s;
}

ac_fixed<12,6,true> Code_fixed_y(ac_fixed<14,2,true> v1,
	ac_fixed<20,6,true> v2, ac_fixed<19,7,true> v3,
	ac_fixed<12,6,true> v4)
{
	//Declaration of sums sd and s
	ac_fixed<14,6,true> sd = 0;
	ac_fixed<12,6,true> s = 0;
	//Computation of c1*v1 in sd
	ac_fixed<17,7,true> c1 = 58.710375667234857;
	sd = sd + c1*v1;
	//Computation of c2*v2 in sd
	ac_fixed<22,8,true> c2 = 67.449296810306308;
	sd = sd + c2*v2;
	//Computation of c3*v3 in sd
	ac_fixed<22,7,true> c3 = 46.929288054009696;
	sd = sd + c3*v3;
	//Computation of c4*v4 in sd
	ac_fixed<15,1,true> c4 = -0.60253754413295468;
	sd = sd + c4*v4;
	s = s + sd;
	// The result is returned
	return s;
}


double impulse()
{
	double X=( rand()/(double)RAND_MAX ) * (55) -25;
	return X;
}


int main(void)
{
	srand(time(NULL));

	double imp = impulse();
	/*int16_t u = (int16_t)imp,
		x1 = 0, x2 = 0, x3 = 0, y = 0,
		xp1 = 0, xp2 = 0, xp3 = 0;*/
	double Du = imp,
		Dx1 = 0, Dx2 = 0, Dx3 = 0, Dy = 0,
		Dxp1 = 0, Dxp2 = 0, Dxp3 = 0,
		maxDy=-1000,minDy=1000,
		maxy=-1000,miny=1000;

	ac_fixed<14,2,true> x1=0, xp1=0;
	ac_fixed<20,6,true> x2=0, xp2=0;
	ac_fixed<19,7,true> x3=0, xp3=0;
	ac_fixed<12,6,true> u=imp, y=0;


	int cpt = 1;
	while(cpt<=10000){

		/*x1=(int16_t)-1360;
		x2=(int16_t)-123;
		x3=(int16_t)101;
		u=(int16_t)22385;
		Dx1=x1*powf(2,-14);
		Dx2= x2*powf(2,-10);
		Dx3= x3*powf(2,-9);
		Du =u*powf(2,-10);*/
		


		xp1 = Code_fixed_x1(x1, x2, x3,u);
		xp2 = Code_fixed_x2(x1, x2, x3,u);
		xp3 = Code_fixed_x3(x1, x2, x3,u);
		y = Code_fixed_y(x1, x2, x3,u);
		x1 = xp1; 
		x2 = xp2; 
		x3 = xp3; 

		Dxp1 = double_x1(Dx1, Dx2, Dx3,Du);
		Dxp2 = double_x2(Dx1, Dx2, Dx3,Du);
		Dxp3 = double_x3(Dx1, Dx2, Dx3,Du);
		Dy = double_y(Dx1, Dx2, Dx3,Du);
		Dx1 = Dxp1; 
		Dx2 = Dxp2; 
		Dx3 = Dxp3;
		if(Dy >maxDy) maxDy=Dy;
		if(Dy<minDy) minDy=Dy;
		if(y.to_double() >maxy) maxy=y.to_double();
		if(y.to_double()<miny) miny=y.to_double();
		//printf("%d %d %d %d\n", x1,x2,x3,y);
		//printf("%g %g %g %g\n", Dx1*powf(2,14),Dx2*powf(2,10),Dx3*powf(2,9),Dy*powf(2,10));

		//printf("%d %g %g -0.125 0.125\n",cpt,imp,y.to_double()-Dy);
		cout << cpt<<" "<< imp << " "<< y.to_double()-Dy << " -0.0768329 0.00575609 -0.125 0.125"<< endl;
		imp = impulse();
		u = imp;
		Du =imp;
		cpt++;
  	}
  	//printf(" %g ; %g\n", minDy,maxDy);
  	//printf(" %g ; %g", miny,maxy);
  return 0;
}
