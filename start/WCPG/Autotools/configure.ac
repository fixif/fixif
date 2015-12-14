#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([WCPG], [0.9], [anastasia.volkova@lip6.fr])
AC_CONFIG_SRCDIR([config.h.in])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIRS([m4])


AM_INIT_AUTOMAKE([1.6 no-define dist-zip dist-bzip2])

###############################################################################
# Checks for programs.
###############################################################################
AC_PROG_CC
AC_PROG_CXX
AM_PROG_LIBTOOL
AC_PROG_F77

#------------------------------------------------------------------------------
# withs...
#------------------------------------------------------------------------------
SO_LIB_PATH=""

AC_ARG_WITH(gmp-include,
            [  --with-gmp-include=DIR  GMP include directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_CPPFLAGS="$AM_CPPFLAGS -I$withval"
             fi])
AC_ARG_WITH(gmp-lib,
            [  --with-gmp-lib=DIR      GMP lib directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_LDFLAGS="$AM_LDFLAGS -L$withval"
               SO_LIB_PATH="${SO_LIB_PATH:+$SO_LIB_PATH:}$withval"
             fi
            ])
AC_ARG_WITH(gmp,
            [  --with-gmp=DIR          GMP install directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_CPPFLAGS="$AM_CPPFLAGS -I$withval/include"
               AM_LDFLAGS="$AM_LDFLAGS -L$withval/lib"
               SO_LIB_PATH="${SO_LIB_PATH:+$SO_LIB_PATH:}$withval/lib"
             fi
            ])


AC_ARG_WITH(mpfr-include,
            [  --with-mpfr-include=DIR  MPFR include directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_CPPFLAGS="$AM_CPPFLAGS -I$withval"
	     fi])
AC_ARG_WITH(mpfr-lib,
            [  --with-mpfr-lib=DIR      MPFR lib directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_LDFLAGS="$AM_LDFLAGS -L$withval"
               SO_LIB_PATH="${SO_LIB_PATH:+$SO_LIB_PATH:}$withval"
	     fi
            ])
AC_ARG_WITH(mpfr,
            [  --with-mpfr=DIR          MPFR install directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_CPPFLAGS="$AM_CPPFLAGS -I$withval/include"
               AM_LDFLAGS="$AM_LDFLAGS -L$withval/lib"
               SO_LIB_PATH="${SO_LIB_PATH:+$SO_LIB_PATH:}$withval/lib"
	     fi
            ])

AC_ARG_WITH(mpfi-include,
            [  --with-mpfi-include=DIR  MPFI include directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
	       AM_CPPFLAGS="$AM_CPPFLAGS -I$withval"
	     fi])
AC_ARG_WITH(mpfi-lib,
            [  --with-mpfi-lib=DIR      MPFI lib directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_LDFLAGS="$AM_LDFLAGS -L$withval"
               SO_LIB_PATH="${SO_LIB_PATH:+$SO_LIB_PATH:}$withval"
	     fi
            ])
AC_ARG_WITH(mpfi,
            [  --with-mpfi=DIR          MPFI install directory ],
            [if test "x$withval" != "xyes" -a "x$withval" != "x"
             then
               AM_CPPFLAGS="$AM_CPPFLAGS -I$withval/include"
               AM_LDFLAGS="$AM_LDFLAGS -L$withval/lib"
               SO_LIB_PATH="${SO_LIB_PATH:+$SO_LIB_PATH:}$withval/lib"
	     fi
            ])

#------------------------------------------------------------------------------
# Save user flags and set flags given by configure for the rest of the tests
#------------------------------------------------------------------------------
USER_CFLAGS="$CFLAGS"
USER_CPPFLAGS="$CPPFLAGS"
USER_LDFLAGS="$LDFLAGS"
CFLAGS="$AM_CFLAGS $USER_CFLAGS"
CPPFLAGS="$AM_CPPFLAGS $USER_CPPFLAGS"
LDFLAGS="$AM_LDFLAGS $USER_LDFLAGS"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$SO_LIB_PATH"


###############################################################################
# Checks for header files.
###############################################################################
AC_CHECK_HEADER_STDBOOL
AC_CHECK_HEADERS([stding.h float.h sys/time.h])
AC_CHECK_HEADERS([f2c.h],[AC_DEFINE([F2C_HEADER], [1], [Define to 1 if f2c.h found])],[AC_MSG_ERROR(No f2c.h header found)])
AC_CHECK_HEADERS([mpfr.h],[],[AC_MSG_ERROR(No mpfr.h header found)])
AC_CHECK_HEADERS([mpfi.h],[],[AC_MSG_ERROR(No mpfi.h header found)])
AC_CHECK_HEADERS([mpfi_io.h],[],[AC_MSG_ERROR(No mpfi_io.h header found)])
#------------------------------------------------------------------------------
#Check for any of blas.h, cblas.h or blaswrap.h header files
#------------------------------------------------------------------------------
BLAS_FLAG="no"

#Check for BLAS headers
ADD_LBLAS="yes"
AC_CHECK_HEADERS([blas.h], [ADD_LBLAS="yes" BLAS_FLAG="yes" AC_DEFINE([BLAS_HEADER], [1], [Define to 1 if blas.h found])], [ADD_LBLAS="no"],
[[#ifdef HAVE_F2C_H
     # include <f2c.h>
     #endif
]])
if test "x${ADD_LBLAS}" = "xyes"
then
  AC_MSG_NOTICE([blas.h found.])
fi

#Check for CBLAS headers
ADD_LCBLAS="yes"
AC_CHECK_HEADERS([cblas.h], [ADD_LCBLAS="yes" BLAS_FLAG="yes" AC_DEFINE([CBLAS_HEADER], [1], [Define to 1 if cblas.h found])], [ADD_LCBLAS="no"],
[[#ifdef HAVE_F2C_H
     # include <f2c.h>
     #endif
]])
if test "x${ADD_LCBLAS}" = "xyes"
then
  AC_MSG_NOTICE([cblas.h found.])
fi

#Check for BLASWRAP headers
ADD_LBLASWRAP="yes"
AC_CHECK_HEADERS([blaswrap.h], [ADD_LBLASWRAP="yes" BLAS_FLAG="yes"], [ADD_LBLASWRAP="no"],
[[#ifdef HAVE_F2C_H
     # include <f2c.h>
     #endif
]])

if test "x${ADD_LBLASWRAP}" = "xyes"
then
  AC_MSG_NOTICE([blaswrap.h found.])
fi

if test "x${BLAS_FLAG}"="xyes"
then
  AC_MSG_NOTICE([At least one blas header file was found.])
else
  AC_MSG_ERROR([No blas header file found.])
fi

#------------------------------------------------------------------------------
#Checking for any of clapack.h lapack.h lapacke.h header files
#------------------------------------------------------------------------------
ADD_FLAG="no"

#Check for clapack.h headers
ADD_LCLAPACK="yes"
AC_CHECK_HEADERS([clapack.h], [ADD_LCLAPACK="yes" ADD_FLAG="yes" AC_DEFINE([CLAPACK_HEADER], [1], [Define to 1 if clapack.h found])], [ADD_LCLAPACK="no"],
[[#ifdef HAVE_BLAS_H
     # include <f2c.h>
     # include <blas.h>
  #endif
]])

if test "x${ADD_LCLAPACK}" = "xyes"
then
  AC_MSG_NOTICE([clapack.h found.])
fi

#Check for lapacke.h headers
ADD_LLAPACKE="yes"
AC_CHECK_HEADERS([lapacke.h], [ADD_LLAPACKE="yes" ADD_FLAG="yes" AC_DEFINE([LAPACKE_HEADER], [1], [Define to 1 if lapacke.h found])], [ADD_LLAPACKE="no"],
[[#ifdef HAVE_BLAS_H
     # include <f2c.h>
     # include <blas.h>
  #endif
]])
if test "x${ADD_LLAPACKE}" = "xyes"
then
  AC_MSG_NOTICE([lapacke.h found.])
fi

#Check for lapack.h headers
ADD_LLAPACK="yes"
AC_CHECK_HEADERS([lapack.h], [ADD_LLAPACK="yes" ADD_FLAG="yes" AC_DEFINE([LAPACK_HEADER], [1], [Define to 1 if lapack.h found])], [ADD_LLAPACK="no"],
[[#ifdef HAVE_BLAS_H
     # include <f2c.h>
     # include <blas.h>
  #endif
]])

if test "x${ADD_FLAG}"="xyes"
then
  AC_MSG_NOTICE([At least one lapack header file found.])
else
  AC_MSG_ERROR([No clapack header file found.])
fi


###############################################################################
# Checks for libraries.
###############################################################################
AC_CHECK_LIB([gmp], [__gmpz_init], [true], AC_MSG_ERROR([libgmp unusable]))
AC_CHECK_LIB([gmp], [__gmpz_fac_ui], [true], AC_MSG_ERROR([libgmp version too old]))
AC_CHECK_LIB([gmp], [__gmpz_bin_uiui], [true], AC_MSG_ERROR([libgmp version too old]))
AC_CHECK_LIB([gmp], [__gmpz_export], [], AC_MSG_ERROR([libgmp version too old])) # This one adds -lgmp in case of success
AC_CHECK_LIB([mpfr], [mpfr_init], [true], AC_MSG_ERROR([libmpfr unusable]))
AC_CHECK_LIB([mpfr], [mpfr_erfc], [], AC_MSG_ERROR([libmpfr version too old])) # This one adds -lmpfr in case of success
AC_CHECK_LIB([mpfi], [mpfi_init], [], AC_MSG_ERROR([libmpfi unusable]))



FLAG="no"
AC_CHECK_LIB([blas],[dgemv],[FLAG="yes" BLAS_LIBS="-lblas"], AC_MSG_WARN([Missing blas but maybe cblas is installed]))
AC_CHECK_LIB([blas],[cblas_dgemv],[FLAG="yes" BLAS_LIBS="-lblas"])
if test "x${FLAG}" != "xyes"
then
    AC_MSG_ERROR([Missing (c)blas, function dgemv not found])
fi

FLAG1="no"
FLAG2="no"
AC_CHECK_LIB([lapacke],[LAPACKE_zgetri],[FLAG1="yes"], AC_MSG_WARN([Missing lapacke but maybe lapack is installed]))
AC_CHECK_LIB([lapack],[zgetri_],[FLAG2="yes" LAPACK_LIBS="-llapack"], AC_MSG_WARN([Missing lapack]))

if test "x${FLAG2}" == "xyes"
then
    LAPACK_LIBS="-llapack"
elif test "x${FLAG1}" == "xyes"
then
    LAPACK_LIBS="$(LAPACK_LIBS) -llapacke"
else
    AC_MSG_ERROR([Missing clapack/lapacke, function zgetri_/LAPACKE_zgetri not found])
fi



FLAG1="no"
FLAG2="no"
AC_CHECK_LIB([lapacke],[LAPACKE_dgeevx],[FLAG1="yes"], AC_MSG_WARN([Missing lapacke but maybe lapack is installed]))
AC_CHECK_LIB([lapack],[dgeevx_],[FLAG2="yes"], AC_MSG_WARN([Missing lapack]))
if test "x${FLAG1}" == "xyes"
then
    LAPACK_LIBS="-llapacke"
elif test "x${FLAG2}" == "xyes"
then
    LAPACK_LIBS="-llapack"
else
    AC_MSG_ERROR([Missing clapack/lapacke, function dgeevx_/LAPACKE_dgeevx not found])
fi


FLAG1="no"
FLAG2="no"
AC_CHECK_LIB([lapacke],[LAPACKE_zgetrf],[FLAG1="yes"], AC_MSG_WARN([Missing lapacke but maybe lapack is installed]))
AC_CHECK_LIB([lapack],[zgetrf_],[FLAG2="yes"], AC_MSG_WARN([Missing lapack]))
if test "x${FLAG1}" == "xyes"
then
    LAPACK_LIBS="-llapacke"
elif test "x${FLAG2}" == "xyes"
then
    LAPACK_LIBS="-llapack"
else
    AC_MSG_ERROR([Missing clapack/lapacke, function zgetrf_/LAPACKE_zgetrf not found])
fi


# Check that dynamic libraries are available at runtime
AC_MSG_CHECKING([if libgmp is found at runtime])
AC_RUN_IFELSE([AC_LANG_PROGRAM([[#include <gmp.h>]],
                               [[mpz_t a; mpz_init(a); mpz_clear(a); return 0;]])],
	      [AC_MSG_RESULT(yes)],
              [AC_MSG_WARN([libgmp is found at compile time but not at run time. Checking /etc/ld.so.conf and running ldconfig could fix the problem.])])


AC_MSG_CHECKING([if libmpfr is found at runtime])
AC_RUN_IFELSE([AC_LANG_PROGRAM([[#include <mpfr.h>]],
                               [[mpfr_t a; mpfr_init2(a, 53); mpfr_clear(a); return 0;]])],
	      [AC_MSG_RESULT(yes)],
              [AC_MSG_WARN([libmpfr is found at compile time but not at run time. Checking /etc/ld.so.conf and running ldconfig could fix the problem.])])


AC_MSG_CHECKING([if libmpfi is found at runtime])
AC_RUN_IFELSE([AC_LANG_PROGRAM([[#include <mpfi.h>]],
                               [[mpfi_t a; mpfi_init(a); mpfi_clear(a); return 0;]])],
	      [AC_MSG_RESULT(yes)],
              [AC_MSG_ERROR([libmpfi is found at compile time but not at run time. Checking /etc/ld.so.conf and running ldconfig could fix the problem.])])

#Check for -Wl,-export-dynamic etc.
CFLAGS="$AM_CFLAGS -fPIC $USER_CFLAGS"
AC_MSG_CHECKING([for -fPIC support])
AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[]], [[]])],
                  [
                     AC_MSG_RESULT(yes)
                     AM_CFLAGS="$AM_CFLAGS -fPIC"
                  ],
                  [
                     AC_MSG_RESULT(no)
                     CFLAGS="$AM_CFLAGS $USER_CFLAGS"
                  ])


###############################################################################
# Checks for typedefs, structures, and compiler characteristics.
###############################################################################
AC_TYPE_UINT32_T
AC_TYPE_UINT64_T
AC_C_INLINE
AC_TYPE_INT32_T
AC_TYPE_INT64_T
AC_TYPE_SIZE_T


###############################################################################
# Checks for library functions.
###############################################################################
AC_CHECK_FUNCS([gettimeofday])
AC_CHECK_FUNCS([sqrt])
AC_CHECK_FUNCS([ceil])
AC_FUNC_MALLOC
AC_FUNC_REALLOC


#return to user flags
CPPFLAGS="$USER_CPPFLAGS"
CFLAGS="$USER_CFLAGS"
LDFLAGS="$USER_LDFLAGS"

AC_SUBST(AM_CPPFLAGS)
AC_SUBST(AM_CFLAGS)
AC_SUBST(AM_LDFLAGS)
AC_SUBST(BLAS_LIBS)
AC_SUBST(LAPACK_LIBS)


AC_CONFIG_FILES([Makefile])
AC_OUTPUT

