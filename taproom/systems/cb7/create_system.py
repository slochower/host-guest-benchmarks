import mdtraj
from openff.toolkit.topology import Molecule, Topology
from openff.toolkit.typing.engines.smirnoff import ForceField
from simtk.openmm.app import Modeller, PDBFile
from simtk.openmm import Vec3
import simtk.unit as unit

box_vectors = unit.Quantity(value=(
    Vec3(x=3.9415999999999998, y=0.0, z=0.0), 
    Vec3(x=0.0, y=3.9303, z=0.0), 
    Vec3(x=0.0, y=0.0, z=6.014900000000001)
    ), 
    unit=unit.nanometer
)

host = Molecule.from_file("cb7.mol2")
guest_codes = [
 "adm", "axm", "bhm", "c6m", "c7m", "c8m", "cha", "chm", "dpm", "haz", "hpm", "hxm", "phm", "prm",
]

for code in guest_codes:
    guest_mol = Molecule.from_file(f"{code}/{code}.mol2")

    new_model = Modeller(host.to_topology().to_openmm(), host.conformers[0])
    new_model.add(guest_mol.to_topology().to_openmm(), guest_mol.conformers[0])
    new_model.topology.setPeriodicBoxVectors(box_vectors)

    residues = [residue for residue in new_model.topology.residues()]
    residues[0].id = '1'
    residues[1].id = '2'
    residues[0].index = 0
    residues[1].index = 1

    chains = [chain for chain in new_model.topology.chains()]
    chains[0].id = ' '
    chains[1].id = ' '

    with open(f"{code}/cb7-{code}-p.pdb", "w") as f:
        PDBFile.writeFile(
            new_model.topology,
            new_model.positions,
            f,
            keepIds=True,
        )

