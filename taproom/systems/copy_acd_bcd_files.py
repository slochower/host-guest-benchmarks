import os
import subprocess as sp
from pathlib import Path

import parmed as pmd

systems = """./a-bam-p
./a-bam-s
./a-but-p
./a-but-s
./a-cbu-p
./a-chp-p
./a-cbu-s
./a-chp-s
./a-cpe-p
./a-coc-p
./a-coc-s
./a-cpe-s
./a-hep-p
./a-ham-s
./a-ham-p
./a-hep-s
./a-hp6-p
./a-hex-p
./a-hex-s
./a-hp6-s
./a-hx2-p
./a-hpa-s
./a-hpa-p
./a-hx2-s
./a-mba-p
./a-hx3-s
./a-hx3-p
./a-mba-s
./a-mhp-p
./a-mha-p
./a-mha-s
./a-mhp-s
./a-nmh-p
./a-nmb-p
./a-nmb-s
./a-nmh-s
./a-oct-p
./a-oam-p
./a-oam-s
./a-oct-s
./a-pnt-p
./a-pam-p
./a-pam-s
./a-pnt-s
./b-ben-s
./b-ben-p
./b-cbu-p
./b-cbu-s
./b-chp-s
./b-chp-p
./b-coc-s
./b-coc-p
./b-cpe-s
./b-cpe-p
./b-ham-s
./b-ham-p
./b-hep-s
./b-hep-p
./b-hex-p
./b-hex-s
./b-m4c-s
./b-m4c-p
./b-m4t-p
./b-m4t-s
./b-mch-s
./b-mha-s
./b-mha-p
./b-mch-p
./b-mo3-s
./b-mo4-p
./b-mo4-s
./b-mo3-p
./b-mp3-s
./b-mp4-s
./b-mp4-p
./b-mp3-p
./b-oam-s
./b-pb3-s
./b-pb3-p
./b-oam-p
./b-pb4-s
./b-pha-s
./b-pb4-p
./b-pha-p
./b-pnt-s
./b-pnt-p"""
systems = systems.split("\n")
systems = [i[2:] for i in systems]
systems = [i for i in systems if "xxxx" not in i]

def write_pdb(output_file, directory_path):
    """
    Save PDB of the host-guest complex with CONECT records.
    """

    input = \
    f"""
    parm smirnoff.prmtop
    trajin smirnoff.inpcrd

    strip :DUM,:Na+,:Cl-,:WAT
    trajout {output_file} conect
    run
    quit
    """
    with open(directory_path.joinpath("tmp.in"), "w") as f:
        f.write(input)
    command = \
    f"""cpptraj -i tmp.in"""
    p = sp.Popen(command, cwd=directory_path, shell=True)
    p.communicate()
    os.remove(directory_path.joinpath("tmp.in"))

def write_mol2(ligand_residue, output_file, directory_path):
    """
    Save MOL2 of the guest molecule with SYBYL/Tripos atom types.
    """

    # 1. Use `cpptraj` to extract just the ligand.

    input = \
    f"""
    parm smirnoff.prmtop
    trajin smirnoff.inpcrd

    strip :MGO,:Na+,:Cl-,:WAT,:DUM
    trajout {ligand_residue}.tmp.mol2
    run
    quit
    """

    with open(directory_path.joinpath("tmp.in"), "w") as f:
        f.write(input)
    command = \
    f"""cpptraj -i tmp.in"""
    p = sp.Popen(command, cwd=directory_path, shell=True)
    p.communicate()
    os.remove(directory_path.joinpath("tmp.in"))

    # 2. Use `antechamber` to make sure we get SYBYL atom types.
    command = \
    f""" antechamber -i {ligand_residue}.tmp.mol2 -fi mol2 -o {output_file} -fo mol2 -at sybyl
    """
    p = sp.Popen(command, cwd=directory_path, shell=True)
    p.communicate()

def grep_anchor_atoms(path, system):
    """
    Create a dictionary of anchor atoms from existing files.
    """

    pdb = path.joinpath(system, "bgbg-tip3p", f"{system}.pdb")
    with open(pdb, "r") as file:
        remark = file.readline()
    remark = remark.rstrip()
    remark = remark.split(" ")

    prmtop = pmd.load_file(
        str(path.joinpath(system, "smirnoff", "smirnoff.prmtop"))
    )
    dummy_residues = prmtop[":DUM"].residues
    host_residue = prmtop[":MGO"].residues[0].number + 1
    guest_residue = prmtop[f":{system.split('-')[1].upper()}"].residues[0].number + 1

    anchor_atoms = {
        "D1": f":{dummy_residues[0].number + 1}",
        "D2": f":{dummy_residues[1].number + 1}",
        "D3": f":{dummy_residues[2].number + 1}",
        "H1": f":{host_residue}@{remark[2].split('@')[1]}",
        "H2": f":{host_residue + 2}@{remark[3].split('@')[1]}",
        "H3": f":{host_residue + 4}@{remark[4].split('@')[1]}",
        "G1": f":{guest_residue}@{remark[5].split('@')[1]}",
        "G2": f":{guest_residue}@{remark[6].split('@')[1]}",
    }
    return anchor_atoms

def write_guest_yaml_header(template_file, anchor_atoms, output_file):
    """
    Write a `guest.yaml` based on a template, replacing the anchor atoms.
    """

    string = [
    f"name: {guest}",
    f"structure: {guest}.mol2",
    f"complex: {host}-{guest}.pdb",
    "net_charge: 0",
    "aliases:",
    f"    - D1: {anchor_atoms['D1']}",
    f"    - D2: {anchor_atoms['D2']}",
    f"    - D3: {anchor_atoms['D3']}",
    f"    - G1: {anchor_atoms['G1']}",
    f"    - G2: {anchor_atoms['G2']}",
    ]


    with open(template_file, "r") as file:
        guest_yaml = file.readlines()

    for line_number in range(10):
        guest_yaml[line_number] = string[line_number]

    with open(output_file, "w") as file:
        file.write(guest_yaml)

for system in systems:

    print(system)

    # Inputs
    host, guest, orientation = system.split("-")
    root_path = Path("/home/davids4/gpfs/smirnoff-host-guest-simulations-data/systems")
    directory_path = root_path.joinpath(system).joinpath("smirnoff")

    write_pdb(output_file=f"{system}.pdb",
              directory_path=directory_path)

    write_mol2(ligand_residue=guest,
               output_file=f"{guest}.mol2",
               directory_path=directory_path)

    # Outputs for `taproom`
    taproom_root = Path("/home/davids4/data/projects/host-guest-benchmarks/taproom/systems")
    taproom_host = taproom_root.joinpath("acd") if "a" in host else taproom_root.joinpath("bcd")
    taproom_directory = taproom_host.joinpath(guest)
    if not taproom_directory:
        os.mkdir(taproom_directory)

    if not os.path.exists(taproom_directory.joinpath("guest.mol2")):
        sp.call(f"cp {directory_path.joinpath(guest + '.mol2')} {taproom_directory}", shell=True)

    if not os.path.exists(taproom_directory.joinpath("guest.yaml")):
        anchor_atoms = grep_anchor_atoms(root_path, system)
        write_guest_yaml_header(template_file=taproom_host.joinpath("hex").joinpath("guest.yaml"),
                                anchor_atoms=anchor_atoms,
                                output_file=taproom_directory.joinpath("guest.yaml"))

    sp.call(f"cp {directory_path.joinpath(system + '.pdb')} {taproom_directory}", shell=True)
