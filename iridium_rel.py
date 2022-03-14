import random
import os
import glob
import sys

import numpy as np
import pandas as pd
import math

from compound.compound import Compound
from ase.io import read

def get_properties(filename, key="dft"):
    """ Returns a dictionary with molecular properties for each xmol-file.
    """

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    properties = dict()

    for line in lines:
        tokens = line.split()

        xyz_name = tokens[0]
        relEXP = float(tokens[1])

        # define fit properties
        if key == "energy":
            properties[xyz_name] = relEXP

    return properties

# get energies
fileName="tsa.txt"
ir_exp_rel_energy = get_properties(fileName, key = "energy")

# search for the following glob pattern and extract all matches into cpds
pattern = "structures/????.*"
cpds = sorted(glob.glob(pattern))

compounds = [Compound(xyz=f) for f in cpds]

for mol in compounds:
    mol.properties3 = ir_exp_rel_energy[mol.name]

random.seed(666)
random.shuffle(compounds)

energy_exp_rel = np.array([mol.properties3 for mol in compounds])
