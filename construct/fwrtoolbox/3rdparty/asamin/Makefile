#***********************************************************************
# MATLAB Gateway Routine for Lester Ingber's Adaptive Simulated
# Annealing (ASA)
# 
# Copyright (c) 1999-2004  Shinichi Sakata.  All Rights Reserved.
#***********************************************************************
# $Id: Makefile,v 1.27 2004/10/03 03:23:06 ssakata Exp ssakata $
#
CFLAGS = -O4
#CFLAGS = -O3 -g -Wall
#CFLAGS = -g
LDFLAGS = -O4 
#LDLIBS = -ldl
#LDFLAGS = -O3 -g -Wall -Zexe
#LDFLAGS = -g
DEBUGFLAG =
#DEBUGFLAG = -DDEBUG
DEFINES = \
  -DUSER_ACCEPTANCE_TEST=TRUE \
  -DUSER_ASA_OUT=TRUE \
  -DLD_LIBRARY_PATH=/usr/lib/ \
  $(DEBUGFLAG)

CC=gcc
MEX=mex -g
#MEX=cmex
#


#GCC_VERSION = 3.3


TARGET = asamin.mex

$(TARGET): asamin.c asamin.h asa.h asa.o
	$(MEX) $(DEFINES) asamin.c asa.o -ll -lm

.c.o:
	$(CC) -c $(CFLAGS) $(DEFINES) -o $@ $<

asa.o: asa.c asa.h asa_usr_asa.h

clean:
	rm -rf *.o asatest[12].log $(TARGET)

new: clean $(TARGET)

package:
	cd ..; \
	tar cvf - \
                asamin/Makefile \
                asamin/LICENSE \
                asamin/README \
                asamin/asamin.c \
                asamin/asamin.h \
                asamin/asamin.m \
                asamin/asatest.m \
                asamin/test_cost_func1.m \
                asamin/test_cost_func2.m \
                | gzip -c - > asamin/asamin.tar.gz
