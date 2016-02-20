#include <stdio.h>
#include <stdlib.h>
#include <assert.h>


#define int16 signed short
#define int32 signed int

#define ORDRE_FILTRE 4

#include "filtres.h"



int main()
{
    double *xn, *xnp;
    int16 *xnf, *xnpf;
    FILE* fin;
    double u, y, yf;
    
    
    /* init */
    xn = (double*) calloc( ORDRE_FILTRE, sizeof(double) );
    xnp = (double*) calloc( ORDRE_FILTRE, sizeof(double) );  
    xnf = (int16*) calloc( ORDRE_FILTRE, sizeof(int16) );
    xnpf = (int16*) calloc( ORDRE_FILTRE, sizeof(int16) );
    
    /* vérif */
    assert( sizeof(int32) == 4);
    assert( sizeof(int16) == 2);
    
	
    /* calcul des sorties */
    fin = fopen("input1.txt","r");
    while (!feof(fin))
    {
    	fscanf( fin, "%lf", &u);

        y = filtreZ1( u, &xn, &xnp);                                  // algo double
        yf = filtreZ1f( (int16) (u*2048), &xnf, &xnpf) * 64;          // algo virgule fixe
        //y = filtreZ6( u, &xn, &xnp);                                  // algo double
        //yf = filtreZ6f( (int16) (u*2048), &xnf, &xnpf) * 64;          // algo virgule fixe
        //y = filtreZ11( u, xn);                                  // algo double
        //yf = filtreZ11f( (int16) (u*2048), xnf) * 64;          // algo virgule fixe
		
		printf( "%.10g   %.10g\n", y, yf);
	}
	
	/* fin */
    fclose( fin);
    
    return EXIT_SUCCESS;
}
