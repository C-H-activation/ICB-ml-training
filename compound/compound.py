from __future__ import print_function

from openbabel import pybel
ob_log_handler = pybel.ob.OBMessageHandler()
ob_log_handler.SetOutputLevel(0)

import numpy as np
import collections

from rdkit import Chem
from rdkit.Chem import AllChem

from .data import NUCLEAR_CHARGE

class Compound(object):
    """ The ``Compound`` class is used to store data from  

        :param xyz: Option to initialize the ``Compound`` with data from an XYZ file.
        :type xyz: string
    """

    def __init__(self, xyz = None):

        empty_array = np.asarray([], dtype = float)

        self.molid = float("nan")
        self.name = None
        self.smile = None
        self.subsmile = None

        # Information about the compound
        self.natoms = float("nan")
        self.natypes = {}
        self.atomtypes = []
        self.atomtype_indices = collections.defaultdict(list)
        self.nuclear_charges = empty_array
        self.coordinates = empty_array
        self.active_atoms = empty_array
        self.unit_cell = None

        # Container for misc properties
        self.energy = float("nan")
        self.properties = empty_array
        self.properties2 = empty_array

        # Representations:
        self.representation = empty_array

        if xyz is not None:
            self.read_xyz(xyz)


    def read_xyz(self, filename):
        """(Re-)initializes the Compound-object with data from an xyz-file.

           :param filename: Input xyz-filename.
           :type filename: string
        """

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        self.natoms = int(lines[0])
        self.atomtypes = []
        self.nuclear_charges = np.empty(self.natoms, dtype=int)
        self.coordinates = np.empty((self.natoms, 3), dtype=float)

        self.name = filename

        for i, line in enumerate(lines[2:self.natoms+2]):
            tokens = line.split()

            if len(tokens) < 4:
                break

            self.atomtypes.append(tokens[0])
            self.atomtype_indices[tokens[0]].append(i)
            self.nuclear_charges[i] = NUCLEAR_CHARGE[tokens[0]]
    
            self.coordinates[i] = np.asarray(tokens[1:4], dtype=float)
   
        self.natypes = dict([(key, len(value)) for key,value in self.atomtype_indices.items()])

    def xyz_to_smiles(self):
        """Convert xyz file to smiles."""
        mol = next(pybel.readfile("xyz", self.name))
        smi = mol.write(format="smi")
        self.smile = smi.split()[0].strip()

    def get_representation(self, dim=128, size=4):
        """Convert xyz to smile and calculate Morgan representation for cutout."""
        # get SMILES from xyz
        self.xyz_to_smiles()
	
        # extract substructure in complex via RDKit
        rdmol = Chem.MolFromSmiles(self.smile, sanitize=False)
        #print(self.smile, self.name)
        # extract Carbon index
        for atom in rdmol.GetAtoms():
            if atom.GetAtomicNum() == 77:
                # get neighbors of Iridum
                neighbors = [x.GetAtomicNum() for x in atom.GetNeighbors()]
                # Carbon position in neighbor list
                carbonPosition = neighbors.index(6)
                # get indices of neighbors in SMILES
                indices = [x.GetIdx() for x in atom.GetNeighbors()]
				# get aufpunkt: Carbon atom attached to Iridium
                carbonIndex = indices[carbonPosition]

        env = Chem.FindAtomEnvironmentOfRadiusN(rdmol, size, carbonIndex)
        submol = Chem.PathToSubmol(rdmol, env)
        submol.UpdatePropertyCache(strict=False)
        Chem.SanitizeMol(submol, 
            Chem.SanitizeFlags.SANITIZE_FINDRADICALS|Chem.SanitizeFlags.SANITIZE_KEKULIZE|Chem.SanitizeFlags.SANITIZE_SETAROMATICITY|Chem.SanitizeFlags.SANITIZE_SETCONJUGATION|Chem.SanitizeFlags.SANITIZE_SETHYBRIDIZATION|Chem.SanitizeFlags.SANITIZE_SYMMRINGS,
            catchErrors=True,
        )
        Chem.GetSymmSSSR(submol)
        representation = AllChem.GetMorganFingerprintAsBitVect(submol, 2, nBits=dim)

        self.representation = np.array(representation)
        self.subsmile = Chem.MolToSmiles(submol)
