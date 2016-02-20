/*
 * clapack_functions_config.c
 *
 *  Created on: Jul 7, 2015
 *      Author: anastasiialozanova
 */

#include "clapack_functions_config.h"



void my_zgetrf(int *m, int *n, complexdouble *A,
 	int *lda, int *ipiv, int *info)
{
		
	#ifdef LAPACKE_HEADER		//if we have non-standard clapack wrapper

		//we convert complexdouble *A into lapacke_complex type
		lapacke_complex *newA = (lapacke_complex*)malloc((*m) * (*n) * sizeof(lapacke_complex));
		int i,j;
		for(i = 0; i < *m; ++i)
		{
			for(j = 0; j < *n; ++j)
			{
				newA[i*(*n)+j] = A[i*(*n)+j].r + I * A[i*(*n)+j].i;
			}
		}

		//then use the lapacke function
	/*	lapack_int LAPACKE_zgetrf( int matrix_order, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv ); */

		 *info = LAPACKE_zgetrf(LAPACK_ROW_MAJOR, *m, *n, newA, *lda, ipiv);

		//and convert back to complexdouble *A type
		for(i = 0; i < *m; ++i)
				{
					for(j = 0; j < *n; ++j)
					{
						A[i*(*n)+j].r = creal(newA[i*(*n)+j]);
						A[i*(*n)+j].i = cimag(newA[i*(*n)+j]);
					}
				}
		free(newA);
	#else
		zgetrf_((integer*)m, (integer*)n, (doublecomplex*)A, (integer*)lda, (integer*)ipiv, (integer*)info);
	#endif

}

void my_zgetri(int *n, complexdouble *A, int *lda,
		int *ipiv, complexdouble *work, int *lwork, int *info)
{
		
	#ifdef LAPACKE_HEADER 	//if we have non-standard clapack wrapper
		
		//we convert complexdouble *A into lapacke_complex type
		lapacke_complex *newA = (lapacke_complex*)malloc((*n) * (*n) * sizeof(lapacke_complex));
		
		int i,j;
		for(i = 0; i < *n; ++i)
		{
			for(j = 0; j < *n; ++j)
			{
				newA[i*(*n)+j] = A[i*(*n)+j].r + I * A[i*(*n)+j].i;
			}
		}

		//then use the lapacke function
		/* lapack_int LAPACKE_zgetri( int matrix_order, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           const lapack_int* ipiv ); */

		
		*info = LAPACKE_zgetri(LAPACK_ROW_MAJOR, *n, newA, *lda, ipiv);

		//and convert back to complexdouble *A type
		for(i = 0; i < *n; ++i)
				{
					for(j = 0; j < *n; ++j)
					{
						A[i*(*n)+j].r = creal(newA[i*(*n)+j]);
						A[i*(*n)+j].i = cimag(newA[i*(*n)+j]);
					}
				}
		free(newA);
	
	#else
		zgetri_((integer*)n, (doublecomplex*)A, (integer*)lda, (integer*)ipiv, (doublecomplex*)work, (integer*)lwork, (integer*)info);
	#endif



}

void my_dgeevx(int *n, double *A, int *lda, double *wr, double *wi, double *vl,  \
	       int *ldvl, double *vr, int *ldvr, int *ilo, int *ihi,  \
	       double *scale, double *abnrm, double *rconde, double *rcondv,  \
	       double *work, int *lwork, long int *iwork, int *info)

{

	#ifdef LAPACKE_HEADER 	//if we have non-standard clapack wrapper

	/*lapack_int LAPACKE_dgeevx( int matrix_order, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n, double* a,
                           lapack_int lda, double* wr, double* wi, double* vl,
                           lapack_int ldvl, double* vr, lapack_int ldvr,
                           lapack_int* ilo, lapack_int* ihi, double* scale,
                           double* abnrm, double* rconde, double* rcondv );	*/

		*info = LAPACKE_dgeevx(LAPACK_COL_MAJOR, 'N', 'V', 'V','B',*n, A, *lda, wr, wi, vl, *ldvl, vr, *ldvr, ilo, ihi, scale, abnrm, rconde, rcondv);

	#else
		/* dgeevx_(char *balanc, char *jobvl, char *jobvr, char *
	sense, integer *n, real *a, integer *lda, real *wr, real *wi, real *
	vl, integer *ldvl, real *vr, integer *ldvr, integer *ilo, integer *
	ihi, real *scale, real *abnrm, real *rconde, real *rcondv, real *work, 
	 integer *lwork, integer *iwork, integer *info);*/
		char *jobvr = "V";
		char *jobvl = "V";
		char *balanc = "N";
		char *sense = "B";
		dgeevx_(balanc, jobvl, jobvr, sense,(integer*)n, (doublereal*)A, (integer*)lda, wr, wi, \
				 vl, (integer*)ldvl, vr, (integer*)ldvr, (integer*)ilo, (integer*)ihi,\
				 scale, abnrm, rconde, rcondv, work, (integer*)lwork, (integer*)iwork,\
				 (integer*)info); 
	
	#endif
}


