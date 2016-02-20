/*------------------------------------------------------------------------------------------------------*/
/* 
"inclusion_verif.c"
This is the sourse file, containing the code for the eigensystem inclusion verification algorithm.
The algorithm is:

k = find_zeta_k(v)
R = A - lambdaI
R(:,k) = -v;
R = inv(R);
[C] = [A] - [lambda][I]
[Z] = -R*([C]*v)
[C(:,k)] = -xs
[C] = [I] - R*[C]
[Y]=[Z]

[Eps] = [eps]*[I]

iterations = 0;
while not ready
	[X] = [Y] + [Eps]
	[XX] = X
	[XX(v,:)] = 0
	[Y] = [Z] + [C]*[X] + [R]*( [XX] * [X(v,:)])
	ready = Y in X
	iterations++
	if iterations > 15
		return false
end
return true


ATTENTION: This algorithm is under reconstruction for a moment!!!

*/
/*-----------------------------------------------------------------------------------------------------*/



#include "inclusion_verif.h"

void context_input_data_init(context_input_data *context_id, complexdouble *A, complexdouble *v, complexdouble lambda, uint64_t n,mpfr_prec_t prec)
{
	context_id->n = n;
	context_id->k = 0;
	context_id->A = A;
 	context_id->v = v;
 	context_id->lambda = lambda;
 	context_id->reA = allocateMPFIMatrix( n, n, prec);
	context_id->imA = allocateMPFIMatrix( n, n, prec);
	context_id->rev = allocateMPFIMatrix( 1, n, prec);
	context_id->imv = allocateMPFIMatrix( 1, n, prec);
	mpfi_init2(context_id->reLambda, prec);
	mpfi_init2(context_id->imLambda, prec);
	context_id->reEps = allocateMPFIMatrix( 1, n, prec);
	context_id->imEps = allocateMPFIMatrix( 1, n, prec);

}

void context_input_data_clear(context_input_data *context_id)
{

	freeMPFIMatrix(context_id->reA, context_id->n, context_id->n);
	freeMPFIMatrix(context_id->imA, context_id->n, context_id->n);
	freeMPFIMatrix(context_id->rev, 1, context_id->n);
	freeMPFIMatrix(context_id->imv, 1, context_id->n);
	freeMPFIMatrix(context_id->reEps, 1, context_id->n);
	freeMPFIMatrix(context_id->imEps, 1, context_id->n);

	mpfi_clear(context_id->reLambda);
	mpfi_clear(context_id->imLambda);


}


void context_algo_data_init(context_algo_data *context, uint64_t n, mpfr_prec_t prec)
{
	context->n = n;
	context->prec = prec;

	context->R = (complexdouble*)malloc(n*n*sizeof(complexdouble*));
	
	context->reR = allocateMPFRMatrix( n, n, prec);
	context->imR = allocateMPFRMatrix( n ,n , prec);

	context->reRint = allocateMPFIMatrix( n, n, prec);
	context->imRint = allocateMPFIMatrix( n ,n, prec);

	context->reZ = allocateMPFIMatrix( 1, n, prec);
	context->imZ = allocateMPFIMatrix( 1, n, prec);

	context->reC = allocateMPFIMatrix( n, n, prec);
	context->imC = allocateMPFIMatrix( n, n, prec);

	context->reC1 = allocateMPFIMatrix( n, n, prec);
	context->imC1 = allocateMPFIMatrix( n, n, prec);

	


}

void context_algo_data_clear(context_algo_data *context_id)
{
	free(context_id->R);
	freeMPFRMatrix(context_id->reR,context_id->n, context_id->n);
	freeMPFRMatrix(context_id->imR,context_id->n, context_id->n);
	
	freeMPFIMatrix(context_id->reRint, context_id->n, context_id->n);
	freeMPFIMatrix(context_id->imRint, context_id->n, context_id->n);

	freeMPFIMatrix(context_id->reC, context_id->n, context_id->n);
	freeMPFIMatrix(context_id->imC, context_id->n, context_id->n);

	freeMPFIMatrix(context_id->reC1, context_id->n, context_id->n);
	freeMPFIMatrix(context_id->imC1, context_id->n, context_id->n);

	freeMPFIMatrix(context_id->reZ, 1, context_id->n);
	freeMPFIMatrix(context_id->imZ, 1, context_id->n);

	


}

/*Function find_zeta_k returns index of the largest in its absolute value elemnt of the inout 
complexdouble vector v.
 */
int find_zeta_k(complexdouble *v, int n )
{
	double index = 0;
	doublereal max = abs_complexdouble(&v[0]);
	doublereal cur;
	int i;
	for(i = 0; i < n; ++i)
	{
		cur = abs_complexdouble(&v[i]);
		if(max <= cur)
		{
			max = cur;
			index = i;
		}
	}
	return index;
}



//------------------------------------------------------------------------------------------//
//------------------------------ New eigensystem algorithm------------------------------//
//------------------------------------------------------------------------------------------//

/*

k = find_zeta_k(v)

R = A - lambdaI
R(:,k) = -v;
R = inv(R);
[C] = [A] - [lambda][I]
[Z] = -R*([C]*v)
[C(:,k)] = -v
[C] = [I] - R*[C]
[Y]=[Z]

[Eps] = [eps]*[I]

while not ready
	[X] = [Y] + [Eps]
	[XX] = [X]
	[XX(v,:)] = 0
	[Y] = [Z] + [C]*[X] + [R]*( [XX] * [X(v,:)])
	ready = Y in X
end

*/

void compute_R(context_algo_data *algo, context_input_data *input)
{
	complexdouble *R;
	R = (complexdouble*)malloc((input->n)*(input->n)*sizeof(complexdouble*));

	complexdouble *lambdaI;
	lambdaI = (complexdouble*)malloc(input->n * input->n * sizeof(complexdouble));
	clapack_matrix_diagonal(lambdaI, input->lambda, input->n);				//lambdaI = lambda * I

	printf("Vector v \n");
	clapack_matrix_print_z(input->v, input->n, 1);

	printf("Lambda = %f + %f \n", input->lambda.r, input->lambda.i);

	clapack_matrix_sub(R, input->A, lambdaI, input->n, input->n);					//R = A - lambda * I

	int i;
	for(i = 0; i < input->n; ++i)
	{
		R[i * input->n + input->k].r = input->v[i].r;			//R(:,k) = -v
		R[i * input->n + input->k].i = -input->v[i].i;
	}


//
	mpfi_t *reR, *imR;
	reR = allocateMPFIMatrix(input->n, input->n, algo->prec);
	imR = allocateMPFIMatrix(input->n, input->n, algo->prec);
	complexdoubleToMPFIMatrix(reR, imR, R, input->n, input->n);
//

	// complexdouble *Rinv;
	// Rinv = (complexdouble*)malloc((input->n)*(input->n)*sizeof(complexdouble*));

	clapack_complex_matrix_inverse(algo->R, R, input->n);

	complexdoubleToMPFIMatrix(algo->reRint, algo->imRint, algo->R, input->n, input->n);

	printf("Matrix R : \n");
    clapack_matrix_print_z(algo->R, input->n, input->n);



	// /* Testing inversion */
	
	mpfi_t *reT, *imT;
	reT = allocateMPFIMatrix(input->n, input->n, algo->prec);
	imT = allocateMPFIMatrix(input->n, input->n, algo->prec);
 	mpfi_t *scratch2;

    scratch2 = allocateMPFIMatrix(2, 1, algo->prec);

    

	MPFIComplexMatrixMultiply(reT, imT, algo->reRint, algo->imRint,reR, imR,  input->n, input->n, input->n, scratch2);
	printf("\n \n TESTING INVERSION: \n");
	MPFIComplexMatrixPrint(reT, imT, input->n, input->n);

	
	free(R);
	free(lambdaI);
	freeMPFIMatrix(scratch2, 2, 1);
	freeMPFIMatrix(reT, input->n, input->n);
	freeMPFIMatrix(imT, input->n, input->n);
	freeMPFIMatrix(reR, input->n, input->n);
	freeMPFIMatrix(imR, input->n, input->n);
}

/* 
	Computes matrix [C1] = [A] - [lambda]*[I]
 */
void compute_C1(context_algo_data *algo, context_input_data *input)
{
	
	mpfi_t *relambdaI, *imlambdaI;
	relambdaI = allocateMPFIMatrix( input->n, input->n, algo->prec);
	imlambdaI = allocateMPFIMatrix( input->n, input->n, algo->prec);
	MPFIConstructDiagonal(relambdaI, imlambdaI, input->reLambda, input->imLambda, input->n);
	// printf("\n Computing matrix lambdaI\n");
	// MPFIComplexMatrixPrint(relambdaI, imlambdaI, input->n, input->n);

	// printf("\n Matrix A: \n");
	// MPFIComplexMatrixPrint(input->reA, input->imA, input->n, input->n);

	MPFIComplexMatrixSub(algo->reC1, algo->imC1, input->reA, input->imA, relambdaI, imlambdaI, input->n, input->n);
	
	freeMPFIMatrix(relambdaI, input->n, input->n);
	freeMPFIMatrix(imlambdaI, input->n, input->n);


}

/* Computes matrix [Z] = -R * ([C1] * v)
	where Z is of size n x 1 */
void compute_Z(context_algo_data *algo, context_input_data *input)
{
	
	printf(" \n Computing matrix Z\n");
	int n = input->n;


	mpfi_t *reT, *imT;
	reT = allocateMPFIMatrix(n, 1, algo->prec);
	imT = allocateMPFIMatrix(n, 1, algo->prec);

	mpfi_t tmp;
	mpfi_init2(tmp, 164);

	printf("\n C1\n");
	MPFIComplexMatrixPrint(algo->reC1, algo->imC1, input->n, input->n);

	complexdouble t;

	int i,k;
	for(i = 0; i < n; ++i)
	{
		mpfi_set_d(reT[i], 0.0);
		mpfi_set_d(imT[i], 0.0);

		t.i = 0.0;
		t.r = 0.0;

		for(k = 0; k < n; ++k)
		{
			//real part of T_i = reC * v.r - imC * v.i
			t.r = -(input->v[k].r);
			t.i = input->v[k].i;
			 printf("i = %d, k = %d \n",i, k);
			 printf("t.r = %f, t.i = %f \n",t.r, t.i);
		
			mpfi_mul_d(tmp, algo->reC1[i*n+k], t.r);
			mpfi_add(reT[i], reT[i], tmp);
			mpfi_mul_d(tmp, algo->imC1[i*n+k], t.i);
			mpfi_sub(reT[i], reT[i], tmp);

			mpfi_set_d(tmp, 0.0);
			//imag part of T_i = reC * v.i + imC * v.r
			mpfi_mul_d(tmp, algo->reC1[i*n+k], t.i);
			mpfi_add(imT[i], imT[i], tmp);
			mpfi_mul_d(tmp, algo->imC1[i*n+k], t.r);
			mpfi_add(imT[i], imT[i], tmp);

		}
		
	}

	printf("Vector T \n");
	MPFIComplexMatrixPrint(reT, imT, input->n, 1);

	for(i = 0; i < n; ++i)
	{
		mpfi_set_d(algo->reZ[i], 0.0);
		mpfi_set_d(algo->imZ[i], 0.0);

		t.i = 0.0;
		t.r = 0.0;

		for(k = 0; k < n; ++k)
		{
			//real part of Z_i = reR * reT - imR * imT
			t.r = algo->R[i * n + k].r;
			t.i = algo->R[i * n + k].i;
			// printf("i = %d, k = %d \n",i, k);
			// printf("t.r = %f, t.i = %f \n",t.r, t.i);


			mpfi_mul_d(tmp, reT[i], t.r);
			mpfi_add(algo->reZ[i], algo->reZ[i], tmp);

			mpfi_mul_d(tmp, imT[i] ,t.i);
			mpfi_sub(algo->reZ[i], algo->reZ[i], tmp);

			mpfi_set_d(tmp, 0.0);
			//imag part of T_i = reR * imT + imR * reT
			mpfi_mul_d(tmp, imT[i], t.r);
			mpfi_add(algo->imZ[i], algo->imZ[i], tmp);
			mpfi_mul_d(tmp, reT[i], t.i);
			mpfi_add(algo->imZ[i], algo->imZ[i], tmp);

		}

		mpfi_neg(algo->reZ[i], algo->reZ[i]);
		mpfi_neg(algo->imZ[i], algo->imZ[i]);


	}
	printf("Vector Z = R*[T] \n");
	MPFIComplexMatrixPrint(algo->reZ, algo->imZ, input->n, 1);

	freeMPFIMatrix(reT, n, 1);
	freeMPFIMatrix(imT, n, 1);
	mpfi_clear(tmp);



}

/* Computes matrix [C]:

	[Ctmp] = [C1]
	[Ctmp(:,k)] = [-v]
	[C] = [I] - R*[Ctmp]

	where C is of size n x n */
void compute_C(context_algo_data *algo, context_input_data *input)
{
	int n = input->n;

	//Computing 	[Ctmp] = [C1]
	//				[Ctmp(:,k)] = [-v]

	mpfi_t *reCtmp, *imCtmp;
	reCtmp = allocateMPFIMatrix( n, n, algo->prec);
	imCtmp = allocateMPFIMatrix( n, n, algo->prec);

	

	int i,j;
	for(i = 0; i < n; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			if(j == input->k)
			{
				mpfi_set(reCtmp[i * n + input->k], input->rev[i]);
				 // mpfi_neg(reCtmp[i * n + input->k], reCtmp[i * n + input->k]);

				mpfi_set(imCtmp[i * n + input->k], input->imv[i]);
				mpfi_neg(imCtmp[i * n + input->k], imCtmp[i * n + input->k]);

			}
			else
			{
				mpfi_set(reCtmp[i * n + j], algo->reC1[i * n + j]);
				mpfi_set(imCtmp[i * n + j], algo->imC1[i * n + j]);
			}

		}
	}

	printf("\n Matrix Ctmp: \n");
	MPFIComplexMatrixPrint(reCtmp, imCtmp,input->n, input->n);

	//Computing [C] = - R*[Ctmp] + [I]


	mpfi_t *reT, *imT, *scratch2;
	reT = allocateMPFIMatrix( n, n, algo->prec);
	imT = allocateMPFIMatrix( n, n, algo->prec);
	scratch2 = allocateMPFIMatrix(2, 1, algo->prec);

	MPFIComplexMatrixMultiply(reT, imT, algo->reRint, algo->imRint,reCtmp, imCtmp, n, n, n, scratch2);

	// printf("\n Matrix R: \n");
	// MPFIComplexMatrixPrint(algo->reRint, algo->imRint,input->n, input->n);
	// printf("\n Matrix R*Ctmp: \n");
	// MPFIComplexMatrixPrint(reT, imT, input->n, input->n);


	mpfi_t *Identity;
	Identity = allocateMPFIMatrix(n, n, algo->prec);
	MPFIIdentMatrix(Identity, n);

	mpfi_t *Zero;
	Zero = allocateMPFIMatrix(n, n, algo->prec);
	MPFIZeroMatrix(Zero, n, n);

	MPFIComplexMatrixSub(algo->reC, algo->imC, Identity, Zero, reCtmp, imCtmp, n, n);
	// printf("\n Matrix I*Ctmp: \n");
	// MPFIComplexMatrixPrint(reT, imT, input->n, input->n);

	MPFIComplexMatrixSub(algo->reC, algo->imC, Identity, Zero, reT, imT, n, n);


	freeMPFIMatrix(reCtmp, n, n);
	freeMPFIMatrix(imCtmp, n, n);
	freeMPFIMatrix(reT, n, n);
	freeMPFIMatrix(imT, n, n);
	freeMPFIMatrix(Identity, n, n);
	freeMPFIMatrix(Zero, n, n);
	freeMPFIMatrix(scratch2, 2, 1);


	printf("\n Matrix C: \n");
	MPFIComplexMatrixPrint(algo->reC, algo->imC,input->n, input->n);

}


int checkEigensystemInclusion(mpfi_t *rev_corrected, mpfi_t *imv_corrected, mpfi_t relambda_corrected, mpfi_t imlambda_corrected, \
								complexdouble *A, complexdouble *v, complexdouble lambda, uint64_t n, double eps_v, double eps_lambda, mpfr_prec_t prec)
{
	

	// computing k - index of the largest in its absolute value elemnt of the input complexdouble vector v.
	printf("Checking eigeninclsion \n");
	context_input_data input;
	// input = (context_input_data*) malloc(sizeof(context_input_data*));
	context_algo_data algo;
	// algo = (context_algo_data*)malloc(sizeof(context_algo_data*));

	context_input_data_init(&input, A, v,  lambda,  n, prec);
	context_algo_data_init(&algo, n, prec);

	input.k = find_zeta_k(v, n);
	printf("k = %llu \n", input.k);

	complexdoubleToMPFIMatrix(input.reA, input.imA, A, n, n);
	complexdoubleToMPFIMatrix(input.rev, input.imv, v, 1, n);

	mpfi_set_d(input.reLambda, lambda.r);
	mpfi_set_d(input.imLambda, lambda.i);

	// Computing vector Eps. 
	// On the output Eps[i] will contain the radius of i-th eigenvector, except for k-th element. 
	// Eps[k] will contain the radius of lambda.
	int i,j;
	for(i = 0; i < n; ++i)
	{
		mpfi_set_d(input.reEps[i], eps_v);
		mpfi_set_d(input.imEps[i], eps_v);
	}
	mpfi_set_d(input.reEps[input.k], eps_lambda);
	mpfi_set_d(input.reEps[input.k], eps_lambda);

	// Computing matrix R
	compute_R(&algo, &input);



	//Computing matrix [C1]
	compute_C1(&algo, &input);

	//Computing matrix [C]
	compute_C(&algo, &input);

	//Computing matrix [Z]
	compute_Z(&algo, &input);

	//Setting matrix [Y] = [Z]
	mpfi_t *reY, *imY;
	reY = allocateMPFIMatrix( 1, n, prec);
	imY = allocateMPFIMatrix( 1, n, prec);
	for(i = 0; i < n; ++i)
	{
		mpfi_set(reY[i], algo.reZ[i]);
		mpfi_set(imY[i], algo.imZ[i]);
	}

	//Preparing matrix X and XX
	mpfi_t *reXX, *imXX;
	reXX = allocateMPFIMatrix( 1, n, prec);
	imXX = allocateMPFIMatrix( 1, n, prec);

	mpfi_t *reX, *imX;
	reX = allocateMPFIMatrix( 1, n, prec);
	imX = allocateMPFIMatrix( 1, n, prec);

	int ready = 0;
	int iterations = 0;


	printf("Checking eigeninclsion/ before while \n");
	while(!ready && iterations < 1 )
	{	
		iterations++;
		//we prepare [X] = [Y] + [Eps] and [XX] = [X];
		for(i = 0; i < n; ++i)
		{
			
			mpfi_add(reX[i], reY[i], input.reEps[i]);
			mpfi_set(reXX[i], reX[i]);

			 
			mpfi_add(imX[i], imY[i],input.imEps[i]);
			mpfi_set(imXX[i], imX[i]);

		}
		//Set [XX(k,:) = 0]
		mpfi_set_ui(reXX[input.k], 0);
		mpfi_set_ui(imXX[input.k], 0);

		printf("Matrix X:\n");
		MPFIComplexMatrixPrint(reX, imX, input.n, 1);
		printf("Matrix XX:\n");
		MPFIComplexMatrixPrint(reXX, imXX, input.n, 1);
	
		mpfi_t *scratch2;
		scratch2 = allocateMPFIMatrix(2, 1, prec);

		mpfi_t scratch1;
		mpfi_init2(scratch1, prec);

		//temporary matrices
		mpfi_t *reT1, *imT1, *reT2, *imT2, *reT3, *imT3;
		reT1 = allocateMPFIMatrix(n, 1, prec);
		reT2 = allocateMPFIMatrix(n, 1, prec);
		reT3 = allocateMPFIMatrix(n, 1, prec);
		imT1 = allocateMPFIMatrix(n, 1, prec);
		imT2 = allocateMPFIMatrix(n, 1, prec);
		imT3 = allocateMPFIMatrix(n, 1, prec);

		//Computing [Y] = [Z] + [C]*[X] + [R]*([XX]*[X(k)])

		// [T1] = [XX]*[X(k)]
		for(i = 0; i < n; ++i)
		{
			mpfi_mul_complex(reT1[i], imT1[i], reXX[i], imXX[i], reX[input.k], imX[input.k], scratch1);
		}

		//[T2] = [R] * [T1]
		MPFIComplexMatrixMultiply(reT2, imT2, algo.reRint, algo.imRint, reT1, imT1, n, n, 1, scratch2);

		//[T3] = [C] * [X]
		MPFIComplexMatrixMultiply(reT3, imT3, algo.reC, algo.imC, reX, imX, n, n, 1, scratch2);

		ready = 1;
		for(i = 0; i < n; ++i)
		{
			mpfi_set(reY[i], algo.reZ[i]);
			mpfi_set(imY[i], algo.imZ[i]);

			mpfi_add(reY[i], reY[i],reT3[i]);
			mpfi_add(imY[i], imY[i], imT3[i]);

			mpfi_add(reY[i],reY[i], reT2[i]);
			mpfi_add(imY[i],imY[i], imT2[i]);

			// mpfi_is_inside
			
			int reYinX = mpfi_is_inside(reY[i], reX[i]);
			int imYinX = mpfi_is_inside(imY[i], imX[i]);

			printf("\n reY:\n");
			mpfi_out_str(stderr, 10, 10, reY[i]);
			printf("\n reX:\n");
			mpfi_out_str(stderr, 10, 10, reX[i]);

			printf("reYinX = %d, imYinX = %d \n", reYinX, imYinX );


			if( reYinX == 0 || imYinX == 0)
			{
				ready = 0;
			}
		}

		if(!ready)	//if not ready, extend interval
		{
			for(i = 0; i < n; ++i)
			{
				mpfi_mul_ui(input.reEps[i],input.reEps[i], 10);
				mpfi_mul_ui(input.imEps[i],input.imEps[i], 10);
			}
		}
		else 		//if ready, construct output intervals for lambda and v
		{
			
			for(i = 0; i < n; ++i)
			{
				if(i == input.k)
				{
					mpfi_add_d(relambda_corrected, reY[i], lambda.r);
					mpfi_add_d(imlambda_corrected, imY[i], lambda.i);

					mpfi_set_d(rev_corrected[i], v[i].r);
					mpfi_set_d(imv_corrected[i], v[i].i);
				}
				else
				{
					mpfi_add_d(rev_corrected[i], reY[i], v[i].r);
					mpfi_add_d(imv_corrected[i], imY[i], v[i].i);
				}
				
			}
			
		}

	}
	context_algo_data_clear(&algo);
	context_input_data_clear(&input);
	


	// If we exited and still not ready, then return false
	if(!ready)
		return 0;
	else
		return 1;

}



/*---------------------------New eigenvalue incluion algorithm end ------------------------------------*/


// /* Eigensystem verification algorithm */




// void buildMatrixR(mpfr_t *reR, mpfr_t *imR, complexdouble *A, complexdouble lambda, complexdouble *v, uint64_t n, int k)
// {
// 	/* Preapring R = [A - eye(n)*lambda, -v; e, 0], where R is _floating-point_ ; */

// 	complexdouble *R;
// 	R = (complexdouble*)malloc((n+1)*(n+1)*sizeof(complexdouble*));

// 	complexdouble *lambdaI;
// 	lambdaI = (complexdouble*)malloc(n * n * sizeof(complexdouble));
// 	clapack_matrix_diagonal(lambdaI, lambda, n);				//lambdaI = lambda * I

// 	printf("Vector v \n");
// 	clapack_matrix_print_z(v, 1, n);

// 	printf("Matrix lambdaI\n");
// 	clapack_matrix_print_z(lambdaI, n, n);

// 	complexdouble *AlambdaI;
// 	AlambdaI =  (complexdouble*)malloc(n*n*sizeof(complexdouble));
// 	clapack_matrix_sub(AlambdaI, A, lambdaI, n, n);					//AlambdaI = A - lambda * I

// 	printf("Matrix A - lambdaI\n");
// 	clapack_matrix_print_z(AlambdaI, n, n);

// 	int i,j;
// 	for(i = 0; i < n+1; ++i)
// 	{
// 		if(i == n)
// 		{
// 			for (j = 0; j < n+1; ++j)		//if it is the last row, we fill it with zeroes,
// 			{
// 				R[n * (n+1) + j].r = 0.0;
// 				R[n * (n+1) + j].i = 0.0;
// 			}

// 		}
// 		else
// 		{
// 			for(j = 0; j < n+1; ++j)
// 			{
// 				if(j == n)		//if is the last column (and already not las row), we fill it with -v
// 				{
// 					R[i * (n+1) + n].r = -v[i].r;
// 					R[i * (n+1) + n].i = -v[i].i;
// 				}
// 				else
// 				{
// 					R[i * (n+1) + j].r = AlambdaI[i * n + j].r;
// 					R[i * (n+1) + j].i = AlambdaI[i * n + j].i;
// 				}
				
// 			}
// 		}
// 	}
// 	R[n * (n+1) + k].r = 1.0;		//and we set the element R_nk to 1. 
// 	R[n * (n+1) + k].i = 0.0;

	

// 	/* Computing R = inv(R) */

// 	complexdouble *inv = (complexdouble*)malloc((n+1)*(n+1)*sizeof(complexdouble*));
// 	complexdouble *invR_clapack;
// 	invR_clapack = (complexdouble*)malloc((n+1)*(n+1)*sizeof(complexdouble*));
// 	//printf("Inverting matrix with my iterative method \n");
// 	inverseMatrix(invR_clapack, R, n+1);
// 	//printf("inv(R):\n");
// 	clapack_matrix_print_z(invR_clapack, n+1, n+1);
// 	complexdoubleToMPFRMatrix(reR, imR, invR_clapack, n+1, n+1);




// 	// complexdouble *invR_clapack;
// 	// invR_clapack = (complexdouble*)malloc((n+1)*(n+1)*sizeof(complexdouble*));
// 	// clapack_complex_matrix_inverse(invR_clapack, R, n + 1);
// 	// complexdoubleToMPFRMatrix(reR, imR, invR_clapack, n+1, n+1);

// }


// void buildMatrixC(eigenInclusion_context *context,mpfr_t *reR, mpfr_t *imR, uint64_t n, int k)
// // void buildMatrixC(mpfi_t *reC, mpfi_t *imC, mpfr_t *reR, mpfr_t *imR, mpfi_t *reA, mpfi_t *imA, mpfi_t reLambda, mpfi_t imLambda, mpfi_t *rev, mpfi_t *imv, uint64_t n, int k);
// {
// 	/* Preapring C1 = [A - lambda*I, -v; e, 0], where C is interval complex ; */

// 	mpfr_prec_t prec = 106;

// 	mpfi_t *scratch2;
// 	scratch2 = allocateMPFIMatrix(1, 3, prec);

// 	mpfi_t *reC1, *imC1;
// 	reC1 = allocateMPFIMatrix( n+1, n+1, prec);
// 	imC1 = allocateMPFIMatrix( n+1, n+1, prec);
// //printf("CHecking inclusion 1\n");

// 	mpfi_t *reLambdaI, *imLambdaI;
// 	reLambdaI = allocateMPFIMatrix( n, n, prec);
// 	imLambdaI = allocateMPFIMatrix( n, n, prec);
// 	MPFIConstructDiagonal(reLambdaI, imLambdaI, context->reLambda, context->imLambda, n);		//lambdaI = lambda * I

// 	mpfi_t *reAlambdaI, *imAlambdaI;
// 	reAlambdaI = allocateMPFIMatrix( n, n, prec);
// 	imAlambdaI = allocateMPFIMatrix( n, n, prec);
// 	MPFIComplexMatrixSub(reAlambdaI, imAlambdaI, context->reA, context->imA, reLambdaI, imLambdaI, n, n); //AlambdaI = A - lambda * I

// //printf("CHecking inclusion 2\n");
// 	int i,j;
// 	for(i = 0; i < n+1; ++i)
// 	{
// 		if(i == n)
// 		{
// 			for (j = 0; j < n+1; ++j)		//if it is the last row, we fill it with zeroes,
// 			{
// 				mpfi_set_d(reC1[n * (n+1) + j],0.0);
// 				mpfi_set_d(imC1[n * (n+1) + j],0.0);
// 			}

// 		}
// 		else
// 		{
// 			for(j = 0; j < n+1; ++j)
// 			{
// 				if(j == n)		//if is the last column (and already not las row), we fill it with -v
// 				{
// 					mpfi_set(reC1[i * (n+1) + n],context->imv[i]);
// 					mpfi_neg(reC1[i * (n+1) + n], reC1[i * (n+1) + n]);
// 					mpfi_set(imC1[i * (n+1) + n],context->rev[i]);
// 					mpfi_neg(imC1[i * (n+1) + n], imC1[i * (n+1) + n]);
// 				}
// 				else
// 				{
// 					mpfi_set(reC1[i * (n+1) + j],reAlambdaI[i * n + j]);
// 					mpfi_set(imC1[i * (n+1) + j],imAlambdaI[i * n + j]);
// 				}
				
// 			}
// 		}
// 	}
// 	mpfi_set_d(reC1[n * (n+1) + k],1.0);			//and we set the element C_nk to 1. 
// 	mpfi_set_d(imC1[n * (n+1) + k],0.0);

// 	/* [C] = [I] - R*[C1] */

// 	// MPFIComplexMatrixMultiplyMPFRComplexMatrix
// 	//printf("CHecking inclusion 3\n");
// 	MPFIComplexMatrixMultiplyMPFRComplexMatrix(context->reC, context->imC, reR, imR, reC1, imC1, n+1, n+1,n+1, scratch2);
// 	//printf("CHecking inclusion 3.5\n");
// 	for(i = 0; i < n +1; ++i)
// 	{
// 		for(j = 0; j < n+1; ++j)
// 		{
// 			mpfi_neg(context->reC[i * (n+1) + j], context->reC[i * (n+1) + j]);
// 			mpfi_neg(context->imC[i * (n+1) + j], context->imC[i * (n+1) + j]);
// 		}
// 		mpfi_add_ui(context->reC[i * (n+1) + i], context->reC[i * (n+1) + i], 1);
// 		mpfi_add_ui(context->imC[i * (n+1) + i], context->imC[i * (n+1) + i], 1);
// 	}

// //printf("CHecking inclusion 4\n");

// }

// /* Building matrix S = [ [A]*[v] - [lambda]*[v]; v(k) - abs(v(k)) ] of size (n+1) x 1 */
// void buildMatrixS(mpfi_t *reS, mpfi_t *imS, eigenInclusion_context *context, uint64_t n, int k, double zeta)
// {
	
// 	mpfr_prec_t prec = 106;
// 	mpfi_t *scratch2;
// 	scratch2 = allocateMPFIMatrix(1, 2, prec);

// 	mpfi_t *reAv, *imAv;
// 	reAv = allocateMPFIMatrix(n, 1, prec);
// 	imAv = allocateMPFIMatrix(n, 1, prec);
// 	MPFIComplexMatrixMultiply(reAv, imAv, context->reA, context->imA, context->rev, context->imv, n, n, 1, scratch2);		//[A] * [v]

// 	mpfi_t *reLambdav, *imLambdav;
// 	reLambdav = allocateMPFIMatrix(n, 1, prec);
// 	imLambdav = allocateMPFIMatrix(n, 1, prec);
// 	ComplexScalarMultiplyMPFIMatrix(reLambdav, imLambdav, context->reLambda, context->imLambda, context->rev, context->imv, 1, n, scratch2[0]);

// 	int i;
// 	for(i = 0; i < n; ++i)
// 	{
// 		mpfi_sub(reS[i], reAv[i], reLambdav[i]);
// 		mpfi_sub(imS[i], imAv[i], imLambdav[i]);
// 	}

// 	//printf("Building matrix S, element v(k) - abs(v(k)) = v(k) - zeta = v(k) - %f:\n", zeta);
// 	mpfi_sub_d(reS[n], context->rev[k], zeta);
// 	mpfi_set(imS[n], context->imv[k]);


// 	// MPFIComplexMatrixPrint( reS, imS, 1, n+1);


// }

// void buildMatrixZ(eigenInclusion_context *context, uint64_t n, int k_zeta, double zeta)
// {
// 	mpfr_prec_t prec = 106;
// 	mpfi_t *reS, *imS;
// 	reS = allocateMPFIMatrix(1, n+1, prec);
// 	imS = allocateMPFIMatrix(1, n+1, prec);
// 	//printf("\t ----------Building matrix S\n");
// 	buildMatrixS(reS, imS, context, n, k_zeta, zeta);
// 	// MPFIComplexMatrixPrint( reS, imS, 1, n+1);

// 	// [Z] = [v, lambda] - [R] * [S]
// 	// Or we can rewrite element-by-element:
// 	// [Z_i] = [v_i] - sum_k=0^(n+1) R_i,k * S_k
// 	// [Z_n+1] = [lambda] - sum_k=0^(n+1) R_(n+1),k * S_k
	
// 	int i,k;
// 	mpfi_t scratch;
// 	mpfi_init2(scratch, prec);


// 	mpfi_t req, imq;
// 	mpfi_init2(req, prec);
// 	mpfi_init2(imq, prec);

// 	for(i = 0; i < n + 1; ++i)
// 	{
// 		if( i != n)
// 		{
// 			mpfi_set(context->reZ[i], context->rev[i]);
// 			mpfi_set(context->imZ[i], context->imv[i]);
// 		}
// 		else
// 		{
// 			mpfi_set(context->reZ[i], context->reLambda);
// 			mpfi_set(context->imZ[i], context->imLambda);
// 		}
		
// 		for(k = 0; k < n + 1; ++k)
// 		{
// 			mpfi_mul_complex(req, imq, context->reR[i * (n +1) + k], context->imR[i * (n +1) + k], reS[k], imS[k], scratch);
// 			mpfi_sub(context->reZ[i], context->reZ[i], req);
// 			mpfi_sub(context->imZ[i], context->imZ[i], imq);
			
// 		}
// 	}
// 	freeMPFIMatrix(reS, 1, n + 1);
// 	freeMPFIMatrix(imS, 1, n + 1);
// }

// /* scratch space at least of size 5 */
// void buildMatrixX(eigenInclusion_context *context, uint64_t n, mpfi_t *scratch)
// {
// 	int i,k;
// 	for(i = 0; i < n+1; ++i)
// 	{
// 		for(k = 0; k < n+1; ++k)
// 		{	

// 			if( i != n)
// 			{
// 				mpfi_sub(scratch[0], context->reY[k], context->rev[k]);
// 				mpfi_sub(scratch[1], context->imY[k], context->imv[k]);		//Q:= scratch[0] = [Y] - [v, lambda]
// 			}
// 			else
// 			{
// 				mpfi_sub(scratch[0], context->reY[n], context->reLambda);
// 				mpfi_sub(scratch[1], context->imY[n], context->imLambda);	

// 			}
// 			mpfi_mul_complex(scratch[3],scratch[4],context->reC[i * (n+1) + k],context->imC[i * (n+1) + k], scratch[0], scratch[1], scratch[2]) ;	//scratch[3] = C_ik * Q_k
// 			mpfi_add(context->reX[i],context->reX[i], scratch[3]);		// reX_i += sum_k C_ik * Q_k
// 			mpfi_add(context->imX[i],context->imX[i], scratch[4]);		// imX_i += sum_k C_ik * Q_k
// 		}
// 	}
// }

// int XinY(eigenInclusion_context *context, uint64_t n)
// {
// 	int i, j;
// 	for(i = 0; i < n + 1; ++i)
// 	{
// 		for(j = 0; j < n+1; ++j)
// 		{
// 			if(!mpfi_is_inside(context->reX[i * (n+1) + j], context->reY[i * (n+1) + j]) && !mpfi_is_inside(context->imX[i * (n+1) + j], context->imY[i * (n+1) + j]))
// 				return 0;
// 		}
// 	}

// 	return 1;

// }


// int checkEigensystemInclusion2(complexdouble *A, complexdouble lambda, complexdouble *v, mpfr_t eps, uint64_t n)
// {
// 	//printf("Started eigensystem inclusion verification \n");
// 	//printf("Checking inclusion for eigenvalue lambda = %f + i* %f and vector v: \n", lambda.r, lambda.i);
// 	clapack_matrix_print_z(v, 1, n);

// 	mpfr_prec_t prec = 106;

// 	mpfr_t *scratch5;
// 	scratch5 = allocateMPFRMatrix(1, 5, prec);

// 	mpfi_t *scratch5intval;
// 	scratch5intval = allocateMPFIMatrix(1, 5, prec);

// 	eigenInclusion_context context;
// 	eigenInclusion_context_init(&context, n, prec);


// 	/* Converting input data to interval */
// 	complexdoubleToMPFIMatrix(context.reA, context.imA, A, n, n);
// 	complexdoubleToMPFIMatrix(context.rev, context.imv, v, 1, n);
// 	mpfi_set_d(context.reLambda, lambda.r);
// 	mpfi_set_d(context.imLambda, lambda.i);


// 	/* Preparing [zeta, k] = max(abs(v)); */
// 	int k = find_zeta_k(v, n);
// 	double zeta = abs_complexdouble(&v[k]);
// 	//printf("\n Zeta and k: %f, %d\n", zeta, k );
// 	//printf("Max re(v) is : %f + i * %f \n", v[k].r, v[k].i);
	


// 	mpfr_t *reR, *imR;
// 	reR = allocateMPFRMatrix(n+1, n+1, prec);
// 	imR = allocateMPFRMatrix(n+1, n+1, prec);
// 	printf("\n------------------------Building matrix R \n");
// 	buildMatrixR_new(reR, imR, A, lambda, v, n, k);		//R = [A - eye(n)*lambda, -v; e, 0], where R is _floating-point_ (n+1)x(n+1) matrix ;
// 	MPFRMatrixToMPFIMatrix(context.reR, context.imR, reR, imR, n+1, n+1);

// 	MPFRComplexMatrixPrint( reR, imR, n+1, n+1);
	

// 	//printf("\n ---------------------Building matrix Z \n");
// 	buildMatrixZ(&context, n, k, zeta);
// 	// MPFIComplexMatrixPrint(context.reZ, context.imZ, 1, n+1);

// 	//printf("\n------------------------Building matrix C \n");
// 	buildMatrixC(&context,reR, imR, n, k);
// 	// MPFIComplexMatrixPrint( context.reC, context.imC, n + 1, n+1);

// 	//printf("\n-------------------------Building matrix X: \n");
// 	MPFIMatrixCopy(context.reX, context.reZ, 1, n+1);
// 	MPFIMatrixCopy(context.imX, context.imZ, 1, n+1);		// [X] = [Z]
// 	// MPFIComplexMatrixPrint( context.reZ, context.imZ, 1, n+1);


// 	//printf("Before while \n");

// 	int flag = 0;
// 	int iter = 1;
// 	while(1 == 1 && iter < 2 )
// 	{

// 		MPFIComplexMatrixMidrad(context.reY, context.imY, context.reX, context.imX, 1, n+1, eps, scratch5);		// [Y] = midrad([X], eps)

// 		//printf("\n Iteration %d, matrix Y: \n", iter);
// 		// MPFIComplexMatrixPrint( context.reY, context.imY, 1, n+1);
// 		buildMatrixX(&context, n, scratch5intval);
// 		//printf("\n Iteration %d, matrix X: \n", iter);
// 		// MPFIComplexMatrixPrint( context.reX, context.imX, 1, n+1);

// 		// if(!XinY(&context,  n))		// if [X] is not in [Y]
// 		// {
// 		// 	mpfr_mul_ui(eps, eps, 10, MPFR_RNDN);
// 		// 	// if eps > 1 or if eigenvalue contains 1, we return negative answer
// 		// 	mpfi_abs_complex(scratch5intval[0], context.reX[n+1], context.imX[n+1], scratch5intval[1]);
// 		// 	if((mpfr_cmp_ui(eps, 1) > 0) || (mpfi_is_inside_ui(1, scratch5intval[0])) > 0)		
// 		// 		return 0;

// 		// }
// 		// else
// 		// {
// 		// 	return 1;
// 		// }
// 		iter++;

// 	}

// 	return 1;

// }






// int checkEigensystemInclusion(complexdouble *A, complexdouble lambda, complexdouble *v, double eps, int n, mpfr_prec_t prec)
// {
  
	
// // 	// //printf("Started eigensystem inclusion verification \n");
// // 	/* Preparing [zeta, k] = max(abs(v)); */
	
// // 	complexdouble *zeta = (complexdouble*)malloc(sizeof(complexdouble));
// // 	int k = find_zeta_k(zeta, v, n);
	
// // 	/* Creating e = zeros(1, n); e(k) = 1; */
	
// // 	complexdouble *e = (complexdouble*)malloc((n+1)*sizeof(complexdouble));
// // 	int i;
// // 	for(i = 0; i < n+1; ++i)
// // 	{
// // 		e[i].r = (doublereal)0.0;
// // 		e[i].i = (doublereal)0.0;
// // 	}
// // 	e[k].r = (doublereal)1.0;
// // 	e[k].i = (doublereal)0.0;
	
// // 	/* Preapring R = [A - eye(n)*lambda, -v; e, 0]; */

// // 	complexdouble *eye_lambda = (complexdouble*)malloc(n*n*sizeof(complexdouble));
// // 	clapack_matrix_diagonal(eye_lambda, lambda, n);
	
// // 	complexdouble *R1 = (complexdouble*)malloc(n*n*sizeof(complexdouble));		//R1 = A - eye(n)*lambda
// // 	clapack_matrix_sub(R1, A, eye_lambda, n, n);
	
// // 	clapack_matrix_neg(v, n, 1);				//-v
	
// // 	complexdouble *R2 = (complexdouble*)malloc(n*(n+1)*sizeof(complexdouble));
// // 	clapack_matrix_hor_concat(R2, R1, v, n, n, 1);					//R2 = [A - eye(n)*lambda, -v]
	
// // 	complexdouble *R3 = (complexdouble*)malloc((n+1)*(n+1)*sizeof(complexdouble));
// // 	clapack_matrix_ver_concat(R3, R2, e, n+1, n, 1);					// R3 = [A - eye(n)*lambda, -v; e, 0];
	
// // 	complexdouble *R = (complexdouble*)malloc((n+1)*(n+1)*sizeof(complexdouble));
// // 	clapack_complex_matrix_inverse(R, R3, n+1);								// R = inv(R3);
	
// // // 	////printf("Matrix inv(R): \n");
// // // 	clapack_matrix_print_z(R, n+1, n+1);
  
// // 	clapack_matrix_neg(v, n, 1);	//-(-v) returning v to its original sign
	
// // 	/* Preparing Z = intval(([v;lambda]) - (R)*[(A)*(v)-(lambda*v); (v(k)) - (zeta)]);
// // 	 * note: converting complexdouble to mpfi prior to all operations */
	
// // 	mpfi_cmatrix_t v_int; 
// // 	mpfi_cmatrix_init2(&v_int, n, 1, prec);
// // 	clapack_complexdouble_to_mpfi_cmatrix(&v_int, v, n, 1);
	
// // 	mpfi_cmatrix_t lambda_int;
// // 	mpfi_cmatrix_init2(&lambda_int, 1, 1, prec);
// // 	mpfi_c_set_d(&(lambda_int.arr[0][0]),lambda.r, lambda.i );
	
// // 	mpfi_cmatrix_t vlambda_concat;
// // 	mpfi_cmatrix_init2(&vlambda_concat, n+1, 1, prec);
// // 	mpfi_cmatrix_ver_concat(&vlambda_concat, &v_int, &lambda_int, 1, n, 1);		//intval([v;lambda])
	
// // 	mpfi_cmatrix_t Aint;
// // 	mpfi_cmatrix_init2(&Aint, n, n, prec);
// // 	clapack_complexdouble_to_mpfi_cmatrix(&Aint, A, n, n);
	
// // 	mpfi_cmatrix_t Av_int;
// // 	mpfi_cmatrix_init2(&Av_int, n, 1, prec);
// // 	mpfi_cmatrix_mul(&Av_int, &Aint, &v_int);		//A*v 
	
// // 	mpfi_cmatrix_t vlambda_int;
// // 	mpfi_cmatrix_init2(&vlambda_int, n, 1, prec);
// // 	mpfi_cmatrix_mul(&vlambda_int, &v_int, &lambda_int);		// lambda*v
	
// // 	mpfi_cmatrix_t Z1;
// // 	mpfi_cmatrix_init2(&Z1, n, 1, prec);
// // 	mpfi_cmatrix_sub(&Z1, &Av_int, &vlambda_int);			// Z1 = (A*v)-(lambda*v)
	
// // 	mpfi_tc vk;
// // 	mpfi_c_init2(&vk, prec);
// // 	mpfi_c_set_d(&vk, v[k].r, v[k].i);
	
// // 	mpfi_tc zeta_int;
// // 	mpfi_c_init2(&zeta_int, prec);
// // 	mpfi_c_set_d(&zeta_int, zeta[0].r, zeta[0].i);
	
// // 	mpfi_tc vzeta;
// // 	mpfi_c_init2(&vzeta, prec);
// // 	mpfi_c_sub(&vzeta, &vk, &zeta_int);
	
// // 	mpfi_cmatrix_t vzeta_matrix;
// // 	mpfi_cmatrix_init2(&vzeta_matrix, 1, 1, prec);
// // 	mpfi_c_set(&(vzeta_matrix.arr[0][0]), &vzeta );
	
// // 	mpfi_cmatrix_t Z2;
// // 	mpfi_cmatrix_init2(&Z2, n+1, 1, prec);
// // 	mpfi_cmatrix_ver_concat(&Z2, &Z1, &vzeta_matrix, 1, n, 1);		// Z2 = [(A)*(v)-(lambda*v); (v(k)) - (zeta)]
	
// // 	mpfi_cmatrix_t Rint;
// // 	mpfi_cmatrix_init(&Rint, n+1, n+1);
// // 	clapack_complexdouble_to_mpfi_cmatrix(&Rint, R, n+1, n+1);				//intval(R)
	
// // 	mpfi_cmatrix_t Z3;
// // 	mpfi_cmatrix_init2(&Z3, n+1, 1, prec);
// // 	mpfi_cmatrix_mul(&Z3, &Rint, &Z2);					// Z3 = R*Z2
	
// // 	mpfi_cmatrix_t Z;
// // 	mpfi_cmatrix_init2(&Z, n+1, 1, prec);
// // 	mpfi_cmatrix_sub(&Z, &vlambda_concat, &Z3 );				// Z = intval([v;lambda]) - Z3
	
	
// // // 	//f//printf(output, "\n Matrix Z: \n");
// // // 	mpfi_cmatrix_out_str(output, 10, (size_t) 10, &Z);
	
	
// // 	/*Preapring matrix C = intval([(A) - (eye(n)*lambda), (-v); (e) 0]);
// // 	 * note: convert complexdouble to mpfi prior to all operations
// // 	 * C = eye(n+1) - R*C; */

// // 	 // //printf("pararam \n");
	
// // 	mpfi_cmatrix_t eye_lambda_int;
// // 	mpfi_cmatrix_init2(&eye_lambda_int, n, n, prec);
// // 	clapack_complexdouble_to_mpfi_cmatrix(&eye_lambda_int, eye_lambda, n, n);
	
// // 	mpfi_cmatrix_t C1;
// // 	mpfi_cmatrix_init2(&C1, n, n, prec);
// // 	mpfi_cmatrix_sub(&C1, &Aint, &eye_lambda_int);		// C1 = (A) - (eye(n)*lambda)
	
// // 	mpfi_cmatrix_t v_int_neg;
// // 	mpfi_cmatrix_init2(&v_int_neg, n, 1, prec);
// // 	mpfi_cmatrix_neg(&v_int_neg, &v_int);			//-v
	
// // 	mpfi_cmatrix_t C2;
// // 	mpfi_cmatrix_init2(&C2, n, n+1, prec);
// // 	mpfi_cmatrix_hor_concat(&C2, &C1, &v_int_neg, n, n, 1);	//C2 = [(A) - (eye(n)*lambda), (-v)]
	
// // 	mpfi_cmatrix_t eint;
// // 	mpfi_cmatrix_init2(&eint, 1, n+1, prec);
// // 	clapack_complexdouble_to_mpfi_cmatrix(&eint, e, 1, n+1);
		
// // 	mpfi_cmatrix_t C3;
// // 	mpfi_cmatrix_init2(&C3, n+1, n+1, prec);
// // 	mpfi_cmatrix_ver_concat(&C3, &C2, &eint, n+1, n, 1);		// C3 = intval([(A) - (eye(n)*lambda), (-v); (e) 0]);
	
// // 	mpfi_cmatrix_t RC;
// // 	mpfi_cmatrix_init2(&RC, n+1, n+1, prec);
// // 	mpfi_cmatrix_mul(&RC, &Rint, &C3);				//RC = R*C
	
// // 	mpfi_cmatrix_t eye_n1;
// // 	mpfi_cmatrix_init2(&eye_n1, n+1, n+1, prec);
// // 	mpfi_cmatrix_ident(&eye_n1);				// eye(n+1)
	
// // 	mpfi_cmatrix_t C;
// // 	mpfi_cmatrix_init2(&C, n+1, n+1, prec);
// // 	mpfi_cmatrix_sub(&C, &eye_n1, &RC);			// C = eye(n+1) - R*C
	
		
	
	
// 	int res = 1;

// 	// mpfi_cmatrix_t Y;
// 	// mpfi_cmatrix_init2(&Y, n+1, 1, prec);

// 	// complexdouble *lambda_arr = (complexdouble*)malloc(sizeof(complexdouble));

// 	//       mpfi_cmatrix_t X1;
// 	//       mpfi_cmatrix_init2(&X1, n+1, 1, prec);	
// 	//       mpfi_cmatrix_t CX1;
// 	//       mpfi_cmatrix_init2(&CX1, n+1, 1, prec);
// 	//       	      mpfi_cmatrix_t X;
// 	//       mpfi_cmatrix_init2(&X, n+1, 1, prec);

// 	//       int iter = 0;
	
// 	// complexdouble *vlambda = (complexdouble*)malloc((n+1)*sizeof(complexdouble));
// 	// while(1 == 1)
// 	// {
// 	//       /*Preparing Y = midrad(Z, eps) */
// 	//       iter++;
// 	//       if(iter > 5)
// 	//       		return 1;


// 	//       midrad_vector(&Y, &Z, eps, n+1, prec);
	
// 	//       /* Preparing X =  Z + C*(Y - [v;lambda]); */
	
	      
// 	//       lambda_arr[0].r = lambda.r;
// 	//       lambda_arr[0].i = lambda.i;
	
	      
// 	//       clapack_matrix_ver_concat(vlambda, v, lambda_arr, 1, n, 1);			//[v, lambda]
	

// 	//       mpfi_cmatrix_sub_complexdouble(&X1, &Y, vlambda, n+1, 1);			//X1 = Y - [v;lambda]
	

// 	//       mpfi_cmatrix_mul(&CX1, &C, &X1);						// CX1 = C * X1
	

// 	//       mpfi_cmatrix_add(&X, &Z, &CX1);

	     
	
		
// 	//       res = mpfi_cmatrix_is_inside(&X, &Y);
// 	//       if(!res )
// 	//       {
// 	//       		// if (eps > 1.0)
// 	//       		// {
// 	//       		// 	//printf("Verification algorithm failure, epsilon became larger than 1. \n");
// 	//       		// 	return 0;
// 	//       		// }
// 	//       		eps *= 10;
// 	//       }
// 	//       else
// 	//       {
// 	// 			return res;
// 	//       }
	
// 	//       // //printf("iteration %d, eps = %e \n", iter, eps);
// 	// }	
  	
// 	return res;
// }





