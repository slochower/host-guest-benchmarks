import os
import yaml
import shutil
import numpy as np
import simtk.unit as unit
from openff.toolkit.topology import Molecule

import collections , yaml

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
  return dumper.represent_mapping(_mapping_tag, data.iteritems())

def dict_constructor(loader, node):
  return collections.OrderedDict(loader.construct_pairs(node))

yaml.add_representer( collections.OrderedDict , dict_representer )
yaml.add_constructor( _mapping_tag, dict_constructor )

raw_data = [
"6;G0;esc;scitalopram;C[NH+](C)CCC[C@@]1(c2ccc(cc2CO1)C#N)c3ccc(cc3)F;-27.99096;0.2092;C9;C19",
"6;G1;trd;olterodine;Cc1ccc(c(c1)[C@H](CC[NH+](C(C)C)C(C)C)c2ccccc2)O;-32.0076;0.16736;C22;C1",
"6;G2;pal;alonosetron;c1cc2c3c(c1)C(=O)N(C[C@@H]3CCC2)[C@@H]4C[NH+]5CCC4CC5;-32.04944;0.2092;C8;N2",
"6;G3;qui;uinine;COc1ccc2c(c1)c(ccn2)[C@H]([C@@H]3C[C@@H]4CC[N@H+]3C[C@@H]4C=C)O;-26.9868;0.25104;C16;C2",
"6;G4;gtr;allamine triethiodate;CC[N+](CC)(CC)CCOc1cccc(c1OCC[N+](CC)(CC)CC)OCC[N+](CC)(CC)CC;-32.6352;0.25104;N1;N2",
"6;G5;thp;1R,2S,4R)-1,7,7-trimethylbicyclo[2.2.1]heptan-2-amine;C[C@@]12CC[C@@H](C1(C)C)C[C@@H]2[NH3+];-34.22512;0.2092;C10;N1",
"6;G6;han;ycloheptanamine;C1CCCC(CC1)[NH3+];-34.89456;0.2092;C2;N1",
"6;G7;oan;yclooctanaine;C1CCCC(CCC1)[NH3+];-41.84;0.4184;C1;N1",
"6;G8;dan;yclododecanamine;C1CCCCCC(CCCCC1)[NH3+];-56.484;0.16736;C1;N1",
"6;G9;mpa;2R,3as,5S,6as)-hexahydro-2,5-methanopentalen-3a(1H)-amine;C1[C@@H]2CC3C[C@H]1CC3(C2)[NH3+];-36.31712;0.33472;C1;N1",
"6;G10;amm;(1s,3r,5R,7S)-3-aminoadam;C1[C@@H]2CC3(C[C@H]1CC(C2)(C3)O)[NH3+];-34.39248;0.29288;C1;N1",
"8;G1;met;ethamphetamine;C[C@@H](Cc1ccccc1)[NH2+]C;-29.4972;0.16736;C1;N1",
"8;G2;fen;entanyl;CCC(=O)N(c1ccccc1)C2CC[NH+](CC2)CCc3ccccc3;-41.58896;0.12552;C1;C2",
"8;G3;mor;orphine;C[N@H+]1CC[C@]23c4c5ccc(c4O[C@H]2[C@H](C=C[C@H]3[C@H]1C5)O)O;-48.65992;0.12552;O1;N1",
"8;G4;hmo;ydromorphone;C[N@H+]1CC[C@]23c4c5ccc(c4O[C@H]2C(=O)CC[C@H]3[C@H]1C5)O;-46.94448;0.12552;O2;N1",
"8;G5;ket;etamine;C[NH2+][C@]1(CCCCC1=O)c2ccccc2Cl;-51.54688;0.16736;N1;C2",
"8;G6;pcp;henylCyclohexylPiperidine (PCP);c1ccc(cc1)C2(CCCCC2)[NH+]3CCCCC3;-58.86888;0.25104;N1;C1",
"8;G7;con;ocaine;C[N@H+]1[C@H]2CC[C@@H]1[C@H]([C@H](C2)OC(=O)c3ccccc3)C(=O)OC;-33.13728;0.16736;C1;N1",
]

data = []
for line in raw_data:
    data.append(line.split(";"))

with open("guest.yaml", "r") as f:
    guest_yaml = yaml.safe_load(f)

with open("measurement.yaml", "r") as f:
    measurement_yaml = yaml.safe_load(f)

for sampl_set, sampl_id, code, name, smiles, fe, sem, G1, G2 in data:
    print(sampl_set, sampl_id, code, name, smiles, fe, sem, G1, G2)

    molecule = Molecule.from_file(f"{code}/{code}.mol2")

    #shutil.copy("guest.yaml", f"{code}/guest.yaml")
    #shutil.copy("measurement.yaml", f"{code}/measurement.yaml")

    guest_yaml["name"] = code
    guest_yaml["structure"] = f"{code}.mol2"
    guest_yaml["complex"] = f"cb8-{code}.pdb"
    guest_yaml["data_set"]["SAMPL"] = int(sampl_set)
    guest_yaml["data_set"]["guest_id"] = sampl_id
    total_charge = molecule.total_charge.value_in_unit(unit.elementary_charge)

    if total_charge >0:
        guest_yaml["net_charge"] = f"+{total_charge:.0f}"
    else:
        guest_yaml["net_charge"] = f"{total_charge:.0f}"
    guest_yaml["aliases"] = [
        ":DM1", ":DM2", ":DM3", f":2@{G1}", f":2@{G2}"
    ]

    with open(f"{code}/guest.yaml", "w") as f:
        yaml.safe_dump(guest_yaml, f, sort_keys=False)

    measurement_yaml["substance"]["name"] = name
    measurement_yaml["substance"]["SMILES"] = smiles
    measurement_yaml["measurement"]["delta_G"] = f"{float(fe):.2f} kJ/mol"
    measurement_yaml["measurement"]["delta_G_uncertainty"] = f"{float(sem):.2f} kJ/mol"

    with open(f"{code}/measurement.yaml", "w") as f:
        yaml.safe_dump(measurement_yaml, f, sort_keys=False)

"""
state:
  temperature: 298 K
  pressure: 1 atm
  pH: 9.2

substance:
  name: 1-adamantylazanium
  SMILES: "C1C2CC3CC1CC(C2)(C3)[NH3+]"
  buffer:
    - "B1(OB2OB(OB(O1)O2)O)O.[Na].[Na]": 0.01 molar

measurement:
  technique: NMR
  delta_G: -58.99 kJ/mol
  delta_G_uncertainty: 0.42 kJ/mol
  stoichiometry: "1:1"

provenance:
  comment: "Table 1"
  doi: 10.1007/s10822-014-9735-1

unusual: False
"""
