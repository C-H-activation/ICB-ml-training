#!/usr/bin/env python3

from openbabel import pybel
pybel.ob.obErrorLog.SetOutputLevel(0)

import sys
print("Printing version info for help reporting bugs")
print("Python version:", sys.version)

from sklearn import metrics

from iridium_db_csv import compounds

####
import pandas as pd
import numpy as np

X = []
names = []
y = []
for mol in compounds:
    try:
        mol.get_representation(dim=256, size=4)
        X.append(mol.representation)
        print(mol.subsmile)
    except:
        continue

X = np.array(X)
df = pd.DataFrame(X)
df.to_csv('db.csv', index=False)
