from simtk.openmm.app import PDBFile, Modeller
from openff.toolkit.topology import Molecule, Topology

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

host = Molecule.from_file("cb8.mol2")

for code in guest_codes:
    print(f"Testing guest molecule: {code}")
    guest = Molecule.from_file(f"{code}/{code}.mol2")

    pdbfile = PDBFile(f"{code}/cb8-{code}-p.pdb")
    #new_model = Modeller(
    #    host.to_topology().to_openmm(),
    #    host.conformers[0],
    #    #pdbfile.topology,
    #    #pdbfile.positions,
    #)
    #new_model.add(guest.to_topology().to_openmm(), guest.conformers[0])
    #chains = [chain for chain in new_model.topology.chains()]
    #chains[0].id = ' '
    #chains[1].id = ' '

    #residues = [residue for residue in new_model.topology.residues()]
    ##residues[0].name = 'CB8'
    ##residues[1].name = 'MET'

    #with open("test.pdb", "w") as f:
    #    PDBFile.writeFile(
    #        new_model.topology,
    #        pdbfile.positions,
    #        f,
    #        keepIds=True,
    #    )
    #pdbfile = PDBFile("test.pdb")

    try:
        topology = Topology.from_openmm(
            pdbfile.topology,
            #new_model.topology,
            unique_molecules=[host, guest],
        )
    except ValueError:
        print(f"Failed creating {code}")
        pass
