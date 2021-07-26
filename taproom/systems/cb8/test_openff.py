from simtk.openmm.app import PDBFile
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

    try:
        topology = Topology.from_openmm(pdbfile.topology, unique_molecules=[host, guest])
    except ValueError:
        print(f"Failed creating {code}")
        pass
