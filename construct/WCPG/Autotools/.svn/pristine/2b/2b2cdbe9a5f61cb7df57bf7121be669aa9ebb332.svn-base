/*
 * inclusion_verif.h
 *
 *This is the header file, containing the prototypes for the eigensystem inclusion verification functions
 */

#ifndef INCLUSION_VERIF_H
#define INCLUSION_VERIF_H

#include <math.h>
#include "glue.h"
#include "mpfi_matrixalg.h"
#include "clapack_linalg.h"
#include "mpfr_linalg.h"

 typedef struct context_input_data_struct
 {
 	uint64_t n;
 	uint64_t k;
 	complexdouble *A;
 	complexdouble *v;
 	complexdouble lambda;
 	mpfi_t *reA, *imA;
 	mpfi_t *rev, *imv;
 	mpfi_t reLambda, imLambda;
 	mpfi_t *reEps, *imEps;
 } context_input_data;

 typedef struct context_algo_data_struct
 {
 	uint64_t n;
 	mpfr_prec_t prec;
 	mpfr_t *reR, *imR;
 	mpfi_t *reRint, *imRint;
 	mpfi_t *reC1, *imC1;
 	mpfi_t *reC, *imC;
 	mpfi_t *reZ, *imZ;

 	complexdouble *R;
 	//mpfi_t *reY, *imY;
 	//mpfi_t *reX, *imX;
 	//mpfi_t *reXX, *imXX;
 }context_algo_data;

void context_input_data_init(context_input_data *context_id, complexdouble *A, complexdouble *v, complexdouble lambda, uint64_t n,mpfr_prec_t prec);
void context_input_data_clear(context_input_data *context_id);
void context_algo_data_init(context_algo_data *context, uint64_t n, mpfr_prec_t prec);
void context_algo_data_clear(context_algo_data *context);

int checkEigensystemInclusion(mpfi_t *rev_corrected, mpfi_t *imv_corrected, mpfi_t relambda_corrected, mpfi_t imlambda_corrected, \
								complexdouble *A, complexdouble *v, complexdouble lambda, uint64_t n, doublereal eps_v, doublereal eps_lambda, mpfr_prec_t prec);


void compute_R(context_algo_data *algo, context_input_data *input);


/* Computes matrix [C1] = [A] - [lambda]*[I] */
void compute_C1(context_algo_data *algo, context_input_data *input);

/* Computes matrix [Z] = -R * ([C1] * v)
	where Z is of size n x 1 */
void compute_Z(context_algo_data *algo, context_input_data *input);

/* Computes matrix [C]:

	[Ctmp] = [C1]
	[Ctmp(:,k)] = [-v]
	[C] = [I] - R*[Ctmp]

	where C is of size n x n */
void compute_C(context_algo_data *algo, context_input_data *input);

 #endif