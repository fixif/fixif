#include <stdio.h>
#include <stdlib.h>
#include <assert.h>


#define int16 signed short
#define int32 signed int


/* importation de fainéant, à changer */
#include "filtreZ1.c"
#include "filtreZ1f.c"



int main()
{
    double *xn, *xnp;
    int16 *xnf, *xnpf;
    FILE* fin;
    double u, y, yf;
    
    
    /* init */
    xn = (double*) calloc( 10, sizeof(double) );
    xnp = (double*) calloc( 10, sizeof(double) );  
    xnf = (int16*) calloc( 10, sizeof(int16) );
    xnpf = (int16*) calloc( 10, sizeof(int16) );
    
    /* vérif */
    assert( sizeof(int32) == 4);
    assert( sizeof(int16) == 2);
    
	
    /* calcul des sorties */
    fin = fopen("input.txt","r");
    while (!feof(fin))
    {
    	fscanf( fin, "%lf", &u);

        y = filtreZ1( u, &xn, &xnp);                                  // algo double
        yf = filtreZ1f( (int16) (u*2048), &xnf, &xnpf) * 64;          // algo virgule fixe

		printf( "%.6g   %.6g\n", y, yf);
	}
	
	/* fin */
    fclose( fin);
    
    return EXIT_SUCCESS;
}
