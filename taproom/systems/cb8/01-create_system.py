import os
import shutil

import mdtraj
import simtk.unit as unit
from openff.toolkit.topology import Molecule, Topology
from openff.toolkit.typing.engines.smirnoff import ForceField
from simtk.openmm import Vec3
from simtk.openmm.app import Modeller, PDBFile

host_code = "cb8"
guest_codes = [
    #"esc",
    #"trd",
    #"pal",
    #"qui",
    #"gtr",
    #"thp",
    #"han",
    #"oan",
    #"dan",
    #"mpa",
    #"amm",
    "met",
    #"fen",
    #"mor",
    #"hmo",
    #"ket",
    #"pcp",
    #"con",
]

# 41.123   40.343   62.946
box_vectors = unit.Quantity(
    value=(
        Vec3(x=4.1123, y=0.0, z=0.0),
        Vec3(x=0.0, y=4.0343, z=0.0),
        Vec3(x=0.0, y=0.0, z=6.2946),
    ),
    unit=unit.nanometer,
)

host = Molecule.from_file(f"{host_code}.mol2")

for i, code in enumerate(guest_codes):
    print(f"Guest molecule: {code}")
    os.makedirs(code, exist_ok=True)
    
    guest_mol = Molecule.from_file(f"{code}/{code}.mol2")

    new_model = Modeller(host.to_topology().to_openmm(), host.conformers[0])
    new_model.add(guest_mol.to_topology().to_openmm(), guest_mol.conformers[0])
    new_model.topology.setPeriodicBoxVectors(box_vectors)

    residues = [residue for residue in new_model.topology.residues()]
    residues[0].id = "1"
    residues[1].id = "2"
    residues[0].index = 0
    residues[1].index = 1
    residues[0].name = host_code.upper()
    residues[1].name = code.upper()

    chains = [chain for chain in new_model.topology.chains()]
    chains[0].id = " "
    chains[1].id = " "

    with open(f"{code}/{host_code}-{code}-p.pdb", "w") as f:
        PDBFile.writeFile(
            new_model.topology,
            new_model.positions,
            f,
            keepIds=True,
        )
