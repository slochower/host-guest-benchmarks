import os
from simtk.openmm.app import Modeller, PDBFile

guest_codes = [
 "adm", "axm", "bhm", "c6m", "c7m", "c8m", "cha", "chm", "dpm", "haz", "hpm", "hxm", "phm", "prm",
]

for code in guest_codes:
    old = PDBFile(f"{code}/cb7-{code}-p.pdb")
    new = PDBFile(f"{code}/{code}.pdb")

    guest_old = [atom.index for atom in old.topology.atoms() if atom.residue.name == f"{code.upper()}"]
    guest_new = [atom.index for atom in new.topology.atoms() if atom.residue.name == f"{code.upper()}"]

    for iatom, jatom in zip(guest_old, guest_new):
        old.positions[iatom] = new.positions[jatom]

    with open(f"{code}/cb7-{code}-p.pdb", "w") as f:
        PDBFile.writeFile(
            old.topology,
            old.positions,
            f,
            keepIds=True,
        )

    os.remove(f"{code}/{code}.pdb")
