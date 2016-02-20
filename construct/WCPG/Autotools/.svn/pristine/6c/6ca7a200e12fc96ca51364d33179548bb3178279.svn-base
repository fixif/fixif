/*
 * clapack_functions_config.h
 *
 *  Created on: Jul 7, 2015
 *      Author: anastasiialozanova
 */

#ifndef SRC_LIB_CLAPACK_FUNCTIONS_CONFIG_H_
#define SRC_LIB_CLAPACK_FUNCTIONS_CONFIG_H_

#include <stdlib.h>
#include "config.h"



#include <f2c.h>

#ifdef CLAPACK_HEADER
	#include <clapack.h>
#endif

#ifdef LAPACK_HEADER
	#include <lapack.h>
#endif

#ifdef LAPACKE_HEADER
	#include <lapacke.h>
#endif

#ifdef BLAS_HEADER
	#include <blas.h>
#endif

#ifdef CBLAS_HEADER
	#include <cblas.h>
#endif

#ifdef BLASWRAP_HEADER
	#include <blaswrap.h>
#endif
 
#include <complex.h>
typedef struct complexdouble
{
	double r;
	double i;
}complexdouble;

#define doublereal double
#define lapack_int int
#define integer long int 
#define lapacke_complex double _Complex




void my_zgetrf(int *m, int *n, complexdouble *A,
 	int *lda, int *ipiv, int *info);

void my_zgetri(int *n, complexdouble *A, int *lda,
		int *ipiv, complexdouble *work, int *lwork, int *info);
void my_dgeevx(int* n, double *A, int* lda, double *wr, double *wi, double *vl,  
	       int* ldvl, double *vr, int* ldvr, int *ilo, int *ihi,  
	       double *scale, double *abnrm, double *rconde, double *rcondv,  
	       double *work, int *lwork, long int *iwork, int *info);

#endif /* SRC_LIB_CLAPACK_FUNCTIONS_CONFIG_H_ */