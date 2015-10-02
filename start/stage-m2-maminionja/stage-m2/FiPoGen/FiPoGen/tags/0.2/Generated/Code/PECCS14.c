#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


double SoP_float(double x0,double x1,double x2,double x3,double x4,double x5,double x6,double x7,double x8)
{
    /*      TP_Float_sop        */
    double r;
    r=0.0053119659423828125 * x1 + 0.0053119659423828125 * x3 + 0.001327991485595703125 * x0 + 0.001327991485595703125 * x4 + 0.00796794891357421875 * x2 -0.3187103271484375 * x8 + 1.63458251953125 * x7 + 2.87109375 * x5 -3.208251953125 * x6;
	return r ;
}


int16_t FIX1(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
    // DELTA = 25

  int16_t c, r=0;
  int64_t r0=0, r1=0, r2=0, r3=0, r4=0;
  c = 23520;
  r0=c*x5;
  r0 = r0<<12;
  c = -26282;
  r1 = c*x6;
  r1 = r1<<12;
  r0 = r0 % 4398046511104;
  r1 = r1 % 4398046511104;
  r2 = r0 + r1;
  c = 22280;
  r0 = c*x0;
  r1 = r2 + r0;
  c = 22280;
  r0 = c*x3;
  r0 = r0 << 2;

  c = -20887;
  r2 = c*x8;
  r2 = r2 <<9;

  r3 = r0 + r2;
  r0 = r1 + r3;
  c = 22280;
  r1 = c*x4;

  c = 26781;
  r2 = c*x7;
  r2 = r2 << 11;

  r2 = r2 % 4398046511104;
  r3 = r1 + r2;

  c = 16710;
  r1 = c*x2;
  r1 = r1 << 3;

  r2 = r3 + r1;

  c = 22280;
  r1 = c*x1;
  r1 = r1 <<2;

  r3 = r2 + r1;
  r1 = r0 + r3;
  r= r1 >> 25 ;
  return r;
}

int16_t FIX2(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  // DELTA = 0

  int16_t c, r=0;
  int32_t r0=0, r1=0, r2=0, r3=0, r4=0;
  c = 23520;
  r0 = c*x5>> 13;
  c = -26282;
  r1 = c*x6>> 13;
  r0 = r0 % 131072;
  r1 = r1 % 131072;
  r2 = r0 + r1;
  c = 22280;
  r0 = c*x0>> 25;
  r1 = r2 + r0;
  c = 22280;
  r0 = c*x3>> 23;
  c = -20887;
  r2 = c*x8>> 16;
  r3 = r0 + r2;
  r0 = r1 + r3;
  c = 22280;
  r1 = c*x4>> 25;
  c = 26781;
  r2 = c*x7>> 14;
  r2 = r2 % 131072;
  r3 = r1 + r2;
  c = 16710;
  r1 = c*x2>> 22;
  r2 = r3 + r1;
  c = 22280;
  r1 = c*x1>> 23;
  r3 = r2 + r1;
  r1 = r0 + r3;
  r = r1;
  return r;
}



int16_t FIX3(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  // DELTA = 4

  int16_t c=0,r=0;
  int32_t r0=0, r1=0, r2=0, r3=0, r4=0;
  c = 23520;
  r0 = c*x5>> 9;
  c = -26282;
  r1 = c*x6>> 9;
  r0 = r0 % 2097152;
  r1 = r1 % 2097152;
  r2 = r0 + r1;
  c = 22280;
  r0 = c*x0>> 21;
  r1 = r2 + r0;
  c = 22280;
  r0 = c*x3>> 19;
  c = -20887;
  r2 = c*x8>> 12;
  r3 = r0 + r2;
  r0 = r1 + r3;
  c = 22280;
  r1 = c*x4>> 21;
  c = 26781;
  r2 = c*x7>> 10;
  r2 = r2 % 2097152;
  r3 = r1 + r2;
  c = 16710;
  r1 = c*x2>> 18;
  r2 = r3 + r1;
  c = 22280;
  r1 = c*x1>> 19;
  r3 = r2 + r1;
  r1 = r0 + r3;
  r2 = r1 >> 4 ;
  r = r2;
  return r;
}

int16_t FIX3b(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  // DELTA = 4

  int16_t c=0,r=0;
  int32_t r0=0, r1=0, r2=0, r3=0, r4=0;
  c = 23520;
  r0 = c*x5>> 9;
  c = -26282;
  r1 = c*x6>> 9;
  r0 = ((r0 +2097152)% 4194304)-2097152;
  r1 = ((r1 +2097152)% 4194304)-2097152;
  r2 = ((r0+r1 +2097152)% 4194304)-2097152;
  c = 22280;
  r0 = c*x0>> 21;
  r1 = ((r2+r0 +2097152)% 4194304)-2097152;
  c = 22280;
  r0 = c*x3>> 19;
  c = -20887;
  r2 = c*x8>> 12;
  r3 = ((r0 + r2 +2097152)% 4194304)-2097152;
  r0 = ((r1 + r3 +2097152)% 4194304)-2097152;
  c = 22280;
  r1 = c*x4>> 21;
  c = 26781;
  r2 = c*x7>> 10;
  r2 = ((r2 +2097152)% 4194304)-2097152;
  r3 = ((r1 + r2 +2097152)% 4194304)-2097152;
  c = 16710;
  r1 = c*x2>> 18;
  r2 = ((r3 + r1 + 2097152)% 4194304)-2097152;
  c = 22280;
  r1 = c*x1>> 19;
  r3 = ((r2 + r1 +2097152)% 4194304)-2097152;
  r1 =((r0 + r3 +2097152)% 4194304)-2097152;
  r2 = r1 >> 4 ;
  r = r2;
  return r;
}

double RandomFloat()
{
    double a = 16385;
    double b = 26624;
    double random = ((double) rand()) / (double) RAND_MAX;
    double diff = b - a;
    double r = random * diff;
    return (pow(-1,rand()%2))*(a + r);
}

double 
impulse(int c)
{
  // int32_t X = (rand()%(0x00006800<<1+1))-0x6800;
  float x1 = sinf(0.01f*c*2*3.14*10);
  float x2 = sinf(0.01f*c*2*3.14);
  float x3 = (x1+2*x2)*4;
  double X = x3*powf(2.f,10);
  X= RandomFloat();
  return X;
}

int
main(void)
{
  srand(time(NULL));
  
  int16_t resB=0, resC=0, resD=0, resE=0, var_int = 0,
    u0 = 0,
    Bu1 = 0, Bu2 = 0, Bu3 = 0, Bu4 = 0, By0 = 0, By1 = 0, By2 = 0, By3 = 0,
    Cu1 = 0, Cu2 = 0, Cu3 = 0, Cu4 = 0, Cy0 = 0, Cy1 = 0, Cy2 = 0, Cy3 = 0,
    Du1 = 0, Du2 = 0, Du3 = 0, Du4 = 0, Dy0 = 0, Dy1 = 0, Dy2 = 0, Dy3 = 0;
  double i =impulse(0), Fu0 =i*powf(2.f,-11), resF = 0,
    Fu1 = 0, Fu2 = 0, Fu3 = 0, Fu4 = 0, Fy0 = 0, Fy1 = 0, Fy2 = 0, Fy3 = 0;

    u0 = (int32_t) i;
  
  int cpt = 0;
  while(cpt<200){
    resB = FIX1(u0, Bu1, Bu2, Bu3, Bu4, By0, By1, By2, By3);
    resC = FIX3(u0, Cu1, Cu2, Cu3, Cu4, Cy0, Cy1, Cy2, Cy3);
    resD = FIX2(u0, Du1, Du2, Du3, Du4, Dy0, Dy1, Dy2, Dy3);

    resF = SoP_float(Fu0,Fu1, Fu2 , Fu3, Fu4, Fy0, Fy1, Fy2, Fy3 );

    printf("%d % 1.19e % 1.19e % 1.19e % 1.19e % 1.19e \n", cpt, Fu0, resB*powf(2.f,-10), resC*powf(2.f,-10), resD*powf(2.f,-10), resF);
    //printf("%d % 1.19e % 1.19e % 1.19e  \n", cpt, resB*powf(2.f,-10)-resF, resC*powf(2.f,-10)-resF, resD*powf(2.f,-10)-resF);

    Bu4 = Bu3;
    Bu3 = Bu2;
    Bu2 = Bu1;
    Bu1 = u0;
    By3 = By2;
    By2 = By1;
    By1 = By0;
    By0 = resB;

    Cu4 = Cu3;
    Cu3 = Cu2;
    Cu2 = Cu1;
    Cu1 = u0;
    Cy3 = Cy2;
    Cy2 = Cy1;
    Cy1 = Cy0;
    Cy0 = resC;

    Du4 = Du3;
    Du3 = Du2;
    Du2 = Du1;
    Du1 = u0;
    Dy3 = Dy2;
    Dy2 = Dy1;
    Dy1 = Dy0;
    Dy0 = resD;

    Fu4 = Fu3;
    Fu3 = Fu2;
    Fu2 = Fu1;
    Fu1 = Fu0;
    Fy3 = Fy2;
    Fy2 = Fy1;
    Fy1 = Fy0;
    Fy0 = resF;

    i =impulse(cpt);
    u0 = (int32_t)i;
    Fu0 =i*powf(2.f,-11);
    cpt++;
  }
  return 0;
}

