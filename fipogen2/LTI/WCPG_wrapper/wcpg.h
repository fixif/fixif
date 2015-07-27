#ifndef WCPG_H
#define WCPG_H

#include "_wcpg.h"



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




#endif  /* WCPG_H */
