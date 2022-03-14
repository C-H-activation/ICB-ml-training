#!/usr/bin/env python3

from openbabel import pybel
pybel.ob.obErrorLog.SetOutputLevel(0)

import sys
print("Printing version info for help reporting bugs")
print("Python version:", sys.version)

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.cross_decomposition import PLSRegression

import joblib
import numpy as np

from iridium_db import compounds
from iridium_rel import ir_exp_rel_energy

X = []
names = []
y = []
for mol in compounds:
    try:
        mol.get_representation(dim=256, size=4)
        X.append(mol.representation)
        names.append(mol.name)
        y.append(ir_exp_rel_energy[mol.name])
    except:
        continue

X = np.array(X)
y = np.array(y)
names = np.array(names)

# PLS PF
pls = make_pipeline(PolynomialFeatures(2), PLSRegression(n_components=13))

pls.fit(X, y)

# Dump fitted model
from joblib import dump
dump(pls, 'pls.mod')
