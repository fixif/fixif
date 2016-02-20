/*------------------------------------------------------------------------------------------------------*/
/* 
"lapack_linalg.c"
This is the sourse file, containing the code for
	- MPFI matrix allocation/freeing functions
	- matrix input/output functions
	- functions for basic matrix arithmetic (multiplication, substraction, etc)
	- some complex interval numbers arithmetic operations (absolute value, multiplication, etc)
	- some functions for interaction of MPFI and MPFR matrices
All the functions work with complex interval multiple precision matrices of type mpfi_t.
Complex matrices are represented with two matrices holding its real and imaginary parts.
All matrices are represented as one-dimension arrays, where for a n*m matrix A the element
A(i,j) is the element A[i * m + j] of the array.
*/
/*-----------------------------------------------------------------------------------------------------*/


#include "mpfi_matrixalg.h"



/* Allocates a n * m matrix and initializes all entries to prec
   bits 
*/
mpfi_t *allocateMPFIMatrix(uint64_t n,uint64_t m, mp_prec_t prec) 
{
 	mpfi_t *A;
  	uint64_t i, j;
  	A = (mpfi_t *)safeCalloc(n * m, sizeof(mpfi_t));
  	for (i=0;i<n;i++) 
  	{
    	for (j=0;j<m;j++) 
    	{
      		mpfi_init2(A[i * m + j], prec);
    	}
  	}
  	return A;
}

void freeMPFIMatrix(mpfi_t *A, uint64_t n, uint64_t m) 
{
  uint64_t i, j;

  for (i=0;i<n;i++) 
  {
    for (j=0;j<m;j++) 
    {
      mpfi_clear(A[i * m + j]);
    }
  }
 
  free(A);
}

void MPFIComplexMatrixPrint( mpfi_t *reA ,mpfi_t *imA, uint64_t m, uint64_t n)
{
	printf("Interval matrix of size %llu x %llu \n", m, n);
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			printf("%f + i %f \t", mpfi_get_d(reA[i * n + j]), mpfi_get_d(imA[i * n + j]));
			// mpfi_out_str(stderr, 10, 20,reA[i * n + j]);
			// mpfi_out_str(stderr, 10, 20,imA[i * n + j]);
		}
		printf("\n");
	}

}

void mpfi_mul_complexdouble(mpfi_t reC, mpfi_t imC, mpfi_t reA, mpfi_t imA, complexdouble b)
{
	mpfi_t tmp;
	mpfi_init2(tmp,106);
	mpfi_mul_d(tmp, imA, b.i);		//tmp = imA * b.im
	mpfi_mul_d(reC, reA, b.r);			//reC = reA * b.r
	mpfi_sub(reC, reC, tmp);			//reC = reC - tmp = reA * b.r - imA * b.im

	mpfi_mul_d(tmp, imA, b.r);			//tmp = imA * b.r
	mpfi_mul_d(imC, reA, b.i);			//imC = reA * b.im
	mpfi_add(imC, imC, tmp);			//imC = imC + tmp = reA * b.im + imA * b.r

	mpfi_clear(tmp);
}


/* For two complex n x m MPFI matrices A and B, represented by their real and imaginary parts
the function returns matrix C = A + B */
void MPFIComplexMatrixAdd(mpfi_t *reC, mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_add(reC[i * n + j], reA[i * n + j], reB[i * n + j]);
			mpfi_add(imC[i * n + j], imA[i * n + j], imB[i * n + j]);
		}
	}
}

/* For two complex n x m MPFI matrices A and B, represented by their real and imaginary parts
the function returns matrix C = A - B */
void MPFIComplexMatrixSub(mpfi_t *reC, mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_sub(reC[i * n + j], reA[i * n + j], reB[i * n + j]);
			mpfi_sub(imC[i * n + j], imA[i * n + j], imB[i * n + j]);
		}
	}
}

/* For complex interval m x n matrix A and complex interval n x p matrix B the function returns a complex
m x p matrix C = A * B.
The function uses a scratch space of size 2, which is assumed to be preinitilized and preallocated
outside the function */

void MPFIComplexMatrixMultiply(mpfi_t *reC,mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch)
{
	int i,j,k;
	mp_prec_t prec1, prec2;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < p; ++j)
		{
			mpfi_set_ui(reC[i * p + j], 0);
			mpfi_set_ui(imC[i * p + j], 0);
			for(k = 0; k < n; ++k)
			{

				/* Real part of C: reC_ij = sum_k {reA_ik*reB_kj - imA_ik*imB_kj} for k=1..n */
				prec1 = mpfi_get_prec(reA[i * n + k]) >= mpfi_get_prec(reB[k * p + j]) ? mpfi_get_prec(reA[i * n + k]) : mpfi_get_prec(reB[k * p + j]);
				prec2 = mpfi_get_prec(imA[i * n + k]) >= mpfi_get_prec(imB[k * p + j]) ? mpfi_get_prec(imA[i * n + k]) : mpfi_get_prec(imB[k * p + j]);
				
				mpfi_set_prec(scratch[0], 2 * prec1);
				mpfi_set_prec(scratch[1], 2 * prec2);

				mpfi_mul(scratch[0], reA[i * n + k], reB[k * p + j]);
				mpfi_mul(scratch[1], imA[i * n + k], imB[k * p + j]);
				mpfi_sub(scratch[0], scratch[0], scratch[1]);	//scratch[0] = reA_ik*reB_kj - imA_ik*imB_kj

				mpfi_add(reC[i * p + j],reC[i * p + j], scratch[0]);		// reC_ij += reA_ik*reB_kj - imA_ik*imB_kj for k=1...n

				/* Imaginary part of C: imC_ij = sum_k {imA_ik*reB_kj + reA_ik*imB_kj} for k=1..n */
				prec1 = mpfi_get_prec(imA[i * n + k]) >= mpfi_get_prec(reB[k * p + j]) ? mpfi_get_prec(imA[i * n + k]) : mpfi_get_prec(reB[k * p + j]);
				prec2 = mpfi_get_prec(reA[i * n + k]) >= mpfi_get_prec(imB[k * p + j]) ? mpfi_get_prec(reA[i * n + k]) : mpfi_get_prec(imB[k * p + j]);
				
				mpfi_set_prec(scratch[0], 2 * prec1);
				mpfi_set_prec(scratch[1], 2 * prec2);

				mpfi_mul(scratch[0], imA[i * n + k], reB[k * p + j]);
				mpfi_mul(scratch[1], reA[i * n + k], imB[k * p + j]);
				mpfi_add(scratch[0], scratch[0], scratch[1]);	//scratch[0] = imA_ik*reB_kj + reA_ik*imB_kj

				mpfi_add(imC[i * p + j], imC[i * p + j], scratch[0]);		// reC_ij += imA_ik*reB_kj + reA_ik*imB_kj for k=1...n

			}
		}
	}
	

}

void ComplexScalarMultiplyMPFIMatrix(mpfi_t *reC, mpfi_t *imC, mpfi_t reK, mpfi_t imK, mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n, mpfi_t scratch)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for( j = 0; j < n; ++j)
		{
			mpfi_mul_complex(reC[i * n + j],imC[i * n + j], reA[i * n + j],imA[i * n + j], reK, imK, scratch);		
		}
	}
}


/* For complex m x n matrix A and complex interval n x p matrix B the function returns a complex
m x p matrix C = A * B.
The function uses a scratch space of size 2, which is assumed to be preinitilized and preallocated
outside the function */

void MPFIComplexMatrixMultiplyMPFRComplexMatrix(mpfi_t *reC,mpfi_t *imC, mpfr_t *reA ,mpfr_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch)
{
	int i,j,k;
	// printf("m = %llu, n = %llu, p = %llu \n", m, n, p);
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < p; ++j)
		{
			mpfi_set_ui(reC[i * p + j], 0);
			mpfi_set_ui(imC[i * p + j], 0);
			for(k = 0; k < n; ++k)
			{
				// printf("i = %d, j = %d, k = %d \n", i, j, k);
				// printf("%ld \n", mpfr_get_prec(reA[i * n + k]));
				/* Real part of C: reC_ij = sum_k {reA_ik*reB_kj - imA_ik*imB_kj} for k=1..n */
				mpfi_mul_fr(scratch[0], reB[k * p + j], reA[i * n + k]);
				
				mpfi_mul_fr(scratch[1], imB[k * p + j], imA[i * n + k]);
				mpfi_sub(scratch[0], scratch[0], scratch[1]);	//scratch[0] = reA_ik*reB_kj - imA_ik*imB_kj

				mpfi_add(reC[i * p + j],reC[i * p + j], scratch[0]);		// reC_ij += reA_ik*reB_kj - imA_ik*imB_kj for k=1...n
				
				/* Imaginary part of C: imC_ij = sum_k {reA_ik*reB_kj - imA_ik*imB_kj} for k=1..n */
				mpfi_mul_fr(scratch[0], reB[k * p + j], imA[i * n + k]);
				mpfi_mul_fr(scratch[1], imB[k * p + j], reA[i * n + k]);
				mpfi_add(scratch[0], scratch[0], scratch[1]);	//scratch[0] = imA_ik*reB_kj + reA_ik*imB_kj

				mpfi_add(imC[i * p + j], imC[i * p + j], scratch[0]);		// reC_ij += imA_ik*reB_kj + reA_ik*imB_kj for k=1...n
				
			}
		}
	}

}

/* For doublereal m x n matrix A and complex interval n x p matrix B and  the function returns a complex
m x p matrix C = A * B.
Function requires a scratch space of size at least 1.
*/
void DoubleMatrixMultiplyMPFIMatrix(mpfi_t *reC,mpfi_t *imC, doublereal *A, mpfi_t *reB ,mpfi_t *imB, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch)
{
	int i,j,k;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < p; ++j)
		{
			for(k = 0; k < n; ++k)
			{
				mpfi_mul_d(scratch[0], reB[k * p + j], A[i * n + k]);
				mpfi_add(reC[i * p + j],reC[i * p + j], scratch[0]);

				mpfi_mul_d(scratch[0], imB[k * p + j], A[i * n + k]);
				mpfi_add(imC[i * p + j],imC[i * p + j], scratch[0]);
			}
		}
	}

}

/* For doublereal m x n matrix A and complex interval n x p matrix B and  the function returns a complex
m x p matrix C = B * A.
Function requires a scratch space of size at least 1.
*/
void MPFIMatrixMultiplyDoubleMatrix(mpfi_t *reC,mpfi_t *imC, mpfi_t *reB ,mpfi_t *imB, doublereal *A, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch)
{
	int i,j,k;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < p; ++j)
		{
			for(k = 0; k < n; ++k)
			{
				// printf("debug re\n");
				mpfi_mul_d(scratch[0], reB[i * n + k], A[k * p + j]);
				mpfi_add(reC[i * p + j],reC[i * p + j], scratch[0]);
				// printf("debug im\n");
				mpfi_mul_d(scratch[0], imB[i * n + k], A[k * p + j]);
				mpfi_add(imC[i * p + j],imC[i * p + j], scratch[0]);
			}
		}
	}

}



void MPFIComplexMatrixNeg(mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n)
{
	int i,j;
		for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_neg(reA[i * n + j], reA[i * n + j]);
			mpfi_neg(imA[i * n + j], imA[i * n + j]);
		}
	}
}

void MPFIComplexMatrixSet(mpfi_t *reA, mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_set(reA[i * n + j], reB[i * n + j]);
			mpfi_set(imA[i * n + j], reB[i * n + j]);
		}
	}
}

void MPFIComplexMatrixSetD(mpfi_t *reA, mpfi_t *imA, complexdouble *B,  uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_set_d(reA[i * n + j], B[i * n + j].r);
			mpfi_set_d(imA[i * n + j], B[i * n + j].i);
		}
	}
}




/* Concatanation functions */

/* Vertical concatanation */


/* For complex interval n x m matrix A and complex interval n x q matrix B
the function returns complex n x (m+q) matrix C such that its first m columns are those of A and the rest
q columns are those of B 
*/

void MPFIComplexMatrixVerticalConcat(mpfi_t *reC,mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t n, uint64_t m, uint64_t q, mpfi_t *scratch)
{
	int i,j;
	for(i = 0; i < n; ++i)
	{
	
		for(j = 0; j < m + q; ++j)
		{
			if(j < m)
			{
				mpfi_set(reC[i * (m + q) + j], reA[i*m + j]);
				mpfi_set(imC[i * (m + q) + j], imA[i*m + j]);

			}
			else
			{
				mpfi_set(reC[i * (m + q) + j], reB[i*q + j - m]);
				mpfi_set(imC[i * (m + q) + j], imA[i*q + j - m]);
			}
		}
	}


}


/* Horizontal concatanation */

/* For complex interval m x n matrix A and complex interval q x n matrix B
the function returns complex n x (m+q) matrix C such that its first m rows are those of A and the rest
q rows are those of B 
Matrix C is assumed to be preallocated outside the function and its precision is not changed 
*/

void MPFIComplexMatrixHorizontalConcat(mpfi_t *reC,mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t n, uint64_t m, uint64_t q, mpfi_t *scratch)
{
	int i,j;
	for(j = 0; j < n; ++j)
	{
		for(i = 0; i < m + q; ++i)
		{
			if(i < m)
			{
				mpfi_set(reC[i * n + j], reA[i*n + j]);
				mpfi_set(imC[i * n + j], imA[i*n + j]);

			}
			else
			{
				mpfi_set(reC[i * n + j], reB[(i - m)*n + j ]);
				mpfi_set(imC[i * n + j], imA[(i - m)*n + j ]);
			}
		}
	}


}

void mpfi_complex_number_print(FILE *stream, mpfi_t reA, mpfi_t imA)
{
	mpfi_out_str(stream, 10, 5, reA);
	printf("\t + \t i*");
	mpfi_out_str(stream, 10, 5, imA);
	printf("\n");
}



/* For complex numbers a and b, represented by their real and imaginary parts, 
the function returnc complex number c = a * b 
The function requires a scratch space of size 1, assumed to be allocated outside the function*/
void mpfi_mul_complex(mpfi_t reC, mpfi_t imC, mpfi_t reA, mpfi_t imA, mpfi_t reB, mpfi_t imB, mpfi_t scratch)
{
	// printf("Multiplying A * B: \n");
	// mpfi_complex_number_print(stderr, reA, imA);
	// mpfi_complex_number_print(stderr, reB, imB);

	mpfi_mul(reC, reA, reB);
	mpfi_mul(scratch, imA, imB);
	mpfi_sub(reC, reC, scratch);

	mpfi_mul(imC, imA, reB);
	mpfi_mul(scratch, reA, imB);
	mpfi_add(reC, reC, scratch);

}

/* For complex number a and complex interval b, represented by their real and imaginary parts, 
the function returnc complex number c = a * b 
The function requires a scratch space of size 1, assumed to be allocated outside the function*/
void mpfi_mul_fr_complex(mpfi_t reC, mpfi_t imC, mpfr_t reA, mpfr_t imA, mpfi_t reB, mpfi_t imB, mpfi_t scratch)
{
	mpfi_mul_fr(reC, reB, reA);
	mpfi_mul_fr(scratch, imB, imA);
	mpfi_sub(reC, reC, scratch);

	mpfi_mul_fr(imC, reB, imA);
	mpfi_mul_fr(scratch, imB, reA);
	mpfi_add(reC, reC, scratch);

}

/* FOr a complex number A, represented by its real and imaginary parts, the funciton
computes its absolute value.
The funciton requires a scratch space of size 1, assumed to be preallocated outside the function. */
void mpfi_abs_complex(mpfi_t absA, mpfi_t reA, mpfi_t imA, mpfi_t scratch)
{
	mpfi_mul(absA, reA, reA);
	mpfi_mul(scratch, imA, imA);
	mpfi_add(absA, absA, scratch);
	mpfi_sqrt(absA, absA);
}


/* For a complex m x n matrix C and eps > 0 the function constructs an interval complex matrix A' which 
has matrix A as middle-point and eps as radius.
A scratch space of size 3 is required, and assumed to be preallocated outside the function.  */
void MPFIComplexMatrixMidrad(mpfi_t *reA, mpfi_t *imA, mpfi_t *reC, mpfi_t *imC, uint64_t m, uint64_t n, mpfr_t eps, mpfr_t *scratch3)
{
	int i,j;
	for(i = 0; i < m; ++i )
	{
		for(j = 0; j < n; ++j)
		{
			/* real part */

			mpfi_get_fr(scratch3[0], reC[i * n + j]); 						//middle of interval
			mpfr_sub(scratch3[1], scratch3[0], eps, MPFR_RNDN); 			//left bound
			mpfr_add(scratch3[2], scratch3[0], eps, MPFR_RNDN); 			//right bound
			mpfi_interv_fr(reA[i * n + j], scratch3[1], scratch3[2]);		//this function creates a new interval with bounds given as operands
			/* imaginary part */
			mpfi_get_fr(scratch3[0], imC[i * n + j]); 						//middle of interval
			mpfr_sub(scratch3[1], scratch3[0], eps, MPFR_RNDN); 			//left bound
			mpfr_add(scratch3[2], scratch3[0], eps, MPFR_RNDN); 			//right bound
			mpfi_interv_fr(imA[i * n + j], scratch3[1], scratch3[2]);		//this function creates a new interval with bounds given as operands
			
		}
	}
}

void MPFIComplexMatrixMidradDouble(mpfi_t *reA, mpfi_t *imA, complexdouble *C, uint64_t m, uint64_t n, mpfr_t eps, mpfr_t *scratch3)
{
	int i,j;
	for(i = 0; i < m; ++i )
	{
		for(j = 0; j < n; ++j)
		{
			/* real part */

			mpfr_set_d(scratch3[0], C[i * n + j].r, MPFR_RNDN); 						//middle of interval
			mpfr_sub(scratch3[1], scratch3[0], eps, MPFR_RNDN); 			//left bound
			mpfr_add(scratch3[2], scratch3[0], eps, MPFR_RNDN); 			//right bound
			mpfi_interv_fr(reA[i * n + j], scratch3[1], scratch3[2]);		//this function creates a new interval with bounds given as operands

			/* imaginary part */
			mpfr_set_d(scratch3[0], C[i * n + j].i, MPFR_RNDN); 						//middle of interval
			mpfr_sub(scratch3[1], scratch3[0], eps, MPFR_RNDN); 			//left bound
			mpfr_add(scratch3[2], scratch3[0], eps, MPFR_RNDN); 			//right bound
			mpfi_interv_fr(imA[i * n + j], scratch3[1], scratch3[2]);		//this function creates a new interval with bounds given as operands
			
		}
	}
}

void MPFIIdentMatrix(mpfi_t *reA, uint64_t n)
{
	int i,j;
	for(i = 0; i < n; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_set_ui(reA[i * n + j], 0);
		}
		mpfi_set_ui(reA[i * n + i], 1);
	}

}

void MPFIZeroMatrix(mpfi_t *reA, uint64_t m, uint64_t n)
{
	int i,j;
	for(i = 0; i < n; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_set_ui(reA[i * n + j], 0);
		}
	}
}


/* For a complex m x n matrix A the method determines a maximum in its absolute value element of A,
i.e. result = max_i,j {abs(A_ij)}.
The function uses a scratch space of size 2, assumed to be preallocated outside the function */
void mpfi_maxabs(mpfi_t max, mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n, mpfi_t *scratch)
{
	int i,j;
	mpfi_set_d(max, -1.0);

	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_abs_complex(scratch[0], reA[i * n + j], imA[i * n + j], scratch[1]);
			if(mpfi_cmp(scratch[0], max) > 0 )
				mpfi_set(max, scratch[0]);
		}
	}


}

void MPFIMatrixNormMax(mpfi_t max, mpfi_t *A, uint64_t m, uint64_t n, mpfi_t scratch)
{
	int i,j;
	mpfi_set_d(max, -1.0);

	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < m; ++j)
		{
			mpfi_abs(scratch, A[i * n + j]);
			if(mpfi_cmp(scratch, max) > 0 )
				mpfi_set(max, scratch);
		}
	}
}

/* For a complex number c, the method constructs a complex n x n matrix cI = c * I, with I - complex 
identity matrix of order n */
void MPFIConstructDiagonal(mpfi_t *recI, mpfi_t *imcI, mpfi_t rec, mpfi_t imc, uint64_t n)
{
	int i,j;
	for(i = 0; i < n; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			mpfi_set_ui(recI[i * n + j], 0);
			mpfi_set_ui(imcI[i * n + j], 0);
		}
		mpfi_set(recI[i * n + i], rec);
		mpfi_set(imcI[i * n + i], imc);
	}
}

/* For a n x m interval matrix A the function copies its content into a preallocated n x m matrix B.
 */
void MPFIMatrixCopy(mpfi_t *B, mpfi_t *A, uint64_t m, uint64_t n)
{
	
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			if(mpfi_get_prec(A[i * n + j]) > mpfi_get_prec(B[i * n + j]))
				mpfi_set_prec(B[i * n + j],mpfi_get_prec(A[i * n + j]));

			mpfi_set(B[i * n + j], A[i * n + j]);
		}
	}

}

// void MPFIComplexMatrixAbs(mpfr_t *reA, mpfr_t *imA, uint64_t m, uint64_t n)
// {
// 	// mpfi_t scratch, absA;
// 	// mpfi_init2(scratch, 106);
// 	// mpfi_init2(absA, 106);

// 	// int i,j;
// 	// for(i = 0; i < m; ++i)
// 	// {
// 	// 	for(j = 0; j < n; ++j)
// 	// 	{
// 	// 		printf("[%f %f] \t", mpfr_get_d(reA[i * n + j], MPFR_RNDN), mpfr_get_d(imA[i * n + j], MPFR_RNDN));
// 	// 	}
// 	// 	printf("\n");
// 	// }

// }


