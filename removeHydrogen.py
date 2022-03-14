import random
import os
import glob
import sys

import numpy as np
import pandas as pd
import math

from compound.compound import Compound
from ase.io import read

def removeAtomByIndex(index: int, inp: str, out: str, path=os.getcwd()):
    """Remove atom with index from structure."""

    location = os.path.join(path, inp)
    f = open(location, 'r')
    lines = f.readlines()
    f.close()

    # reduce atom count
    nat = int(lines[0]) - 1
    # drop number of atoms line
    lines.pop(0)
    # increase index by 1
    index += 1
    # drop atom
    lines.pop(index)
    
    location = os.path.join(path, out)
    f = open(location, 'w')
    s = os.linesep
    f.write("{:>5}".format(nat) + s)
    for line in lines:
        f.write(line)
    f.close()

# search for the following glob pattern and extract all matches into cpds
pattern = "structures/????.*"
cpds = sorted(glob.glob(pattern))

for cpd in cpds:
    removeAtomByIndex(index=19, inp=cpd, out=cpd)
