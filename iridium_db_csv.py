import random
import os
import glob
import sys

import numpy as np
import pandas as pd
import math

from compound.compound import Compound

# search for the following glob pattern and extract all matches into cpds
pattern = "structures/????.*"
cpds = sorted(glob.glob(pattern))

compounds = [Compound(xyz=f) for f in cpds]
