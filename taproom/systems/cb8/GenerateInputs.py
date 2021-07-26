#!/usr/bin/env python
# coding: utf-8

# # SAMPL6 host-guest preparation
# 
# This notebook prepares small molecule structure files for the SAMPL6 host-guest challenge from source files already present in the source directories. OpenEye toolkits are required, as well as openbabel for the case of oxaliplatin.
# 
# The procedure basically is as follows:
# - Load and prepare receptors (hosts) from provided PDB files
# - Prepare receptors for docking (to place guests into binding site)
# - Load guests molecules from SMILES strings
# - Charge guests and generate conformers
# - Dock to hosts
# - Write out results to mol2 and SDF
# - Handle oxaliplatin (a platinum-containing CB8 ligand) separately via openbabel for conformer generation; no charges
# 
# ## Handle imports of tools we're using throughout
# 

# In[1]:


from openeye.oechem import *
from openeye.oeomega import *
from openeye.oequacpac import *
from openeye.oedocking import *
import os


# ## Load receptors from provided structure files (see README.md files)
# 
# The receptors are loaded from the provided files (PDB for OA and TEMOA; SDF for CB8) and written out so that we have sdf, mol2, and PDB formats all available.

# In[2]:


# Specify source directory
source_dir = '.'

# Load host files
ifile = oemolistream('CB8_charge.mol2')
CB8 = OEMol()
OEReadMolecule(ifile, CB8)
ifile.close()

# Assign partial charges; this step will take a while and isn't necessary to generate basic files
# (I ran this for about 25minutes and didn't get even the first one to converge on my laptop, so I'm skipping for now)
#for mol in [OA, TEMOA, CB8]:
#    OEAssignCharges(mol, OEAM1BCCCharges())

# Add write of CB8
for fmt in ['.pdb', '.mol2']:
    ofile = oemolostream('CB8'+fmt)
    OEWriteMolecule(ofile, CB8)
    ofile.close()


# ## Prepare hosts for docking
# 
# To place the guests into the binding site, we will dock into the receptors (hosts) so prep for docking. **This step can be somewhat slow (a few minutes)**.

# In[3]:


# Make receptors of the hosts for use in docking; takes about 4 minutes on my Mac
receptors = {}

for (hostname, hostmol) in [('CB8', CB8)]:
    # Start by getting center of mass to use as a hint for where to dock
    com = OEFloatArray(3)
    OEGetCenterOfMass(hostmol, com) #Try octa acid for now
    # Create receptor, as per https://docs.eyesopen.com/toolkits/python/dockingtk/receptor.html#creating-a-receptor
    receptor = OEGraphMol()
    OEMakeReceptor(receptor, hostmol, com[0], com[1], com[2])
    receptors[hostname]=receptor


# ## Load, prepare, dock, and write CB8 guests
# 
# We load each guest from SMILES (assigning protonation states roughly appropriate for neutral pH), use Omega to generate conformers, assign AM1-BCC charges, then dock to CB8 and write out. Conformer generation for oxaliplatin (a bonus case) to CB8 fails because of the platinum, so a separate procedure is used in an additional cell below for this case.
# 
# Disclaimer: We have no idea whether these are likely binding modes, good starting poses, etc. We are providing these as a potentially reasonable set of geometries, but use at your own risk.

# In[ ]:


#Get SMILES, build names
smiles = [
#    "CN(C)CCC[C@]1(C2=CC=C(F)C=C2)C3=CC=C(C#N)C=C3CO1",
#    "CC(C)N(C(C)C)CC[C@H](C1=CC=CC=C1)C2=CC(C)=CC=C2O",
#    "O=C(C1=CC=CC(CCC2)=C1[C@]2([H])C3)N3[C@H]4[C@H]5CC[N@](CC5)C4",
#    "COC1=CC=C(N=CC=C2[C@](O)([H])[C@]3([N@](C[C@]4([H])C=C)CC[C@H]4C3)[H])C2=C1",
#    "O(c1c(OCC[N+](CC)(CC)CC)cccc1OCC[N+](CC)(CC)CC)CC[N+](CC)(CC)CC",
#    "CC1(C)[C@@]2(C)CC[C@@H]1C[C@@H]2N",
#    "NC1CCCCCC1",
#    "NC1CCCCCCC1",
#    "NC1CCCCCCCCCCC1",
#    "N[C@@]12C[C@@H]3C[C@H](C2)C[C@H]1C3",
#    "N[C@]12C[C@@H]3C[C@H](C1)C[C@@](C2)(O)C3",
#    "N[C@H]1CC[C@H](N)CC1",
#    "O=C1[C@H](CC2CCN(CC3=CC=CC=C3)CC2)CC4=C1C=C(OC)C(OC)=C4",
#     "O=C(C(O1)=O)O[Pt]21[NH2][C@@H]3CCCC[C@H]3[NH2]2",
    "C[C@H](NC)CC1=CC=CC=C1",
#    "O=C(CC)N(C1=CC=CC=C1)C(CC2)CCN2CCC3=CC=CC=C3",
#    "CN(CC1)[C@H]2[C@]3([H])C=C[C@H](O)[C@@]4([H])[C@]31C5=C(O4)C(O)=CC=C5C2",
#    "CN(CC1)[C@H]2[C@]([C@]1([C@@]3([H])O4)C5=C4C(O)=CC=C5C2)([H])CCC3=O",
#    "O=C1CCCCC1(NC)C2=CC=CC=C2Cl",
#    "N1(CCCCC1)C2(C3=CC=CC=C3)CCCCC2",
#    "CN1[C@H]2CC[C@@H]1[C@@H](C(OC)=O)[C@@H](OC(C3=CC=CC=C3)=O)C2",
]
guest_names = [
#    "esc",
#    "trd",
#    "pal",
#    "qui",
#    "gtr",
#    "thp",
#    "han",
#    "oan",
#    "dan",
#    "mpa",
#    "amm",
#    "hxd",
#    "dpz",
#     "oxa",    
    "met",
#    "fen",
#    "mor",
#    "hmo",
#    "ket",
#    "pcp",
#    "con",
]

guest_dict = {name: smi for (smi, name) in zip(smiles, guest_names)}

#initialize omega
omega = OEOmega()
omega.SetMaxConfs(100) #Generate up to 100 conformers since we'll use for docking
omega.SetIncludeInput(False)
omega.SetStrictStereo(True) #Refuse to generate conformers if stereochemistry not provided

#Initialize charge generation
chargeEngine = OEAM1BCCCharges()

# Initialize docking
dock = OEDock()
dock.Initialize(receptors['CB8']) 

# Build OEMols from SMILES
oemols = []
for name in guest_dict:
    smi = guest_dict[name]
# for (smi, name) in zip(smiles, guest_names):
    print(f"Docking guest molecule {name.upper()}-[{smi}] to CB8")
    os.makedirs(name, exist_ok=True)
    
    # Generate new OEMol and parse SMILES
    mol = OEMol()
    ifile = oemolistream('G1.mol2')
    OEReadMolecule(ifile, mol)
    ifile.close()
    #OEParseSmiles( mol, smi)
    OESetNeutralpHModel(mol)

    # Generate conformers with Omega; keep only best conformer
    status = omega(mol)
    if not status:
        print("Error generating conformers for %s, %s." % (smi, name))
    #print(smi, name, mol.NumAtoms()) #Print debug info -- make sure we're getting protons added as we should

    # Assign AM1-BCC charges
    #OEAssignCharges(mol, chargeEngine)

    # Dock to hosts
    dockedMol = OEGraphMol()
    status = dock.DockMultiConformerMolecule(dockedMol, mol) #By default returns only top scoring pose
    sdtag = OEDockMethodGetName(OEDockMethod_Chemgauss4)
    OESetSDScore(dockedMol, dock, sdtag)
    dock.AnnotatePose(dockedMol)

    # Write out docked pose if docking successful, otherwise write out first generated conformer
    if status == OEDockingReturnCode_Success:
        outmol = dockedMol
    else:
        print("Docking failed for %s; storing input pose." % name)
        # Delete excess conformers -- we want to write only one
        for k, conf in enumerate(mol.GetConfs() ):
            if k > 0:
                mol.DeleteConf(conf)
        outmol = mol

    # Write out
    tripos_mol2_filename = os.path.join(name, name+'.mol2')
    ofile = oemolostream( tripos_mol2_filename )
    OEWriteMolecule(ofile, outmol)
    ofile.close()

    # Save to oemols
    oemols.append(OEMol(outmol))

    # Clean up residue names in mol2 files that are tleap-incompatible: replace substructure names with valid text.
    infile = open(tripos_mol2_filename, 'r')
    lines = infile.readlines()
    infile.close()
    newlines = [line.replace('<0>', name.upper()) for line in lines]
    outfile = open(tripos_mol2_filename, 'w')
    outfile.writelines(newlines)
    outfile.close()


# ## Handle conformer generation and docking of oxaliplatin
# OpenBabel appears to be able to handle conformer generation for oxaliplatin, so generate its conformer and then use the same docking procedure (though this time skipping charging of the guest).
# 
# I am told that the resulting geometry of oxaliplatin is incorrect, which is perhaps not surprising since presumably the platinum poses problems for most of our modeling tools. If participants would like to study this compounds, they are encouraged to carefully examine and prepare a suitable 3D conformation before beginning their studies.

# In[ ]:


# # Oxaliplatin fails, so use openbabel to at least generate a 3D structure of it
#import os
#with open('oxaliplatin.smi', 'w') as f:
#    f.write("O=C(C(O1)=O)O[Pt]21[NH2][C@@H]3CCCC[C@H]3[NH2]2")
#
#os.system('obabel -ismi oxaliplatin.smi -omol2 -O tmp.mol2 --gen3d')
#istream = oemolistream('tmp.mol2')
#mol = OEMol()
#OEReadMolecule(istream, mol)
#istream.close()
#os.system('rm oxaliplatin.smi')
#os.system('rm tmp.mol2')
#
## Can't charge this (no BCCs for Pt) so skip
#
## Dock to at least place in right region
#dockedMol = OEGraphMol()
#status = dock.DockMultiConformerMolecule(dockedMol, mol) #By default returns only top scoring pose
#sdtag = OEDockMethodGetName(OEDockMethod_Chemgauss4)
#OESetSDScore(dockedMol, dock, sdtag)
#dock.AnnotatePose(dockedMol)
#outmol = dockedMol
#
## Write out
#tripos_mol2_filename = os.path.join('oxa/oxa.mol2')
#ofile = oemolostream( tripos_mol2_filename )
#OEWriteMolecule( ofile, outmol)
#ofile.close()

