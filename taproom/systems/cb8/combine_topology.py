import simtk.unit as unit
from simtk.openmm import Vec3
from simtk.openmm.app import PDBFile, Modeller
from openff.toolkit.topology import Molecule, Topology

box_vectors = unit.Quantity(
    value=(
        Vec3(x=4.1123, y=0.0, z=0.0),
        Vec3(x=0.0, y=4.0343, z=0.0),
        Vec3(x=0.0, y=0.0, z=6.2946),
    ),
    unit=unit.nanometer,
)

host = Molecule.from_file("cb8.mol2")
guest = Molecule.from_file("G1.mol2")

pdbfile = PDBFile("met/cb8-met-p.pdb")
host_topology = []

new_model = Modeller(host.to_topology().to_openmm(), host.conformers[0])
new_model.add(guest.to_topology().to_openmm(), guest.conformers[0])
new_model.topology.setPeriodicBoxVectors(box_vectors)

residues = [residue for residue in new_model.topology.residues()]
#residues[0].id = 0
#residues[1].id = 1
residues[0].name = 'CB8'
residues[1].name = 'MET'

chains = [chain for chain in new_model.topology.chains()]
chains[0].id = ' '
chains[1].id = ' '

with open("test.pdb", "w") as f:
    PDBFile.writeFile(
        new_model.topology,
        pdbfile.positions,
        f,
        True,
    )

pdbfile = PDBFile("test.pdb")
topology = Topology.from_openmm(pdbfile.topology, unique_molecules=[host, guest])
