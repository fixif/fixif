#include "mpfi_cmpx.h"



void mpfi_c_abs(mpfi_t *rop, mpfi_tc *op)
{

	// printf("\n -----------Entering mpfi_c_abs ---------------\n");
	// printf("Searching for absolute value of \n");
	// mpfi_c_out_str(stderr, 10, 10, op);

	mpfi_t a, b, c;
	mpfi_init(a);
	mpfi_init(b);
	mpfi_init(c);
	
	mpfi_mul(a, op->real,  op->real);

	mpfi_mul(b, op->imag, op->imag);
	// 	printf("\n b^2 \n");
	// mpfi_out_str(stderr, 10, 10, b);
	mpfi_add(c, a, b);
	// printf("\n C = a^2 + b^2 \n");
	// mpfi_out_str(stderr, 10, 10, c);
	mpfi_sqrt(*rop, c);

	// printf("\n Result \n");
	// mpfi_out_str(stderr, 10, 10, *rop);

	// printf("\n -----------Leaving mpfi_c_abs ---------------\n");
	mpfi_clear(a);
	mpfi_clear(b);
	mpfi_clear(c);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_add( mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2)
{
	mpfi_add(rop->real, op1->real, op2->real);
	mpfi_add(rop->imag, op1->imag, op2->imag);
}
int mpfi_c_add_d(mpfi_tc *rop, mpfi_tc *op1, double op2)
{
	mpfi_set(rop->imag, op1->imag);
	return mpfi_add_d(rop->real, op1->real, op2);
}
void mpfi_c_add_r(mpfi_tc *rop, mpfi_tc *op1, mpfi_t op2)
{
	mpfi_set(rop->imag, op1->imag);
	mpfi_add(rop->real, op1->real, op2);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_alea(mpfr_tc *rop, mpfi_tc *op)
{
	mpfi_alea(rop->real, op->real);
	mpfi_alea(rop->imag, op->imag);
}
/*
 * cbounded_p.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_bounded_p(mpfi_tc *op)
{
	if (mpfi_bounded_p(op->real) != 0 || mpfi_bounded_p(op->imag) != 0)
			return 1;
	return 0;
}
/*
 * c_clear.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_clear(mpfi_tc *x)
{
	mpfi_clear(x->real);
	mpfi_clear(x->imag);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int	 mpfi_c_cmp(mpfi_tc *op1, mpfi_tc *op2)
{
	//compare for equality
	if  ( mpfi_cmp(op1->real, op2->real) == 0 && mpfi_cmp(op1->imag, op2->imag) == 0)
		return 0;
	else
	{
		mpfi_t abs1, abs2;
		mpfi_init(abs1);
		mpfi_init(abs2);
		mpfi_c_abs(&abs1, op1);
		mpfi_c_abs(&abs2, op2);
		return mpfi_cmp(abs1, abs2);
	}
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
/* Interval functions with floating-point results */
int mpfi_c_diam_abs (mpfr_tc *rop, mpfi_tc *op)
{
	int i1 = mpfi_diam_abs(rop->real, op->real);
	int i2 = mpfi_diam_abs(rop->imag, op->imag);
	return i1 + i2;
}
int mpfi_c_diam_real(mpfr_tc *rop, mpfi_tc *op)
{
	int i1 = mpfi_diam_rel(rop->real, op->real);
	int i2 = mpfi_diam_rel(rop->imag, op->imag);
	return i1 + i2;
}
int mpfi_c_diam(mpfr_tc *rop, mpfi_tc *op)
{
	int i1 = mpfi_diam(rop->real, op->real);
	int i2 = mpfi_diam(rop->imag, op->imag);
	return i1 + i2;
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_div( mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2)			//can be improved
{
	mpfi_t a,b,x,y, p, q, num1, num2, dnom;
	mpfi_init(a);
	mpfi_init(b);
	mpfi_init(x);
	mpfi_init(y);
	mpfi_init(p);
	mpfi_init(q);
	mpfi_init(num1);
	mpfi_init(num2);
	mpfi_init(dnom);
	mpfi_mul(a, op1->real, op2->real);
	mpfi_mul(b, op1->imag, op2->imag);
	mpfi_mul(x, op2->real, op1->imag);
	mpfi_mul(y, op1->real, op2->imag);
	mpfi_sqr(p, op2->real);
	mpfi_sqr(q, op2->imag);
	mpfi_add(num1, a, b);
	mpfi_sub(num2, x, y);
	mpfi_add(dnom, p, q);
	mpfi_div(rop->real, num1, dnom);
	mpfi_div(rop->imag, num2, dnom);
	mpfi_clear(a);
	mpfi_clear(b);
	mpfi_clear(x);
	mpfi_clear(y);
	mpfi_clear(p);
	mpfi_clear(q);
	mpfi_clear(num1);
	mpfi_clear(num2);
	mpfi_clear(dnom);
}
void mpfi_c_div_d( mpfi_tc *rop, mpfi_tc *op1, double op2)
{
	mpfi_div_d(rop->real, op1->real, op2);
	mpfi_div_d(rop->imag, op1->imag, op2);
}
int mpfi_c_is_empty(mpfi_tc *op)
{
	if (mpfi_is_empty(op->imag) > 0  && mpfi_is_empty(op->real) > 0 )
			return 1;
		return 0;
}
/*
 * cinf_p.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_inf_p(mpfi_tc *op)
{
	if (mpfi_inf_p(op->real) != 0 || mpfi_inf_p(op->imag) != 0)
			return 1;
		return 0;
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
/* Initialization functions */
void mpfi_c_init(mpfi_tc *x)
{
	mpfi_init(x->real);
	mpfi_init(x->imag);
}
void mpfi_c_init2(mpfi_tc *x, mp_prec_t prec)
{
	mpfi_init2(x->real, prec);
	mpfi_init2(x->imag, prec);
}
void mpfi_c_init3(mpfi_tc *x, mp_prec_t r_prec, mp_prec_t i_prec)
{
	mpfi_init2(x->real, r_prec);
	mpfi_init2(x->imag, i_prec);
}

// /* Initialization functions for MPFR complex*/
// void mpfr_c_init(mpfr_tc *x)
// {
// 	mpfr_init(x->real);
// 	mpfr_init(x->imag);
// }
// void mpfr_c_init2(mpfr_tc *x, mp_prec_t prec)
// {
// 	mpfr_init2(x->real, prec);
// 	mpfr_init2(x->imag, prec);
// }
// void mpfr_c_init3(mpfr_tc *x, mp_prec_t r_prec, mp_prec_t i_prec)
// {
// 	mpfr_init2(x->real, r_prec);
// 	mpfr_init2(x->imag, i_prec);
// }

/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_is_strictly_inside(mpfi_tc *op1, mpfi_tc *op2)
{
	if (mpfi_is_strictly_inside(op1->imag, op2->imag) > 0  && mpfi_is_strictly_inside(op1->real, op2->real) > 0 )
		return 1;
	return 0;
}
int mpfi_c_is_inside(mpfi_tc *op1, mpfi_tc *op2)
{
	if (mpfi_is_inside(op1->imag, op2->imag) > 0  && mpfi_is_inside(op1->real, op2->real) > 0 )
			return 1;
		return 0;
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
/* Input and Output functions */
size_t mpfi_c_inp_str(mpfi_tc *op, FILE *stream, int base)
{
	struct mpfi_c_tag;
	mpfi_c_init(op);
	size_t r = mpfi_inp_str(op->real, stream, base);
	size_t i = mpfi_inp_str(op->imag, stream, base);
	if (r == 0 || i == 0)
			return (size_t)0;
	else
		return r + i;
}
/*Output function: real = [number1, number2] \n imag = [number1, number2] */
size_t mpfi_c_out_str(FILE *stream, int base, size_t n_digits, mpfi_tc *op)
{
	int b1 = fprintf(stream, "real = ");
	size_t r = mpfi_out_str(stream, base, n_digits, op->real);
	int b2 = fprintf(stream, "\n");
	int b3 = fprintf(stream, "image = ");
	size_t i = mpfi_out_str(stream, base, n_digits, op->imag);
	int b4 = fprintf(stream, "\n");
	if (r == 0 || i == 0)
			return (size_t)0; //we don't count here b1 + b2 + b3
	else
		return (size_t) (r + i + b1 + b2 + b3 + b4);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_mag(mpfr_tc *rop, mpfi_tc *op)
{
	int i1 = mpfi_mag(rop->real, op->real);
	int i2 = mpfi_mag(rop->imag, op->imag);
	return i1 + i2;
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_mid(mpfr_tc *rop, mpfi_tc *op)
{
	int i1 = mpfi_mid(rop->real, op->real);
	int i2 = mpfi_mid(rop->imag, op->imag);
	return i1 + i2;
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_mul( mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2)
{
	//here we can handle the precision of intermediate operations
	mpfi_t a,b,x,y;
	mpfi_init(a);
	mpfi_init(b);
	mpfi_init(x);
	mpfi_init(y);
	//we should handle flags returned by operations here
	//and I haven't yet decided how we calculate final flags using interim calculations
	mpfi_mul(a, op1->real, op2->real);
	mpfi_mul(b, op1->imag, op2->imag);
	mpfi_mul(x, op1->real, op2->imag);
	mpfi_mul(y, op2->real, op1->imag);
	mpfi_sub(rop->real, a, b);
	mpfi_add(rop->imag, x, y);
	mpfi_clear(a);
	mpfi_clear(b);
	mpfi_clear(x);
	mpfi_clear(y);
}
void mpfi_c_mul_d( mpfi_tc *rop, mpfi_tc *op1, double op2)
{
	mpfi_mul_d(rop->real, op1->real, op2);
	mpfi_set(rop->imag, op1->imag);
}
void	mpfi_c_mul_r		(mpfi_tc *rop, mpfi_tc op1, mpfi_t op2)
{
	mpfi_mul(rop->real, op1.real, op2);
	mpfi_mul(rop->imag, op1.imag, op2);
}
void	mpfi_r_mul_c		(mpfi_tc *rop, mpfi_t op1, mpfi_tc op2)
{
	mpfi_mul(rop->real, op1, op2.real);
	mpfi_mul(rop->imag, op1, op2.imag);
}
/*
 * cnan_p.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_nan_p(mpfi_tc *op)
{
	if (mpfi_nan_p(op->real) != 0 || mpfi_nan_p(op->imag) != 0)
		return 1;
	return 0;
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_conj( mpfi_tc *rop, mpfi_tc *op)
{
	mpfi_t neg;
	mpfi_init(neg);
	mpfi_neg(neg, op->imag);
	mpfi_set(rop->imag, neg);		//need to work this out carefully
	mpfi_set(rop->real, op->real);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
/* Conversion functions */
void mpfi_c_get_d(double* rop,  mpfi_tc *op)		//consider creating struct double_complex
{
	printf("Entering mpfi_c_get_d \n ");
	rop[0] = mpfi_get_d(op->real);
	rop[1] = mpfi_get_d(op->imag);
}
void mpfi_c_get_fr(mpfr_tc *rop, mpfi_tc *op)
{
	mpfi_get_fr(rop->real, op->real);
	mpfi_get_fr(rop->imag, op->imag);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
/* Assignment functions */
void mpfi_c_set( mpfi_tc *rop, mpfi_tc *op)
{
	mpfi_set(rop->real, op->real);
	mpfi_set(rop->imag, op->imag);
}
void mpfi_c_set_d( mpfi_tc *rop, double real, double imag)
{
	mpfi_set_d(rop->real, real);
	mpfi_set_d(rop->imag, imag);
}
// input string in format [left_r , right_r];[left_i , right_i]
//returns 1 if input of either real or imaginary part is incorrect, and 0 otherwise
int mpfi_c_set_str(mpfi_tc *rop, char *s, int base)
{
	int flag;
	char *tok = NULL;
	tok = strtok(s, ";");
	//we need to handle tok's size
	flag = mpfi_set_str(rop->real, tok, base);
	if(flag)
		return 1;
	else
	{
		flag = mpfi_set_str(rop->imag, tok, base);
		return flag;
	}
}


// /* Assignment functions for MPFR complex */
// void mpfr_c_set( mpfr_tc *rop, mpfr_tc *op, mpfr_rnd_t rnd)
// {
// 	mpfr_set(rop->real, op->real, rnd);
// 	mpfr_set(rop->imag, op->imag, rnd);
// }
// void mpfr_c_set_d( mpfr_tc *rop, double real, double imag, mpfr_rnd_t rnd)
// {
// 	mpfr_set_d(rop->real, real, rnd);
// 	mpfr_set_d(rop->imag, imag, rnd);
// }
// // input string in format [left_r , right_r];[left_i , right_i]
// //returns 1 if input of either real or imaginary part is incorrect, and 0 otherwise
// int mpfr_c_set_str(mpfr_tc *rop, char *s, int base, mpfr_rnd_t rnd)
// {
// 	int flag;
// 	char *tok = NULL;
// 	tok = strtok(s, ";");
// 	//we need to handle tok's size
// 	flag = mpfr_set_str(rop->real, tok, base, rnd);
// 	if(flag)
// 		return 1;
// 	else
// 	{
// 		flag = mpfr_set_str(rop->imag, tok, base, rnd);
// 		return flag;
// 	}
// }

/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_sub( mpfi_tc *rop, mpfi_tc *op1, mpfi_tc *op2)
{
	mpfi_sub(rop->real, op1->real, op2->real);
	mpfi_sub(rop->imag, op1->imag, op2->imag);
}
int mpfi_c_sub_d(mpfi_tc *rop, mpfi_tc *op1, double op2)
{
	mpfi_set(rop->imag, op1->imag);
	return mpfi_sub_d(rop->real, op1->real, op2);
}
void mpfi_c_sub_r(mpfi_tc *rop, mpfi_tc op1, mpfi_t op2)
{
	mpfi_set(rop->imag, op1.imag);
	mpfi_sub(rop->real, op1.real, op2);
}
void mpfi_r_sub_c(mpfi_tc *rop, mpfi_t op1, mpfi_tc op2)
{
	mpfi_set(rop->imag, op2.imag);
	mpfi_sub(rop->real, op1, op2.real);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
void mpfi_c_swap(mpfi_tc *x, mpfi_tc *y)
{
	mpfi_swap(x->real, y->real);
	mpfi_swap(x->imag, y->imag);
}
/*
 * cinit.c
 *
 *  Created on: Jan 9, 2014
 *      Author: user
 */
int mpfi_c_is_zero(mpfi_tc *op)
{
	if (mpfi_is_zero(op->real) > 0 && mpfi_is_zero(op->imag) > 0)
		return 1;
	return 0;
}
int mpfi_c_has_zero(mpfi_tc *op)
{
	if (mpfi_has_zero(op->real) > 0 || mpfi_has_zero(op->imag) > 0)
		return 1;
	return 0;
}

int mpfi_c_are_conj(mpfi_tc *op1, mpfi_tc *op2)
{
	if(mpfi_cmp(op1->real, op2->real) == 0)
	{
		mpfi_t tmp;
		mpfi_init(tmp);
		mpfi_set(tmp, op2->imag);
		mpfi_neg(tmp, tmp);
		if(mpfi_cmp(op1->imag, tmp) == 0)
		{
		  mpfi_clear(tmp);
		  return 0;
		}
		else
		{
		  mpfi_clear(tmp);
		  return 1;
		}
	}
	return 1;
  
}


