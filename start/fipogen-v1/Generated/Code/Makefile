all: _code.so

code_wrap.cxx: code.i
	swig -c++ -python code.i

code_wrap.o: code_wrap.cxx
	gcc -c -arch i386 -fPIC code_wrap.cxx -I/Library/Frameworks/Python.framework/Versions/Current/include/python2.7 -L/Library/Frameworks/Python.framework/Versions/Current/include/python2.7

code.o: code.cpp
	gcc -c -arch i386 -fPIC code.cpp

_code.so: code.o code_wrap.o
	ld -bundle -flat_namespace -undefined suppress -o _code.so code.o code_wrap.o

clean:
	rm code_wrap.o code.o _code.so code.py code.pyc code_wrap.cxx
