#!/bin/bash

# Compile python wrapper using distutils
clear

#set LD_LIBRARY_PATH
#LD_LIBRARY_PATH='/usr/local/lib/'

# This script is LINUX ONLY and enables the user to compile and install the wrapper without global installation of libWCPG.
# if installed as global, remove rpath option. Otherwise libWCPG will be searched for in current folder
# http://stackoverflow.com/questions/1099981/why-cant-python-find-shared-objects-that-are-in-directories-in-sys-path

rm -rf ./build/*
rm _pyWCPG.so
CURRENTDIR=$(pwd)
python setup.py build_ext --inplace --rpath=$CURRENTDIR
#python setup.py build

#--libraries ./libwcpg.so.0.0.9

#echo "valeur de retour : $?"

if [[ $? = "0" ]] ; then

  echo 'Copying compiled lib to ../'
  cp -f _pyWCPG.so ../
  
  if [[ $1 = "d" ]] ; then
    echo 'Testing that WCPG_ABCD is there'
    echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
    nm -g /usr/local/lib/libwcpg.so|grep 'ABCD'
    echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
    nm -g _pyWCPG.so|grep 'ABCD'
    echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
    ldd -d _pyWCPG.so
    readelf -d _pyWCPG.so
    #rm _pyWCPG.so
  fi
  
else

  echo 'Compile FAILED'
  
fi

# If it doesn't work good'ol GCC will rock da place
#gcc
