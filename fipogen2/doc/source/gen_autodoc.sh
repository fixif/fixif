#!/bin/bash

# Testing autodoc with automatic discovery of source docs

sphinx-apidoc -o ./autodoc ../../dSS
sphinx-apidoc -o ./autodoc ../../SIF