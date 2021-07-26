import os
from simtk.openmm.app import Modeller, PDBFile

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
    if code != "met":
        continue
    old = PDBFile(f"{code}/cb8-{code}-p.pdb")
    new = PDBFile(f"{code}/{code}-aligned-z.pdb")

    all_old = [atom.index for atom in old.topology.atoms()]
    all_new = [atom.index for atom in new.topology.atoms()]

    for iatom, jatom in zip(all_old, all_new):
        old.positions[iatom] = new.positions[jatom]

    with open(f"{code}/cb8-{code}-p.pdb", "w") as f:
        PDBFile.writeFile(
            old.topology,
            old.positions,
            f,
            keepIds=True,
        )

    os.remove(f"{code}/{code}.pdb")
    os.remove(f"{code}/{code}-aligned.pdb")
