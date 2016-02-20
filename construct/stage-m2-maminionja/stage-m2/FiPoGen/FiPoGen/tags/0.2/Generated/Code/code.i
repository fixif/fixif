/* example.i */
%module code

// This tells SWIG to treat float * as a special case
%typemap(in) float * {
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (float *) malloc((size+1)*sizeof(float));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyFloat_Check(o))
	$1[i] = PyFloat_AsDouble(PyList_GetItem($input,i));
      else {
	PyErr_SetString(PyExc_TypeError,"list must contain strings");
	free($1);
	return NULL;
      }
    }
    $1[i] = 0;
  } else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) float * {
  free((float*) $1);
}

%{
    extern float RandomFloat(int beta);
    extern double SoP_float(float * tab);
    extern double SoP_int(float * tab);
    extern double SoP_ac_fixed(float * tab);
%}

#include "ac_fixed.h"
extern float RandomFloat(int beta);
extern double SoP_float(float * tab);
extern double SoP_int(float * tab);
extern double SoP_ac_fixed(float * tab);
