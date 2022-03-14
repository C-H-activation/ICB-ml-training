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
