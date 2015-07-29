#!/bin/bash

# Compile python wrapper using distutils
clear

#set LD_LIBRARY_PATH
LD_LIBRARY_PATH='/usr/local/lib/'

python setup.py build_ext --inplace

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
