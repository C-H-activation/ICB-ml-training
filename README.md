# ICB-ml-training
Machine learning training set for the Iridium-catalyzed borylation.

# Details
Relative energies are given in kJ/mol. Template structures have been obtained at the B3LYP-D3(BJ)/LACVP**/PB(THF) level of theory.
New substrates have been docked into the template using the [kallisto](https://github.com/AstraZeneca/kallisto) software. 
All structures are optimzed at the GFN2-xtb/ALPB(THF) level of theory with tight thresholds.
Reference relative energie have been extracted from our [regioselectivity database](https://github.com/f3rmion/db_regioselectivity), where we adopted the naming of the compounds accordingly that we composed from works in the literature -- all citations are listed in the DB repository. 

Ratios for c1 to c15 have been created experimentally and are therefore not part of the regioselectivity database.

## Training data
All training data is given in ``tsa.txt`` where we use the following columns:

```bash
 xmol_structure relative_energy compound_name ch_position
```

The experimental center of borylation is set to 0 kJ/mol, while all non-reactive center have been set to 14 kJ/mol (approximately 0% in Boltzmann populations).
When more then one regioisomer is formed, we used Eyrings' equation to back calculate the relative energy between regioisomers from experimental ratios.

## Train a PLSRegressor model using ICB-ml-training data
First we clone the data set into the current working directory

```bash
> git clone https://github.com/C-H-activation/ICB-ml-training.git
```

We create a Python virtual environment for training purposes and activate it

```bash
> conda create --name training-env python=3.8
... (setup details)
> conda activate training-env
```

We install necessary dependencies to facilitate operations as described in the Compound class to read `xmol` files, to calculate ECFP4 fingerprints, and to use scikit's machine-learning infrastructure

```bash
> conda install -c conda-forge openbabel
... (installation details)
> conda install -c conda-forge numpy
... (installation details)
> conda install -c conda-forge scipy
... (installation details)
> conda install -c conda-forge joblib
... (installation details)
> conda install -c conda-forge pandas
... (installation details)
> conda install -c conda-forge rdkit
... (installation details)
```

Finally, we train the model using the `pls-pf.py` script.

```bash
> python pls-pf.py
... (fitting details)
```

This script will create submolecules, aggregate all training data (X=ECFP4 fingerprints of the submolecule -> y=reference penalties), and create a PLSRegressor (`pls.mod`).
The final model can then be used to perform predictions for any X. The logic how we extract a submolecule is given in the [Compound](https://github.com/C-H-activation/ICB-ml-training/blob/main/compound/compound.py#L100) class.

## Create training database
We use a training database to check whether a system of interest is similar to the training set. For this purpose we store ECFP4 fingerprints of all the references and perform similarity checks on-the-fly.
The trainin database can be created using the `create-csv.py` script

```bash
> python create_csv.py
... (database setup details)
```

This script creates a `db.csv` file with all reference ECFP4 fingerprints.

