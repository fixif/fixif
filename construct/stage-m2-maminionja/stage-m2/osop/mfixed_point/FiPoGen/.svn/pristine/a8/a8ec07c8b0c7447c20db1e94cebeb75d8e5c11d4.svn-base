#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


static inline int16_t __shrw(int16_t X, uint16_t n)
{
  return (X >> n);
}

static inline int16_t mul(int16_t a, int16_t b)
{
  int32_t t0 = a;
  int32_t t1 = b;
  int32_t t2 = ( t0 * t1 ) >> 16;
  return t2;
}


double SoP_float(double x0,double x1,double x2,double x3,double x4,double x5,double x6,double x7,double x8)
{
    /*      TP_Float_sop        */
    double r;
    r=0.0053119659423828125 * x1 + 0.0053119659423828125 * x3 + 0.001327991485595703125 * x0 + 0.001327991485595703125 * x4 + 0.00796794891357421875 * x2 -0.3187103271484375 * x8 + 1.63458251953125 * x7 + 2.87109375 * x5 -3.208251953125 * x6;
	return r ;
}


int16_t 
Amine(int16_t x0, int16_t x1, int16_t x2, int16_t x3, int16_t x4, int16_t x5, int16_t x6, int16_t x7, int16_t x8)
/*{
  int16_t r0  = mul(0x5708, x0);                        // (+) Q[ -3. 19] in ~ [-0.0172653,0.0172634]     -> error ~ [-2^{-19},0]
  int16_t r1  = __shrw(r0, 12);                         // (+) Q[  9.  7] in ~ [-0.0234375,0.015625]      -> error ~ [-2^{-7},0]
  int16_t r2  = mul(0x5708, x1);                        // (+) Q[ -1. 17] in ~ [-0.0690613,0.0690536]     -> error ~ [-2^{-17},0]
  int16_t r3  = mul(0x4146, x2);                        // (+) Q[  0. 16] in ~ [-0.103592,0.103577]       -> error ~ [-2^{-16},0]
  int16_t r4  = r3 << 1;                                // (+) Q[ -1. 17] in ~ [-0.103592,0.103577]       -> error ~ [-2^{-16},0]
  int16_t r5  = r2 + r4;                                // (+) Q[ -1. 17] in ~ [-0.172653,0.17263]        -> error ~ [-2^{-15.415},0]
  int16_t r6  = __shrw(r5, 1);                          // (+) Q[  0. 16] in ~ [-0.172653,0.172623]       -> error ~ [-2^{-15},0]
  int16_t r7  = mul(0x5708, x3);                        // (+) Q[ -1. 17] in ~ [-0.0690613,0.0690536]     -> error ~ [-2^{-17},0]
  int16_t r8  = r7 << 1;                                // (+) Q[ -2. 18] in ~ [-0.0690613,0.0690536]     -> error ~ [-2^{-17},0]
  int16_t r9  = mul(0x5708, x4);                        // (+) Q[ -3. 19] in ~ [-0.0172653,0.0172634]     -> error ~ [-2^{-19},0]
  int16_t r10 = __shrw(r9, 1);                          // (+) Q[ -2. 18] in ~ [-0.0172653,0.0172615]     -> error ~ [-2^{-18},0]
  int16_t r11 = r8 + r10;                               // (+) Q[ -2. 18] in ~ [-0.0863266,0.0863152]     -> error ~ [-2^{-16.415},0]
  int16_t r12 = __shrw(r11, 2);                         // (+) Q[  0. 16] in ~ [-0.0863342,0.0863037]     -> error ~ [-2^{-15.415},0]
  int16_t r13 = r6 + r12;                               // (+) Q[  0. 16] in ~ [-0.258987,0.258926]       -> error ~ [-2^{-14.1926},0]
  int16_t r14 = __shrw(r13, 9);                         // (+) Q[  9.  7] in ~ [-0.265625,0.257812]       -> error ~ [-2^{-6.99297},0]
  int16_t r15 = mul(0x5be0, x5);                        // (+) Q[  9.  7] in ~ [-49.1719,49.1641]         -> error ~ [-2^{-7},0]
  int16_t r16 = r15 << 1;                               // (+) Q[  8.  8] in ~ [-49.1719,49.1641]         -> error ~ [-2^{-7},0]
  int16_t r17 = mul(0x9956, x6);                        // (+) Q[  9.  7] in ~ [-54.9453,54.9375]         -> error ~ [-2^{-7},0]
  int16_t r18 = r17 << 1;                               // (+) Q[  8.  8] in ~ [-54.9453,54.9375]         -> error ~ [-2^{-7},0]
  int16_t r19 = r16 + r18;                              // (+) Q[  8.  8] in ~ [-104.117,104.102]         -> error ~ [-2^{-6},0]
  int16_t r20 = __shrw(r19, 1);                         // (+) Q[  9.  7] in ~ [-104.117,104.102]         -> error ~ [-2^{-6},0]
  int16_t r21 = mul(0x689d, x7);                        // (+) Q[  8.  8] in ~ [-27.9922,27.9883]         -> error ~ [-2^{-8},0]
  int16_t r22 = r21 << 1;                               // (+) Q[  7.  9] in ~ [-27.9922,27.9883]         -> error ~ [-2^{-8},0]
  int16_t r23 = mul(0xae69, x8);                        // (+) Q[  6. 10] in ~ [-5.45801,5.45703]         -> error ~ [-2^{-10},0]
  int16_t r24 = __shrw(r23, 1);                         // (+) Q[  7.  9] in ~ [-5.45898,5.45703]         -> error ~ [-2^{-9},0]
  int16_t r25 = r22 + r24;                              // (+) Q[  7.  9] in ~ [-33.4512,33.4453]         -> error ~ [-2^{-7.41504},0]
  int16_t r26 = __shrw(r25, 2);                         // (+) Q[  9.  7] in ~ [-33.4531,33.4453]         -> error ~ [-2^{-6.41504},0]
  int16_t r27 = r20 + r26;                              // (+) Q[  9.  7] in ~ [-137.57,137.547]          -> error ~ [-2^{-5.19265},0]
  int16_t r28 = r14 + r27;                              // (+) Q[  9.  7] in ~ [-137.836,137.805]         -> error ~ [-2^{-4.82851},0]
  int16_t r29 = r1 + r28;                               // (+) Q[  9.  7] in ~ [-137.859,137.82]          -> error ~ [-2^{-4.53929},0]
  return r29;
}*/
  {
 int16_t r0  = mul(0x5708, x1);                        // (+) Q[ -1. 17] in ~ [-0.0690613,0.0690536]     -> error ~ [-2^{-17},0]
 int16_t r1  = mul(0x5708, x3);                        // (+) Q[ -1. 17] in ~ [-0.0690613,0.0690536]     -> error ~ [-2^{-17},0]
 int16_t r2  = r0 + r1;                                // (+) Q[ -1. 17] in ~ [-0.138123,0.138107]       -> error ~ [-2^{-16},0]
 int16_t r3  = mul(0x5708, x0);                        // (+) Q[ -3. 19] in ~ [-0.0172653,0.0172634]     -> error ~ [-2^{-19},0]
 int16_t r4  = mul(0x5708, x4);                        // (+) Q[ -3. 19] in ~ [-0.0172653,0.0172634]     -> error ~ [-2^{-19},0]
 int16_t r5  = r3 + r4;                                // (+) Q[ -3. 19] in ~ [-0.0345306,0.0345268]     -> error ~ [-2^{-18},0]
 int16_t r6  = __shrw(r5, 2);                          // (+) Q[ -1. 17] in ~ [-0.0345306,0.034523]      -> error ~ [-2^{-16.6781},0]
 int16_t r7  = r2 + r6;                                // (+) Q[ -1. 17] in ~ [-0.172653,0.17263]        -> error ~ [-2^{-15.2996},0]
 int16_t r8  = __shrw(r7, 1);                          // (+) Q[  0. 16] in ~ [-0.172653,0.172623]       -> error ~ [-2^{-14.9125},0]
 int16_t r9  = mul(0x4146, x2);                        // (+) Q[  0. 16] in ~ [-0.103592,0.103577]       -> error ~ [-2^{-16},0]
 int16_t r10 = r8 + r9;                                // (+) Q[  0. 16] in ~ [-0.276245,0.276199]       -> error ~ [-2^{-14.3561},0]
 int16_t r11 = __shrw(r10, 9);                         // (+) Q[  9.  7] in ~ [-0.28125,0.273438]        -> error ~ [-2^{-6.99402},0]
 int16_t r12 = mul(0xae69, x8);                        // (+) Q[  6. 10] in ~ [-5.45801,5.45703]         -> error ~ [-2^{-10},0]
 int16_t r13 = __shrw(r12, 1);                         // (+) Q[  7.  9] in ~ [-5.45898,5.45703]         -> error ~ [-2^{-9},0]
 int16_t r14 = mul(0x689d, x7);                        // (+) Q[  8.  8] in ~ [-27.9922,27.9883]         -> error ~ [-2^{-8},0]
 int16_t r15 = r14 << 1;                               // (+) Q[  7.  9] in ~ [-27.9922,27.9883]         -> error ~ [-2^{-8},0]
 int16_t r16 = r13 + r15;                              // (+) Q[  7.  9] in ~ [-33.4512,33.4453]         -> error ~ [-2^{-7.41504},0]
 int16_t r17 = __shrw(r16, 1);                         // (+) Q[  8.  8] in ~ [-33.4531,33.4453]         -> error ~ [-2^{-7},0]
 int16_t r18 = mul(0x5be0, x5);                        // (+) Q[  9.  7] in ~ [-49.1719,49.1641]         -> error ~ [-2^{-7},0]
 int16_t r19 = r18 << 1;                               // (+) Q[  8.  8] in ~ [-49.1719,49.1641]         -> error ~ [-2^{-7},0]
 int16_t r20 = r17 + r19;                              // (+) Q[  8.  8] in ~ [-82.625,82.6094]          -> error ~ [-2^{-6},0]
 int16_t r21 = __shrw(r20, 1);                         // (+) Q[  9.  7] in ~ [-82.625,82.6094]          -> error ~ [-2^{-5.67807},0]
 int16_t r22 = mul(0x9956, x6);                        // (+) Q[  9.  7] in ~ [-54.9453,54.9375]         -> error ~ [-2^{-7},0]
 int16_t r23 = r21 + r22;                              // (+) Q[  9.  7] in ~ [-137.57,137.547]          -> error ~ [-2^{-5.19265},0]
 int16_t r24 = r11 + r23;                              // (+) Q[  9.  7] in ~ [-137.852,137.82]          -> error ~ [-2^{-4.82875},0]
 return r24;
}

int16_t Benoit_16(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  /*      TP_Int_sop        */
  int16_t c=0, x=0, r16_0=0, r16_1=0, r16_2=0, r16_3=0, r16_4=0;

  c = 22280;
  r16_0 = (c*x1)>> 16;
  c = 22280;
  r16_1 = (c*x3)>> 16;
  r16_2 = r16_0 + r16_1;
  c = 22280;
  r16_0 = (c*x0)>> 16;
  c = 22280;
  r16_1 = (c*x4)>> 16;
  r16_3 = r16_0 + r16_1;
  r16_0 = r16_2 + (r16_3>> 2);
  c = 16710;
  r16_1 = (c*x2)>> 16;
  r16_2 = (r16_0 >> 1)+ r16_1;
  c = -20887;
  r16_0 = (c*x8)>> 16;
  c = 26781;
  r16_1 = (c*x7)>> 16;
  r16_3 = r16_0 + (r16_1 << 2);
  c = 23520;
  r16_0 = (c*x5)>> 16;
  r16_1 = r16_3 + (r16_0 << 3);
  c = -26282;
  r16_0 = (c*x6)>> 16;
  r16_3 = r16_1 + (r16_0 << 3);
  r16_0 = (r16_2 >> 6) + r16_3;

  return r16_0;
}

int16_t Benoit_32(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  int16_t c, x;
  int32_t r0, r1, r2, r3, r4;

  c = 22280;
  r0 = c*x1;
  c = 22280;
  r1 = c*x3;
  r2= r0 + r1 ;
  c = 22280;
  r0 = c*x0;
  c = 22280;
  r1 = c*x4;
  r3= r0 + r1 ;
  r0= r2 + ( r3 >> 2 );
  c = 16710;
  r1 = c*x2;
  r2= ( r0 >> 1 ) + r1 ;
  c = -20887;
  r0 = c*x8;
  c = 26781;
  r1 = c*x7;
  r3= r0 + ( r1 << 2 );
  c = 23520;
  r0 = c*x5;
  r1= r3 + ( r0 << 3 );
  c = -26282;
  r0 = c*x6;
  r3= r1 + ( r0 << 3 );
  r0= ( r2 >> 6 ) + r3 ;

  r1= r0 >> 16 ;
  return r1;
}

int16_t Bits_clean(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  // One of the most parallelized scheme
  int16_t c=0;
  int32_t r20_0=0, r20_1=0, r20_2=0, r20_3=0, r20_4=0;
  c = 22280;
  r20_0 = c*x4>> 21;
  c = 22280;
  r20_1 = c*x1>> 19;
  //r20_0 = r20_0 >> 9;
  //r20_1 = r20_1 >> 7;
  r20_2 = r20_0 + r20_1;
  c = 16710;
  r20_0 = c*x2>> 18;
  c = -20887;
  r20_1 = c*x8>> 12;
  //r20_0 = r20_0 >> 6;
  r20_3 = r20_0 + r20_1;
  c = 26781;
  r20_0 = c*x7>> 12;
  r20_0 = r20_0 % 262144;
  r20_0 = r20_0 << 2;
  r20_1 = r20_3 + r20_0;
  r20_0 = r20_2 + r20_1;
  c = 22280;
  r20_1 = c*x0>> 21;
  c = 22280;
  r20_2 = c*x3>> 19;
  //r20_1 = r20_1 >> 9;
  //r20_2 = r20_2 >> 7;
  r20_3 = r20_1 + r20_2;
  c = -26282;
  r20_1 = c*x6>> 12;
  r20_1 = r20_1 % 131072;
  r20_1 = r20_1 << 3;
  r20_2 = r20_3 + r20_1;
  c = 23520;
  r20_1 = c*x5>> 12;
  r20_1 = r20_1 % 131072;
  r20_1 = r20_1 << 3;
  r20_3 = r20_2 + r20_1;
  r20_1 = r20_0 + r20_3;
  r20_2= r20_1 >> 4 ;
  return r20_2;
}

  int16_t Bits_clean2(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
{
  // Adapted from best 32 bits scheme
  int16_t c=0;
  int32_t r20_0=0, r20_1=0, r20_2=0, r20_3=0, r20_4=0;

  c = 22280;
  r20_0 = (c*x1) >> 19;
  c = 22280;
  r20_1 = (c*x3) >> 19;
  r20_2 = r20_0 + r20_1;
  c = 22280;
  r20_0 = (c*x0) >> 21;
  c = 22280;
  r20_1 = (c*x4) >> 21;
  r20_3 = r20_0 + r20_1;
  r20_0= r20_2 + r20_3;
  c = 16710;
  r20_1 = (c*x2) >> 18;
  r20_2= r20_0 + r20_1 ;
  c = -20887;
  r20_0 = (c*x8) >> 12;
  c = 26781;
  r20_1 = (c*x7) >> 12;
  r20_1 = r20_1 % 262144;
  r20_1 = r20_1 << 2;
  r20_3= r20_0 + r20_1;
  c = 23520;
  r20_0 = (c*x5) >> 12;
  r20_0 = r20_0 % 131072;
  r20_0 = r20_0 << 3;
  r20_1= r20_3 + r20_0;
  c = -26282;
  r20_0 = (c*x6) >> 12;
  r20_0 = r20_0 % 131072;
  r20_0 = r20_0 << 3;
  r20_3= r20_1 + r20_0;
  r20_0= r20_2 + r20_3;

  r20_1= r20_0 >> 4 ;
  return r20_1;
}

double RandomFloat(int beta)
{
    double a = pow(2,beta-2)+1;
    double b = pow(2,beta-1)-1;
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
  X= RandomFloat(16);
  return X;
}

int
main(void)
{
  srand(time(NULL));
  
  int16_t resA=0, resB=0, resC=0, resD=0, resE=0,
    u0 = 0,
    Au1 = 0, Au2 = 0, Au3 = 0, Au4 = 0, Ay0 = 0, Ay1 = 0, Ay2 = 0, Ay3 = 0,
    Bu1 = 0, Bu2 = 0, Bu3 = 0, Bu4 = 0, By0 = 0, By1 = 0, By2 = 0, By3 = 0,
    Cu1 = 0, Cu2 = 0, Cu3 = 0, Cu4 = 0, Cy0 = 0, Cy1 = 0, Cy2 = 0, Cy3 = 0,
    Du1 = 0, Du2 = 0, Du3 = 0, Du4 = 0, Dy0 = 0, Dy1 = 0, Dy2 = 0, Dy3 = 0,
    Eu1 = 0, Eu2 = 0, Eu3 = 0, Eu4 = 0, Ey0 = 0, Ey1 = 0, Ey2 = 0, Ey3 = 0;
  double i =impulse(0), Fu0 =i*powf(2.f,-11), resF = 0,
    Fu1 = 0, Fu2 = 0, Fu3 = 0, Fu4 = 0, Fy0 = 0, Fy1 = 0, Fy2 = 0, Fy3 = 0;

    u0 = (int32_t) i;
  
  int cpt = 0;
  while(cpt<100){
  	resA = Amine(u0, Au1, Au2, Au3, Au4, Ay0, Ay1, Ay2, Ay3);
    resB = Benoit_32(u0, Bu1, Bu2, Bu3, Bu4, By0, By1, By2, By3);
    resC = Bits_clean(u0, Cu1, Cu2, Cu3, Cu4, Cy0, Cy1, Cy2, Cy3);
    resD = Benoit_16(u0, Du1, Du2, Du3, Du4, Dy0, Dy1, Dy2, Dy3);
    resE = Bits_clean2(u0, Eu1, Eu2, Eu3, Eu4, Ey0, Ey1, Ey2, Ey3);

    resF = SoP_float(Fu0,Fu1, Fu2 , Fu3, Fu4, Fy0, Fy1, Fy2, Fy3 );

    printf("%d % 1.19e % 1.19e % 1.19e % 1.19e % 1.19e % 1.19e % 1.19e\n", cpt, Fu0, resA*powf(2.f,-7), resB*powf(2.f,-10), resC*powf(2.f,-10),resD*powf(2.f,-10), resE*powf(2.f,-10),resF);

    Au4 = Au3;
    Au3 = Au2;
    Au2 = Au1;
    Au1 = u0;
    Ay3 = Ay2;
    Ay2 = Ay1;
    Ay1 = Ay0;
    Ay0 = resA << 3;

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

    Eu4 = Eu3;
    Eu3 = Eu2;
    Eu2 = Eu1;
    Eu1 = u0;
    Ey3 = Ey2;
    Ey2 = Ey1;
    Ey1 = Ey0;
    Ey0 = resE;

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

