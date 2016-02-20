

AM_LDFLAGS = -lm -lgmp -lmpfr -lmpfi $(LAPACK_LIBS) $(BLAS_LIBS)

lib_LTLIBRARIES = libwcpg.la
include_HEADERS = wcpg.h \
			   clapack_linalg.h \
			   glue.h \
			   inclusion_verif.h \
			   mpfi_cmpx.h \
			   mpfi_matrixalg.h \
			   mpfr_linalg.h \
			   _wcpg.h \
			   clapack_functions_config.h
libwcpg_la_SOURCES  = clapack_linalg.c \
			   glue.c \
			   inclusion_verif.c \
			   mpfi_cmpx.c \
			   mpfi_matrixalg.c \
			   mpfr_linalg.c \
			   _wcpg.c \
			   wcpg.c \
			   clapack_functions_config.c  

libwcpg_la_LDFLAGS = -version-info 0:9:0 $(AM_LDFLAGS)


bin_PROGRAMS = wcpg_test
wcpg_test_SOURCES = wcpg_test.c wcpg_test.h
wcpg_test_CFLAGS = $(AM_CFLAGS)
wcpg_test_CXXFLAGS = $(AM_CXXFLAGS)
wcpg_test_LDFLAGS = $(AM_LDFLAGS)
wcpg_test_LDADD = libwcpg.la


ACLOCAL_AMFLAGS = -I m4

LIBTOOL_DEPS = @LIBTOOL_DEPS@
libtool: $(LIBTOOL_DEPS)
	$(SHELL) ./config.status libtool
