What is FiPoGen
---------------

FiPoGen means Fixed-point generator.
It is a program to generate fixed-point algorithms for filters, that can be burned into silicon using a vhdl translator

How do I install FiPoGen
------------------------

pip install fipogen

What are its dependencies ?
--------------------------

Mostly pyhthon packages as dependences : jinga2, numpy, scipy

What does /bin contain ?
------------------------

 - run_me.py : A topical example of how the API can be used to start from a problem and get a solution relative to the user's needs.
 - test_me.py : runs the test suite of the FiPoGen software
 
 Can I run demos ?
-----------------

A demo is a parameter file to run a complete experiment without user interaction. See examples folder

Can I run tests ?
-----------------

Yes, you will find a test orchestrator in ./bin 