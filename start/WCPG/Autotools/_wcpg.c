/* WCPG.c */

#include "_wcpg.h"

/* Swaps two MPFR array pointers */
static inline void swapMPFRArrayPointers(mpfr_t **p, mpfr_t **q) {
  mpfr_t *temp;
  temp = *p;
  *p = *q;
  *q = temp;
}

void wcpg_result_init(wcpg_result *result)
{
	result->N = 0;
	result->time_overall = 0;
	result->time_Ncomp = 0;
	result->time_Summation = 0;
	mpfr_init2(result->one_minus_rhoA, 64);
	mpfr_init(result->maxSN);
	mpfr_init(result->minSN);
	result->inversion_Iter = 0;
	result->maxprec_PN = 0;
	result->maxprec_U = 0;
	result->maxprec_SN = 0;
}

void wcpg_result_clear(wcpg_result *result)
{
	mpfr_clear(result->maxSN);
	mpfr_clear(result->minSN);
	mpfr_clear(result->one_minus_rhoA);
}

void wcpg_result_print(FILE *stream, wcpg_result *result, size_t ndigits)
{
	fprintf(stream, "Truncation order N: %d\n", result->N);
	fprintf(stream, "1 - rho(A): \n");
	mpfr_out_str(stream, (int)10, ndigits, result->one_minus_rhoA, MPFR_RNDN );
	fprintf(stream, "\nInversion iterations: %d \n", result->inversion_Iter );
	fprintf(stream, "max(S_N): \n");
	mpfr_out_str(stream, (int)10, ndigits, result->maxSN, MPFR_RNDN );
	fprintf(stream, "\nmin(S_N): \n");
	mpfr_out_str(stream, (int)10, ndigits, result->minSN, MPFR_RNDN );
	fprintf(stream, "\nOverall time spent: %.2f \n", result->time_overall );
	fprintf(stream, "N computation time: %.2f \n", result->time_Ncomp );
	fprintf(stream, "Summation time: %.2f \n", result->time_Summation );
	fprintf(stream, "Maximum precision of U = inv(V): %ld \n", result->maxprec_U );
	fprintf(stream, "Maximum precision of P_N: %ld \n", result->maxprec_PN );
	fprintf(stream, "Maximum precision of S_N: %ld \n", result->maxprec_SN );

}

/* --------------Functions for N_lower_bound algorithm. To be replaced later. -----------------*/



/* For complex p x n matrix Phi, complex n x q matrix Psi the funciton constructs
l-th residue matrix R, wich is a complex p x q. */
void R_l(mpfi_t *reRl, mpfi_t *imRl, mpfi_t *rePhi, mpfi_t *imPhi, mpfi_t *rePsi, mpfi_t *imPsi, uint64_t n, uint64_t p, uint64_t q, int l)
{
	int i, j;
	// if (l >= n)
	// 	printf("Error! R_(%d)th residue matrix does not exist!\n", l);
	mpfi_t scratch;
	mpfi_init2(scratch, 64*2);
	for( i = 0; i < p; ++i)
	{
		for( j = 0; j < q; ++j)
		{
			mpfi_mul_complex(reRl[i*q + j], imRl[i*q + j], rePhi[i * n + l], imPhi[i * n + l], rePsi[l * q + j], imPsi[l * q + j], scratch);

		}
	}


}

/* This funciton coputes the lower bound on truncation order N for WCPG sum. The algorithm for 
this bound is described in details in report(article). Short exmplanation:
Suppose state-space [A,B,C,D] representation of LTI filter is given. 
Then,

N >= ceil{log(eps/norm(M)_min) / log(1 - rho(A))}

with 
	* eps - desired error of truncation;
	* norm(M)_min = min_i,j {M_ij}
	* M = sum_l=1:n {k_l * R_l} is p x q real matrix
	* k_l = abs(lambda_l) / ((1 - abs(lambda_l))*rho) is a scalar coefficient
	* R_l is l-th residue matrix 
 */

int lowerBoundN(mpfi_t *rePhi, mpfi_t *imPhi, mpfi_t *rePsi, mpfi_t *imPsi, \
					 mpfi_t *reLambda, mpfi_t *imLambda,mpfr_t eps, uint64_t n, uint64_t p, uint64_t q, mpfr_prec_t prec, wcpg_result *result)
{

	mpfi_t scratch1, scratch2, scratch3, scratchabs, *scratchVector2;
	mpfi_init2(scratch1, prec);
	mpfi_init2(scratch2, prec);
	mpfi_init2(scratch3, prec);
	mpfi_init2(scratchabs, prec);
	scratchVector2 = allocateMPFIMatrix(1,2,prec);

	mpfi_t rho;
	mpfi_init2(rho, prec);
	mpfi_maxabs(rho, reLambda, imLambda, 1, n, scratchVector2);

	mpfi_t oneMinusRho;						
	mpfi_init2(oneMinusRho, prec);
	mpfi_ui_sub(oneMinusRho, 1, rho);

	mpfr_t rhofr;
	mpfr_init(rhofr);
	mpfi_get_fr(rhofr, oneMinusRho);		// converting interval to floating point
	mpfr_set(result->one_minus_rhoA, rhofr, MPFR_RNDU);

	mpfi_t denum;				
	mpfi_init2(denum, prec);
	mpfi_log2(denum, rho);		
	mpfi_abs(denum, denum);		//denum = abs(log2(rho));


	//We need to compute M = sum_1^n (K_i* R_i) with K = rho*abs(lambda) / (1 - abs(lambda))
	mpfi_t K;
	mpfi_init2(K, prec);

	mpfi_t *reRl, *imRl;
	reRl = allocateMPFIMatrix(p, q, prec);
	imRl = allocateMPFIMatrix(p, q, prec);

	mpfi_t Mij, min;
	mpfi_init2(min, prec);
	mpfi_init2(Mij, prec);
	mpfi_set_d(min, 100000.0);

	int l, i, j;
	for(l = 0; l < n; ++l)
	{
		mpfi_abs_complex(scratch1, reLambda[l], imLambda[l], scratchabs);    //scratch1 = abs(lambda_l)
		mpfi_ui_sub(scratch2, 1, scratch1); 						//scratch2 = 1 - abs(lambda_l);
		mpfi_mul(scratch3, scratch2, rho); 						// scratch3 = (1 - abs(lambda_l))*rho
		mpfi_div(K, scratch1, scratch3); 							// K = abs(lambda_l) / ((1 - abs(lambda_l))*rho)
		R_l(reRl, imRl, rePhi, imPhi, rePsi, imPsi, n, p, q, l);		//l-th residue matrix 
		
		for(i = 0; i < p; ++i)
		{
			for(j = 0; j < q; ++j)
			{
				
				mpfi_abs_complex(scratch1, reRl[i * q + j], imRl[i * q + j], scratchabs);	//scratch1 = abs(R_l(i,j))
				mpfi_mul(Mij, K, scratch1);		// M(i,j) = K * abs(R_l(i,j))
				if(mpfi_cmp(Mij, min) < 0)
					mpfi_set(min, Mij);
			}
		}
	}

	// so now we know the norm_min of matrix M: min = norm(M)_min;

	mpfi_fr_div(scratch1, eps, min);  //scratch1 = eps / norm(M)_min
	mpfi_log2(scratch1, scratch1);	// scratch1 = log2(eps / norm(M)_min)

	mpfi_div(scratch2, scratch1, denum); //scratch2 = scratch1 / denum = log2(eps / norm(M)_min) / log2(rho(A))
	mpfi_abs(scratch2, scratch2);


	mpfr_t Nsup;
	mpfr_init(Nsup);
	mpfi_get_right(Nsup, scratch2);

	int N = ceil(mpfr_get_d(Nsup, 53));

	return N;
}



/* ---------------- End of N_lower_bound algorithm functions ---------*/



/* THe function determines the minimal and maximum values of the
computed WCPG matrix and adds them to the corresonding fields
of the result structure. 
 */
void getDeltaOfWCPG(mpfr_t *reS, uint64_t p, uint64_t q, wcpg_result *result)
{
	int i,j;

	mpfr_prec_t e = getMaxPrecision(reS, reS, p, q);

	mpfr_t min;
	mpfr_init2(min, e);
	mpfr_set(min, reS[0], MPFR_RNDN);

	mpfr_t max;
	mpfr_init2(max, e);
	mpfr_set(max, reS[0], MPFR_RNDN);

	for( i = 0; i < p; ++i)
	{
		for(j = 0; j < q; ++j)
		{
			if(mpfr_cmp(reS[i * q + j],min) < 0 )
			{
				mpfr_set(min, reS[i * q + j], MPFR_RNDN);

			}
			if(mpfr_cmp(reS[i * q + j],max) > 0 )
				mpfr_set(max, reS[i * q + j], MPFR_RNDN);
		}
	}

	mpfr_set_prec(result->maxSN, e);
	mpfr_set_prec(result->minSN, e);

	mpfr_set(result->maxSN, max, MPFR_RNDN);
	mpfr_set(result->minSN, min, MPFR_RNDU);


}


/* For an LTI filter given in its State-Space representation {A,B,C,D}, 
where A is n*n, B is n*q, C is p*n and D is p*q real matrix,
and for an eps>0 the function returns a multi-precision n*q real matrix Sk of Worst-Case Peak Gains 
of the system such that the overall error of computation is bounded by eps. */
int WCPG(mpfr_t *Sk, double *A, double *B, double *C, double *D, mpfr_t mpeps, uint64_t n, uint64_t p, uint64_t q, wcpg_result *result)
{


	//Because of an issue of checking whether the structure wcpg_result is initilized or not
	//I have decided to initilize it in the method directly, so user needs just to declare it 
	//outside without initilizing;

	wcpg_result_init(result);


	clock_t begin, end, begin_Ncomp, end_Ncomp, begin_summation, end_summation;
	mpfr_prec_t prec = 106;
	
	int i;


	/* Convertion of the double matrices into multiprecision complex format */

	mpfr_t *reA, *imA;
	reA = allocateMPFRMatrix(n, n, prec);
	imA = allocateMPFRMatrix(n, n, prec);
	setMatrixZero(imA, n, n);
	doublerealToMPFRMatrix(reA, A, n, n);

	mpfr_t *reB, *imB;
	reB = allocateMPFRMatrix(n, q, prec);
	imB = allocateMPFRMatrix(n, q, prec);
	setMatrixZero(imB, n, q);
	doublerealToMPFRMatrix(reB, B, n, q);

	mpfr_t *reC, *imC;
	reC = allocateMPFRMatrix(p, n, prec);
	imC = allocateMPFRMatrix(p, n, prec);
	setMatrixZero(imC, p, n);
	doublerealToMPFRMatrix(reC, C, p, n);

	mpfr_t *reD, *imD;
	reD = allocateMPFRMatrix(p, q, prec);
	imD = allocateMPFRMatrix(p, q, prec);
	setMatrixZero(imD, p, q);
	doublerealToMPFRMatrix(reD, D, p, q);


	/* starting the timer */

	begin = clock();				//we start timer here!
	begin_Ncomp = clock();


	/* Computing eps_1 = eps/6 */

	mpfr_t eps_1;
	mpfr_init2_my(eps_1, prec);				//eps_1 = eps / 6
	mpfr_set(eps_1, mpeps, MPFR_RNDD);
	mpfr_div_ui(eps_1, eps_1, 6, MPFR_RNDD);	



	/* Preparing scratch variables*/

	mpfi_t *scratch3intval;
	scratch3intval = allocateMPFIMatrix(1,3, prec);

	mpfr_t *scratch3;
	scratch3 = allocateMPFRVector(3, 64);

	mpfr_t *scratchT;
	scratchT = allocateMPFRVector(2 * n + 1, 64);

	mpfr_t scratch, scratch2;
	mpfr_init2_my(scratch, prec);
	mpfr_init2_my(scratch2, prec);

	/* prepare Zero Matrices of different sizes that will be used for multiplyAndADDMPFRMatrices */
	mpfr_t *In;
	In = allocateMPFRMatrix(n,n, 64);
	setMatrixIdentity(In, n);

	mpfr_t *Zeronn;
	Zeronn = allocateMPFRMatrix(n,n, 64);
	setMatrixZero(Zeronn, n, n);

	mpfr_t *Zeropn;
	Zeropn = allocateMPFRMatrix(p,n, 64);
	setMatrixZero(Zeropn, p, n);

	mpfr_t *Zeronq;
	Zeronq = allocateMPFRMatrix(n,q, 64);
	setMatrixZero(Zeronq, n, q);

	mpfr_t *Zeropq;
	Zeropq = allocateMPFRMatrix(p,q, 64);
	setMatrixZero(Zeropq,p,q);

	/* -------------Step 1. Computing lower bound on N --------------*/

	/* If we want to separate this algorithm, then
	we must define local context structure for:
	1. Input: A,B,C,D, result, prec, n, p, q,mpeps
	2. Output: Nmax, reV, imV, reVint, imVint, Vinv

	*/

	
	/*Finding eigenvalues and eigenvectors*/
	complexdouble *V, *eigv;
 	V = (complexdouble*)malloc(n*n*sizeof(complexdouble));
 	eigv = (complexdouble*)malloc(n*sizeof(complexdouble));

	doublereal *Acpy = (doublereal*)malloc(n*n*sizeof(doublereal));		// we copy the matrix, because CLAPACK changes it in eigensolver
	clapack_matrix_copy_d(Acpy, A, n, n);
	
	doublereal *eerrbnd = (doublereal*)malloc(n*sizeof(doublereal));
	doublereal *verrbnd = (doublereal*)malloc(n*sizeof(doublereal));
	doublereal eps_prec = DBL_EPSILON;
		
	clapack_eigenSolver(eigv, V, eerrbnd, verrbnd, Acpy, n, eps_prec);	//eigensolver, which returns approx error bounds


	// Variables for interval matrices of eigenvectors and eigenvalues
	mpfi_t *reVint, *imVint;
	reVint = allocateMPFIMatrix(n, n, prec);
	imVint = allocateMPFIMatrix(n, n, prec);

	mpfi_t *reLambdaint, *imLambdaint;
	reLambdaint = allocateMPFIMatrix(1, n, prec);
	imLambdaint = allocateMPFIMatrix(1, n, prec);

	/* Checking Inclusion */

	/* ATTENTION: EIGENVALUE INCLUSION ALGORITHM IS CURRENTLY UNDER RECONSTRUCTION! */

	complexdouble lambda;
	complexdouble *xs = (complexdouble*)malloc(n*sizeof(complexdouble));
	complexdouble *Az = (complexdouble*)malloc(n*n*sizeof(complexdouble));
	clapack_rmatrix_as_zmatrix(Az, A, n, n);

	mpfr_t epsV, epsLambda;
	mpfr_init2(epsV, prec);
	mpfr_init2(epsLambda, prec);

	getMaxInMPFR(epsV, verrbnd, 1, n);			//we get the max error bound on V and Lambda and further
	getMaxInMPFR(epsLambda, eerrbnd, 1, n);		//construct interval matrices with them as radius


	
	int j = 0;
	for(j = 0; j < n; ++j)
	{
	  	
	      lambda.r = eigv[j].r + eerrbnd[j];
	      lambda.i = eigv[j].i + eerrbnd[j];
	      //if lambda returned by CLAPACK is already such that its absolute value is larger than 1, then we quit
	      if((abs_complexdouble(&lambda)) > 1)		
	      {
	      		fprintf(stderr, "There Exists an eigenvalue lambda larger than 1. Precedure exits.\n");
	      		fprintf(stderr, "1 - abs(lambda) = %f \n", 1 - (abs_complexdouble(&lambda)));
	      		end_Ncomp = clock();
	      		begin_summation = clock();
	      		end_summation = clock();
				end = clock();
				result->time_overall = (double)(end - begin) / CLOCKS_PER_SEC;	
				result->time_Summation  = (double)(end_summation - begin_summation) / CLOCKS_PER_SEC;
				result->time_Ncomp = (double)(end_Ncomp - begin_Ncomp) / CLOCKS_PER_SEC;
				
	      		return 0;
	      		
	      }
	      

//	      int i;
//	      for(i = 0; i < n; ++i)
//	      {
//		      xs[i].r = V[i*n + j].r;
//		      xs[i].i = V[i*n + j].i;
//	      }
//
//	      /* For the moment inclusion verification functions are under reconstruction */
//
//	      mpfi_t *rev_corrected;
//	      mpfi_t *imv_corrected;
//	      mpfi_t relambda_corrected,imlambda_corrected;
//
//	      mpfi_init2(relambda_corrected, prec);
//	      mpfi_init2(imlambda_corrected, prec);
//	      rev_corrected = allocateMPFIMatrix(1, n, prec);
//	      imv_corrected = allocateMPFIMatrix(1, n, prec);
//	      //int res = checkEigensystemInclusion(rev_corrected, imv_corrected, relambda_corrected, imlambda_corrected, Az, xs, lambda, n, mpfr_get_d(epsV, MPFR_RNDU), mpfr_get_d(epsLambda, MPFR_RNDU), prec*2);
//	     	int  res = 1;
//
//	       if( !res )
//	       {
//	       		printf("Inclusion failed! Terminating process. \n");
//	       		return 0;
//	       }
//
	 }

	getMaxInMPFR(epsV, verrbnd, 1, n);			//we get the max error bound on V and Lambda and further
	getMaxInMPFR(epsLambda, eerrbnd, 1, n);		//construct interval matrices with them as radius

	//constructing [V] = [V - epsV, V + epsV]
	MPFIComplexMatrixMidradDouble(reVint, imVint, V, n, n, epsV,  scratch3);
	//doing the same for [Lambda]	
	MPFIComplexMatrixMidradDouble(reLambdaint, imLambdaint, eigv,1, n, epsLambda, scratch3);		

	/* Preparing variables for inversion of V */
	mpfr_t *reV;
	mpfr_t *imV;
	reV = allocateMPFRMatrix(n, n, prec);
	imV = allocateMPFRMatrix(n, n, prec);
	MPFIMatrixtoMPFRMatrix(reV, imV, reVint, imVint, n, n);


	/* Compute inv(V) with clapack and check if we can use our inverse method */
	complexdouble *Vinv = (complexdouble*)malloc(n*n*sizeof(complexdouble));
	complexdouble *Vcpy = (complexdouble*)malloc(n*n*sizeof(complexdouble));		// we copy the matrix, because CLAPACK changes it in eigensolver
	clapack_matrix_copy_z(Vcpy, V, n, n);
	if(!clapack_complex_matrix_inverse(Vinv, Vcpy, n))
		return 0;

	/* Transform inv(V) into MPFR format matrix */
	mpfr_t *reVinv;
	mpfr_t *imVinv;
	reVinv = allocateMPFRMatrix(n,n, prec);
	imVinv = allocateMPFRMatrix(n,n, prec);
	complexdoubleToMPFRMatrix(reVinv, imVinv, Vinv, n,n);


	/* Check if we can inverse. 
	To update after frobeniusNormUpperBound basic brick implemented*/

	
	 //if(!inverseConditionsTest())
	 //{
	 //	printf("Could not compute WCPG, test for inversion possibility failed. Algorithm exits.\n");
	 //	return 0;
	 //}

	

	/* Calculating Psi = inv(V) * B */      

  	/* Here we inverse matrix V with just twice the precision, that would CLAPACK use, and after we inverse it with larger precision when compute matrix T.. */
  	/* Further we would like to do it only once, with max precision. */
	mpfr_t *reU1;				
	mpfr_t *imU1;
	imU1 = allocateMPFRMatrix(n,n, prec);
	reU1 = allocateMPFRMatrix(n,n, prec);
	setMatrixZero(imU1, n,n);
	setMatrixZero(reU1, n,n);

	invertComplexMatrix(reU1, imU1, reV, imV, reVinv, imVinv, n, -prec);

	mpfi_t *reU1_int, *imU1_int;
    reU1_int = allocateMPFIMatrix(n, n, prec);
    imU1_int = allocateMPFIMatrix(n, n, prec);
    MPFRMatrixToMPFIMatrix(reU1_int, imU1_int, reU1, imU1, n, n);	//convert computed inverse to mpfi

    freeMPFRMatrix(reU1, n, n);
    freeMPFRMatrix(imU1, n, n);

    /* Construct Psi = inv(V) * B */
	mpfi_t *rePsi, *imPsi;
    rePsi = allocateMPFIMatrix(n, q, prec);
    imPsi = allocateMPFIMatrix(n, q, prec);

    MPFIMatrixMultiplyDoubleMatrix(rePsi, imPsi, reU1_int, imU1_int, B, n, n, q, scratch3intval);	//Psi = inv(V) * B

  	/* Computing Phi = C * V */
    mpfi_t *rePhi, *imPhi;
   	rePhi = allocateMPFIMatrix(p, n, prec);
   	imPhi = allocateMPFIMatrix(p, n, prec);

    DoubleMatrixMultiplyMPFIMatrix(rePhi, imPhi, C, reVint, imVint, p, n, n, scratch3intval);		//[Phi] = C*[V];

    /* Compute lower bound on N using formula (28) [see paper] */
    int Nmax = lowerBoundN(rePhi, imPhi, rePsi, imPsi, reLambdaint, imLambdaint,eps_1, n, p, q, prec, result);
  
    result->N = Nmax;

    end_Ncomp = clock();

    

	/* Freeing complexdouble and doublereal matrices */

	/* TO BE COMPLETED */


	
	/* -------------------Summation stage------------------------ */


	begin_summation = clock();

	/* Step 2. Constructing matrix T = inv(V)*A*V */

	/* Prepare variables for our inversion method */
	mpfr_t *reU;
	mpfr_t *imU;
	imU = allocateMPFRMatrix(n,n, prec);
	reU = allocateMPFRMatrix(n,n, prec);
	setMatrixZero(imU, n,n);
	setMatrixZero(reU, n,n);



	//Compute upper bounds on Frobenius norms of our matrices V, Vinv, B, C

	mpfr_t frobV;
	mpfr_init2_my(frobV, prec);
	frobeniusNormUpperBound(frobV, reV, imV, n, n, scratch);

	mpfr_t frobC;
	mpfr_init2_my(frobC, prec);
	frobeniusNormUpperBound(frobC, reC, imC, p, n, scratch);

	mpfr_t frobB;
	mpfr_init2_my(frobB, prec);
	frobeniusNormUpperBound(frobB, reB, imB, n, q, scratch);

	mpfr_t frobVinv;				//Frobenius norm of the inverse computed with CLAPACK
	mpfr_init2_my(frobVinv, prec);
	frobeniusNormUpperBound(frobVinv, reVinv, imVinv, n, n, scratch);


	/* Precisions for each step are computed via following formulas: */
	/*
		Step 2. eps_2 <= eps / { 6 * sqrt(n) * (Nmax + 1) * (Nmax + 2) * ||C||_F * ||V||_F * ||Vinv||_F * ||B||_F  }

		Step 3. eps_3 = min(eps_3C, eps_3B) = min {eps/(3 * sqrt(n) * 6 * (Nmax + 1) * ||C||_F * ||V||_F), 
			eps/(3 * sqrt(n) * 6 * (Nmax + 1) * ||B||_F * ||Vinv||_F)}

		Step 4. eps_4_k <= eps / {sqrt(n) * (Nmax + 1) * (Nmax -1) * 6 * ||C'||_F * ||B'||_F}

		Step 5. eps_5_k <= eps / {6 * (Nmax + 1)}

		Step 6. eps_6_k <= eps / {6 * (Nmax + 1)}

	 */

	mpfr_t sqrtn;
	mpfr_init2_my(sqrtn, prec);
	mpfr_sqrt_ui(sqrtn, n, MPFR_RNDU);


	mpfr_t eps_2;
	mpfr_init2_my(eps_2, prec);							//eps_2 = eps
	mpfr_set(eps_2, mpeps, MPFR_RNDD);
	mpfr_div(eps_2, eps_2, sqrtn, MPFR_RNDD);			//eps_2 = eps / sqrt(n)
	uint64_t beta = 6 * (Nmax + 1) * (Nmax + 2);	
	mpfr_div_ui(eps_2, eps_2, beta, MPFR_RNDD);			//eps_2 = eps / 6 * sqrt(n) * (Nmax + 1) * (Nmax + 2) 
	mpfr_div(eps_2, eps_2, frobVinv, MPFR_RNDD);
	mpfr_div(eps_2, eps_2, frobC, MPFR_RNDD);
	mpfr_div(eps_2, eps_2, frobB, MPFR_RNDD);
	mpfr_div(eps_2, eps_2, frobV, MPFR_RNDD);			//eps_2 = eps / { 6 * sqrt(n) * (Nmax + 1) * (Nmax + 2) * ||C||_F * ||V||_F * ||Vinv||_F * ||B||_F
	mpfr_exp_t eps_2_exp = mpfr_get_exp(eps_2) - 5;


	mpfr_t eps_3C;
	mpfr_init2_my(eps_3C, prec);				//eps_3C = eps
	mpfr_set(eps_3C, mpeps, MPFR_RNDD);
	mpfr_div(eps_3C, eps_3C, sqrtn, MPFR_RNDD);			//eps_3C = eps / sqrt(n)
	beta = 3 * 6 * (Nmax + 1);	
	mpfr_div_ui(eps_3C, eps_3C, beta, MPFR_RNDD);		//eps_3C = eps / 3* 6 * sqrt(n) * (Nmax + 1) 
	mpfr_div(eps_3C, eps_3C, frobC, MPFR_RNDD);
	mpfr_div(eps_3C, eps_3C, frobV, MPFR_RNDD);			//eps_3C = eps/(3 * sqrt(n) * 6 * (Nmax + 1) * ||C||_F * ||V||_F
	mpfr_exp_t eps_3C_exp = mpfr_get_exp(eps_3C) - 5;

	mpfr_t eps_3B;
	mpfr_init2_my(eps_3B, prec);				//eps_3C = eps
	mpfr_set(eps_3B, mpeps, MPFR_RNDD);
	mpfr_div(eps_3B, eps_3B, sqrtn, MPFR_RNDD);			//eps_3B = eps / sqrt(n)
	beta = 3 * 6 * (Nmax + 1);	
	mpfr_div_ui(eps_3B, eps_3B, beta, MPFR_RNDD);		//eps_3B = eps / 3* 6 * sqrt(n) * (Nmax + 1) 
	mpfr_div(eps_3B, eps_3B, frobB, MPFR_RNDD);
	mpfr_div(eps_3C, eps_3C, frobVinv, MPFR_RNDD);		//eps_3B = eps/(3 * sqrt(n) * 6 * (Nmax + 1) * ||B||_F * ||Vinv||_F
	mpfr_exp_t eps_3B_exp = mpfr_get_exp(eps_3B) - 5;


	mpfr_t eps_5;
	mpfr_init2_my(eps_5, prec);				//eps_5 = eps / {6 * (Nmax + 1)}
	mpfr_set(eps_5, mpeps, MPFR_RNDD);
	beta = 6 * (Nmax + 1);	
	mpfr_div_ui(eps_5, eps_5, beta, MPFR_RNDD);	
	mpfr_exp_t eps_5_exp = mpfr_get_exp(eps_5) - 5;

	mpfr_t eps_6;							//eps_6 = eps_5
	mpfr_init2_my(eps_6, prec);				
	mpfr_set(eps_6, eps_5, MPFR_RNDD);
	mpfr_exp_t eps_6_exp = mpfr_get_exp(eps_6) - 5;

	int invIterations = invertComplexMatrix(reU, imU, reV, imV, reVinv, imVinv, n, eps_2_exp);
	result->inversion_Iter = invIterations;

	/* Step 2 */

	// Construct T = inv(V)*A*V

	//Compute Ttmp = A*V
	mpfr_t *reTtmp, *imTtmp;
	reTtmp = allocateMPFRMatrix(n,n, 64);
	imTtmp = allocateMPFRMatrix(n,n, 64);
	setMatrixZero(Zeronn, n, n);
	complexMatrixMultiplyAndAdd(reTtmp, imTtmp, 1, reA, imA, reV, imV, 1, Zeronn, Zeronn, n,n,n, eps_2_exp, scratchT);

	//Compute T = inv(V) * Ttmp
	mpfr_t *reT, *imT;
	reT = allocateMPFRMatrix(n,n, 64);
	imT = allocateMPFRMatrix(n,n, 64);
	complexMatrixMultiplyAndAdd(reT, imT, 1, reU, imU, reTtmp, imTtmp, 1, Zeronn, Zeronn, n,n,n, eps_2_exp, scratchT);

	/* Here we check if norm(T)_2 <= 1 */
	int normTcheck = checkTwoNorm(reT, imT, n);
	if(!normTcheck)
	{
		fprintf(stderr, "Error! norm(T)_2 > 1. Algorithms exit. \n");
		return 0;
	}

	/* Step 3 */

	//Compute C' = C * V
	mpfr_t *reCV, *imCV;
	reCV = allocateMPFRMatrix(p,n, 64);
	imCV = allocateMPFRMatrix(p,n, 64);
	complexMatrixMultiplyAndAdd(reCV, imCV, 1, reC, imC, reV, imV, -1, Zeropn, Zeropn, p, n, n,eps_3C_exp, scratchT);

	//Compute B' = inv(V) * B
	mpfr_t *reBV, *imBV;
	reBV = allocateMPFRMatrix(n,q, 64);
	imBV = allocateMPFRMatrix(n,q, 64);
	complexMatrixMultiplyAndAdd(reBV, imBV, 1, reU, imU, reB, imB, -1, Zeronq, Zeronq, n, n, q, eps_3B_exp, scratchT);

	//Compute Frobenius norms of C' and B'
	mpfr_t frobCV;
	mpfr_init2_my(frobCV, prec);
	frobeniusNormUpperBound(frobCV, reCV, imCV, p, n, scratch);

	mpfr_t frobBV;
	mpfr_init2_my(frobBV, prec);
	frobeniusNormUpperBound(frobBV, reBV, imBV, n, q, scratch);


	/* Prepare variables for summation */

	//Compute Sk = abs(D)
	absMPFRMatrix(Sk, reD, p, q);

	// Set Pk = I

	mpfr_t *rePk, *imPk;
	rePk = allocateMPFRMatrix(n, n, 64);
	imPk = allocateMPFRMatrix(n, n, 64);
	setMatrixIdentity(rePk, n);
	setMatrixZero(imPk, n, n);

	// Set matrix P_k+1 to zero matrix

	mpfr_t *rePkp1, *imPkp1;
	rePkp1 = allocateMPFRMatrix(n, n, 64);
	imPkp1 = allocateMPFRMatrix(n, n, 64);
	setMatrixZero(rePkp1, n, n);
	setMatrixZero(imPkp1, n, n);

	//Set intermidiate matrix Ltmp to zero matrix

	mpfr_t *reLtmp, *imLtmp;
	reLtmp = allocateMPFRMatrix(n, q, 64);
	imLtmp = allocateMPFRMatrix(n, q, 64);
	setMatrixZero(reLtmp, n, q);
	setMatrixZero(imLtmp, n, q);


	/* Steps 4 - 5 - 6 */

	//Compute eps_4 for powerting matrix T
	mpfr_t eps_4;
	mpfr_init2_my(eps_4, prec);							//eps_4 = eps
	mpfr_set(eps_4, mpeps, MPFR_RNDD);
	mpfr_div(eps_4, eps_4, sqrtn, MPFR_RNDD);			//eps_4 = eps / sqrt(n)
	beta = 6 * (Nmax + 1) * (Nmax -1);	
	mpfr_div_ui(eps_4, eps_4, beta, MPFR_RNDD);			//eps_2 = eps / 6 * sqrt(n) * (Nmax + 1) * (Nmax -1) 
	mpfr_div(eps_4, eps_4, frobCV, MPFR_RNDD);
	mpfr_div(eps_4, eps_4, frobBV, MPFR_RNDD);			//eps_2 = eps / { 6 * sqrt(n) * (Nmax + 1) * (Nmax + 2) * ||C||_F * ||V||_F * ||Vinv||_F * ||B||_F
	mpfr_exp_t eps_4_exp = mpfr_get_exp(eps_4) - 5;

	//Compute sum for k = 0 before the main sycle: S_0 = abs(D) + abs(C'*B')

	// Set L = C' x B' 
	
	mpfr_t *reL, *imL;
	reL = allocateMPFRMatrix(p,q, 64);
	imL = allocateMPFRMatrix(p,q, 64);
	complexMatrixMultiplyAndAdd(reL, imL, 1, reCV, imCV, reBV, imBV, 1, Zeropq, Zeropq, p, n, q, eps_5_exp, scratchT);

	// Accumulate Sk = Sk + abs(Lk)
	accumulateAbsoluteValue(Sk, Sk, reL, imL, p, q, eps_6_exp, scratch3);

	int k;
	for(k = 1; k < Nmax + 1; ++k)
	{

		// P_k+1 = T * P_k
		complexMatrixMultiplyAndAdd(rePkp1, imPkp1, 1, reT, imT, rePk, imPk, 1, Zeronn, Zeronn, n, n, n, eps_4_exp, scratchT); // P_(k+1) = T x P_k

		// Ltmp = P_k+1 * C'
		complexMatrixMultiplyAndAdd(reLtmp, imLtmp, 1, rePkp1, imPkp1, reBV, imBV, 1, Zeronq, Zeronq, n, n, q, eps_5_exp, scratchT);	
	
		// L_k+1 = B' * Ltmp
		complexMatrixMultiplyAndAdd(reL, imL, 1, reCV, imCV, reLtmp, imLtmp,1, Zeropq, Zeropq, p, n, q, eps_5_exp, scratchT);

		//S_k+1 = S_k + abs(L_k+1)
		accumulateAbsoluteValue(Sk, Sk, reL, imL, p, q, eps_6_exp, scratch3);

		// P_k = P_k+1
		swapMPFRArrayPointers(&rePk, &rePkp1);
    	swapMPFRArrayPointers(&imPk, &imPkp1);
	}

	end_summation = clock();
	end = clock();

	result->time_overall = (double)(end - begin) / CLOCKS_PER_SEC;
	result->time_Summation = (double)(end_summation - begin_summation) / CLOCKS_PER_SEC;
	result->time_Ncomp = (double)(end_Ncomp - begin_Ncomp) / CLOCKS_PER_SEC;
	
	mpfr_prec_t maxPN = getMaxPrecision(rePk, imPk, n, n);
	mpfr_prec_t maxSN = getMaxPrecision(Sk, Zeropq, p, q);
	mpfr_prec_t maxU = getMaxPrecision(reU, imU, n, n);

	result->maxprec_U = maxU;
	result->maxprec_PN = maxPN;
	result->maxprec_SN = maxSN;

	getDeltaOfWCPG(Sk, p, q, result);


	freeMPFRMatrix(Zeropn, p, n);
	freeMPFRMatrix(Zeronn, n, n);
	freeMPFRMatrix(Zeronq, n, q);
	freeMPFRMatrix(Zeropq, p, q);
	freeMPFRMatrix(reV, n, n);
	freeMPFRMatrix(imV, n, n);
	freeMPFRMatrix(reA, n, n);
	freeMPFRMatrix(imA, n, n);
	freeMPFRMatrix(reB, n, q);
	freeMPFRMatrix(imB, n, q);
	freeMPFRMatrix(reC, p, n);
	freeMPFRMatrix(imC, p, n);
	freeMPFRMatrix(reD, p, q);
	freeMPFRMatrix(imD, p, q);
	freeMPFRMatrix(reCV, p, n);
	freeMPFRMatrix(imCV, p, n);
	freeMPFRMatrix(reBV, n, q);
	freeMPFRMatrix(imBV, n, q);
	freeMPFRMatrix(reU, n, n);
	freeMPFRMatrix(imU, n, n);
	freeMPFRMatrix(reT, n, n);
	freeMPFRMatrix(imT, n, n);
	freeMPFRMatrix(reTtmp, n, n);
	freeMPFRMatrix(imTtmp, n, n);
	freeMPFRMatrix(rePk, n, n);
	freeMPFRMatrix(imPk, n, n);
	freeMPFRMatrix(rePkp1, n, n);
	freeMPFRMatrix(imPkp1, n, n);
	freeMPFRMatrix(reL, p, q);
	freeMPFRMatrix(imL, p, q);
	freeMPFRMatrix(reLtmp, n, q);
	freeMPFRMatrix(imLtmp, n, q);
	freeMPFRMatrix(In, n, n);


	mpfr_clear(scratch);
	mpfr_clear(scratch2);
	mpfr_clear(frobV);
	mpfr_clear(frobVinv);
	mpfr_clear(frobC);
	mpfr_clear(frobCV);
	mpfr_clear(frobB);
	mpfr_clear(frobBV);
	mpfr_clear(eps_1);
	mpfr_clear(eps_2);
	mpfr_clear(eps_3C);
	mpfr_clear(eps_3B);
	mpfr_clear(eps_4);
	mpfr_clear(eps_5);
	mpfr_clear(eps_6);



	return 1;

}


