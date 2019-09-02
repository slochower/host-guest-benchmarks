import os
from openeye import oechem
from glob import glob


guests = glob("../systems/*/*")
guests = [i for i in guests if os.path.isdir(i)]

for guest in guests:
    guest_mol2 = os.path.basename(guest) + ".mol2"

    ifs = oechem.oemolistream()
    ofs = oechem.oemolostream()

    if ifs.open(os.path.join(guest, guest_mol2)):
        if ofs.open(os.path.join(guest, "tmp.mol2")):
            for mol in ifs.GetOEGraphMols():
                oechem.OEPerceiveBondOrders(mol)
                oechem.OEWriteMolecule(ofs, mol)
                mol.SetTitle(guest.upper())
        else:
            oechem.OEThrow.Fatal("Unable to create 'tmp.mol2'")
    else:
        oechem.OEThrow.Fatal(f"Unable to open '{guest_mol2}'")

    f = open(os.path.join(guest, "tmp.mol2"), 'r')
    file_data = f.read()
    f.close()

    new_data = file_data.replace("<0>", os.path.basename(guest).upper())

    f = open(os.path.join(guest, "tmp.mol2"), 'w')
    f.write(new_data)
    f.close()


    if os.path.exists(os.path.join(guest, "tmp.mol2")):
        os.rename(os.path.join(guest, "tmp.mol2"),
                  os.path.join(guest, guest_mol2))

