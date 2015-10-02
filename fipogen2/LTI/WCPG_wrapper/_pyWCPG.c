/* This module uses a single function to calculate the WCPG from a quatuor of matrixes .
  It should be extended in the future to wrap the WCPG arbitrary precision function.
  
  Joachim Kruithof
  LIP6 - 2015 
  
  See
  
  http://dan.iel.fm/posts/python-c-extensions/
  http://stackoverflow.com/questions/27829946/extend-python-with-c-return-numpy-array-gives-garbage
  http://docs.scipy.org/doc/numpy/reference/c-api.dtype.html
  
  */

#include <Python.h>
#include <numpy/arrayobject.h>
#include <dlfcn.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION // remove warning for old versions of numpy

#include "libwcpg.h"


static char module_docstring[] =
   "This module uses WCPG prog by A. Lozanova to compute WCPG with double precision or arbitrary precision (FUTURE)" ;
   

static char pyWCPG_docstring[] =
   "For an LTI filter given in its State-Space representation {A,B,C,D}, \
where A is n*n, B is n*q, C is p*n and D is p*q real matrix the function \
returns integer value indicating if WCPG was successfully computed. \
In p*q matrix W the Worst-Case peak gain is stored if algorithm successfully exited. \
Input: \
	A, B, C, D - pointers for double arrays representing filter in state-space realization \
	n, p, q - order of filter, number of inputs and number of outputs respectively \
	W (output) - if function succeeds, on the output will hold the p*q size WCPG matrix of the filter {A,B,C,D} \
				space for W is assumed to be preallocated outside the function \
Output: \
	integer value equal to 1 if WCPG computation is successful and 0 otherwise." ;

	
static PyObject *WCPG_pyWCPG(PyObject *self, PyObject *args) ;


static PyMethodDef module_methods[] = {
   {"pyWCPG", WCPG_pyWCPG, METH_VARARGS, pyWCPG_docstring},
   {NULL, NULL, 0, NULL}
} ;


PyMODINIT_FUNC init_pyWCPG(void){
  PyObject *m = Py_InitModule3("_pyWCPG", module_methods, module_docstring);

  
  if (m == NULL){
    return;
  };
  
  /* load 'numpy' */
  import_array() ; 
} ;


static PyObject *WCPG_pyWCPG(PyObject *self, PyObject *args){

  PyObject *A_obj, *B_obj, *C_obj, *D_obj ;
  
  int n = 0, 
      p = 0, 
      q = 0 ;
      
  int tmp = 0 ;
  
  /* Parse tuple */
  
  if (!PyArg_ParseTuple(args, "OOOOiii", &A_obj, &B_obj, &C_obj, &D_obj, &n, &p, &q))
  {
    return NULL;
  }

  /* Interpret objects part of the tuple */
  
  PyObject *A_loc = PyArray_FROM_OTF(A_obj, NPY_DOUBLE, NPY_IN_ARRAY) ;
  PyObject *B_loc = PyArray_FROM_OTF(B_obj, NPY_DOUBLE, NPY_IN_ARRAY) ;
  PyObject *C_loc = PyArray_FROM_OTF(C_obj, NPY_DOUBLE, NPY_IN_ARRAY) ;
  PyObject *D_loc = PyArray_FROM_OTF(D_obj, NPY_DOUBLE, NPY_IN_ARRAY) ;
  
if (A_obj == NULL || B_obj == NULL || C_obj == NULL || D_obj == NULL) {
  
  Py_XDECREF(A_obj) ;
  Py_XDECREF(B_obj) ;
  Py_XDECREF(C_obj) ;
  Py_XDECREF(D_obj) ;
  
  return NULL ;
  
} ;

 // Create new array W with good size

  double W[q*p] ;
  
  for (tmp=0 ; tmp<q*p ; tmp++){
    W[tmp] = 0.0 ;
  }
  
/* Get pointers to the data as C-types */
  
  double *A = (double*)PyArray_DATA(A_loc) ;
  double *B = (double*)PyArray_DATA(B_loc) ;
  double *C = (double*)PyArray_DATA(C_loc) ;
  double *D = (double*)PyArray_DATA(D_loc) ;
    
  /* Open shared library */
  
  void *handle ;
  char *error ;
  
  int (*WCPG_ABCD)(double*, double*, double*, double*, double*, uint64_t, uint64_t, uint64_t) ;
  
  int loc_n = (uint64_t)n,
      loc_p = (uint64_t)p, 
      loc_q = (uint64_t)q ;
  
  //handle = dlopen("./libWCPG.so.0.0.9", RTLD_LAZY) ;
  handle = dlopen("libwcpg.so", RTLD_GLOBAL | RTLD_LAZY) ;
  
  if (!handle) {
   fprintf(stderr, "%s\n", dlerror()) ;
   exit(EXIT_FAILURE) ;
  } ;
  
  dlerror(); // clear any existing error, see http://linux.die.net/man/3/dlopen
  
  *(void **) (&WCPG_ABCD) = dlsym(handle, "WCPG_ABCD") ; // C-99 style
  
  if ((error = dlerror()) != NULL) {
   fprintf(stderr, "%s\n", dlerror()) ;
   exit(EXIT_FAILURE) ; 
  } ;
  
  // We pass the references to another function which does not get ownership of the data, so we have to Py_INCREF
  
  Py_INCREF(A_obj);
  Py_INCREF(B_obj);
  Py_INCREF(C_obj);
  Py_INCREF(D_obj);
  
  (*WCPG_ABCD)(W, A, B, C, D, loc_n, loc_p, loc_q) ;
  
  Py_DECREF(A_obj);
  Py_DECREF(B_obj);
  Py_DECREF(C_obj);
  Py_DECREF(D_obj);
  
  dlclose(handle) ;
  

  /* Dimension of array W */
  npy_intp dims[2] = {q,p} ;
  
  PyObject *Wobj_out = PyArray_SimpleNew(2, dims, NPY_DOUBLE) ;
  memcpy(PyArray_DATA(Wobj_out), W, sizeof(W));
  
  return Wobj_out;
  
}