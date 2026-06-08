FiXiF
*****

FiXiF is a suite of tools to implement filters on embedded devices (usually DSPs, micro-controllers or FPGAs) with finite-precision effects in mind.
It allows to transform a filter/controller into some code (to be executed on a given target) using Fixed-Point Arithmetic, and guaranteeing that the final output error (due to the quantization of the coefficients and the round-off error) is less than a given epsilon.
It allows to consider various possible equivalent (in infinite precision, but no more in finite precision) algorithms (like direct Forms, lattice, state-space, rho-operator based, etc), and find a "good" one, and perform the error analysis.

For the moment FiXif is not fully usable (partly because it is the merge of various previous tools) for everyone. It is based on a several years research work done in academic lab.

## Installation (with uv)

```bash
uv venv
uv pip install -e ".[dev]"
```
`FiXiF` depends on certain other python modules, like `numpy`, `scipy`, `mpmath`, `pytest`

But it also uses other modules :
- pythonsollya (needs Sollya)
- slycot (pip install slycot, see https://github.com/avventi/Slycot)
- matlabengineforpython (needs Matlab http://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
- WCPG (needs the fixif.WCPG library and its Python wrapper, see https://github.com/fixif/WCPG)

## Structure

```
fixif/
├── fixif/
│   ├── SIF/         # sub-module SIF
│   └── LTI/         # Sub-module LTI
└── tests/           # associated tests
    ├── test_SIF/
    └── test_LTI/
```

## to run the tests

```bash
uv run pytest --cov
```
(`--cov` is used to run them with coverage)



## AUTHORS

- Thibault HILAIRE
- Anastasia VOLKOVA
- Benoit LOPEZ
- Joachim KRUITHOF
- Maminionja RAVOSON