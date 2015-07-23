#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double double_x1(double v0,double v1,double v2,double v3)
{
	double r;
	//r = 17.046156049603884 * v0 + 39.744067440163633 * v1 + 28.378107434473844 * v2 -0.0037970798478361681 * v3;
    r = 17.0458984375 * v0 + 39.744140625 * v1 + 28.3779296875 * v2 -0.003797054290771484375 * v3;
	return r;
}

double double_x2(double v0,double v1,double v2,double v3)
{
	double r;
    //r = -298.2602130449506 * v0 + -695.769371652887 * v1 + -496.7940220240763 * v2 -0.0054937169032137729 * v3;
	r = -298.265625 * v0 + -695.78125 * v1 + -496.796875 * v2 -0.005493640899658203125 * v3;
	return r;
}

double double_x3(double v0,double v1,double v2,double v3)
{
	double r;
    //r = 407.54042536627691 * v0 + 951.00287341471483 * v1 + 679.04108126568019 * v2 + 0.0090279643251138016 * v3;
	r = 407.546875 * v0 + 951 * v1 + 679.03125 * v2 + 0.009027957916259765625 * v3;
	return r;
}

double double_y(double v0,double v1,double v2,double v3)
{
	double r;
    //r = 58.710375667234857 * v0 + 67.449296810306308 * v1 + 46.929288054009696 * v2 -0.60253754413295468 * v3;
	r = 58.7109375 * v0 + 67.44921875 * v1 + 46.9296875 * v2 -0.6025390625 * v3;
	return r;
}



int16_t C_int_x1(int16_t v0,int16_t v1,int16_t v2,int16_t v3)
{	// Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -31852*v3;
	r0 = r0 >> 3;
	// Computation of c0*v0 in r1
	r1 = 17455*v0;
	r1 = r1 << 6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 20349*v1;
	r1 = r1 << 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 29059*v2;
	r1 = r1 << 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_x2(int16_t v0,int16_t v1,
	int16_t v2,int16_t v3)
{	// Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -23042*v3;
	r0 = r0 >> 6;
	// Computation of c0*v0 in r1
	r1 = -19089*v0;
	r1 = r1 << 6;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = -22265*v1;
	r1 = r1 << 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = -31795*v2;
	r1 = r1 << 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_x3(int16_t v0,int16_t v1,
	int16_t v2,int16_t v3)
{	// Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = 18933*v3;
	r0 = r0 >> 6;
	// Computation of c0*v0 in r1
	r1 = 26083*v0;
	r1 = r1 << 5;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 30432*v1;
	r1 = r1 << 10;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 21729*v2;
	r1 = r1 << 11;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}

int16_t C_int_y(int16_t v0,int16_t v1,
	int16_t v2,int16_t v3)
{	// Registers declaration
	int32_t r0, r1;
	// Computation of c3*v3 in r0
	r0 = -19744*v3;
	r0 = r0 << 1;
	// Computation of c0*v0 in r1
	r1 = 30060*v0;
	r1 = r1 << 3;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c1*v1 in r1
	r1 = 17267*v1;
	r1 = r1 << 8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// Computation of c2*v2 in r1
	r1 = 24028*v2;
	r1 = r1 << 8;
	// Computation of r0+r1 in r0
	r0 = r0 + r1;
	// The result is returned with a final right shift
	return r0 >> 16;
}


double impulse()
{
	double X=( rand()/(double)RAND_MAX ) * (55) -25;
	return X*powf(2,10);
}


int main(void)
{
	srand(time(NULL));

	double imp = impulse();
	int16_t u = (int16_t)imp,
		x1 = 0, x2 = 0, x3 = 0, y = 0,
		xp1 = 0, xp2 = 0, xp3 = 0;
	double Du = imp*powf(2,-10),
		Dx1 = 0, Dx2 = 0, Dx3 = 0, Dy = 0,
		Dxp1 = 0, Dxp2 = 0, Dxp3 = 0,
		maxDy=-1000,minDy=1000,
		maxy=-1000,miny=1000,
		min_delta_y=1000, max_delta_y=-1000;
	double err_rel=0.;

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
	


 	xp1 = C_int_x1(x1, x2, x3,u);
 	xp2 = C_int_x2(x1, x2, x3,u);
 	xp3 = C_int_x3(x1, x2, x3,u);
 	y = C_int_y(x1, x2, x3,u);
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
	if(y*powf(2,-10) >maxy) maxy=y*powf(2,-10);
	if(y*powf(2,-10)<miny) miny=y*powf(2,-10);
	if (Dy-y*powf(2,-10) <min_delta_y) min_delta_y = Dy-y*powf(2,-10);
	if (Dy-y*powf(2,-10) >max_delta_y) max_delta_y = Dy-y*powf(2,-10);

 	//printf("%d %d %d %d\n", x1,x2,x3,y);
 	//printf("%g %g %g %g\n", Dx1*powf(2,14),Dx2*powf(2,10),Dx3*powf(2,9),Dy*powf(2,10));
	err_rel = fabs(y*powf(2,-10)-Dy) / 23.7637;
 	printf("%d %g %g -0.262932 0.0356409 %g \n",cpt,imp,y*powf(2,-10)-Dy, err_rel);

 	imp = impulse();
    u = (int16_t) imp;
    Du =imp*powf(2,-10);
    cpt++;
  }
  //printf(" %g ; %g\n", min_delta_y,max_delta_y);
  return 0;
}
