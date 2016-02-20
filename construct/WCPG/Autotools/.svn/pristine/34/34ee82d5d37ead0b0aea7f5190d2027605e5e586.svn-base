#ifndef _WCPG_H_
#define _WCPG_H_

#include "glue.h"
#include <time.h>
#include <float.h>
#include "inclusion_verif.h"

//Structure wcpg_result contains the information that will be saved after WCPG computation
typedef struct wcpg_result_struct
{
	int N;
	mpfr_t one_minus_rhoA;	
	mpfr_t maxSN;
	mpfr_t minSN;
	double time_overall;
	double time_Ncomp;
	double time_Summation;
	int inversion_Iter;
	mpfr_prec_t maxprec_PN;
	mpfr_prec_t maxprec_U;
	mpfr_prec_t maxprec_SN;


}wcpg_result;

void wcpg_result_init(wcpg_result *result);
void wcpg_result_clear(wcpg_result *result);
void wcpg_result_print(FILE *stream, wcpg_result *result, size_t ndigits);

/* THe function determines the minimal and maximum values of the
computed WCPG matrix and adds them to the corresonding fields
of the result structure. 
 */
void getDeltaOfWCPG(mpfr_t *reS, uint64_t p, uint64_t q, wcpg_result *result);

/* For an LTI filter given in its State-Space representation {A,B,C,D}, 
where A is n*n, B is n*q, C is p*n and D is p*q real matrix,
and for an eps>0 the function returns a multi-precision n*q real matrix Sk of Worst-Case Peak Gains 
of the system such that the overall error of computation is bounded by eps. */
int WCPG(mpfr_t *Sk, double *A, double *B, double *C, double *D, mpfr_t mpeps, uint64_t n, uint64_t p, uint64_t q, wcpg_result *result);



/* Support functions for N_lower_bound algorithm. Their placement to be duscussed later.
A priori, user does not need access to them (though possibly to lowerBoundN function).
However, circular dependency of headers makes result structure xcpg_result invisible, therefore
for the moment these functions are left here. */
void R_l(mpfi_t *reRl, mpfi_t *imRl, mpfi_t *rePhi, mpfi_t *imPhi, mpfi_t *rePsi, mpfi_t *imPsi, uint64_t n, uint64_t p, uint64_t q, int l);

int lowerBoundN(mpfi_t *rePhi, mpfi_t *imPhi, mpfi_t *rePsi, mpfi_t *imPsi, \
					 mpfi_t *reLambda, mpfi_t *imLambda,mpfr_t eps, uint64_t n, \
					  uint64_t p, uint64_t q, mpfr_prec_t prec, wcpg_result *context);









#endif  /* _WCPG_H */