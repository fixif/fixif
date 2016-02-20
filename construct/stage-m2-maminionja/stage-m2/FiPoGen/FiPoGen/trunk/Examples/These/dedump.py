# -*- coding: utf-8 -*-

from pickle import load


file = open("Examples/These/liste_osops_19.pkl" ,'r')
L_osops = load(file)
file.close()

print L_osops[0]._Top._operands[0]._var_result.FPF