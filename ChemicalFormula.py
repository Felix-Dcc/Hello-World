import pubchempy as pcp

#Define the chemical formula of the hydrocarbon
chemical_formula = input("Enter chemical formula: ")
try:
    compound = pcp.get_compounds(chemical_formula, "formula")[0]

    #Display info about compound
    print(f"Name: {compound.iupac_name}")
    print(f"Common Name: {compound.synonyms[0]}")
    print(f"Molecular Weight: {compound.molecular_weight}")
   

except IndexError:
    print(f"No information found for {chemical_formula}. Please check formula.")

import pubchempy as pcp

#Define the chemical formula of the hydrocarbon
chemical_formula = input("Enter chemical formula: ")
try:
    compound = pcp.get_compounds(chemical_formula, "formula")[0]

    #Display info about compound
    print(f"Name: {compound.iupac_name}")
    print(f"Common Name: {compound.synonyms[0]}")
    print(f"Molecular Weight: {compound.molecular_weight}")
   

except IndexError:
    print(f"No information found for {chemical_formula}. Please check formula.")

