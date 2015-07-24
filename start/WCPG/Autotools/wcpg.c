#include "wcpg.h"


/**
 * @brief For an LTI filter given in its State-Space representation {A,B,C,D},
where A is n*n, B is n*q, C is p*n and D is p*q real matrix the function 
returns integer value indicating if WCPG is successfully computed.
In p*q matrix W the Worst-Case peak gain is stored if algorithm successfully exited. */
int WCPG_ABCD(double *W, double *A, double *B, double *C, double *D, uint64_t n, uint64_t p, uint64_t q)
{
	int flag = 0;

	mpfr_t mpeps;
	mpfr_init2_my(mpeps, 64);
	mpfr_set_str(mpeps, "1e-54", 2, MPFR_RNDN);

	mpfr_t *S;
	S = allocateMPFRMatrix(p, q, 54);


	wcpg_result result;
	if (!WCPG(S, A, B, C, D, mpeps, n, p, q, &result))
	{
		mpfr_clear(mpeps);
		freeMPFRMatrix(S, p, q);
		wcpg_result_clear(&result);
		return 0;
	}
		
	else
	{
		int i, j;
		for(i = 0; i < p; ++i)
		{
			for(j = 0; j < q; ++j)
			{
				W[i * q + j] = mpfr_get_d(S[i * q + j], MPFR_RNDN);
			}
		}
		mpfr_clear(mpeps);
		freeMPFRMatrix(S, p, q);
		return 1;
	}

}

/* For an LTI filter given in its State-Space representation {A,B,C,D},
where A is n*n, B is n*q, C is p*n and D is p*q real matrix the function 
returns integer value indicating if WCPG is successfully computed.
The function takes eps, a desired absolute error bound on the computed WCPG measure.
In p*q MPFR matrix W the Worst-Case peak gain is stored if algorithm successfully exited. */
int WCPG_ABCD_mprec(mpfr_t *W, double *A, double *B, double *C, double *D, uint64_t n, uint64_t p, uint64_t q, mpfr_t eps)
{

	wcpg_result result;
	if (!WCPG(W, A, B, C, D, eps, n, p, q, &result))
	{
		wcpg_result_clear(&result);
		return 0;
	}
	else
	{
		wcpg_result_clear(&result);
		return 1;
	}


}


/* Nth order LTI filter is represented by its transfer function numerator (array of size Nb) and
denumerator (array of size Na), where N := max(Na, Nb).
For such a filter, the function computes its WCPG */
int WCPG_tf(double *W, double *num, double *denum, uint64_t Nb, uint64_t Na)
{

	// FIrst, we need to convert tf representation to state-space
	//and then call the general WCPG function.

	uint64_t flag = 0;

	uint64_t n = (Nb-1) >= Na ? Nb - 1 : Na;		//n = max(Nb, Na)

	double *alpha = (double*)malloc((n) * sizeof(double*));
	double *beta = (double*)malloc((n) * sizeof(double*));
	double *b = (double*)malloc((n+1) * sizeof(double*));
	int i, j;
	for(i = 0; i < n; ++i)
	{
		if(i < (Na)) alpha[i] = denum[i];
		else alpha[i] = 0.0;	

		
	}
	for(i = 0; i < (n+1); ++i)
	{
		if(i < Nb + 1) b[i] = num[i];
		else b[i] = 0.0;
	}

	double b0 = num[0];
	for(i = 0; i < n; ++i)
	{
		beta[i] = b[i+1] - b0 * alpha[i];
	}
	uint64_t p = 1;
	uint64_t q = 1;

	double *A = (double*)malloc(n * n * sizeof(double*));
	double *B = (double*)malloc(n * q * sizeof(double*));
	double *C = (double*)malloc(p * n * sizeof(double*));
	double *D = (double*)malloc(p * q * sizeof(double*));

	//building matrix A;
	for(i = 0; i < n; ++i)
	{
		if(i == 0)
		{
			for(j = 0; j < n; ++j)
			{
				A[i * n + j] = -alpha[j];
			}
		}
		else
			A[i * n + i - 1] = 1.0;	

	}

	//building matrix B
	B[0] = 1.0;
	for(i = 1; i < n; ++i)
		B[i] = 0.0;
	
	//building matrix C
	for(i = 0; i < n; ++i)
		C[i] = beta[i];

	//building matrix D
	D[0] = b0;


	//printing result state-space
//	printf("Matrix A: \n");
//	clapack_matrix_print_d(A, n, n);
//	printf("Matrix B: \n");
//	clapack_matrix_print_d(B, n, 1);
//	printf("Matrix C: \n");
//	clapack_matrix_print_d(C, 1, n);
//	printf("Matrix D: \n");
//	clapack_matrix_print_d(D, 1, 1);

	//computing WCPG with double precision
	if(!WCPG_ABCD(W, A, B, C, D, n, 1, 1))
	{
		free(alpha);
		free(beta);
		free(b);
		free(A);
		free(B);
		free(C);
		free(D);
		return 0;
	}

	else
	{
		free(alpha);
		free(beta);
		free(b);
		free(A);
		free(B);
		free(C);
		free(D);
		return 1;
	}
	
}


