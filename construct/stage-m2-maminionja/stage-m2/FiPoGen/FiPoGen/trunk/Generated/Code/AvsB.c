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

// Coefficients
// a0 = 0x5708p-24 ~~> 0x5708p-24
// a1 = 0x5708p-22 ~~> 0x5708p-22
// a2 = 0x4146p-21 ~~> 0x4146p-21
// a3 = 0x5708p-22 ~~> 0x5708p-22
// a4 = 0x5708p-24 ~~> 0x5708p-24
// a5 = 0x5be0p-13 ~~> 0x5be0p-13
// a6 = 0x9956p-13 ~~> -0x66aap-13
// a7 = 0x689dp-14 ~~> 0x689dp-14
// a8 = 0xae69p-16 ~~> -0x5197p-16

int16_t 
Amine(int16_t x0, int16_t x1, int16_t x2, int16_t x3, int16_t x4, int16_t x5, int16_t x6, int16_t x7, int16_t x8)
{
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
}

/* Error bound computed using MPFI:    [-189146330965b-42,0b0]
 *                                   ~ [-2^{-4.53929},2^{-inf}]
 *                                   ~ [-0.0430069,-0]
 */

int16_t Benoit(int16_t x0,int16_t x1,int16_t x2,int16_t x3,int16_t x4,int16_t x5,int16_t x6,int16_t x7,int16_t x8)
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


double 
impulse(int c)
{
  // int32_t X = (rand()%(0x00006800<<1+1))-0x6800;
  float x1 = sinf(0.001*c*2*3.1416*20);
  float x2 = sinf(0.001*c*2*3.1416);
  float x3 = (x1+2*x2)*133-75;
  double X = x3*powf(2.f,10); //32 bits de PE
  return X;
}

int
main(void)
{
  srand(time(NULL));
  
  int16_t resA = 0, resB=0,
    u0 = (int32_t)impulse(0),
    Au1 = 0, Au2 = 0, Au3 = 0, Au4 = 0, Ay0 = 0, Ay1 = 0, Ay2 = 0, Ay3 = 0,
    Bu1 = 0, Bu2 = 0, Bu3 = 0, Bu4 = 0, By0 = 0, By1 = 0, By2 = 0, By3 = 0;
  double Fu0 =impulse(0)*powf(2.f,-11), resF = 0,
    Fu1 = 0, Fu2 = 0, Fu3 = 0, Fu4 = 0, Fy0 = 0, Fy1 = 0, Fy2 = 0, Fy3 = 0, m=100000, M=-100000;
  
  int cpt = 0;
  while(cpt<1000){
    /*resA = Amine(u0, Au1, Au2, Au3, Au4, Ay0, Ay1, Ay2, Ay3);
    resB = Benoit(u0, Bu1, Bu2, Bu3, Bu4, By0, By1, By2, By3);
    resF = SoP_float(Fu0,Fu1, Fu2 , Fu3, Fu4, Fy0, Fy1, Fy2, Fy3 );*/
    if(Fu0 > M) M=Fu0;
    if(Fu0 < m) m=Fu0;
    //printf("%d %g  \n",cpt,Fu0);
    
    /*Au4 = Au3;
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

    Fu4 = Fu3;
    Fu3 = Fu2;
    Fu2 = Fu1;
    Fu1 = Fu0;
    Fy3 = Fy2;
    Fy2 = Fy1;
    Fy1 = Fy0;
    Fy0 = resF;*/

    u0 = (int32_t)impulse(cpt);
    Fu0 =impulse(cpt)*powf(2.f,-11);
    cpt++;
  }
  printf("%d %g  %g\n",cpt,M,m);
  return 0;
}
