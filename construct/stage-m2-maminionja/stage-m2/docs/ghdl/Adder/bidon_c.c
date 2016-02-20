#include <stdio.h>
int sum( int i)
	{
	printf("Somme %d+%d+%d = %d\n", (i>>2)&1, (i>>1)&1, i&1, (((i >> 2) & 1) + ((i>>1) & 1) + ( i & 1)) & 1);
	return (((i >> 2) & 1) + ((i>>1) & 1) + ( i & 1)) & 1;
	}
