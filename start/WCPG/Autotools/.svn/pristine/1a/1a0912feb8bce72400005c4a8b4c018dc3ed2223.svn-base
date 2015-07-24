/*
 * mpfi_cmpx.h
 *
 *	This is an extension of MPFI library.
 *	Basic complex interval operations support added.
 *
 *
 */

#ifndef MPFI_CMPX_H_
#define MPFI_CMPX_H_

#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "mpfi.h"
#include "mpfi_io.h"
#include "mpfr.h"


/* Defining complex number */
 typedef struct 
 {
 	mpfr_t real;
 	mpfr_t imag;
 }mpfr_tc;

/* Defining complex interval */
typedef struct 
{
	mpfi_t real;
	mpfi_t imag;
}mpfi_tc;


/* Initialization functions */
void 	mpfi_c_init			(mpfi_tc *x);  													//tested
void 	mpfi_c_init2		(mpfi_tc *x, mp_prec_t prec);
void 	mpfi_c_init3		(mpfi_tc *x, mp_prec_t r_prec, mp_prec_t i_prec);
void 	mpfi_c_clear		(mpfi_tc *x);

// /* Initialization functions for MPFR complex */
// void 	mpfr_c_init			(mpfr_tc *x);  													//tested
// void 	mpfr_c_init2		(mpfr_tc *x, mp_prec_t prec);
// void 	mpfr_c_init3		(mpfr_tc *x, mp_prec_t r_prec, mp_prec_t i_prec);
// void 	mpfr_c_clear		(mpfr_tc *x);


/* Assignment functions */
void 	mpfi_c_set			(mpfi_tc *rop, mpfi_tc *op);							//tested
void 	mpfi_c_set_d		(mpfi_tc *rop, double real, double imag);			//tested
int 	mpfi_c_set_str		(mpfi_tc *rop, char *s, int base); 							//tested
void 	mpfi_c_swap			(mpfi_tc *x, mpfi_tc *y);

// /* Assignment functions for MPFR complex*/
// void 	mpfr_c_set 			( mpfr_tc *rop, mpfr_tc *op, mpfr_rnd_t rnd);						//tested
// void 	mpfr_c_set_d		(mpfr_tc *rop, double real, double imag, mpfr_rnd_t rnd);			//tested
// int 	mpfr_c_set_str		(mpfr_tc *rop, char *s, int base, mpfr_rnd_t rnd); 							//tested


/* Input and Output functions */
size_t 	mpfi_c_out_str		(FILE *stream, int base, size_t n_digits, mpfi_tc *op); 		//tested
size_t 	mpfi_c_inp_str		(mpfi_tc *op, FILE *stream, int base); 						//tested

/* Basic arithmetic functions between complex intervals*/
void 	mpfi_c_add			(mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2);				//tested
int 	mpfi_c_add_d			(mpfi_tc *rop, mpfi_tc *op1, double op2);							//tested
void 	mpfi_c_sub			(mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2);				// to test
int 	mpfi_c_sub_d			(mpfi_tc *rop, mpfi_tc *op1, double op2);							// to test
void 	mpfi_c_mul			(mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2);				// to test
void 	mpfi_c_mul_d			(mpfi_tc *rop, mpfi_tc *op1, double op2);				// to test
void 	mpfi_c_div			(mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2);				// to test
void 	mpfi_c_div_d			(mpfi_tc *rop, mpfi_tc *op1, double op2);				// to test
void 	mpfi_c_conj			(mpfi_tc *rop, mpfi_tc *op);
void 	mpfi_c_abs			(mpfi_t *rop, mpfi_tc *op);


/*Basic arithmetic functions between complex and real intervals */
void 	mpfi_c_add_r		(mpfi_tc *rop, mpfi_tc *op1, mpfi_t op2);
void 	mpfi_c_sub_r		(mpfi_tc *rop, mpfi_tc op1, mpfi_t op2);
void 	mpfi_r_sub_c		(mpfi_tc *rop, mpfi_t op1, mpfi_tc op2);
void	mpfi_c_mul_r		(mpfi_tc *rop, mpfi_tc op1, mpfi_t op2);
void	mpfi_r_mul_c		(mpfi_tc *rop, mpfi_t op1, mpfi_tc op2);
void 	mpfi_c_div_r		(mpfi_tc *rop, mpfi_tc *op1, mpfi_t *op2);

/* Interval functions with floating-point results */
int 	mpfi_c_diam_abs 	(mpfr_tc *rop, mpfi_tc *op);
int 	mpfi_c_diam_real	(mpfr_tc *rop, mpfi_tc *op);
int 	mpfi_c_diam			(mpfr_tc *rop, mpfi_tc *op);
int 	mpfi_c_mag			(mpfr_tc *rop, mpfi_tc *op);
int 	mpfi_c_mid			(mpfr_tc *rop, mpfi_tc *op);
void 	mpfi_c_alea			(mpfr_tc *rop, mpfi_tc *op);

/* Conversion functions */
void 	mpfi_c_get_d		(double* rop,  mpfi_tc *op);
void 	mpfi_c_get_fr		(mpfr_tc *rop, mpfi_tc *op);

/* Comparison functions */
int		mpfi_c_cmp			(mpfi_tc *op1, mpfi_tc *op2);	//compare for equality, if not equal compare absolute values
int 	mpfi_c_is_zero		(mpfi_tc *op);
int 	mpfi_c_has_zero		(mpfi_tc *op);
int 	mpfi_c_nan_p		(mpfi_tc *op);
int 	mpfi_c_inf_p		(mpfi_tc *op);
int 	mpfi_c_bounded_p	(mpfi_tc *op);
int 	mpfi_c_are_conj		(mpfi_tc *op1, mpfi_tc *op2);

/* Set functions on complex intervals */
int 	mpfi_c_is_strictly_inside	(mpfi_tc *op1, mpfi_tc *op2);
int 	mpfi_c_is_inside			(mpfi_tc *op1, mpfi_tc *op2);
int 	mpfi_c_is_empty				(mpfi_tc *op);




#endif /* MPFI_CMPX_H_ */
