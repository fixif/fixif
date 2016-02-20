/*------------------------------------------------------------------------------------------------------*/
/* 
"GLUE.c"
This is the sourse file, containing the code for
	- MPFR Complex matrix input/output functions
	- Conversion functions between complexdouble/doublereal/MPFR/MPFI types
	- CLAPACK matrices input/output functions
	- CLAPACK and MPFR matrix interaction functions
*/
/*-----------------------------------------------------------------------------------------------------*/
#include "glue.h"

// mpfr_prec_t MaxPrec = 0;

// void mpfr_init2_my(mpfr_t op, mpfr_prec_t prec)
// {
// 		mpfr_init2(op, prec);
// 		if (prec > MaxPrec)
// 			MaxPrec = prec;
		
// }

// void mpfr_set_prec_my(mpfr_t op, mpfr_prec_t prec)
// {
// 		mpfr_set_prec(op, prec);
// 		if (prec > MaxPrec)
// 			MaxPrec = prec;
		
// }


/* Allocates size bytes of memory; on failure prints an error message
   and calls exit(1) 
*/
void *safeMalloc(size_t size) {
  void *ptr;
  
  ptr = malloc(size);
  if (ptr == NULL) {
    fprintf(stderr, "Could not allocate %zd bytes of memory\n", size);
    exit(1);
  }

  return ptr;
}

/* Allocates an array of nmemb elements, each of which occupies size
   bytes of memory; on failure prints an error message and calls
   exit(1)
*/
void *safeCalloc(size_t nmemb, size_t size) 
{
  void *ptr;
  
  ptr = calloc(nmemb, size);
  if (ptr == NULL) {
    fprintf(stderr, "Could not allocate an array of %zd elements with %zd bytes of memory each\n", nmemb, size);
    exit(1);
  }

  return ptr;
}

/* Reallocates size bytes of memory at the location pointed by ptr; 
   on failure prints an error message and calls exit(1)
*/
void *safeRealloc(void *ptr, size_t size) 
{
  void *newPtr;
  
  newPtr = realloc(ptr, size);
  if ((newPtr == NULL) && (!((size == 0) && (ptr != NULL)))) {
      fprintf(stderr, "Could not rellocate %zd bytes of memory at address %p\n", size, ptr);
    exit(1);
  }

  return newPtr;
}

/* Frees the memory at the location pointed by ptr */
void safeFree(void *ptr) {
  free(ptr);
}

void MPFRComplexMatrixPrint( mpfr_t *reA ,mpfr_t *imA, uint64_t m, uint64_t n)
{
	printf("MPFR matrix of size %llu x %llu \n", m, n);
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			printf("%f + i %f \t", mpfr_get_d(reA[i * n + j], MPFR_RNDN), mpfr_get_d(imA[i * n + j], MPFR_RNDN));
		}
		printf("\n");
	}
}

void MPFRComplexMatrixPrint2( FILE *file, mpfr_t *reA ,mpfr_t *imA, uint64_t m, uint64_t n)
{
	printf("MPFR matrix of size %llu x %llu \n", m, n);
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			fprintf(file, "%f + i %f \t", mpfr_get_d(reA[i * n + j], MPFR_RNDN), mpfr_get_d(imA[i * n + j], MPFR_RNDN));
		}
		fprintf(file, "\n");
	}
}



/*
Read a floating-point matrix A of size m * n from file stream, using rounding direction rnd.
Matrix A is assumed to be declared and initialized outside this function. Precision of matrix A is set outside this function.
Format of input: floating-point numbers must be in base 10 in form A@B or AeB, where A is mantissa and B is exponent.
*/
void readMPFRMatrix(mpfr_t *A, FILE *stream, uint64_t m, uint64_t n, mpfr_rnd_t rnd)
{

	int i, j;
	for(i = 0; i < m; ++i)
	{
	      for(j = 0; j < n; ++j)
	      {
		      mpfr_inp_str(A[i * n + j], stream, (int)10, rnd);
	      }
	}
}

/*
Write to file stream a complex m * n matrix rounded in the direction rnd with its real and imaginary parts in ReA and ImA respectively.
The function prints nmbr significant digits exactly, or if nmbr is 0, enough digits
so that matrix could be read back exactly.
Format of output: first line is two difits, representing size of matrix.
Then values are printed in form "ReAij + i*Imij", separated with tabulation.
The function prints matrix in base 10.
*/
void writeMPFRComplexMatrix(FILE *stream, mpfr_t *ReA, mpfr_t *ImA, uint64_t m, uint64_t n,size_t nmbr, mpfr_rnd_t rnd)
{
	fprintf(stream, "%d %d \n", (int)m, (int)n);
	int i, j;
	for(i = 0; i < m; ++i)
	{
	      for(j = 0; j < n; ++j)
	      {
		      mpfr_out_str(stream, (int)10, nmbr, ReA[i * n + j], rnd);
		      fprintf(stream, " + i* ");
		      mpfr_out_str(stream, (int)10, nmbr, ImA[i * n + j], rnd);
		      fprintf(stream, "\t");
	      }
	      fprintf(stream, "\n");
	}
}

void writeMPFRMatrix(FILE *stream, mpfr_t *A, uint64_t m, uint64_t n,size_t nmbr, mpfr_rnd_t rnd)
{
	fprintf(stream, "%d %d \n", (int)m, (int)n);
	int i, j;
	for(i = 0; i < m; ++i)
	{
	      for(j = 0; j < n; ++j)
	      {
		      mpfr_out_str(stream, (int)10, nmbr, A[i * n + j], rnd);
		      fprintf(stream, "\t");
	      }
	      fprintf(stream, "\n");
	}
}



/* For a complex interval m x n matrix A the function returns its conversion to floating-point.
Output matrix B is assumed to be preallocated outside the function. Its precision may be changed.
 */
void MPFIMatrixtoMPFRMatrix(mpfr_t *reB, mpfr_t *imB, mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n)
{
	int i,j;
	mpfr_prec_t precA;
	mpfr_prec_t precB;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			precA = mpfi_get_prec(reA[i * n + j]);
			precB = mpfr_get_prec(reB[i * n + j]);
			if(precA > precB)
				mpfr_set_prec(reB[i * n + j], precA);
			mpfi_get_fr(reB[i * n + j], reA[i * n + j]);

			precA = mpfi_get_prec(imA[i * n + j]);
			precB = mpfr_get_prec(imB[i * n + j]);
			if(precA > precB)
				mpfr_set_prec(imB[i * n + j], precA);
			mpfi_get_fr(imB[i * n + j], imA[i * n + j]);

		}
	}
}





/* Convert a complex n * m matrix A represented in format clapack complexdouble to the format of two n * m mpfrt_t matrices 
ReA and ImA containing real and imaginary parts of A respectively, possibly changing their precision.
Matrices ReA and ImA are assumed to have been allocated outside this function. 
The function uses the MPFR variable scratch as scratch space, assuming they have been allocated, possibly changing its
precision and not clearing it.
*/
void complexdoubleToMPFRMatrix(mpfr_t *ReA, mpfr_t *ImA, complexdouble *A, int m, int n)
{
	int i, j;
	mp_prec_t prec = ceil(sizeof(complexdouble)/2);

	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			prec = (prec >= mpfr_get_prec(ReA[i * n + j]) ? prec : mpfr_get_prec(ReA[i * n + j]));
			mpfr_set_prec(ReA[i * n + j], prec);
			mpfr_set_d(ReA[i * n + j], A[i * n + j].r, MPFR_RNDN);
			
			prec = (prec >= mpfr_get_prec(ImA[i * n + j]) ? prec : mpfr_get_prec(ReA[i * n + j]));
			mpfr_set_prec(ImA[i * n + j], prec);
			mpfr_set_d(ImA[i * n + j], A[i * n + j].i,MPFR_RNDN );
		}
	}

}

/* Convert a real n * m matrix A represented in format clapack doublereal to the MPFR matrix ReA.
Matrix ReA is assumed to be declared and pre-allocated outside the function.
THe function changes precision of ReA to 64. 
*/
void doublerealToMPFRMatrix(mpfr_t *ReA, doublereal *A, int m, int n)
{
	int i, j;
	mp_prec_t prec = 64;

	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			mpfr_set_prec(ReA[i * n + j], prec);
			mpfr_set_d(ReA[i * n + j], A[i * n + j], MPFR_RNDN);
		}
	}
}

void MPFRMatrixToDoublecomplex(mpfr_t *ReA, mpfr_t *ImA, complexdouble *A, int m, int n)
{
	int i, j;

	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			A[i * n + j].r = mpfr_get_d(ReA[i * n + j], MPFR_RNDN);
			A[i * n + j].i = mpfr_get_d(ImA[i * n + j], MPFR_RNDN);

		}
	}

}

 /* For a complex m x n MPFR matrix A the function returns its conversion to complex interval matrix. The result
 matrix B is assumed to be preallocated outside the function. Its precision may be changed. */
void MPFRMatrixToMPFIMatrix(mpfi_t *reB, mpfi_t *imB, mpfr_t *reA, mpfr_t *imA,uint64_t m, uint64_t n)
{
	int i,j;
	mpfr_prec_t precA;
	mpfr_prec_t precB;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			precA = mpfr_get_prec(reA[i * n + j]);
			precB = mpfi_get_prec(reB[i * n + j]);
			if(precA > precB)
				mpfi_set_prec(reB[i * n + j], precA);
			mpfi_set_fr(reB[i * n + j], reA[i * n + j]);

			precA = mpfr_get_prec(imA[i * n + j]);
			precB = mpfi_get_prec(imB[i * n + j]);
			if(precA > precB)
				mpfi_set_prec(imB[i * n + j], precA);
			mpfi_set_fr(imB[i * n + j], imA[i * n + j]);

		}
	}

}


void getMPFRMatrixPrecision(mp_prec_t *ReA_p, mp_prec_t *ImA_p, mpfr_t *ReA, mpfr_t *ImA, uint64_t m, uint64_t n)
{
	int i, j;
	mpfr_prec_t maxR, maxI;
	maxR = 0; maxI = 0;
	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			if(mpfr_zero_p(ReA[i * n + j])) ReA_p[i * n + j] = 0;
			// else ReA_p[i * n + j] = mpfr_get_prec(ReA[i * n + j]);
			if(mpfr_zero_p(ImA[i * n + j])) ImA_p[i * n + j] = 0;
			// else ImA_p[i * n + j] = mpfr_get_prec(ImA[i * n + j]);
			// printf("(%d, %d) \t",(int)ReA_p[i * n + j], (int)ImA_p[i * n + j]);

			if (mpfr_get_prec(ReA[i * n + j]) > maxR) maxR = mpfr_get_prec(ReA[i * n + j]);
			if (mpfr_get_prec(ImA[i * n + j]) > maxR) maxI = mpfr_get_prec(ImA[i * n + j]);
		}
		// printf("\n");

	}
	fprintf(stderr, "Max precisions: (%ld, %ld)\n", maxR, maxI);
}

mpfr_prec_t getMaxPrecision(mpfr_t *ReA, mpfr_t *ImA,  uint64_t m, uint64_t n)
{
	int i, j;
	mpfr_prec_t maxR, maxI;
	maxR = 0; maxI = 0;
	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			if (mpfr_get_prec(ReA[i * n + j]) > maxR) maxR = mpfr_get_prec(ReA[i * n + j]);
			if (mpfr_get_prec(ImA[i * n + j]) > maxR) maxI = mpfr_get_prec(ImA[i * n + j]);
		}

	}
	int res = (maxR > maxI ? maxR : maxI);
	return res;
}


//The function computes the element-by-element abs of matrix A
void absMPFRMatrix(mpfr_t *Aabs,mpfr_t *A, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfr_abs(Aabs[i*n + j], A[i*n + j], MPFR_RNDN);
		}
	}

}

/*------------------------------------------------------------------------------------------------------*/
/* Input\Output functions for clapack */
/*------------------------------------------------------------------------------------------------------*/

void clapack_matrix_print_d(doublereal *D, int mD, int kD)
{
	int i,j;
	for(i = 0; i < mD; ++i)
	{
		for(j = 0; j < kD; ++j)
		{
		     printf("%e \t", (D[i*(kD) + j]));
		}
		printf("\n");
	}
}


void clapack_matrix_print_z(complexdouble *D, int m, int n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
		      printf("(%e + i*%e) \t",D[i*n + j].r, D[i*n + j].i);
			// printf("%e \t", abs_complexdouble(&D[i*(kD) + j]));
		}
		printf("\n");
	}
}

/* CHeck if any of the elements of a double m x n matrix is NaN.
Returns a non-zero value (true) if A has NaN value, and zero (false) otherwise. */
int matrixIsNan_double(doublereal *A, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
		    if(isnan(A[i*n + j])) return 1;	
		}
	}
	return 0;
}

/* CHeck if any of the elements of a complexdouble m x n matrix is NaN.
Returns a non-zero value (true) if A has NaN value, and zero (false) otherwise. */
int matrixIsNan_complexdouble(complexdouble *A, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
		    if(isnan(A[i*n + j].r)) return 1;	
		    if(isnan(A[i*n + j].i)) return 1;	
		}
	}
	return 0;

}

/* CHeck if any of the elements of a double m x n matrix is NaN.
Returns a non-zero value (true) if A has NaN value, and zero (false) otherwise. */
int matrixIsNan_mpfr(mpfr_t *A, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
		    if(!mpfr_number_p(A[i*n + j])) return 1;	
		}
	}
	return 0;

}

/*Read matrix from the input file. Returns 0 in case of success and 1 in case of a failure. */
int clapack_matrix_inp_str_d(doublereal *A,int m, int n, FILE *stream)
{
	
	int i, j;
	for(i = 0; i < m; ++i)
	{
	      for(j = 0; j < n; ++j)
	      {
		      if(!fscanf(stream, " %le ", &(A[i*n + j])))
		      {
		      		fprintf(stderr, "Problem reading matrix from file using scanf function. Process exit.\n");
		      		return 1;
		      }	
		      if(isnan(A[i*n + j]))	
		      {
		      		fprintf(stderr, "Problem reading matrix from file. One of the elements is a NaN. Process exit.\n");
		      		return 1;
		      }	
	      }
	}
	return 0;
  
}

void clapack_matrix_inp_str_z(complexdouble *A, int m, int k, FILE *stream)
{

	int i, j;
	for(i = 0; i < m; ++i)
	{
	      for(j = 0; j < k; ++j)
	      {
		      fscanf(stream, "%lf", &A[i*k + j].r );
		      fscanf(stream, "%lf", &A[i*k + j].i);
	      }
	}
  
}

/*------------------------------------------------------------------------------------------------------*/
/* CLAPACK and MPFI interaction functions */
/*------------------------------------------------------------------------------------------------------*/

/* Convert a complex n * m matrix A represented in format clapack complexdouble to the format of two the interval n * m mpfi_t matrices 
ReA and ImA containing real and imaginary parts of A respectively, possibly changing their precision.
Matrices ReA and ImA are assumed to have been allocated outside this function. 
The function uses the MPFR variable scratch as scratch space, assuming they have been allocated, possibly changing its
precision and not clearing it.
*/
void complexdoubleToMPFIMatrix(mpfi_t *ReA, mpfi_t *ImA, complexdouble *A, int m, int n)
{
	int i, j;
	// mp_prec_t prec = ceil(sizeof(complexdouble)/2);

	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			mpfi_set_ui(ReA[i * n + j], 0);
			mpfi_set_ui(ImA[i * n + j], 0);
			mpfi_set_d(ReA[i * n + j], A[i * n + j].r);
			
			mpfi_set_d(ImA[i * n + j], A[i * n + j].i);
		}
	}

	// for(i = 0; i < m; ++i)
	// {
	// 	for (j = 0; j < n; ++j)
	// 	{
	// 		prec = (prec >= mpfi_get_prec(ReA[i * n + j]) ? prec : mpfi_get_prec(ReA[i * n + j]));
	// 		mpfi_set_prec(ReA[i * n + j], prec);
	// 		mpfi_set_d(ReA[i * n + j], A[i * n + j].r);
			
	// 		prec = (prec >= mpfi_get_prec(ImA[i * n + j]) ? prec : mpfi_get_prec(ReA[i * n + j]));
	// 		mpfi_set_prec(ImA[i * n + j], prec);
	// 		mpfi_set_d(ImA[i * n + j], A[i * n + j].i);
	// 	}
	// }



}

void complexdoubleCopy(complexdouble *Acopy, complexdouble *A, int m, int n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for (j = 0; j < n; ++j)
		{
			Acopy[i * n + j].r = A[i * n + j].r;
			Acopy[i * n + j].i = A[i * n + j].i;
		}
	}

}



/* For a doublereal m x n matrix A the function returns its maximum in absolute value
element, converted to MPFR. Output variable is assumed to be allocated outside the function and its
precision is not changes within the function. */
void getMaxInMPFR(mpfr_t max, doublereal *A, uint64_t m, uint64_t n)
{
	doublereal maxA = abs(A[0]);
	doublereal current = abs(A[0]);
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			current = abs(A[i * n + j]);
			if(current > maxA)
				maxA = current;
		}
	}
	mpfr_set_d(max, maxA, MPFR_RNDU);
}




