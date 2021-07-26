from simtk.openmm.app import Modeller, PDBFile

inpcrd = PDBFile("esc/cb8-esc-p.pdb")

guest = [atom for atom in inpcrd.topology.atoms() if atom.residue.name == "ESC"]

new_model = Modeller(inpcrd.topology, inpcrd.positions)
new_model.delete(guest)

chains = [chain for chain in new_model.topology.chains()]
chains[0].id = ' '

with open("cb8.pdb", "w") as f:
    PDBFile.writeFile(
        new_model.topology,
        new_model.positions,
        f,
        keepIds=True,
    )
