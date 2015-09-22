#!/bin/bash

# Script used to launch tests for FiPoGen

  clear ;
  
# Run all tests
if [ "$1" = "all" ] ;
then
  python -m unittest discover ;
fi

# Run unit tests, but not all
#python -m unittest LTI.test.test_dSS

if [ "$1" = "FIPObject" ] ;
then
  python -m unittest FIPObject.test.test_FIPObject ;
fi

if [ "$1" = "SIF" ] ;
then
  python -m unittest SIF.test.test_SIF ;
fi