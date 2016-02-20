/* 
"main.c"

Represents an interactive test script for the WCPG computation.

The input file is HARDCODED, you need to uncomment file with path
to the test you wish to run.

After execution, enter an epsilon in format 1e-X
.
*/
#include "wcpg_test.h"



int main()
{


	/* Input files that we use for examples have following structure:
		n, n
		matrix_A, for wich column elements are separated with tabular and rows are each on new line 
		n, p
		matrix_B
		q, n
		matrix_C
		q, p
		matrix_D
	*/


	// // /* Old examples */
	 FILE *input = fopen("./examples/input3_f53bits.txt", "r");
	// FILE *input = fopen("./examples/txt/input2.txt", "r");
	// FILE *input = fopen("./examples/txt/input1.txt", "r");

	/* Arith examples */
	
	// FILE *input = fopen("./examples/txt/Arith/DL_Cor.txt", "r");
	// FILE *input = fopen("./examples/txt/Arith/Companion.txt", "r");
	// FILE *input = fopen("./examples/txt/Arith/butter12.txt", "r");
	// FILE *input = fopen("./examples/txt/Arith/ex3-60.txt", "r");

	 if(input == NULL)
	 	fprintf(stderr, "Error opening example file \n");


	/* Reading matrices */
	int n;	
	fscanf(input,"%d %d \n", &n, &n);	
	double *A;
	A = (double*)malloc(n*n*sizeof(double));
	clapack_matrix_inp_str_d(A,n, n, input);
	
	
	double *B;
	int q;
	fscanf(input,"%d %d \n", &n, &q);	
	B = (double*)malloc(n*q*sizeof(double));
	clapack_matrix_inp_str_d(B,n, q, input);
	
	double *C;
	int p;
	fscanf(input,"%d %d \n", &p, &n);	
	C = (double*)malloc(p*n*sizeof(double));
	clapack_matrix_inp_str_d(C,p, n, input);
	
	double *D;
	fscanf(input,"%d %d \n", &p, &q);	
	D = (double*)malloc(p*q*sizeof(double));
	clapack_matrix_inp_str_d(D,p, q, input);

	// Declaration and space allocation for the result wcpg approximation matrix
	//The default precision is 64, but the precision of the result variable is
	//modified by the algorithm in order to satisfy error bound eps.

	 /*-----------------------------------------------------------------------*/
	 //							Testing WCPG
	 /*-----------------------------------------------------------------------*/
	char epschar[256];
    	
   
  	// printf( "Enter epsilon in format 1e-X in base 2. \nFor example, 1e-20 : \n" );
  	// scanf( "%s", epschar ); 

  	printf("/*-----------------------------------------------------------------------*/\n \t\t\t\tTesting WCPG general function \n/*-----------------------------------------------------------------------*/\n");

	mpfr_t mpeps;
	mpfr_init2_my(mpeps, 64);

	
	mpfr_set_str(mpeps, epschar, 2, MPFR_RNDN);
	mpfr_set_str(mpeps, "1e-54", 2, MPFR_RNDN);
	mpfr_t *S_N;
	S_N = allocateMPFRMatrix(p,q, 64);

	wcpg_result result;
	if (!WCPG(S_N, A, B, C, D, mpeps, n, p, q, &result))
		printf("Could not compute WCPG \n");
	else
	{
		printf("\nWorst-case Peak Gain:\n");
		writeMPFRMatrix(stdout, S_N, p, q, 20, MPFR_RNDN);
		printf("\n");
		printf("Additional information on WCPG computation: \n\n");
		wcpg_result_print(stdout, &result, 5);
	}



	 /*-----------------------------------------------------------------------*/
	 //							Testing WCPG_ABCD
	 /*-----------------------------------------------------------------------*/
 	printf("/*-----------------------------------------------------------------------*/\n \t\t\t\tTesting WCPG_ABCD \n/*-----------------------------------------------------------------------*/\n");
 	double *W = (double*)malloc(p * q * sizeof(double*));
 	 if (!WCPG_ABCD(W, A, B, C, D,n, p, q))
 	 	printf("Could not compute WCPG \n");
 	 else
 	 {
 	 	printf("\nWorst-case Peak Gain of WCPG_ABCD:\n");
 	 	clapack_matrix_print_d(W, p, q);
 	 }

 /*-----------------------------------------------------------------------*/
	 //							Testing WCPG_ABCD_mprec
	 /*-----------------------------------------------------------------------*/
 	printf("/*-----------------------------------------------------------------------*/\n \t\t\t\tTesting WCPG_ABCD_mprec \n/*-----------------------------------------------------------------------*/\n");
 	mpfr_t *W_mprec;
	W_mprec = allocateMPFRMatrix(p,q, 64);
 	 if (!WCPG_ABCD_mprec(W_mprec, A, B, C, D,n, p, q, mpeps))
 	 	printf("Could not compute WCPG \n");
 	 else
 	 {
 	 	printf("\nWorst-case Peak Gain of WCPG_ABCD_mprec:\n");
 	 	clapack_matrix_print_d(W, p, q);
 	 }
	 /*-----------------------------------------------------------------------*/
	 //							Testing WCPG_tf
	 /*-----------------------------------------------------------------------*/
	  printf("/*-----------------------------------------------------------------------*/\n \t\t\t\tTesting WCPG_tf \n/*-----------------------------------------------------------------------*/\n");


	  double num[3] = {1.0, 2.0, 3.0};
	  double denum[2] = {1.0/2.0, 1.0/3.0};

	  p = 1;
	  q = 1;
	  double *W2 = (double*)malloc(p * q * sizeof(double*));
	  if (!WCPG_tf(W2, num, denum, 3, 2))
	  	printf("Could not compute WCPG \n");
	  else
	  {
	  	printf("\nWorst-case Peak Gain of WCPG_tf:\n");
	  	clapack_matrix_print_d(W2, 1, 1);
	  }


		mpfr_clear(mpeps);
		wcpg_result_clear(&result);
		freeMPFRMatrix(S_N, p, q);
		freeMPFRMatrix(W_mprec, p, q);
		free(A);
		free(B);
		free(C);
		free(D);




	return 0;
}
