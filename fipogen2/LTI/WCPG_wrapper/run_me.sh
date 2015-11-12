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

#http://stackoverflow.com/questions/394230/detect-the-os-from-a-bash-script

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  SUFFIX=".so"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  SUFFIX=".dylib"
else
  echo -e '\033[1;31m OS TYPE NOT SUPPORTED'
  exit 127
fi

if [[ $? = "0" ]] ; then

  echo -e '\033[1;31m Copying compiled lib to ../'
  echo -e "\033[0m "
  cp -f _pyWCPG.so ../
  
  if [[ $1 = "d" ]] ; then
    echo -e '\033[1;31m Testing that WCPG_ABCD is there'
    echo -e '\033[1;31m =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
    echo -e "\033[0m "
    nm -g ./libwcpg$SUFFIX|grep 'ABCD'
    echo -e '\033[1;31m =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
    echo -e "\033[0m "
    nm -g _pyWCPG$SUFFIX|grep 'ABCD'
    echo -e '\033[1;31m =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
    echo -e "\033[0m "
    ldd -d _pyWCPG$SUFFIX
    readelf -d _pyWCPG$SUFFIX
    #rm _pyWCPG.so
  fi
  
else

  echo -e '\033[1;31m Compile FAILED'
  
fi

echo -e "\033[0m "

# If it doesn't work good'ol GCC will rock da place
#gcc
