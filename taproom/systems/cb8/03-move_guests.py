from paprika.build.align import zalign
import parmed as pmd

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
mask1 = "C9 C22 C8 C16 N1 C10 C2 C1 C1 C1 C1 C1 C1 O1 O2 N1 N1 C1".split()
mask2 = "C19 C1 N2 C2 N2 N1 N1 N1 N1 N1 N1 N1 C2 N1 N1 C2 C1 N1".split()

for i, code in enumerate(guest_codes):
    if code != "met":
        continue
    print(f"Processing guest molecule: {code}")
    structure = pmd.load_file(f"{code}/{code}.pdb", structure=True)
    zalign(structure, mask1=f":{code.upper()}@{mask1[i]}", mask2=f":{code.upper()}@{mask2[i]}", atom_mask=f":{code.upper()}")
    structure.save(f"{code}/{code}-aligned.pdb", overwrite=True)
