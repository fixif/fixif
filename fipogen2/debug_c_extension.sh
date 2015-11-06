#!/bin/bash

# This script launches test mode with gdb
# run
# backtrace

clear ; gdb -ex=r -ex=backtrace -ex=quit --args python -m unittest LTI.test.test_dSS
