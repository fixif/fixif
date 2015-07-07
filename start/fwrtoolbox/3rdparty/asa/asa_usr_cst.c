/***********************************************************************
* Adaptive Simulated Annealing (ASA)
* Lester Ingber <ingber@ingber.com>
* Copyright (c) 1993-2004 Lester Ingber.  All Rights Reserved.
* The LICENSE file must be included with ASA code.
***********************************************************************/

 /* $Id: asa_usr_cst.c,v 25.15 2004/09/23 18:10:44 ingber Exp ingber $ */

 /* asa_usr_cst.c for Adaptive Simulated Annealing */

#include "asa_usr.h"

#if COST_FILE

 /* Note that this is a trimmed version of the ASA_TEST problem.
    A version of this cost_function with more documentation and hooks for
    various templates is in asa_usr.c. */

 /* If you use this file to define your cost_function (the default),
    insert the body of your cost function just above the line
    "#if ASA_TEST" below.  (The default of ASA_TEST is FALSE.)

    If you read in information via the asa_opt file (the default),
    define *parameter_dimension and
    parameter_lower_bound[.], parameter_upper_bound[.], parameter_int_real[.]
    for each parameter at the bottom of asa_opt.

    The minimum you need to do here is to use
    x[0], ..., x[*parameter_dimension-1]
    for your parameters and to return the value of your cost function.  */

#if HAVE_ANSI
double
cost_function (double *x,
               double *parameter_lower_bound,
               double *parameter_upper_bound,
               double *cost_tangents,
               double *cost_curvature,
               ALLOC_INT * parameter_dimension,
               int *parameter_int_real,
               int *cost_flag, int *exit_code, USER_DEFINES * USER_OPTIONS)
#else
double
cost_function (x,
               parameter_lower_bound,
               parameter_upper_bound,
               cost_tangents,
               cost_curvature,
               parameter_dimension,
               parameter_int_real, cost_flag, exit_code, USER_OPTIONS)
     double *x;
     double *parameter_lower_bound;
     double *parameter_upper_bound;
     double *cost_tangents;
     double *cost_curvature;
     ALLOC_INT *parameter_dimension;
     int *parameter_int_real;
     int *cost_flag;
     int *exit_code;
     USER_DEFINES *USER_OPTIONS;
#endif
{

  /* *** Insert the body of your cost function here. *** */

#if ASA_TEST
  double q_n, d_i, s_i, t_i, z_i, c_r;
  int k_i;
  ALLOC_INT i, j;
  static LONG_INT funevals = 0;

  s_i = 0.2;
  t_i = 0.05;
  c_r = 0.15;

  q_n = 0.0;
  for (i = 0; i < *parameter_dimension; ++i) {
    if (fabs (parameter_upper_bound[i] - parameter_lower_bound[i]) <
        (double) EPS_DOUBLE)
      continue;

    j = i % 4;
    switch (j) {
    case 0:
      d_i = 1.0;
      break;
    case 1:
      d_i = 1000.0;
      break;
    case 2:
      d_i = 10.0;
      break;
    default:
      d_i = 100.0;
    }
    if (x[i] > 0.0) {
      k_i = (int) (x[i] / s_i + 0.5);
    } else if (x[i] < 0.0) {
      k_i = (int) (x[i] / s_i - 0.5);
    } else {
      k_i = 0;
    }

    if (fabs (k_i * s_i - x[i]) < t_i) {
      if (k_i < 0) {
        z_i = k_i * s_i + t_i;
      } else if (k_i > 0) {
        z_i = k_i * s_i - t_i;
      } else {
        z_i = 0.0;
      }
      q_n += c_r * d_i * z_i * z_i;
    } else {
      q_n += d_i * x[i] * x[i];
    }
  }
  funevals = funevals + 1;

  *cost_flag = TRUE;

#if TIME_CALC
  if ((PRINT_FREQUENCY > 0) && ((funevals % PRINT_FREQUENCY) == 0)) {
    printf ("funevals = %ld  ", funevals);
    print_time ("", stdout);
  }
#endif

  return (q_n);
#endif /* ASA_TEST */
}
#endif /* COST_FILE */
