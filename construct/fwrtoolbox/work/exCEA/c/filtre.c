#include <stdio.h>
#include <stdlib.h>

/* importation de fainéant */
#include "filtre1double.c"


int main()
{
    double xn[10];
    FILE* fin;
    double u,y;
    int i;
    
    /* init */
    for( i=0; i<10; i++)
    	xn[i] = 0;
    fin = fopen("input.txt","r");
    	
    /* calcul des sorties */
    while (!feof(fin))
    {
    	fscanf( fin, "%lf", &u);
		y = filtre1double( u, xn);

		printf( "%.255g\n",y);
	}
	
	/* fin */
    fclose( fin);
    
    return EXIT_SUCCESS;
}
