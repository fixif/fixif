/*------------------------------------------------------------------------------------------------------*/
/* 
"GLUE.c"
This is the header file, containing the prototypes for
	- MPFR Complex matrix input/output functions
	- Conversion functions between complexdouble/doublereal/MPFR/MPFI types
	- CLAPACK matrices input/output functions
	- CLAPACK and MPFR matrix interaction functions
*/
/*-----------------------------------------------------------------------------------------------------*/



#ifndef GLUE_H
#define GLUE_H


#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>

#include "clapack_functions_config.h"	


#include <gmp.h>
#include <mpfr.h>
#include <mpfi.h>

#include "mpfi_cmpx.h"
#include "mpfr_linalg.h"
#include "mpfi_matrixalg.h"
#include "clapack_linalg.h"



extern mpfr_prec_t MaxPrec;


void mpfr_init2_my(mpfr_t op, mpfr_prec_t prec);
void mpfr_set_prec_my(mpfr_t op, mpfr_prec_t prec);


void *safeMalloc(size_t size);
void *safeCalloc(size_t nmemb, size_t size);
void *safeRealloc(void *ptr, size_t size);
void safeFree(void *ptr);
void MPFRComplexMatrixPrint( mpfr_t *reA ,mpfr_t *imA, uint64_t m, uint64_t n);


mpfr_prec_t getMaxPrecision(mpfr_t *ReA, mpfr_t *ImA,  uint64_t m, uint64_t n);

/*
Read a floating-point matrix A of size m * n from file stream, using rounding direction rnd.
Matrix A is assumed to be declared and initialized outside this function. Precision of matrix A is set outside this function.
Format of input: floating-point numbers must be in base 10 in form A@B or AeB, where A is mantissa and B is exponent.
*/
void readMPFRMatrix(mpfr_t *A, FILE *stream, uint64_t m, uint64_t n, mpfr_rnd_t rnd);

//  Convert a complex n * m matrix A represented in format mpfi_cmatrix_t to the format of two n * m mpfrt_t matrices 
// ReA and ImA containing real and imaginary parts of A respectively, possibly changing their precision.
// Matrices ReA and ImA are assumed to have been allocated outside this function. 
// The function uses the MPFR variable scratch as scratch space, assuming they have been allocated, possibly changing its
// precision and not clearing it.

// void MPFICtoMPFRMatrix(mpfr_t *ReA, mpfr_t *ImA, mpfi_cmatrix_t *A, mpfr_t scratch);


/* For a complex interval m x n matrix A the function returns its conversion to floating-point.
Output matrix B is assumed to be preallocated outside the function. Its precision may be changed.
 */

void MPFIMatrixtoMPFRMatrix(mpfr_t *reB, mpfr_t *imB, mpfi_t *reA, mpfi_t *imA, uint64_t m, uint64_t n);

 /* For a complex m x n MPFR matrix A the function returns its conversion to complex interval matrix. The result
 matrix B is assumed to be preallocated outside the function. Its precision may be changed. */

void MPFRMatrixToMPFIMatrix(mpfi_t *reB, mpfi_t *imB, mpfr_t *ReA, mpfr_t *ImA,uint64_t m, uint64_t n);

void complexdoubleCopy(complexdouble *Acopy, complexdouble *A, int m, int n);


/* Convert a complex n * m matrix A represented in format clapack complexdouble to the format of two n * m mpfrt_t matrices 
ReA and ImA containing real and imaginary parts of A respectively, possibly changing their precision.
Matrices ReA and ImA are assumed to have been allocated outside this function. 
The function uses the MPFR variable scratch as scratch space, assuming they have been allocated, possibly changing its
precision and not clearing it.
*/
void complexdoubleToMPFRMatrix(mpfr_t *ReA, mpfr_t *ImA, complexdouble *A, int m, int n);

/* Convert a complex n * m matrix A represented in format clapack complexdouble to the format of two the interval n * m mpfi_t matrices 
ReA and ImA containing real and imaginary parts of A respectively, possibly changing their precision.
Matrices ReA and ImA are assumed to have been allocated outside this function. 
The function uses the MPFR variable scratch as scratch space, assuming they have been allocated, possibly changing its
precision and not clearing it.
*/
void complexdoubleToMPFIMatrix(mpfi_t *ReA, mpfi_t *ImA, complexdouble *A, int m, int n);

/* Convert a real n * m matrix A represented in format clapack doublereal to the MPFR matrix ReA.
Matrix ReA is assumed to be declared and pre-allocated outside the function.
THe function changes precision of ReA to 64. 
*/
void doublerealToMPFRMatrix(mpfr_t *ReA, doublereal *A, int m, int n);


void MPFRMatrixToDoublecomplex(mpfr_t *ReA, mpfr_t *ImA, complexdouble *A, int m, int n);
// void MPFRMatrixToMPFI(mpfr_t *ReA, mpfr_t *ImA, mpfi_cmatrix_t *A, int m, int n);

/*
Write to file stream a complex m * n matrix rounded in the direction rnd with its real and imaginary parts in ReA and ImA respectively.
The function prints nmbr significant digits exactly, or if nmbr is 0, enough digits
so that matrix could be read back exactly.
Format of output: first line is two difits, representing size of matrix.
Then values are printed in form "ReAij + i*Imij", separated with tabulation.
The function prints matrix in base 10.
*/
void writeMPFRComplexMatrix(FILE *stream, mpfr_t *ReA, mpfr_t *ImA, uint64_t m, uint64_t n,size_t nmbr, mpfr_rnd_t rnd);



/* 
Write to file stream a real m * n matrix rounded in the direction rnd.
The function prints nmbr significant digits exactly, or if nmbr is 0, enough digits
so that matrix could be read back exactly.
Format of output: first line is two difits, representing size of matrix.
Then values are separated with tabulation.
The function prints matrix in base 10.
*/
void writeMPFRMatrix(FILE *stream, mpfr_t *A, uint64_t m, uint64_t n,size_t nmbr, mpfr_rnd_t rnd);

void getMPFRMatrixPrecision(mp_prec_t *ReA_p, mp_prec_t *ImA_p, mpfr_t *ReA, mpfr_t *ImA, uint64_t m, uint64_t n);

void absMPFRMatrix(mpfr_t *Aabs,mpfr_t *A, uint64_t m, uint64_t n);

/*Input & Output functions */
void 	clapack_matrix_inp_str_z		(complexdouble *A, int m, int k, FILE *stream);
void 	clapack_matrix_inp_str_d		(doublereal *A,int m, int k, FILE *stream);
void 	clapack_matrix_print_d			(doublereal *D, int mD, int kD);
void clapack_matrix_print_z(complexdouble *D, int m, int n);

/* For a doublereal m x n matrix A the function returns its maximum in absolute value
element, converted to MPFR. Output variable is assumed to be allocated outside the function and its
precision is not changes within the function. */
void getMaxInMPFR(mpfr_t max, doublereal *A, uint64_t m, uint64_t n);


/* CLAPACK and MPFI_MATRIX interaction functions */
// void mpfi_cmatrix_sub_complexdouble(mpfi_cmatrix_t *rop, mpfi_cmatrix_t *op1, complexdouble *op2, int rows, int columns);
// void mpfi_complexdouble_mul_cmatrix(mpfi_cmatrix_t *rop, complexdouble *op1, mpfi_cmatrix_t *op2, int ar, int ac_br, int bc);
// void clapack_complexdouble_to_mpfi_cmatrix(mpfi_cmatrix_t *rop, complexdouble *op, int n, int m);


#endif 