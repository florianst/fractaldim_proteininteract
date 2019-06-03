[![Build Status](https://travis-ci.com/RMeli/TFDofPPIN.svg?token=EifNcegf8usjx9yAqxnK&branch=master)](https://travis-ci.com/RMeli/TFDofPPIN)
[![codecov](https://codecov.io/gh/RMeli/TFDofPPIN/branch/master/graph/badge.svg?token=QVfYDX3saY)](https://codecov.io/gh/RMeli/TFDofPPIN)

# Topological Fractal Dimension of Protein-Protein Interaction Networks
We scrutinise protein-protein interaction data from various organisms, report on several centrality measures for the highest-ranking proteines and use box-covering algorithms to determine the non-integer topological dimension of the resulting interaction network. We compare different algorithms and observe that higher-order organisms do not generally show a higher topological dimension.

For an in-depth report in PNAS-style, see report/main.pdf.

## Installation
Run
```
pip install .
```
from the root directory.

### Development
For development use
```
python setup.py develop
```
instead.
