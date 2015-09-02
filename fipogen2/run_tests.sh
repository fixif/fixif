#!/bin/bash

# Script used to launch tests for FiPoGen

# Run all tests
if [ "$1" = "all" ] ;
then
  clear ;
  python -m unittest discover ;
fi
# Run unit tests, but not all
#python -m unittest LTI.test.test_dSS
if [ "$1" = "FIPObject" ] ;
then
  python -m unittest FIPObject.test.test_FIPObject ;
fi