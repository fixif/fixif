/*------------------------------------------------------------------------------------------------------*/
/* 
"lapack_linalg.c"
This is the sourse file, containing the code for
	- matrix input/output functions
	- functions for basic matrix arithmetic (multiplication, substraction, etc)
	- Linear System Solver
	- Eigensolver
All the functions work with matrices of CLAPACK's types doublereal and complexdouble.
All matrices are represented as one-dimension arrays, where for a n*m matrix A the element
A(i,j) is the element A[i * m + j] of the array.
*/
/*-----------------------------------------------------------------------------------------------------*/


#include "clapack_linalg.h"


//The function returns an absolute value of a complex number z.
doublereal abs_complexdouble(complexdouble *z)
{
	return sqrt((z->i)*(z->i) + (z->r)*(z->r));
}



//The function copies a complexdouble m x n matrix src to matrix cpy.
void clapack_matrix_copy_z(complexdouble *cpy, complexdouble *src, int m, int n)
{	
	int i,j;
	double tmp;

	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
		
			cpy[i*n+j].r = 0.0;
			cpy[i*n+j].i = 0.0;

			cpy[i*n+j].r = src[i*n+j].r;
			cpy[i*n+j].i = src[i*n+j].i;
		}
	}  
}

//The function copies a real m x n matrix src to matrix cpy.
void clapack_matrix_copy_d(doublereal *cpy, doublereal *src, int m, int n)
{	
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			cpy[i*n+j] = src[i*n+j];
		}
	}  
}

//For a square complex matrix the function returns its transpose T
void clapack_matrix_transp_sqr(complexdouble *T, complexdouble *A, int n)
{
	  
	  int i,j;
	  for(i = 0; i < n; ++i)
	  {
		  for(j = 0; j < n; j++)
		  {
			  T[i + j * n] = A[i * n + j];
		  }
	  }
}

//Function represents a real matrix as complex one, setting imaginary part to zero
void clapack_rmatrix_as_zmatrix(complexdouble *res, doublereal *a, int m, int n)
{
	//memory for res should be preallocated!
	int i,j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			res[i*n+j].r = a[i*n+j];
			res[i*n+j].i = (doublereal)0.0;
		}
	}
  
}

//The function returns product of two complex numbers op1 and op2
complexdouble complexdouble_mul(complexdouble op1, complexdouble op2)
{
	complexdouble rop;
	rop.r = op1.r * op2.r - op1.i * op2.i;
	rop.i = op1.i * op2.r + op1.r * op2.i;
	return rop;
}


//For two square matrices A and B the function returns its product C = A * B
void clapack_matrix_mul(complexdouble *C, complexdouble *A, complexdouble *B, int n)
{

	// printf("Multiplying two matrices: \n");
	// printf("-------Matrix 1: \n");
	// clapack_matrix_print_z(A, n, n);
	// printf("-------Matrix 2: \n");
	// clapack_matrix_print_z(B, n, n);


	int i,j,k;
	for(i = 0; i < n; ++i)
	{
		for(j = 0; j < n; ++j)
		{
			C[i * n + j].r = 0;
			C[i * n + j].i = 0;
			for(k = 0; k < n; ++k)
			{
				/* Real part of C: reC_ij = sum_k {reA_ik*reB_kj - imA_ik*imB_kj} for k=1..n */
				// printf("C[%d,%d].r += A[%d,%d].r * B[%d,%d].r - A[%d,%d].i * B[%d,%d].i =  \n", i,j,i,k,k,j,i,k,k,j);
				// printf("%f += %f * %f- %f * %f \n", C[i * n + j].r,A[i * n + k].r, B[k * n + j].r, A[i * n + k].i,B[k * n + j].i);
				C[i * n + j].r += A[i * n + k].r * B[k * n + j].r - A[i * n + k].i * B[k * n + j].i;

				/* Imaginary part of C: imC_ij = sum_k {imA_ik*reB_kj + reA_ik*imB_kj} for k=1..n */
				// printf("C[%d,%d].i += A[%d,%d].r * B[%d,%d].i - A[%d,%d].i * B[%d,%d].r =  \n", i,j,i,k,k,j,i,k,k,j);
				// printf("%f += %f * %f- %f * %f \n", C[i * n + j].r,A[i * n + k].r, B[k * n + j].i, A[i * n + k].i,B[k * n + j].r);
				
				C[i * n + j].i += A[i * n + k].r * B[k * n + j].i + A[i * n + k].i * B[k * n + j].r;

			}
			// printf("C[%d,%d].r = %f \t C[%d,%d].i = %f \n", i, j, C[i * n + j].r, i, j, C[i * n + j].i );
		}
	}
}

//For two m x n matrices op1 and op2 the funciton returns rop = op1 - op2
void clapack_matrix_sub(complexdouble *rop, complexdouble *op1, complexdouble *op2, int rows, int cols)
{
	int i,j;
	for(i = 0; i < rows; ++i)
	{
		for(j = 0; j < cols; ++j)
		{
		      
			rop[i*cols + j].r = op1[i*cols + j].r - op2[i*cols + j].r;
			rop[i*cols + j].i = op1[i*cols + j].i - op2[i*cols + j].i;
			
		}
	}
  
}

//For a complex number v the funciton returns a pointer to the square matrix rop = v * I,
//where I is the complex identity matrix of size n x n
void clapack_matrix_diagonal(complexdouble *rop, complexdouble v, int n)
{
	//space for rop should be preallocated, size(rop) = n*n
	int i,j;
	for(i = 0; i < n; ++i)
	{
	    for(j = 0; j < n; ++j)
	    {
		  	rop[i*n + j].r = (doublereal)0.0;
			rop[i*n + j].i = (doublereal)0.0;
		      
	    }
	    rop[i*n + i].r = v.r;
		rop[i*n + i].i = v.i;
	}
	      
}

//The function inverts the signs of all entries of the matrix op.
void clapack_matrix_neg(complexdouble *op, int rows, int columns)
{
	int i,j;
	for(i = 0 ; i < rows; ++i)
	{
		for(j = 0; j < columns; ++j)
		{
			op[i*columns+j].r = -op[i*columns+j].r;
			op[i*columns+j].i = -op[i*columns+j].i;
		}
	}
  
}

//The function creates a complex identity matrix I_ii = 1 + i*0
void clapack_matrix_ident(complexdouble *Identity, int m, int n)
{
	int i, j;
	for(i = 0; i < m; ++i)
	{
		for(j = 0; j < n; ++i)
		{
			Identity[i * n + j].r = 0.0;
			Identity[i * n + j].i = 0.0;
		}
		Identity[i * n + i].r = 1.0;
	}
}


//Concatenates two matrices horizontally Res = [op1; op2]
void clapack_matrix_hor_concat(complexdouble *rop, complexdouble *op1, complexdouble *op2, int rows, int col1, int col2)
{
	 int final_col = col1 + col2;
	 //space for rop should be preallocated
	 int i,j, j2;
	for(i = 0; i < rows; ++i)
	{
		for(j = 0; j < col1; ++j)
		{
			//mpfi_c_set(&(rop->arr[i][j]), &(op1->arr[i][j]));
			rop[i*final_col + j].r = op1[i*col1 + j].r;
			rop[i*final_col + j].i = op1[i*col1 + j].i;
		}
		for(j2 = 0; j2 < col2; ++j2)
		{
			//mpfi_c_set(&(rop->arr[i][j]), &(op2->arr[i][j2]));
			rop[i*final_col + j].r = op2[i*col2 + j2].r;
			rop[i*final_col + j].i = op2[i*col2 + j2].i;
			++j;
		}
	}
  
  
  
}

//Concatenates two matrices vertically Res = [op1 op2]
void clapack_matrix_ver_concat(complexdouble *rop, complexdouble *op1, complexdouble *op2, int cols, int rows1, int rows2)
{
	 int final_rows = rows1 + rows2;
	 //space for rop should be preallocated
	 int i,j, i2;
	for(j = 0; j < cols; ++j)
	{
		for(i = 0; i < rows1; ++i)
		{			
			rop[i*cols + j].r = op1[i*cols + j].r;
			rop[i*cols + j].i= op1[i*cols + j].i;
		}
		for(i2 = 0; i2 < rows2; ++i2)
		{			
			rop[i*cols + j].r = op2[i2*cols + j].r;
			rop[i*cols + j].i = op2[i2*cols + j].i;
			++i;
		}
	}
  
  
  
}



//Finds eigensystem (eigenvalues and right eigenvectors) of real matrix A of size n x n and appros. error bounds
//p - complex vector of eigenvalues
//V - complex matrix of right eigenvectors,t hat are saved as rows
//verrbnd - vector of approx. error bounds on each eigevector (row of matrix V)
//eerrbnd - vector of approx. error bounds on each eigenvalue
void clapack_eigenSolver(complexdouble *p, complexdouble *V,doublereal *verrbnd, doublereal *eerrbnd, doublereal *A, int n, double eps)
{
  
	/* Subroutine  int sgeevx_(char *balanc, char *jobvl, char *jobvr, char *
	sense, integer *n, real *a, integer *lda, real *wr, real *wi, real *
	vl, integer *ldvl, real *vr, integer *ldvr, integer *ilo, integer *
	ihi, real *scale, real *abnrm, real *rconde, real *rcondv, real *work, 
	 integer *lwork, integer *iwork, integer *info); 
	 *
	 *  EERRBD(I) = EPSMCH*ABNRM/RCONDE(I)
     *  VERRBD(I) = EPSMCH*ABNRM/RCONDV(I)
     */


            
	int lda, ldvl, ldvr, lwork, info, ihi, ilo;
	doublereal abnrm;//output; The one-norm of the balanced matrix (the maximum of the sum of absolute values of entries of any column)

	lda = n;
	ldvr = n;
	ldvl = n;
	lwork = n*(n+6);
	
	doublereal *wr = (doublereal*)malloc(n*sizeof(doublereal));
	doublereal *wi = (doublereal*)malloc(n*sizeof(doublereal));;
	doublereal *vl = (doublereal*)malloc(ldvl*n*sizeof(doublereal));
	doublereal *vr = (doublereal*)malloc(ldvr*n*sizeof(doublereal));
	doublereal *work = (doublereal*)malloc(lwork*sizeof(doublereal));
	
	doublereal *rconde = (doublereal*)malloc(n*sizeof(doublereal)); //output
	doublereal *rcondv = (doublereal*)malloc(n*sizeof(doublereal));	//output
	doublereal *scale = (doublereal*)malloc(n*sizeof(doublereal));	//output
	integer *iwork = (integer*)malloc((2*n-2)*sizeof(integer)) ;
	

	my_dgeevx((int*)&n, A, &lda, wr, wi, vl, &ldvl, vr, &ldvr, &ilo, &ihi, scale, &abnrm, rconde, rcondv, work, &lwork, iwork, &info); 
	////printf("Info : %d \n", info );

	wiwr_to_matrix(p, (doublereal*)wr, (doublereal*)wi, n);				//memory for p should be preallocated!!
	
	int* flags = (int*)malloc(n*sizeof(int));
	eigval_flags(flags, (doublereal*)wi, (doublereal*)wr, n);
	eigvect_to_matrix(V, (doublereal*)vl,flags, n);				//memory for V should be preallocated!!
	  	
	int i;
	for(i = 0; i < n; ++i)
	{
		eerrbnd[i] = eps * abnrm / rconde[i];
		verrbnd[i] = eps * abnrm / rcondv[i];
		}
	
	
	free(flags);
	free(work);
	free(iwork);
	free(vr);
	free(vl);
	free(wi);
	free(wr);
	free(rconde);
	free(rcondv);
	free(scale);

}


//returns array of flags which eigenvslue is real and wich is complex (conjugate)
//Requered for eigvect_to_matrix function
void eigval_flags(int *flags, doublereal *wi, doublereal *wr, int n)
{
	//memory for flags should be preallocated 
	int real_flag = 0;
	int complex_flag = 1;
	int i;
	for(i = 0; i < n; ++i)
	{
		if(wi[i] == 0.0)
		  flags[i] = real_flag;
		else
		  flags[i] = complex_flag;
		
	}
  
}

//transforms two arrays wi and wr returned by clapack routines, that hold real and imaginary part of eigenvalues 
//to a complex array
void wiwr_to_matrix(complexdouble *p, doublereal *wr, doublereal *wi, int n)
{
	int i;
	for(i = 0; i < n; ++i )
	{
		p[i].r = wr[i];
		p[i].i = wi[i];
	}
}

//transforms array of eigenvectors returned by ClALAPCK according to flags
//Required because CLAPACK tries to return a redused sized array, without saving conjugated vectors 
//for complex eigenvalues
void eigvect_to_matrix(complexdouble *V, doublereal *v,int* flags, int n)
{
  
	complexdouble *tmp = (complexdouble*)malloc(n*n*sizeof(complexdouble));
	int i, j;
	int k = 0;
	double real, image;
	for(i = 0; i < n; i++)
	{
		if(flags[i] == 1)
		{
			for(j = 0; j < n; ++j)
			{
			      real = v[i*n + j];
			      image = v[(i+1)*n + j];
			      tmp[i*n + j].r = real;
			      tmp[i*n + j].i = image;
			      tmp[(i+1)*n + j].r = real;
			      tmp[(i+1)*n + j].i = -image;
			     
			  }
			 i++;
		}
		  else
		  {
			for(j = 0; j < n; ++j)
			{
			      tmp[i*n + j].r = v[i*n + j];
			      tmp[i*n + j].i = (doublereal)0.0;
			}
		  }
		
	
	}
	clapack_matrix_transp_sqr(V, tmp, n);
	free(tmp); 
  
}

/* Linear system solution */

//void clapack_LSSolver(complexdouble *X,doublereal *ferr,doublereal *berr, complexdouble *A, complexdouble *B, integer n, integer bcols)
//{
//
//// 	/* Subroutine */ int zgerfs_(char *trans, integer *n, integer *nrhs,
//// 	complexdouble *a, integer *lda, complexdouble *af, integer *ldaf,
//// 	integer *ipiv, complexdouble *b, integer *ldb, complexdouble *x,
//// 	integer *ldx, doublereal *ferr, doublereal *berr, complexdouble *work,
//// 	 doublereal *rwork, integer *info);
//
//// 	/* Subroutine */ int zgetrf_(integer *m, integer *n, complexdouble *a,
//// 	integer *lda, integer *ipiv, integer *info);
//
//// 	/* Subroutine */ int zgetrs_(char *trans, integer *n, integer *nrhs,
//// 	complexdouble *a, integer *lda, integer *ipiv, complexdouble *b,
//// 	integer *ldb, integer *info);
//
//	//We prepare LU factorization of A, because it's an input for zgerfs_
//
//	integer info_lu;
//	integer lda = n;
//	integer *ipiv = (integer*)malloc(n*sizeof(integer));
//	complexdouble *AF = (complexdouble*)malloc(n*n*sizeof(complexdouble));
//	clapack_matrix_copy_z(AF, A, n, n);
//
//
//	zgetrf_(&n, &n, AF, &lda, ipiv, &info_lu);
//	integer *ipiv_cpy = (integer*)malloc(n*sizeof(integer));
//	int i;
//	for(i = 0; i < n; ++i)
//	{
//		ipiv_cpy[i] = ipiv[i];
//	}
//
//	//printf("\n Info zgetrf_: %d", (int)info_lu );
//
//	// Then we solve the linear system A*X=B with zgetrs routine
//	char *trans = "N";
//	integer info_ls;
//	integer ldb =  n;
//	integer nhrs = bcols;
//	//integer *ipiv_ls = (integer*)malloc(n*sizeof(integer));
//
//	clapack_matrix_copy_z(X, B, n, bcols); //we pass it too zgetrs_ and on the output it will contain the solution X;
//
//	zgetrs_(trans, &n, &nhrs, AF, &lda,ipiv, X, &ldb, &info_ls );
//	//printf("\n Info zgetrs_: %d \n", (int)info_ls );
//
//	//Then we improve the solution X and get error bounds on forward and backward error with zgerfs_ routine.
//	integer info;
//	integer ldaf = n;
//	integer ldx = n;
//
//
//
//	complexdouble *work = (complexdouble*)malloc(2*n*sizeof(complexdouble));
//	doublereal *rwork = (doublereal*)malloc(n*sizeof(doublereal));
//	nhrs = bcols;
//	ldb = n;
//
//	zgerfs_(trans, &n, &nhrs, A, &lda, AF, &ldaf, ipiv, B, &ldb, X, &ldx, ferr, berr, work, rwork, &info);
//
//	//printf("\n Info zgerfs_: %d", (int)info );
//
//	//clapack_matrix_print_z(X, n, bcols);
//
//	//printf("\n Relative backward error of each Psi(j) vector: \n");
//	// clapack_matrix_print_d(berr, 1, nhrs);
//
//	//printf("\n Estimated forward error of each Psi(j) vector: \n");
//	// clapack_matrix_print_d(ferr, 1, nhrs);
//
//}


/* For a square complex matrix A in format complexdouble the function
finds its inverse with CLAPACK routines. */
int clapack_complex_matrix_inverse(complexdouble *U, complexdouble *A, integer n)
{
//   /* Subroutine */ int zgetrf_(integer *m, integer *n, complexdouble *a, 
// 	integer *lda, integer *ipiv, integer *info); -- LU factorization of complex A

	// printf("Starting inverse\n");
	integer info;
	integer lda = n;
	integer ipiv_size = n;
	integer *ipiv = (integer*)malloc(ipiv_size*sizeof(integer));
	
//	zgetrf_(&n, &n, A, &lda, ipiv, &info);
	my_zgetrf ((int*)&n, (int*)&n, (complexdouble*)A, (int*)&lda, (int*)ipiv, (int*)&info);
	if((int)info != 0)
	{
		printf("Error occured while inverting matrix with CLAPACK (routine zgetrf_). Inversion impossible. Info = %ld \n", info);
		return 0;
	}
	// printf("PLU info: %d\n", info);		
	// Now A = P * L * U
	// printf("Result of PLU: \n");
	// clapack_matrix_print_z(A, n, n);
	// printf("pivot indeces: \n");
	// int i;
	// for(i = 0; i < n; ++i)
	// 	printf("%d\t", ipiv[i]);
	
// 	/* Subroutine */ int zgetri_(integer *n, complexdouble *a, integer *lda, 
// 	integer *ipiv, complexdouble *work, integer *lwork, integer *info); -- inversion routine

	integer lwork, info2;
	lwork = 10*n;
	complexdouble *work = (complexdouble*)malloc(lwork*sizeof(complexdouble));
	
	my_zgetri((int*)&n, (complexdouble*)A, (int*)&lda, (int*)ipiv, (complexdouble*)work, (int*)&lwork, (int*)&info2);
	if((int)info2 != 0)
	{
		printf("Error occured while inverting matrix with CLAPACK(routine zgetri_). Inversion impossible. Info = %d \n", info2);
		return 0;
	}
	// printf("Zgetri info: %d\n", info2);	
	//memory for res must be preallocated!!!

	// printf("\n Result of inversion: \n");
	// clapack_matrix_print_z(A, n, n);

	clapack_matrix_copy_z(U, A, n, n);
	// printf("Zgetri info: %d\n", info2);	
	free(work);
	free(ipiv);
	return 1;
	
}

