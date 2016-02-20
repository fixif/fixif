all: main

DIR = testfiles
FILE = direct_form2.slx


main: slx2sif.py 
	 python $< $(DIR)/$(FILE)

extract: 
	python slxextract.py  $(DIR)/$(FILE)

clean:
	rm -f blockdiagram.xml SIF.txt *~ *.pyc

.PHONY: main extract clean test

test:
	python -m unittest
	
