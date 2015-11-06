

#include "mpfr_linalg.h"


/* Allocates a n * m matrix and initializes all entries to prec
   bits 
*/
mpfr_t *allocateMPFRMatrix(uint64_t n,uint64_t m, mp_prec_t prec) {
  mpfr_t *A;
  uint64_t i, j;

  A = (mpfr_t *) safeCalloc(n * m, sizeof(mpfr_t));
  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_init2(A[i * m + j], prec);
    }
  }

  return A;
}



/* Clears all entries of a n * m matrix A and frees the memory
   allocated to that matrix 
*/
void freeMPFRMatrix(mpfr_t *A, uint64_t n, uint64_t m) {
  uint64_t i, j;

  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_clear(A[i * m + j]);
    }
  }
 
  safeFree(A);
}

/* Allocates a n sized vector and initializes all entries to prec
   bits 
*/
mpfr_t *allocateMPFRVector(uint64_t n, mp_prec_t prec) {
  mpfr_t *v;
  uint64_t i;

  v = (mpfr_t *) safeCalloc(n, sizeof(mpfr_t));
  for (i=0;i<n;i++) {
    mpfr_init2(v[i], prec);
  }

  return v;
}

/* Clears all entries of a n sized vector v and frees the memory
   allocated to that vector
*/
void freeMPFRVector(mpfr_t *v, uint64_t n) {
  uint64_t i;

  for (i=0;i<n;i++) {
      mpfr_clear(v[i]);
  }
 
  safeFree(v);
}


/* Sets a n * m matrix A to all zeros */
void setMatrixZero(mpfr_t *A, uint64_t n, uint64_t m) {
  uint64_t i, j;

  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_set_si(A[i * m + j], 0, GMP_RNDN); /* exact */
    }
  }
}

/* Sets a n * n matrix A to identity */
void setMatrixIdentity(mpfr_t *A, uint64_t n) {
  uint64_t i, j;

  for (i=0;i<n;i++) {
    for (j=0;j<n;j++) {
      mpfr_set_si(A[i * n + j], 0, GMP_RNDN); /* exact */
    }
    mpfr_set_si(A[i * n + i], 1, GMP_RNDN); /* exact */
  }
}



/* Copies a matrix exactly, changing the precision of the elements of
   the output matrix where needed
*/
void copyMatrix(mpfr_t *B, mpfr_t *A, uint64_t n, uint64_t m) {
  uint64_t i,j;

  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_set_prec(B[i * m + j], mpfr_get_prec(A[i * m + j]));
      mpfr_set(B[i * m + j], A[i * m + j], GMP_RNDN); /* exact */
    }
  }
}



/* Computes an upper bound on ceil(log2(max(m,n))) */
static inline uint64_t ceilLog2(uint64_t n, uint64_t m) {
  if(n >= m)
  {
    if (n <= 4) return 2;
    return 64 - __builtin_clz(n-1);
  }
  else
  {
    if (m <= 4) return 2;
    return 64 - __builtin_clz(m-1);

  }
}

/* Swaps two MPFR array pointers */
static inline void swapMPFRArrayPointers(mpfr_t **p, mpfr_t **q) {
  mpfr_t *temp;

  temp = *p;
  *p = *q;
  *q = temp;
}


  /* Computes a rigorous lower bound on the Frobenius norm of a n * m
   complex matrix A, given as ReA (real part) and ImA (imaginary
   part). The function uses the MPFR variable scratch as scratch
   space, assuming it has been allocated, possibly changing its
   precision and not clearing it.  
*/
void frobeniusNormLowerBound(mpfr_t frob, mpfr_t *ReA, mpfr_t *ImA, uint64_t n, uint64_t m, mpfr_t scratch) {
  uint64_t i, j;
  
  /* Set precision of scratch variables to output precision + some
     guard bits 
  */
  mpfr_set_prec(scratch, mpfr_get_prec(frob) + 2 * ceilLog2(n, m) + 15);

  /* Set scratch variable to zero. We will accumulate in that
     variable.
  */
  mpfr_set_si(scratch, 0, GMP_RNDN); /* exact */
  
  /* Compute sum_i sum_j Re(aij)^2 + Im(aij)^2 with rounding down */
  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_fma(scratch, ReA[i * m + j], ReA[i * m + j], scratch, GMP_RNDD);                           
      mpfr_fma(scratch, ImA[i * m + j], ImA[i * m + j], scratch, GMP_RNDD);                
    }
  }

  /* Compute square root of accumulated sum with rounding down,
     putting the result in result variable frob.
  */
  mpfr_sqrt(frob, scratch, GMP_RNDD); /* 0 <= frob <= ||A||_F */
}



/* Computes a rigorous upper bound on the Frobenius norm of a n * m
   complex matrix A, given as ReA (real part) and ImA (imaginary
   part). The function uses the MPFR variable scratch as scratch
   space, assuming it has been allocated, possibly changing its
   precision and not clearing it.  
*/
void frobeniusNormUpperBound(mpfr_t frob, mpfr_t *ReA, mpfr_t *ImA, uint64_t n,uint64_t m, mpfr_t scratch) {
  uint64_t i, j;
  
  /* Set precision of scratch variables to output precision + some
     guard bits 
  */
  mpfr_set_prec(scratch, mpfr_get_prec(frob) + 2 * ceilLog2(n,m) + 15);

  /* Set scratch variable to zero. We will accumulate in that
     variable.
  */
  mpfr_set_si(scratch, 0, GMP_RNDN); /* exact */
  
  /* Compute sum_i sum_j Re(aij)^2 + Im(aij)^2 with rounding down */
  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_fma(scratch, ReA[i * m + j], ReA[i * m + j], scratch, GMP_RNDU);                           
      mpfr_fma(scratch, ImA[i * m + j], ImA[i * m + j], scratch, GMP_RNDU);                
    }
  }

  /* Compute square root of accumulated sum with rounding down,
     putting the result in result variable frob.
  */
  mpfr_sqrt(frob, scratch, GMP_RNDU); /* 0 <= ||A||_F <= frob */
}

/* Checks if the Frobenius norm of a n * m complex matrix A, given as
   ReA (real part) and ImA (imaginary part), is rigorously upper
   bounded by 2^k, k given in input. Returns a non-zero value if the
   Frobenius norm can be shown to be less than or equal to 2^k, return
   zero otherwise. The function uses the MPFR variables scratch1 and
   scratch2 as scratch space, assuming they have been
   allocated, possibly changing their precision and not clearing
   them.
*/
int checkFrobeniusNorm(mpfr_t *ReA, mpfr_t *ImA, uint64_t n,uint64_t m, mp_exp_t k, mpfr_t scratch1, mpfr_t scratch2) {

  /* Set precision of scratch variable scratch1 to precision of k +
     some guard bits. 
  */
  mpfr_set_prec(scratch1, 8 * sizeof(k) + 5);

  /* Compute a rigorous upper bound on the Frobenius norm */
  frobeniusNormUpperBound(scratch1, ReA, ImA, n, m, scratch2);

  /* If the Frobenius norm is something else than a real number or is
     negative, we don't know nothing 
  */
  if (!mpfr_number_p(scratch1)) return 0;
  if (mpfr_sgn(scratch1) < 0) return 0;

  /* If the Frobenius norm is zero, it is surely below 2^k */
  if (mpfr_zero_p(scratch1)) return 1;

  /* Return the result of the comparison scratch1 <= 2^k */
  return (mpfr_cmp_si_2exp(scratch1, 1, k) <= 0);
}

/* Computes the sum of the elements of a n sized vector v with an
   overall error bounded in magnitude by 2^k, adapting the precision
   of the result variable if necessary to satisfy the absolute error
   bound. 
*/
void sumVectorWithAbsoluteErrorBound(mpfr_t sum, mpfr_t *v, uint64_t n, mp_exp_t k) 
{
  uint64_t i;
  mp_exp_t maxExponent, e;
  mp_prec_t prec, precSum;
  
  /* Compute maximum exponent of non-zero real entries in the vector */
  maxExponent = mpfr_get_emin_min();
  for (i=0;i<n;i++) {
    if (mpfr_number_p(v[i]) && (!mpfr_zero_p(v[i]))) {
      e = mpfr_get_exp(v[i]);
      if (e > maxExponent) maxExponent = e;
    }
  }
   
  /* Here we know that each real entry in the vector is bounded in
     magnitude by 2^maxExponent. 

     Hence the sum of the vector elements is bounded in magnitude by 
     2^(maxExponent + ceil(log2(n))) as n is bounded by 2^ceil(log2(n)). 

     In the case when 2^(maxExponent + ceil(log2(n))) < 2^k, i.e. when
     maxExponent + ceil(log2(n)) < k, we do not need to compute the sum, unless
     we have non-real (Infinity or NaN) entries in the vector.
  */
  mp_exp_t tmp = maxExponent + ceilLog2(n,n); //WHY it did not work without it??
  if (tmp < k) 
  {
    /* Sum once with some precision to see if there are non-real entries */
    precSum = mpfr_get_prec(sum);
    mpfr_set_prec(sum, 64);
    mpfr_set_si(sum, 0, GMP_RNDN);
    for (i=0;i<n;i++) 
    {
      mpfr_add(sum, sum, v[i], GMP_RNDN); /* We don't care about the
                                             result exponent */

    }

    if (mpfr_number_p(sum)) 
    {
      /* All inputs were real as their FP sum is real. Reset the
         precision of sum and set the result to zero. 
      */
      mpfr_set_prec(sum, precSum);
      mpfr_set_si(sum, 0, GMP_RNDN); /* exact */
      return;
    }
    /* Some inputs were non-real. Reset the precision of sum */
    mpfr_prec_round(sum, precSum, GMP_RNDN); /* "rounding" Inf or NaN */
    return;
  }
  /* Here, we have maxExponent + ceil(log2(n)) >= k. 

     We know that the exact sum is bounded in magnitude by 2^(maxExponent + ceil(log2(n))). 

     Let prec = maxExponent + ceil(log2(n)) - k + ceil(log2(n)) + 5.

     So when performing n < 2^ceil(log2(n)) additions on a prec bit precision (or
     more precise) variable, each of which induces an error smaller
     than 2^(-prec) * 2^(maxExponent + ceil(log2(n))), we get an accumulated sum
     with an accumulated error smaller than n * 2^(k - ceil(log2(n)) - 5) <= 2^(k
     - 5).
  */

  prec = (mp_prec_t) (((int) (maxExponent - k)) + 2 * ceilLog2(n,n) + 5);


  /* Keep the precision of the sum argument */
  precSum = mpfr_get_prec(sum);

  /* Set the accumulation precision to prec as explained above, if
     prec is greater than the precision of the sum variable. 
  */


  if (prec > precSum) 
  {
    mpfr_set_prec(sum, prec);
  }

  /* Now accumulate */
  
  mpfr_set_si(sum, 0, GMP_RNDN); /* exact */
  for (i=0;i<n;i++) 
  {
    mpfr_add(sum, sum, v[i], GMP_RNDN); /* sum = sum + delta, |delta| <= 2^(-prec + maxExponent + ceil(log2(n))) */
    
  }
  // mpfr_out_str(stderr, 10, 10, sum, MPFR_RNDU);

  /* If the accumulated some is non-real, we got a non-real
     entry. Just reset the precision of the sum operand. 
  */
  if (!mpfr_number_p(sum)) {
    mpfr_prec_round(sum, precSum, GMP_RNDN); /* "rounding" Inf or NaN */
    return;
  }

  /* The accumulated sum is real and we know that it satisfies

     sum = sum_i v[i] + delta

     with |delta| <= 2^(k - 5).

     If the current precision of the sum variable is less than or
     equal to its original precision, we can leave it as is.
  */
  if (mpfr_get_prec(sum) <= precSum) {
    return;
  }
  
  /* Here, the current precision of the sum variable is greater than
     its original precision. We have to round the sum to some precision 
     that is closest to the original precision, while maintaining the 
     overall error on the sum bounded by 2^k.

     First check if sum is equal to zero, in which case, we can just
     "round it" to the original precision of the sum variable.
  */
  if (mpfr_zero_p(sum)) {
    mpfr_prec_round(sum, precSum, GMP_RNDN); /* exact */
    return;
  }
  
  /* Here the sum variable is real and non-zero */
  e = mpfr_get_exp(sum);

  /* Here we know that |sum| < 2^e. If e <= k - 1, we can set sum to
     zero and reset its precision as we have:

     |sum_i v[i]| = |sum + delta| <= |sum| + |delta| <= 2^(k - 1) + 2^(k - 5) <= 2^k.

  */
  if (e <= k - 1) {
    mpfr_set_prec(sum, precSum);
    mpfr_set_si(sum, 0, GMP_RNDN); /* exact */
    return;
  }

  /* Here we have e > k - 1. When rounding sum to precSum bits, we will have

     sum' = sum + delta' with 

     |delta'| <= 2^(-precSum) * |sum| <= 2^(e - precSum).

     If e - precSum <= k - 1, we can just perform that rounding as we
     then have:

     sum' = sum + delta' = sum_i v[i] + delta + delta'

     where 

     |delta| <= 2^(k - 5)
     
     and 

     |delta'| <= 2^(e - precSum) <= 2^(k - 1)

     and 

     2^(k - 5) + 2^(k - 1) <= 2^k.
  */
  if ((e - ((mp_exp_t) precSum)) <= k - 1) {
    mpfr_prec_round(sum, precSum, GMP_RNDN); /* sum' = sum + delta'
                                                with delta' bounded as
                                                shown above. */
    return;
  }

  /* Here we just round sum to e - k + 1 bits, inducing an additional 
     error delta' bounded in magnitude by 2^(k - 1). 

     This is the only case when the final precision of the sum
     variable is not equal to the original precision of the sum
     variable.

  */
    
  prec = ((mp_prec_t) (e - k)) + 1;
  
  mpfr_prec_round(sum, prec, GMP_RNDN); /* sum' = sum + delta' with
                                           delta' bounded in magnitude
                                           by 2^(k - 1)
                                        */
}

/* Computes a rigorous upper bound on the Frobenius norm of a n * m
   complex matrix A, given as ReA (real part) and ImA (imaginary
   part). 

   The result value is guaranteed to satisfy

   frob = ||A||_F + delta 

   with 

   0 <= delta < 2^k.

   The function uses a vector scratch of size (2 * n * m + 2) of MPFR
   variables as scratch space, assuming it has been allocated and
   initialized, possibly changing its precision and not clearing nor
   freeing it.

*/
void frobeniusNormUpperBoundWithAbsoluteErrorBound(mpfr_t frob, mpfr_t *ReA, mpfr_t *ImA, uint64_t n, uint64_t m, mp_exp_t k, mpfr_t *scratch) {
  uint64_t i, j;
  mp_exp_t e, E, F, G;
  mp_prec_t p, pp, ppp;

  /* Basic idea of the algorithm:

     (i)    Check if any of the inputs is non-real, if yes, fall back to
            stupid Frobenius Upper Bound (yielding Inf or NaN)

     (ii)   Compute all Re(aij)^2 and Im(aij)^2 exactly, storing them in
            scratch space. This seems a lot of data but is of the same size 
            as the input.

     (iii)  Sum the Re(aij)^2 and Im(aij)^2 with an error bounded by
            2^(2 * k - 6); call this result s.

     (iv)   Exactly add 2^(2 * k - 5) to s, in order to obtain a rigorous
            upper bound of sum_ij Re(aij)^2 + Im(aij)^2 with an error bounded
            by 2^(2 * k - 4). Call this result t.

            Formulawise, we have

            t = (sum_ij Re(aij)^2 + Im(aij)^2) + delta

            with 0 <= delta < 2^(2 * k - 4).

            Further we have for any x >= 0 and any d >= 0 

            sqrt(x + d^2) >= sqrt(x)

            and therefore

            sqrt(x + d^2) - sqrt(x) <= d.

            Hence for any x >= 0 and any dd >= 0

            sqrt(x + dd) - sqrt(x) <= sqrt(dd).

            Thus we have 

            sqrt(t) = sqrt(sum_ij Re(aij)^2 + Im(aij)^2 + delta) 
                    = sqrt(sum_ij Re(aij)^2 + Im(aij)^2) + sqrt(delta)

            Since 0 <= delta < 2^(2 * k - 4), we have

            sqrt(t) = ||A||_F + delta'

            with 0 <= delta' < 2^(k - 2).
            
     (v)    If t happens to be zero, set the output variable frob to zero
            and return. If t happens to be zero, an error occured; just
            set the output to NaN and return.

     (vi)   Otherwise determine the least e such that t < 2^e. Therefore 
            sqrt(t), even rounded upwards, will be bounded by 

            sqrt(t) <= 2^(floor(e/2) + 2)      

            (This bound is rigorous but might be not damn tight.)

            Set the precision of the output variable frob to at least 

            p = floor(e/2) - k + 5.

            Then compute sqrt(t), rounding upwards, in the precision
            of the output variable. 

            We get

            frob = sqrt(t) * (1 + eps) 

            with 0 <= eps < 2^(-p + 1).

            Therefore

            frob = sqrt(t) + eps * sqrt(t) 

                 = sqrt(t) + delta''

            with 

            delta'' = eps * sqrt(t) 

            bounded by 

            0 <= delta'' <  2^(-p + 1) * 2^(floor(e/2) + 2)
                         <= 2^(-floor(e/2) + k - 5 + 1 + floor(e/2) + 2)
                         <= 2^(k - 2).

            So finally,

            frob = sqrt(t) + delta'' 
                 = ||A||_F + delta' + delta''
                 = ||A||_F + delta'''

            with

            0 <= delta''' < 2^(k - 2) + 2^(k - 2) <= 2^k.

  */

  /* Perform step (i):

     (i)    Check if any of the inputs is non-real, if yes, fall back to
            stupid Frobenius Upper Bound (yielding Inf or NaN)

  */
  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      if (!(mpfr_number_p(ReA[i * m + j]) &&
	    mpfr_number_p(ImA[i * m + j]))) {
	frobeniusNormUpperBound(frob, ReA, ImA, n, m, scratch[0]);
	return;
      }
    }
  }
  
  /* Perform step (ii): 

     (ii)   Compute all Re(aij)^2 and Im(aij)^2 exactly, storing them in
            scratch space. This seems a lot of data but is of the same size 
            as the input.

  */
  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      /* Set precision of the two scratch variables 
	 
	 scratch[1 + 2 * (i * m + j) + 0] resp. ... + 1]

	 to twice the precision of the real resp. imaginary part of aij.

	 This way, the subsequent squarings will be exact.
      */
      mpfr_set_prec(scratch[2 + 2 * (i * m + j) + 0], 2 * mpfr_get_prec(ReA[i * m + j]));
      mpfr_set_prec(scratch[2 + 2 * (i * m + j) + 1], 2 * mpfr_get_prec(ImA[i * m + j]));

      /* Compute Re(aij)^2 and Im(aij)^2 exactly */
      mpfr_sqr(scratch[2 + 2 * (i * m + j) + 0], ReA[i * m + j], GMP_RNDN); /* exact */
      mpfr_sqr(scratch[2 + 2 * (i * m + j) + 1], ImA[i * m + j], GMP_RNDN); /* exact */
    }
  }

  /* Perform step (iii):

     (iii)  Sum the Re(aij)^2 and Im(aij)^2 with an error bounded by
            2^(2 * k - 6); call this result s.
  
     We are going to put the sum result into scratch[0] that we left over 
     on purpose.
     
  */
  sumVectorWithAbsoluteErrorBound(scratch[0], &(scratch[2]), n * m,
				  ((((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 6)))
				    <= ((mp_exp_t) 0)) ?
				   ((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 6))) : ((mp_prec_t) 0)));

  /* Perform step (iv):

     (iv)   Exactly add 2^(2 * k - 5) to s, in order to obtain a rigorous
            upper bound of sum_ij Re(aij)^2 + Im(aij)^2 with an error bounded
            by 2^(2 * k - 4). Call this result t.

     We are going to just modify the contents of scratch[0].

     In the case when scratch[0] is exactly zero, just set its 
     precision to 5 and set its value to 2^(2 * k - 5). If scratch[0] is
     non-real (Inf or NaN), do nothing.

     We can exactly add 2^(2 * k - 5) into scratch[0] if the precision
     of scratch[0] under certain conditions:

     Let E be the least integer such that |scratch[0]| < 2^E, with
     scratch[0] taken before the modification.
     
     Let F be 

     F = max(E, 2 * k - 5) + 1.

     In other words, F is an upper bound on the exponent of the
     result, including the possibility of a carry propagating through
     and moving the exponent.

     Further, let be pp the precision of the scratch[0] variable 
     before the modification. 

     Hence the weight of the ulp of the scratch[0] variable is 
     2^(E - pp).

     Let G be

     G = min(E - pp, 2 * k - 5).

     Then (scratch[0] + 2^(2 * k - 5)) is an integer multiple of 
     2^G, and, as stated above, bounded by 2^F. This means it holds
     on F - G and thus on

     ppp = max(5, pp, F - G) + 1.

     bits.

  */

  if (mpfr_zero_p(scratch[0])) {
    /* Here scratch[0] is zero. Set its precision to 5 and 
       set its value to 2 * k - 5.
    */
    mpfr_set_prec(scratch[0], (mp_prec_t) 5);
    mpfr_set_si_2exp(scratch[0], 1, ((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 5))), GMP_RNDN);
  } else {
    if (mpfr_number_p(scratch[0])) {
      /* Here scratch[0] is a non-zero real. It might still be negative. */
      E = mpfr_get_exp(scratch[0]);
      pp = mpfr_get_prec(scratch[0]);

      /* Compute F = max(E, 2 * k - 5) + 1 */
      F = E;
      if (((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 5))) > F) F = ((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 5)));
      F++;

      /* Compute G = min(E - pp, 2 * k - 5) */
      G = E - ((mp_exp_t) pp);
      if (((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 5))) < G) G = ((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 5)));

      /* Compute ppp = max(5, pp, F - G) + 1 */
      ppp = 5;
      if (pp > ppp) ppp = pp;
      if (((mp_prec_t) (F - G)) > ppp) ppp = ((mp_prec_t) (F - G));
      ppp++;

      /* Set precision of scratch[0] variable to ppp, which is always
	 greater than its current precision pp, making sure not to
	 loose the current value of scratch[0].
      */
      mpfr_prec_round(scratch[0], ppp, GMP_RNDN); /* exact */

      /* Construct 2^(2 * k - 5), putting it into scratch[1], left
	 over for that purpose. 
      */
      mpfr_set_prec(scratch[2], (mp_prec_t) 5);
      mpfr_set_si_2exp(scratch[1], 1, ((mp_exp_t) (((mp_exp_t) 2) * k - ((mp_exp_t) 5))), GMP_RNDN);

      /* Add exactly */
      mpfr_add(scratch[0], scratch[0], scratch[1], GMP_RNDN); /* exact by what precedes */
    }
  }

  /* Perform step (v):

     (v)    If t happens to be zero, set the output variable frob to zero
            and return. If t happens to be zero, an error occured; just
            set the output to NaN and return.

  */
  if (mpfr_zero_p(scratch[0]) ||
      (!mpfr_number_p(scratch[0])) ||
      (mpfr_sgn(scratch[0]) < 0)) {
    mpfr_sqrt(frob, scratch[0], GMP_RNDN); /* exact or yields NaN or Inf */
  }

  /* Perform step (vi): 

     Let e be the least integer such that scratch[0] < 2^e.

     Compute p = floor(e/2) - k + 5.

     Set the precision of the output variable frob to at least p. Use
     caution: the computed p might be less than 2, which is the least
     precision possible. Just take the maximum of the incoming
     precision of frob, p and, say, 5.

     Compute sqrt(scratch[0]), rounding upwards, into and with the
     precision of frob.
     
  */
  e = mpfr_get_exp(scratch[0]);
  p = ((mp_prec_t) (e >> 1)) - ((mp_prec_t) k) + ((mp_prec_t) 5);
  if (p < ((mp_prec_t) 5)) p = (mp_prec_t) 5;
  if (p < mpfr_get_prec(frob)) p = mpfr_get_prec(frob);
  mpfr_set_prec(frob, p);

  mpfr_sqrt(frob, scratch[0], GMP_RNDU); /* Error analysis: see above */
}

/* Computes the absolute value (modulus) of the complex number re + i
   * im with an absolute error bounded in magnitude by 2^k, adapting
   the precision of the result variable if necessary to satisfy the
   absolute error bound. The function uses the MPFR variable scratch,
   as scratch space, assuming it has been allocated, possibly changing
   its precision and not clearing it.
*/
void computeAbsoluteValue(mpfr_t res, mpfr_t re, mpfr_t im, mp_exp_t k, mpfr_t scratch) {
  mp_exp_t e, maxExp;
  mp_prec_t prec, precRes;
  int tern;

  /* Handle inputs that are non-real */
  if (!(mpfr_number_p(re) && 
        mpfr_number_p(im))) {
    /* Do stupid FP arithmetic, this will yield a NaN or Inf */
    mpfr_mul(res, re, re, GMP_RNDN); 
    mpfr_fma(res, im, im, res, GMP_RNDN);
    mpfr_sqrt(res, res, GMP_RNDN);
    return;
  }

  /* Here both inputs re and im are real 

     Handle the case when one of the inputs is zero.

  */
  if (mpfr_zero_p(re)) {
    /* Here the exact result is |im|. 

       However, we have to be careful as precision of res might be
       smaller.
    */
    if ((mpfr_get_prec(res) >= mpfr_get_prec(im)) ||
        mpfr_zero_p(im)) {
      mpfr_abs(res, im, GMP_RNDN); /* exact */
      return;
    }

    /* Here im is a non-zero real. Get its exponent. */
    e = mpfr_get_exp(im);

    /* Here we have |im| < 2^e. If e <= k, zero is a reasonable
       answer. 
    */
    if (e <= k) {
      mpfr_set_si(res, 0, GMP_RNDN); /* exact */
      return;
    }

    /* If e - prec(res) <= k, we can just round |im| to the 
       precision of the result:

       res = |im| + delta

       with

       |delta| <= 2^-prec * |im| <= 2^-prec * 2^(k + prec) = 2^k.

    */
    if (e - ((mp_exp_t) mpfr_get_prec(res)) <= k) {
      mpfr_abs(res, im, GMP_RNDN); /* Error bounded as shown above. */
      return;
    }

    /* We need at least prec = e - k bits in res to have an absolute
       error bounded by 2^k. 
    */
    prec = (mp_prec_t) (e - k);
    mpfr_set_prec(res, prec);
    mpfr_abs(res, im, GMP_RNDN); /* Error bounded by 2^-prec * |im| <= 2^k. */
    return;
  }

  if (mpfr_zero_p(im)) {
    /* Here the exact result is |re|. 

       However, we have to be careful as precision of res might be
       smaller.
    */
    if ((mpfr_get_prec(res) >= mpfr_get_prec(re)) ||
        mpfr_zero_p(re)) {
      mpfr_abs(res, re, GMP_RNDN); /* exact */
      return;
    }

    /* Here re is a non-zero real. Get its exponent. */
    e = mpfr_get_exp(re);

    /* Here we have |re| < 2^e. If e <= k, zero is a reasonable
       answer. 
    */
    if (e <= k) {
      mpfr_set_si(res, 0, GMP_RNDN); /* exact */
      return;
    }

    /* If e - prec(res) <= k, we can just round |re| to the 
       precision of the result:

       res = |re| + delta

       with

       |delta| <= 2^-prec * |re| <= 2^-prec * 2^(k + prec) = 2^k.

    */
    if (e - ((mp_exp_t) mpfr_get_prec(res)) <= k) {
      mpfr_abs(res, re, GMP_RNDN); /* Error bounded as shown above. */
      return;
    }

    /* We need at least prec = e - k bits in res to have an absolute
       error bounded by 2^k. 
    */
    prec = (mp_prec_t) (e - k);
    mpfr_set_prec(res, prec);
    mpfr_abs(res, re, GMP_RNDN); /* Error bounded by 2^-prec * |re| <= 2^k. */
    return;
  }

  /* Here, both inputs are non-zero reals. 

     Get the maximum exponent of re and im.

  */
  maxExp = mpfr_get_exp(re);
  e = mpfr_get_exp(im);
  if (e > maxExp) maxExp = e;

  /* Here we know that |re| < 2^maxExp and |im| < 2^maxExp.
     Hence |re + i * im| < 2^(maxExp) * sqrt(2) < 2^(maxExp + 1).

     First test if 2^(maxExp + 1) <= 2^k, i.e. if maxExp + 1 <= k,
     in which case zero is a reasonable answer.
  */
  if (maxExp + 1 <= k) {
    mpfr_set_si(res, 0, GMP_RNDN); /* exact */
    return;
  }

  /* Here, maxExp + 1 > k. 

     Take now prec = max(max(maxExp + 1 - k + 2, 5), prec(res)).

  */
  prec = (mp_prec_t) (maxExp - k + 1 + 2);
  if (prec < 5) prec = 5;
  
  /* Keep the original precision of the result variable res and set
     its precision to prec. 
  */
  precRes = mpfr_get_prec(res);
  if (prec > precRes) {
    mpfr_set_prec(res, prec);
  }

  /* Set the precision of the scratch variable to the double of the re
     variable. 
  */
  mpfr_set_prec(scratch, 2 * mpfr_get_prec(re));
  
  /* Compute an preliminary result as follows. */
  mpfr_sqr(scratch, re, GMP_RNDN);          /* exact */
  mpfr_fma(res, im, im, scratch, GMP_RNDN); /* res = (re^2 + im^2) * (1 + eps1) */
  mpfr_sqrt(res, res, GMP_RNDN);            /* res = sqrt(re^2 + im^2) * sqrt(1 + eps1) * (1 + eps2) */
  
  /* We now have 

     res = sqrt(re^2 + im^2) * sqrt(1 + eps1) * (1 + eps2) = 
         = sqrt(re^2 + im^2) * (1 + eps) 

     with

     eps = sqrt(1 + eps1) * (1 + eps2) - 1

     which is bounded by

     |eps| <= |eps1| + |eps2| + |eps1| * |eps2|

     as |sqrt(1 + eps1) - 1| <= |eps1| for all |eps1| <= 2^-1.

     As |eps1| and |eps2| are bounded by 

     |eps1| <= 1/4 * 2^(-(maxExp - k + 1))
     |eps2| <= 1/4 * 2^(-(maxExp - k + 1))

     we have |eps| bounded by

     |eps| <= 2^(-(maxExp - k + 1))

     Since sqrt(re^2 + im^2) <= 2^maxExp + 1, we have 

     |eps| * sqrt(re^2 + im^2) <= 2^k.

     Now we can see that in a lot of cases (when im is small with
     respect to re for example), result actually holds on the original
     precision of res. So we try to round to the original precision of
     res and check if this operation was exact.

     We first check if res is a real.
  */
  if (!mpfr_number_p(res)) {
    mpfr_prec_round(res, precRes, GMP_RNDN); /* "rounding" inf or Nan */
    return;
  }
  
  /* Here res is a real */
  mpfr_set_prec(scratch, precRes);
  tern = mpfr_set(scratch, res, GMP_RNDN); /* rounds to original precision of res */
  
  if ((tern == 0) && mpfr_number_p(scratch)) {
    /* We have scratch = res and scratch on the original precision of
       res 
    */
    mpfr_set_prec(res, precRes);
    mpfr_set(res, scratch, GMP_RNDN); /* exact */
  }
}

/* Computes in the n * m real matrix C the sum of the n * m matrix A
   and the element-by-element absolute value (modulus) of the n * m
   complex matrix B, given as its real part reB and imaginary part
   imB.

   The C matrix will be such that there exists a real matrix Delta

   Delta = C - A + |B|

   for which every element Delta_ij is bounded in magnitude by 2^k:

   |Delta_ij| <= 2^k.

   The function changes the precision of the elements of matrix C
   where needed to satisfy the absolute error bound.
   
   The function uses a vector scratch of size 3 of MPFR variables as
   scratch space, assuming it has been allocated and initialized,
   possibly changing its precision and not clearing nor freeing it.

   Pointers A and C may point to the same matrix; matrices reB and imB
   must be distinct and be distinct from A and C.

 */
void accumulateAbsoluteValue(mpfr_t *C, mpfr_t *A, mpfr_t *reB, mpfr_t *imB, uint64_t n,uint64_t m, mp_exp_t k, mpfr_t *scratch) {
  uint64_t i, j;

  /* Easy thing: compute absolute value with error bounded by 2^(k-1),
     add with value A_ij with error bounded by 2^(k-1). 
  */
  for (i=0;i<n;i++) {
    for (j=0;j<m;j++) {
      mpfr_set_prec(scratch[0], mpfr_get_prec(A[i * m + j]));
      mpfr_set(scratch[0], A[i * m + j], GMP_RNDN); /* exact */
      mpfr_set_prec(scratch[1], mpfr_get_prec(C[i * m + j]));
      computeAbsoluteValue(scratch[1], reB[i * m + j], imB[i * m + j], k - 1, scratch[2]);
      sumVectorWithAbsoluteErrorBound(C[i * m + j], scratch, 2, k - 1);      
      // printf("accumulateAbsoluteValue debug %d %d \n",i,j);
    }
  }
}

/* Computes in the n * m real matrix B element-by-element absolute value(modulus)
  of the n * m real matrix A. 
  Pointers A and B may point to the same matrix. 
  If precision of B is less than that of A, the function increases precision 
  of matrix B (for it to be equal to the precision of A). */
  void absoluteValue(mpfr_t *B, mpfr_t *A, uint64_t n, uint64_t m)
  {
    uint64_t i,j;
    mpfr_prec_t precA;
    for(i = 0; i < n; ++i)
    {
      for(j = 0; j < m; ++j)
      {
        precA = mpfr_get_prec(A[i * m + j]);
        if(mpfr_get_prec(B[i * m + j]) < precA) 
          mpfr_set_prec(B[i * m + j], precA);
        else
          mpfr_abs(B[i * m + j], A[i * m + j], MPFR_RNDN);
      }
    }
    
  }




/* Computes in the m * q complex matrix D the sum of an m * q complex
   matrix C and the product of a m * n complex matrix A and n * q complex matrix B. The
   signs of the two integers signP and signS allow for the computation
   of subtraction of matrices instead of multiplication.

   Formulawise we have for signP and signS assumed in 

   signP in {-1, 1}

   signS in {-1, 1}

   a matrix D satisfying

   D = signP * A * B + signS * C + Delta

   where Delta is a m * q complex absolute error matrix.

   D will be computed such that all elements Delta_ij of Delta are
   bounded in magnitude (modulus) by 

   |Delta_ij| <= 2^t.

   All matrices A, B, C and D are given as their real and imaginary
   parts.

   The function changes the precision of the elements of matrices reD
   and imD where needed to satisfy the absolute error bound.

   The function uses a vector scratch of size 2 * n + 1 of MPFR
   variables as scratch space, assuming it has been allocated and
   initialized, possibly changing its precision and not clearing nor
   freeing it.

   All pointers to matrices must be distinct and must be distinct from 
   the pointer to the scratch space.
*/
void complexMatrixMultiplyAndAdd(mpfr_t *reD, mpfr_t *imD, 
                                 int signP,
                                 mpfr_t *reA, mpfr_t *imA,
                                 mpfr_t *reB, mpfr_t *imB,
                                 int signS, 
                                 mpfr_t *reC, mpfr_t *imC,
                                 uint64_t m,  uint64_t n,  uint64_t q,
                                 mp_exp_t t,
                                 mpfr_t *scratch) {
  uint64_t i,j,k;

  /* The algorithm is pretty easy: 

     Go over all rows and colums of the output matrix D
          - compute exactly in the scratch vector of products 
                Re(aik) * Re(bkj), -Im(aik)*Im(bkj) and Re(Cij)
          - sum with error bound 2^(t-1) to obtain Re(Dij)
          - compute exactly in the scratch vector of products 
                Re(aik) * Im(bkj), Im(aik)*Re(bkj) and Im(Cij)
          - sum with error bound 2^(t-1) to obtain Im(Dij)

     As for all elements of D the error will be bounded 
     in the real part by 2^(t-1) and in the imaginary part by 2^(t-1),
     the element Delta_ij will be bounded in modulus by

     sqrt((2^(t-1))^2 + (2^(t-1))^2) = sqrt(2^(t-1)) 
                                     = 2^t * sqrt(1/2)
                                     <= 2^t.
           
     We have just to be sure to take the additional signs signP and
     signS into account.
     
  */
  for (i=0;i<m;i++) 
  {
    for (j=0;j<q;j++) 
    {
      /* Real part of Dij */
      mpfr_set_prec(scratch[0], mpfr_get_prec(reC[i * q + j]));
      if (signP < 0) 
      {
               mpfr_neg(scratch[0], reC[i * q + j], GMP_RNDN); /* exact */
      } 
      else 
      {
               mpfr_set(scratch[0], reC[i * q + j], GMP_RNDN); /* exact */
      }
      for (k=0;k<n;k++) 
      {
               mpfr_set_prec(scratch[1 + 2 * k], (mpfr_get_prec(reA[i * n + k]) + 
                                           mpfr_get_prec(reB[k * q + j])));
               mpfr_mul(scratch[1 + 2 * k], reA[i * n + k], reB[k * q + j], GMP_RNDN); /* exact */
               if (signP < 0) 
               {
                   mpfr_neg(scratch[1 + 2 * k], scratch[1 + 2 * k], GMP_RNDN); /* exact */
               }
               mpfr_set_prec(scratch[1 + 2 * k + 1], (mpfr_get_prec(imA[i * n + k]) + 
                                               mpfr_get_prec(imB[k * q + j])));
               mpfr_mul(scratch[1 + 2 * k + 1], imA[i * n + k], imB[k * q + j], GMP_RNDN); /* exact */
               if (signP >= 0) 
               {
                   mpfr_neg(scratch[1 + 2 * k + 1], scratch[1 + 2 * k + 1], GMP_RNDN); /* exact */
               }
      }

      sumVectorWithAbsoluteErrorBound(reD[i * q + j], scratch, 2 * n + 1, t - 1);
      /* Imaginary part of Dij */
      mpfr_set_prec(scratch[0], mpfr_get_prec(imC[i * q + j]));
      if (signP < 0) 
      {
               mpfr_neg(scratch[0], imC[i * q + j], GMP_RNDN); /* exact */
      } 
      else 
      {
               mpfr_set(scratch[0], imC[i * q + j], GMP_RNDN); /* exact */
      }
      for (k=0;k<n;k++)  
      {
               mpfr_set_prec(scratch[1 + 2 * k], (mpfr_get_prec(reA[i * n + k]) + 
                                           mpfr_get_prec(imB[k * q + j])));
               mpfr_mul(scratch[1 + 2 * k], reA[i * n + k], imB[k * q + j], GMP_RNDN); /* exact */
               if (signP < 0) 
         {
                   mpfr_neg(scratch[1 + 2 * k], scratch[1 + 2 * k], GMP_RNDN); /* exact */
               }
               mpfr_set_prec(scratch[1 + 2 * k + 1], (mpfr_get_prec(imA[i * n + k]) + 
                                               mpfr_get_prec(reB[k * q + j])));
               mpfr_mul(scratch[1 + 2 * k + 1], imA[i * n + k], reB[k * q + j], GMP_RNDN); /* exact */
               if (signP < 0) 
         {
                   mpfr_neg(scratch[1 + 2 * k + 1], scratch[1 + 2 * k + 1], GMP_RNDN); /* exact */
               }
      }
      sumVectorWithAbsoluteErrorBound(imD[i * q + j], scratch, 2 * n + 1, t - 1);
    }
  }
}


/* Complete analogue of complexMatrixMultiplyAndAdd, but for square matrices. To be removed later. */
void complexMatrixMultiplyAndAdd_square(mpfr_t *reD, mpfr_t *imD, 
         int signP,
         mpfr_t *reA, mpfr_t *imA,
         mpfr_t *reB, mpfr_t *imB,
         int signS, 
         mpfr_t *reC, mpfr_t *imC,
         uint64_t n,
         mp_exp_t t,
         mpfr_t *scratch) {
  uint64_t i,j,k;

  for (i=0;i<n;i++) 
  {
    for (j=0;j<n;j++) 
    {
      /* Real part of Dij */
      mpfr_set_prec(scratch[0], mpfr_get_prec(reC[i * n + j]));
      if (signS < 0) 
      {
         mpfr_neg(scratch[0], reC[i * n + j], GMP_RNDN); /* exact */
      } 
      else 
      {
         mpfr_set(scratch[0], reC[i * n + j], GMP_RNDN); /* exact */
      }
      for (k=0;k<n;k++) 
      {
         mpfr_set_prec(scratch[1 + 2 * k], (mpfr_get_prec(reA[i * n + k]) + 
             mpfr_get_prec(reB[k * n + j])));
         mpfr_mul(scratch[1 + 2 * k], reA[i * n + k], reB[k * n + j], GMP_RNDN); /* exact */
         if (signP < 0) 
         {
             mpfr_neg(scratch[1 + 2 * k], scratch[1 + 2 * k], GMP_RNDN); /* exact */
         }
         mpfr_set_prec(scratch[1 + 2 * k + 1], (mpfr_get_prec(imA[i * n + k]) + 
                 mpfr_get_prec(imB[k * n + j])));
         mpfr_mul(scratch[1 + 2 * k + 1], imA[i * n + k], imB[k * n + j], GMP_RNDN); /* exact */
         if (signP >= 0) 
         {
             mpfr_neg(scratch[1 + 2 * k + 1], scratch[1 + 2 * k + 1], GMP_RNDN); /* exact */
         }
      }
      sumVectorWithAbsoluteErrorBound(reD[i * n + j], scratch, 2 * n + 1, t - 1);

      /* Imaginary part of Dij */
      mpfr_set_prec(scratch[0], mpfr_get_prec(imC[i * n + j]));
      if (signS < 0) 
      {
         mpfr_neg(scratch[0], imC[i * n + j], GMP_RNDN); /* exact */

      } 
      else 
      {
         mpfr_set(scratch[0], imC[i * n + j], GMP_RNDN); /* exact */

      }
      for (k=0;k<n;k++)  
      {
         mpfr_set_prec(scratch[1 + 2 * k], (mpfr_get_prec(reA[i * n + k]) + 
             mpfr_get_prec(imB[k * n + j])));
         mpfr_mul(scratch[1 + 2 * k], reA[i * n + k], imB[k * n + j], GMP_RNDN); /* exact */
  
         if (signP < 0) 
         {
             mpfr_neg(scratch[1 + 2 * k], scratch[1 + 2 * k], GMP_RNDN); /* exact */
         }
         mpfr_set_prec(scratch[1 + 2 * k + 1], (mpfr_get_prec(imA[i * n + k]) + 
                 mpfr_get_prec(reB[k * n + j])));
         mpfr_mul(scratch[1 + 2 * k + 1], imA[i * n + k], reB[k * n + j], GMP_RNDN); /* exact */

         if (signP < 0) 
         {
             mpfr_neg(scratch[1 + 2 * k + 1], scratch[1 + 2 * k + 1], GMP_RNDN); /* exact */
         }
      }

      sumVectorWithAbsoluteErrorBound(imD[i * n + j], scratch, 2 * n + 1, t - 1);


    }
  }

}

/* Computes in the n * n complex matrix U the inverse of the n * n
   complex matrix V, using the n * n complex matrix S as a seed for an
   iterative inversion process and returns the number of iterations.

   Let Delta_1 be the error defined by 

   Delta_1 = S - V^-1 

   and 

   Delta_final = U - V^-1.

   The function ensures that U is computed such that 

   ||Delta_final||_2 <= ||Delta_final||_F <= 2^p

   where ||Delta_final||_2 resp. ||Delta_final||_F are the Euclidian
   2-norm resp. the Frobenius norm of Delta_final.

   To do so, the function assumes the following:

   * ||Delta_1||_2 <= 3/8
   
   * ||V||_2 <= 3/2

   * ||V^-1||_2 <= 3/2

   It is up to the caller of the function to ensure these conditions
   are satisfied.

   Each of the complex matrices U, V and S are given by their real and
   imagniary parts. 

   The function changes the precision of the elements of matrices reU
   and imU where needed to satisfy the bound on the norm of the error, 
   which corresponds to a absolute error bound.

   The function allocates, initializes and uses scratch space which it
   clears and frees on its own.

   -----------------------------------------------------------

   The algorithm the function implements performs an iteration 

   U_1 = S
   R_k   = V * U_k - I + K_k           with a small error K_k
   U_k+1 = U_k - U_k * R_k + Sha_k+1   with a small error Sha_k+1
   
   Assuming that 

   * ||Delta_1||_2 <= 3/8
   * ||V||_2 <= 3/2
   * ||V^-1||_2 <= 3/2

   and for all k

   * ||K_k||_2 <= 2^(t-4) <= 2^-6
   * ||Sha_k||_2 <= 2^(t-4) <= 2^-6

   and notating

   Delta_k = U_k - V^-1

   it is possible to show that there exists a rank k* such that for all
   k >= k* we have

   ||Delta_k||_2 <= 2^t.

   This means that under the given hypotheses, there exists a rank k*
   such that for all k >= k* we have 

   ||R_k||_2 <= ||V * U_k - I + K_k||_2 
             <= ||V||_2 * ||Delta_k||_2 + ||K_k||
             <= 3/2 * 2^t + 2^(t-4)
             <= 2^(t+1)

   As ||A||_F <= sqrt(n) * ||A||_2 for any n * n matrix A, by taking
   t <= p - 2 * ceil(log2(sqrt(n))) - 1 - 5 we get (with above hypotheses) that 
   there exists a rank k* such that for all k >= k* the Frobenius norm
   of R_k is bounded by 2^(p-ceil(log2(sqrt(n)))-5):

   ||R_k|_F <= sqrt(n) * ||R_k||_2 
            <= sqrt(n) * 2^(t+1) 
            <= sqrt(n) * 2^(p-2*ceil(log2(sqrt(n)))-1-5+1) 
            <= 2^(p-ceil(log2(sqrt(n)))-5)
                
   We have 2 * ceil(log2(sqrt(n))) <= ceil(log2(n))) + 4.

   Hence let 

   t = p - ceil(log2(n)) - 4 - 1 - 5.

   With such t, we can hence iterate until we detect that the
   Frobenius norm of R_k has become less than
   2^(p-ceil(log2(sqrt(n)))-2) >= 2^(p-ceil(log2(sqrt(n)))-5).  The
   extra 3 exponents allow for headroom in Frobenius norm computation
   and testing.

   When we will have attained a rank k' such that ||R_k'||_F <=
   2^(p-ceil(log2(sqrt(n)))-1), we will further have

   ||Delta_k'||_F <= sqrt(n) * ||Delta_k'||_2
                  <= sqrt(n) * ||V^-1 * R_k - V^-1 * K_k||_2
                  <= sqrt(n) * (||V^-1||_2 * ||R_k||_2 + ||V^-1||_2 * ||K_k||_2)
                  <= sqrt(n) * (3/2 * 2^(p-ceil(log2(sqrt(n)))-2) + 3/2 * 2^(t-4))
                  <= sqrt(n) * (3/2 * 2^(p-ceil(log2(sqrt(n)))-2) + 3/2 * 2^(p-ceil(log2(sqrt(n)))-2))
                  <= 2^p
 
   Notate

   h = p-floor(1/2 * ceil(log2(n)))-1-1 <= p-ceil(log2(sqrt(n)))-1

   So having chosen t, it is just important to ensure that for all k

   * ||K_k||_2 <= 2^(t-4) <= 2^-6
   * ||Sha_k||_2 <= 2^(t-4) <= 2^-6

   We obtain these conditions by ensuring that in each element

   |K_k| <= 2^q <= 2^(t-4-ceil(log2(n)))

   and 

   |Sha_k| <= 2^q <= 2^(t-4-ceil(log2(n)))

   because hence the 2 norms and Frobenius norms of K_k and Sha_k are bounded as follows

   ||K_k||_2 <= ||K_k||_F <= sqrt(n^2 * (2^(t-4-ceil(log2(n))))^2)
                          <= 2^(t-4).

   As t = p - ceil(log2(n)) - 4 - 1 - 5, we choose 

   q = min(p,-1) - 2 * ceil(log2(n)) - 4 - 1 - 5 - 4

   The minimum ensures that we get 2^(t-4) <= 2^-6 (to be verified).

*/
int invertComplexMatrix(mpfr_t *reU, mpfr_t *imU,
                         mpfr_t *reV, mpfr_t *imV,
                         mpfr_t *reS, mpfr_t *imS,
                         uint64_t n,
                         mp_exp_t p) 
{
  mp_exp_t minP, q, h;
  mpfr_t *reR, *imR;
  mpfr_t *reUk, *imUk;
  mpfr_t *reUkP1, *imUkP1;
  mpfr_t *reI, *imI;
  mpfr_t *scratchV;
  mpfr_t scratchT1, scratchT2;

  /* Determine absolute error bound for computations yielding R_k and
     U_k+1 
  */
  minP = p; 
  if (-1 < minP) minP = -1;
  q = minP - 2 * ceilLog2(n,n) - 4 - 1 - 5 - 4;

  /* Determine bound for convergence */
  h = minP-(ceilLog2(n,n) >> 1)-1-1;

  /* Allocate matrices R and Uk and UkP1 */
  reR = allocateMPFRMatrix(n,n, 64);
  imR = allocateMPFRMatrix(n,n, 64);
  reUk = allocateMPFRMatrix(n,n, 64);
  imUk = allocateMPFRMatrix(n,n, 64);
  reUkP1 = allocateMPFRMatrix(n,n, 64);
  imUkP1 = allocateMPFRMatrix(n,n, 64);
  
  /* Allocate and set complex identity matrix */
  reI = allocateMPFRMatrix(n,n, 5);
  imI = allocateMPFRMatrix(n,n, 5);
  setMatrixIdentity(reI, n);
  setMatrixZero(imI, n,n);
  

  /* Allocate a scratch space vector of size 2 * n + 1 and initialize
     two scalar scratch variables 
  */
  scratchV = allocateMPFRVector(2 * n + 1, 640);
  mpfr_init2(scratchT1, 64);
  mpfr_init2(scratchT2, 64);

  /* Initialize Uk */
  copyMatrix(reUk, reS, n,n);
  copyMatrix(imUk, imS, n,n);  

  
  /* Compute first R_k */
  complexMatrixMultiplyAndAdd_square(reR, imR, 1, reV, imV, reUk, imUk, -1, reI, imI, n, q, scratchV);
  // complexMatrixMultiplyAndAdd(reR, imR, 1, reV, imV, reUk, imUk, -1, reI, imI, n, n, n, q, scratchV);

  int iterations = 0;
  /* Iterate until convergence */
  while (!checkFrobeniusNorm(reR, imR, n, n, h, scratchT1, scratchT2)) 
  { 
    /* Compute U_k+1 out of U_k and R_k */
    complexMatrixMultiplyAndAdd_square(reUkP1, imUkP1, -1, reUk, imUk, reR, imR, 1, reUk, imUk, n, q, scratchV);
    // complexMatrixMultiplyAndAdd(reUkP1, imUkP1, -1, reUk, imUk, reR, imR, 1, reUk, imUk, n, n, n, q, scratchV);

    /* Make U_k+1 become U_k for next iteration */
    swapMPFRArrayPointers(&reUk, &reUkP1);
    swapMPFRArrayPointers(&imUk, &imUkP1);

    /* Compute R_k for next iteration */
    complexMatrixMultiplyAndAdd_square(reR, imR, 1, reV, imV, reUk, imUk, -1, reI, imI, n, q, scratchV);
    // complexMatrixMultiplyAndAdd(reR, imR, 1, reV, imV, reUk, imUk, -1, reI, imI, n, n, n,  q, scratchV);

    iterations++;

  }
  // printf("\n Iterations while inverting: %d \n", iterations);

  /* Copy Uk into result matrix */
  copyMatrix(reU, reUk, n, n);
  copyMatrix(imU, imUk, n, n);

  /* Clear and free scratch space */
  mpfr_clear(scratchT2);
  mpfr_clear(scratchT1);
  freeMPFRVector(scratchV, 2 * n + 1);

  /* Clear and free all temporary matrices */
  freeMPFRMatrix(imI, n, n);
  freeMPFRMatrix(reI, n, n);
  freeMPFRMatrix(imUkP1, n, n);
  freeMPFRMatrix(reUkP1, n, n);
  freeMPFRMatrix(imUk, n, n);
  freeMPFRMatrix(reUk, n, n);
  freeMPFRMatrix(imR, n, n);
  freeMPFRMatrix(reR, n, n);
  return iterations;
}


  
/* Compute the square of absolte value for a complex number, i.e.
    res = re^2 + im^2 + delta

    such that abs(delta) <= 2^k

    Function changes precision of res if neccesary.

  */

void squareOfAbsoluteValue(mpfr_t res, mpfr_t re, mpfr_t im, mp_exp_t k, mpfr_t scratch)
{
  mp_exp_t e, maxExp;
  mp_prec_t prec, precRes;
  int tern;

  /* Handle inputs that are non-real */
  if (!(mpfr_number_p(re) && 
  mpfr_number_p(im))) {
    /* Do stupid FP arithmetic, this will yield a NaN or Inf */
    mpfr_mul(res, re, re, GMP_RNDN); 
    mpfr_fma(res, im, im, res, GMP_RNDN);
    mpfr_sqrt(res, res, GMP_RNDN);
    return;
  }


/*  

     Get the maximum exponent of re and im.

  */
  maxExp = mpfr_get_exp(re);
  e = mpfr_get_exp(im);
  if (e > maxExp) maxExp = e;

  /*  
     Take now prec = max(max(maxExp + 1 - k + 2, 5), prec(res)).
  */

  prec = (mp_prec_t) (maxExp - k + 1 + 2);
  if (prec < 5) prec = 5;
  
  /* Keep the original precision of the result variable res and set
     its precision to prec. 
  */
  precRes = mpfr_get_prec(res);
  if (prec > precRes) {
    mpfr_set_prec(res, prec);
  }

  /* Set the precision of the scratch variable to the double of the re
     variable. 
  */
  mpfr_set_prec(scratch, 2 * mpfr_get_prec(re));
  
  /* Compute an preliminary result as follows. */
  mpfr_sqr(scratch, re, GMP_RNDU);          /* exact */
  mpfr_fma(res, im, im, scratch, GMP_RNDU); /* res = (re^2 + im^2) * (1 + eps1) */
  // mpfr_sqrt(res, res, GMP_RNDN);            /* res = sqrt(re^2 + im^2) * sqrt(1 + eps1) * (1 + eps2) */
  
  
  if (!mpfr_number_p(res)) {
    mpfr_prec_round(res, precRes, GMP_RNDU); /* "rounding" inf or Nan */
    return;
  }
  
  /* Here res is a real */
  mpfr_set_prec(scratch, precRes);
  tern = mpfr_set(scratch, res, GMP_RNDU); /* rounds to original precision of res */
  
  if ((tern == 0) && mpfr_number_p(scratch)) {
    /* We have scratch = res and scratch on the original precision of
       res 
    */
    mpfr_set_prec(res, precRes);
    mpfr_set(res, scratch, GMP_RNDU); /* exact */
  }
}


/* Functions for norm(T)_2 < 1 verification */


// Function extracts the non-diagonal part of complex square matrix T
// Function changes the precision of results in dependence of precision of elements of T
void extractDiagonal(mpfr_t *reR, mpfr_t *imR, mpfr_t *reT, mpfr_t *imT, uint64_t n)
{
  mpfr_prec_t precRe, precIm;
  int i, j;
  for(i = 0; i < n; ++i)
  {
    for(j = 0; j < n; ++j)
    {
      if(i != j)
      {
        precRe = mpfr_get_prec(reT[i * n + j]);
        mpfr_set_prec(reR[i * n + j], precRe);    //setting precision of result 
        mpfr_set(reR[i * n + j], reT[i * n + j], MPFR_RNDU);

        precIm = mpfr_get_prec(imT[i * n + j]);
        mpfr_set_prec(imR[i * n + j], precRe);    //setting precision of result 
        mpfr_set(imR[i * n + j], imT[i * n + j], MPFR_RNDU);

      }
      else
      {
        mpfr_set_zero(imR[i * n + i], +1);
        mpfr_set_zero(reR[i * n + i], +1);
      }
    }
  }
}

//The function checks if the norm(T)_2 of complex matrix T is less than 1
// It uses the Gershgorin's cercle theorem
//See article for detailes

int checkTwoNorm(mpfr_t *reT, mpfr_t *imT, uint64_t n)
{


  int result = 0;
  mpfr_prec_t prec = 64;
  mpfr_prec_t maxT = getMaxPrecision(reT, imT, n, n);
  mpfr_prec_t p = prec + prec + 1;

  mpfr_t scratch;
  mpfr_init2(scratch, p);    //setting precision of multiplication to 2*prec



  mpfr_t *reR, *imR;
  reR = allocateMPFRMatrix(n, n, prec);
  imR = allocateMPFRMatrix(n, n, prec);



  //extract the non-diagonal elements of T
  extractDiagonal(reR, imR, reT, imT, n);

  // printf("\n R: \n" );
  // writeMPFRComplexMatrix(stderr, reR, imR, n, n, 10, MPFR_RNDU);

  mpfr_t alpha;
  mpfr_init2(alpha, prec);
  frobeniusNormUpperBound(alpha, reR, imR, n, n, scratch);    //alpha = norm(R)_frob

  mpfr_t beta;
  mpfr_init2(beta, prec);
  mpfr_sqrt_ui(beta, n, MPFR_RNDU);     //beta = sqrt(n)

  

  mpfr_t gamma;
  mpfr_init2(gamma, prec);

  mpfr_t scratch2;
  mpfr_init2(scratch2, prec);


  mpfr_mul_d(scratch, beta, 2, MPFR_RNDU);    //scratch = 2 * beta;
  mpfr_mul(scratch2, scratch, alpha, MPFR_RNDU);  //scratch2 = 2 * beta * alpha
  mpfr_fma(gamma, alpha, alpha, scratch2, GMP_RNDU);  //gamma = 2 * beta*alpha + alpha^2
  mpfr_mul_ui(gamma, gamma, (n - 1), MPFR_RNDU);    // gamma = (n-1) * gamma

  // so now we have gamma in precision prec;
  //for each T_ii we check if abs(T_ii)^2 + alpha^2 + gamma <= 1


  mpfr_t absTii;
  mpfr_init2(absTii, maxT);

  mpfr_t absTgamma;
  mpfr_init2(absTgamma, maxT);

  mpfr_t scratch3;
  mpfr_init2(scratch3, maxT);

  mp_exp_t k, re, im;
  int i;
  for(i = 0; i < n; ++i)
  {
    // re = mpfr_get_exp(reT[i * n + i]);
    // im = mpfr_get_exp(imT[i * n + i]);
    // k = re < im ? re : im;

    //we compute the absTii = reT_ii^2 + imT_ii^2 + delta with delta < 2^k
    squareOfAbsoluteValue(absTii, reT[i * n + i], imT[i * n + i], -prec, scratch);


    mpfr_add(scratch3, absTii, gamma, MPFR_RNDU);
    mpfr_fma(absTgamma, alpha, alpha, scratch3, MPFR_RNDU);

    // printf("\n Gershrogin check: \n");
    // mpfr_out_str(stderr, 10, 100, absTgamma, MPFR_RNDU);

    if(mpfr_cmp_ui(absTgamma, (uint64_t)1) > 0) 
    {
      fprintf(stderr,"Gershgorin's circle is larger than 1 \n ");
      mpfr_clear(scratch);
      mpfr_clear(alpha);
      mpfr_clear(beta);
      mpfr_clear(gamma);
      mpfr_clear(scratch2);
      mpfr_clear(absTii);
      mpfr_clear(absTgamma);
      mpfr_clear(scratch3);
      freeMPFRMatrix(reR, n, n);
      freeMPFRMatrix(imR, n, n);
      return 0;

    }
    result = 1;
  
  }

// printf("Exit Tnorm\n");
  mpfr_clear(scratch);
  mpfr_clear(alpha);
  mpfr_clear(beta);
  mpfr_clear(gamma);
  mpfr_clear(scratch2);
  mpfr_clear(absTii);
  mpfr_clear(absTgamma);
  mpfr_clear(scratch3);
  freeMPFRMatrix(reR, n, n);
  freeMPFRMatrix(imR, n, n);
  return result;

}

/* For a complex n x n matrix V the function checks if conditions
for matrix inverse algorithm are satisfied 
with S is inverse of V computed with clapack;
    */
int inverseConditionsTest(complexdouble *V, complexdouble *S, uint64_t n)
{
 

 return 1;

}




