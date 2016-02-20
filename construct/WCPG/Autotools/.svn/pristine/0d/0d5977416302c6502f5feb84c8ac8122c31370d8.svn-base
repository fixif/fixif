/*------------------------------------------------------------------------------------------------------*/
/* 
"lapack_linalg.h"
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



ATTANTION: THIS HEADER NEEDS REARRANGMENT INTO GROUPS, TODO LATER.
*/
/*-----------------------------------------------------------------------------------------------------*/


#ifndef MPFI_MATRIX_ALG_H
#define MPFI_MATRIX_ALG_H

#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "mpfi.h"
#include "mpfi_io.h"
#include "mpfr.h"
#include "clapack_linalg.h"
#include "glue.h"

mpfi_t *allocateMPFIMatrix(uint64_t n,uint64_t m, mp_prec_t prec);
void freeMPFIMatrix(mpfi_t *A, uint64_t n, uint64_t m) ;

void MPFIComplexMatrixAdd(mpfi_t *reC, mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n);
void MPFIComplexMatrixSub(mpfi_t *reC, mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n);
void MPFIComplexMatrixMultiply(mpfi_t *reC,mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch);
void MPFIComplexMatrixMultiplyMPFRComplexMatrix(mpfi_t *reC,mpfi_t *imC, mpfr_t *reA ,mpfr_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch);

void MPFIIdentMatrix(mpfi_t *reA, uint64_t n);
void MPFIZeroMatrix(mpfi_t *reA, uint64_t m, uint64_t n);

void MPFIComplexMatrixSetD(mpfi_t *reA, mpfi_t *imA, complexdouble *B,  uint64_t m, uint64_t n);
void MPFIComplexMatrixSet(mpfi_t *reA, mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t m, uint64_t n);
void MPFIComplexMatrixNeg(mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n);

// void MPFIComplexMatrixAbs(mpfr_t *reA, mpfr_t *imA, uint64_t n, uint64_t m);

void MPFIMatrixCopy(mpfi_t *B, mpfi_t *A, uint64_t m, uint64_t n);
void MPFIComplexMatrixPrint( mpfi_t *reA ,mpfi_t *imA, uint64_t m, uint64_t n);

/* Concatanation functions */
void MPFIComplexMatrixVerticalConcat(mpfi_t *reC,mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t n, uint64_t m, uint64_t q, mpfi_t *scratch);
void MPFIComplexMatrixHorizontalConcat(mpfi_t *reC,mpfi_t *imC, mpfi_t *reA ,mpfi_t *imA, mpfi_t *reB, mpfi_t *imB, uint64_t n, uint64_t m, uint64_t q, mpfi_t *scratch);


void mpfi_mul_complexdouble(mpfi_t reC, mpfi_t imC, mpfi_t reA, mpfi_t imA, complexdouble b);
void mpfi_mul_complex(mpfi_t reC, mpfi_t imC, mpfi_t reA, mpfi_t imA, mpfi_t reB, mpfi_t imB, mpfi_t scratch);
void mpfi_mul_fr_complex(mpfi_t reC, mpfi_t imC, mpfr_t reA, mpfr_t imA, mpfi_t reB, mpfi_t imB, mpfi_t scratch);

void mpfi_abs_complex(mpfi_t absA, mpfi_t reA, mpfi_t imA, mpfi_t scratch);


void MPFIComplexMatrixMidrad(mpfi_t *reA, mpfi_t *imA, mpfi_t *reC, mpfi_t *imC, uint64_t m, uint64_t n, mpfr_t eps, mpfr_t *scratch3);
void MPFIComplexMatrixMidradDouble(mpfi_t *reA, mpfi_t *imA, complexdouble *C, uint64_t m, uint64_t n, mpfr_t eps, mpfr_t *scratch3);

void ComplexScalarMultiplyMPFIMatrix(mpfi_t *reC, mpfi_t *imC, mpfi_t reK, mpfi_t imK, mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n, mpfi_t scratch);

void MPFIMatrixNormMax(mpfi_t max, mpfi_t *A, uint64_t m, uint64_t n, mpfi_t scratch);

void mpfi_maxabs(mpfi_t max, mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n, mpfi_t *scratch);

void MPFIConstructDiagonal(mpfi_t *recI, mpfi_t *imcI, mpfi_t rec, mpfi_t imc, uint64_t n);


void DoubleMatrixMultiplyMPFIMatrix(mpfi_t *reC,mpfi_t *imC, doublereal *A, mpfi_t *reB ,mpfi_t *imB, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch);
void MPFIMatrixMultiplyDoubleMatrix(mpfi_t *reC,mpfi_t *imC, mpfi_t *reB ,mpfi_t *imB, doublereal *A, uint64_t m, uint64_t n, uint64_t p, mpfi_t *scratch);



#endif