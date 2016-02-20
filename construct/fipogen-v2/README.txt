What is FiPoGen
---------------

FiPoGen means Fixed-point generator.
It is a program to generate fixed-point algorithms for filters.

What are its dependencies ?
--------------------------

Mostly python packages as dependences : jinga2, numpy, scipy

jinga2
numpy (1.10.1)
scipy (0.16.1)
slycot (0.2.0)

Needs sphinx >=1.3.1 to generate doc because otherwie all imports are documented...

Run tests
---------

See ./run_tests.sh for all possible args. Some examples :

./run_tests.sh SIF
./run_tests.sh LTI

Create package
--------------

- pack the modules as tar file using ./create_package.sh

Generation of documentation
---------------------------

go to ./doc/ folder then (examples, other options available) :

make help
make html
make latexpdf

settings are located inside the ./source folder :

conf.py contains the configuration
index.rst is the master file to generate the doc (needs entry for each class)