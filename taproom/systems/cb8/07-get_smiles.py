from openeye.oechem import *
from openeye.oeiupac import *
from openff.toolkit.topology import Molecule

guest_codes = [
    "esc",
    "trd",
    "pal",
    "qui",
    "gtr",
    "thp",
    "han",
    "oan",
    "dan",
    "mpa",
    "amm",
    "met",
    "fen",
    "mor",
    "hmo",
    "ket",
    "pcp",
    "con",
]

for code in guest_codes:
    molecule = Molecule.from_file(f"{code}/{code}.mol2")
    smiles = molecule.to_smiles(isomeric=True, explicit_hydrogens=False, mapped=False)

    mol = OEMol()
    OEParseSmiles(mol, smiles)
    name = OECreateIUPACName(mol)

    #print(f"{code}; {name}; {smiles}")
    print(f"{code}; {smiles}")

