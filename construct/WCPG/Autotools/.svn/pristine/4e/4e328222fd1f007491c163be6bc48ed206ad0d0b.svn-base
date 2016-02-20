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

/* Support functions for N_lower_bound algorithm. Their placement to be duscussed later.
A priori, user does not need access to them (though possibly to lowerBoundN function).
However, circular dependency of headers makes result structure xcpg_result invisible, therefore
for the moment these functions are left here. */
void R_l(mpfi_t *reRl, mpfi_t *imRl, mpfi_t *rePhi, mpfi_t *imPhi, mpfi_t *rePsi, mpfi_t *imPsi, uint64_t n, uint64_t p, uint64_t q, int l);

int lowerBoundN(mpfi_t *rePhi, mpfi_t *imPhi, mpfi_t *rePsi, mpfi_t *imPsi, \
					 mpfi_t *reLambda, mpfi_t *imLambda,mpfr_t eps, uint64_t n, \
					  uint64_t p, uint64_t q, mpfr_prec_t prec, wcpg_result *context);
					  

/* Compute the lower bound on the WCPG matrix of a LTI filter
represented with state matrices A, B, C, D with a given 
absolute error bound 2^k:
	W = W' + 2^k
where k < 0 is given in the argument.

Returns non-zero value (true) if computation is succesful and zero (false)
if could not compute lower bound on WCPG. */
int WCPGLowerBound(mpfr_t *W, mpfr_t* A, mpfr_t* B, mpfr_t* C, mpfr_t* D, uint64_t n, uint64_t p, uint64_t q, mpfr_exp_t k);


/* For an LTI filter given in its State-Space representation {A,B,C,D}, 
where A is n*n, B is n*q, C is p*n and D is p*q real matrix,
and for an eps>0 the function returns a multi-precision n*q real matrix Sk of Worst-Case Peak Gains 
of the system such that the overall error of computation is bounded by eps. */
int WCPG(mpfr_t *Sk, double *A, double *B, double *C, double *D, mpfr_t mpeps, uint64_t n, uint64_t p, uint64_t q, wcpg_result *result);



/** @brief For an LTI filter given in its State-Space representation {A,B,C,D},
where A is n*n, B is n*q, C is p*n and D is p*q real matrix the function 
returns integer value indicating if WCPG was successfully computed.
In p*q matrix W the Worst-Case peak gain is stored if algorithm successfully exited.
Input:
	A, B, C, D - pointers for double arrays representing filter in state-space realization
	n, p, q - order of filter, number of inputs and number of outputs respectively
	W (output) - if function succeeds, on the output will hold the p*q size WCPG matrix of the filter {A,B,C,D}
				space for W is assumed to be preallocated outside the function
Output:
	integer value equal to 1 if WCPG computation is successful and 0 otherwise.
 */
int WCPG_ABCD(double *W, double *A, double *B, double *C, double *D, uint64_t n, uint64_t p, uint64_t q);

/* For an LTI filter given in its State-Space representation {A,B,C,D},
where A is n*n, B is n*q, C is p*n and D is p*q real matrix the function 
returns integer value indicating if WCPG is successfully computed.
The function takes eps, a desired absolute error bound on the computed WCPG measure.
In p*q MPFR matrix W the Worst-Case peak gain is stored if algorithm successfully exited. 
Input:
	A, B, C, D - pointers for double arrays representing filter in state-space realization
	n, p, q - order of filter, number of inputs and number of outputs respectively
	W (output) - if function succeeds, on the output will hold the p*q MPFR WCPG matrix of the filter {A,B,C,D}
				matrix W is assumed to be preallocated outside the function
Output:
	integer value equal to 1 if WCPG computation is successful and 0 otherwise.*/
int WCPG_ABCD_mprec(mpfr_t *W, double *A, double *B, double *C, double *D, uint64_t n, uint64_t p, uint64_t q, mpfr_t eps);



/** @brief Nth order LTI filter is represented by its transfer function numerator (array of size Nb) and
denumerator (array of size Na), where N := max(Na, Nb).
For such a filter, the function computes its WCPG in double precision
(i.e. such that the absolute error of WCPG computation is bounded by 2^53).
Input:
	num - pointer for the array holding numerator coefficients, sizeof(num) must be Nb
	denum - pointer for the array holding denumerator coefficients, sizeof(denum) must be Na
	W(output) - if function succeeds, on the output will hold the WCPG of filter represented with transfer function num/denum
				space for W is assumed to be preallocated outside the function
Output:
	integer value equal to 1 if WCPG computation is successful and 0 otherwise.
*/
int WCPG_tf(double *W, double *num, double *denum, uint64_t Nb, uint64_t Na);


#endif  /* _WCPG_H */