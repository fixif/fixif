#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

double RandomFloat(int c)
{
    int beta = 16;
    double a = pow(2,beta-2)+1;
    double b = pow(2,beta-1)-1;
    double random = ((double) rand()) / (double) RAND_MAX;
    double diff = b - a;
    double r = random * diff;
    return (pow(-1,rand()%2))*(a + r);
}


int16_t SoP_int_T0(int16_t x0,int16_t x1)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
  int16_t c, x;
  int32_t r0, r1, r2, r3;

  //Computation of c0*x0 in register r0
  c = 16384;
  r0 = c*x0;

  //Computation of c1*x1 in register r1
  c = 30664;
  r1 = c*x1;

  //Computation of r0+r1 in register r2
  r2= ( r0 << 2 ) + ( r1 >> 2 );

  //Computation of the final right shift
  r3= r2 >> 16 ;
  return r3;
}

int16_t SoP_int_xn0(int16_t x0,int16_t x1,int16_t x2,int16_t x3)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
  int16_t c, x;
  int32_t r0, r1, r2, r3, r4;

  //Computation of c1*x1 in register r0
  c = -22208;
  r0 = c*x1;

  //Computation of c3*x3 in register r1
  c = 16384;
  r1 = c*x3;

  //Computation of r0+r1 in register r2
  r2= r0 + ( r1 << 1 );

  //Computation of c0*x0 in register r0
  c = -32078;
  r0 = c*x0;

  //Computation of c2*x2 in register r1
  c = -19560;
  r1 = c*x2;

  //Computation of r0+r1 in register r3
  r3= r0 + ( r1 >> 8 );

  //Computation of r2+r3 in register r0
  r0= r2 + ( r3 >> 2 );

  //Computation of the final right shift
  r1= r0 >> 16 ;
  return r1;
}

int16_t SoP_int_xn1(int16_t x0,int16_t x1,int16_t x2,int16_t x3)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
  int16_t c, x;
  int32_t r0, r1, r2, r3, r4;

  //Computation of c2*x2 in register r0
  c = 24604;
  r0 = c*x2;

  //Computation of c3*x3 in register r1
  c = 16384;
  r1 = c*x3;

  //Computation of r0+r1 in register r2
  r2= ( r0 >> 2 ) + ( r1 << 1 );

  //Computation of c0*x0 in register r0
  c = 25437;
  r0 = c*x0;

  //Computation of c1*x1 in register r1
  c = 17788;
  r1 = c*x1;

  //Computation of r0+r1 in register r3
  r3= r0 + r1 ;

  //Computation of r2+r3 in register r0
  r0= r2 + r3 ;

  //Computation of the final right shift
  r1= r0 >> 16 ;
  return r1;
}

int16_t SoP_int_xn2(int16_t x0,int16_t x1,int16_t x2,int16_t x3)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
  int16_t c, x;
  int32_t r0, r1, r2, r3, r4;

  //Computation of c2*x2 in register r0
  c = -20371;
  r0 = c*x2;

  //Computation of c3*x3 in register r1
  c = 16384;
  r1 = c*x3;

  //Computation of r0+r1 in register r2
  r2= ( r0 >> 4 ) + ( r1 << 2 );

  //Computation of c0*x0 in register r0
  c = -24969;
  r0 = c*x0;

  //Computation of c1*x1 in register r1
  c = -16660;
  r1 = c*x1;

  //Computation of r0+r1 in register r3
  r3= ( r0 << 1 ) + r1 ;

  //Computation of r2+r3 in register r0
  r0= r2 + r3 ;

  //Computation of the final right shift
  r1= r0 >> 16 ;
  return r1;
}

int16_t SoP_int_xn3(int16_t x0,int16_t x1,int16_t x2)
{
    /*      TP_Int_dec        */
    

    
    /*      TP_Int_sop        */
  int16_t c, x;
  int32_t r0, r1, r2, r3;

  //Computation of c1*x1 in register r0
  c = -18611;
  r0 = c*x1;

  //Computation of c2*x2 in register r1
  c = 18234;
  r1 = c*x2;

  //Computation of r0+r1 in register r2
  r2= r0 + ( r1 >> 7 );

  //Computation of c0*x0 in register r0
  c = 28863;
  r0 = c*x0;

  //Computation of r2+r0 in register r1
  r1= ( r2 >> 1 ) + ( r0 << 1 );

  //Computation of the final right shift
  r2= r1 >> 16 ;
  return r2;
}







double 
impulse(int c)
{
  /* Retourne un double de 16 bits (signe) de parties entieres */

  // sinusoide
  /* float x1 = sinf(0.01f*c*2*3.14*10);
  float x2 = sinf(0.01f*c*2*3.14);
  float x3 = (x1+2*x2)*4;
  double X = x3*powf(2.f,10); */

  //impulsion random

  double X = RandomFloat(c);
  return X;
}


int
main(void)
{
  srand(time(NULL));
  double res1=0.;
  int16_t     T0=0, xn0=0, xn1=0, xn2=0, xn3=0;
  double  u=impulse(0),y=0., max_y=0., T0_float=0., xn0_float=0., xn1_float=0., xn2_float=0., xn3_float=0.;
  
  int cpt = 0;
  while(cpt<200){

    /* Algo Entier */

    T0 = SoP_int_T0(xn0,(int16_t)u);
    xn0 = SoP_int_xn0(xn0,(int16_t)u,T0,xn1);
    xn1 = SoP_int_xn1(xn1,(int16_t)u,T0,xn2);
    xn2 = SoP_int_xn2(xn2,(int16_t)u,T0,xn3);
    xn3 = SoP_int_xn3(xn3,(int16_t)u,T0);

    /* Algo Double */

    // intermediate variables
    T0_float = xn0_float\
    + 0.467891544297045103295573653667815960943698883056640625*u*powf(2.f,-11)    ;

    // output(s)
    y = T0_float   ;
    if (abs(y) >max_y) max_y = abs(y);
    // states
    xn0_float = -0.12236628927527419541387843082702602259814739227294921875*xn0_float\
      + -1.3554822828291879233120198477990925312042236328125*u*powf(2.f,-11)    \
      + -0.00029145984329026486392422157223336398601531982421875*T0_float   \
      + xn1_float   ;
    xn1_float = 0.388136596759655450039616653157281689345836639404296875*xn1_float\
      + 0.54284325134847366545187696829088963568210601806640625*u*powf(2.f,-11)    \
      + 0.0469279637109754066415234774467535316944122314453125*T0_float   \
      + xn2_float   ;
    xn2_float = -0.7620024487294585480157138590584509074687957763671875*xn2_float\
      + -0.25421489137462227603236897266469895839691162109375*u*powf(2.f,-11)    \
      + -0.00485692688638879321860741811178741045296192169189453125*T0_float   \
      + xn3_float   ;
    xn3_float = 0.88082344225689779282362223966629244387149810791015625*xn3_float\
      + -0.1419926166774596598685320714139379560947418212890625*u*powf(2.f,-11)    \
      + 0.0002717061364786166333118444526917301118373870849609375*T0_float   ;

    // Affiche le signal de sortie entier, le signal d'entrée, le signal de sortie flottant et le plus grand signal
    //  de sortie observé
    printf("%d % 1.19e % 1.19e % 1.19e % 1.19e\n", cpt, T0*powf(2.f,-9), u*powf(2.f,-11), y, max_y);
    // Affiche l'erreur entre les signaux de sortie entier et flottant
    printf("%d % 1.19e \n", cpt, T0*powf(2.f,-9)-y);

    /* Calcul nouvelle impulsion */
    u = impulse(++cpt);
    

  }
  return 0;
}
