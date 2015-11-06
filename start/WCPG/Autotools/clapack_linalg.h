/*
// "lapack_linalg.h"
This is the header file, containing the headers for
	- matrix input/output functions
	- functions for basic matrix arithmetic (multiplication, substraction, etc)
	- Linear System Solver
	- Eigensolver
All the functions work with matrices of CLAPACK's types doublereal and complexdouble.
All matrices are represented as one-dimension arrays, where for a n*m matrix A the element
A(i,j) is the element A[i * m + j] of the array.
 */

#ifndef CLAPACK_LINALG_H
#define CLAPACK_LINALG_H

#include <stdlib.h>
#include <math.h>
#include "glue.h"

#include "clapack_functions_config.h"
 

/* clapack matrix functions */
void 	clapack_matrix_neg			(complexdouble *op, int rows, int columns);
void 	clapack_matrix_diagonal		(complexdouble *rop, complexdouble v, int n);
void	clapack_matrix_ident		(complexdouble *Identity, int m, int n);
void 	clapack_matrix_sub			(complexdouble *rop, complexdouble *op1, complexdouble *op2, int rows, int cols);
void 	clapack_matrix_mul			(complexdouble *C, complexdouble *A, complexdouble *B, int n);
void 	clapack_rmatrix_as_zmatrix	(complexdouble *res, doublereal *a, int m, int n);
void 	clapack_matrix_transp_sqr	(complexdouble *T, complexdouble *A, int n);
void 	clapack_matrix_copy_d		(doublereal *cpy, doublereal *src, int m, int n);
void 	clapack_matrix_copy_z		(complexdouble *cpy, complexdouble *src, int m, int n);

complexdouble complexdouble_mul(complexdouble op1, complexdouble op2);
doublereal abs_complexdouble(complexdouble *z);

/*Matrix concat functions */
void 	clapack_matrix_ver_concat	(complexdouble *rop, complexdouble *op1, complexdouble *op2, int cols, int rows1, int rows2);
void 	clapack_matrix_hor_concat	(complexdouble *rop, complexdouble *op1, complexdouble *op2, int rows, int col1, int col2);

/* Eigendecomposition related functions */

void 	eigvect_to_matrix		(complexdouble *V, doublereal *v,int* flags, int n);
void 	wiwr_to_matrix			(complexdouble *p, doublereal *wr, doublereal *wi, int n);
void 	eigval_flags			(int *flags, doublereal *wi, doublereal *wr, int n);
int 	clapack_eigenSolver		(complexdouble *p, complexdouble *V,doublereal *verrbnd, doublereal *eerrbnd, doublereal *A, int n, double eps);

/* Linear system solution */
//void 	clapack_LSSolver					(complexdouble *X,doublereal *ferr,doublereal *berr, complexdouble *A, complexdouble *B, integer n, integer bcols);

/* Matrix inverse */
int 	clapack_complex_matrix_inverse					(complexdouble *U, complexdouble *A, integer n);




 #endif
