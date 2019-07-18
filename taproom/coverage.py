import pkg_resources
import yaml
import json
import logging
from openeye import oechem

logger = logging.getLogger(__name__)

try:
    from openforcefield.topology import Molecule, Topology
    from openforcefield.typing.engines import smirnoff
except ImportError as e:
    raise ImportError(f"{e}: If the `openforcefield` toolkit is installed, this will check the coverage of SMIRNOFF99Frosst "
          f"provided by `taproom`.")

# https://github.com/openforcefield/nistdataselection/blob/a111537902db4fff249e0602ccd124d6832333e0/nistdataselection/nistdataselection.py
def find_smirks_parameters(smiles_list, molecule_paths):
    """Finds the force field parameters which would
    be assigned to a list of molecules defined by the provided
    SMILES patterns.

    Parameters
    ----------
    smiles_list: list of str
        The SMILES patterns of the target molecules
    molecule_paths: list of Path
        The list of molecules that correspond to the SMILES strings (to make it easier to see which molecules
        utilize which parameters)

    Returns
    -------
    dict of str and list of str
        A dictionary with keys of SMIRKS patterns, and
        values of lists of SMILES patterns which would utilize
        those patterns, and the parameter ID in the force field.
    """

    force_field = smirnoff.ForceField('smirnoff99Frosst-1.0.9.offxml')

    smiles_by_smirks = {}
    smiles_by_smirks["Bonds"] = {}
    smiles_by_smirks["Angles"] = {}
    smiles_by_smirks["ProperTorsions"] = {}
    smiles_by_smirks["vdW"] = {}
    smiles_by_smirks["ImproperTorsions"] = {}
    smiles_by_smirks["Electrostatics"] = {}

    # Populate the dictionary using the open force field toolkit.
    for index, smiles in enumerate(smiles_list):

        ifs = oechem.oemolistream()
        if not ifs.open(molecule_paths[index]):
            logging.error(f'Unable to open {molecule_paths[index]} for reading...')

        ifs.open(molecule_paths[index])
        oe_mols = []
        for mol in ifs.GetOEMols():
            oe_mols.append(oechem.OEMol(mol))
        oechem.OE3DToAtomStereo(oe_mols[0])
        molecule = Molecule.from_openeye(oe_mols[0])

        # molecule = Molecule.from_smiles(smiles, allow_undefined_stereo=True)
        topology = Topology.from_molecules([molecule])

        molecule_force_list = force_field.label_molecules(topology)

        for molecule_index, molecule_forces in enumerate(molecule_force_list):
            print(f'Forces for molecule {molecule_index}')
            for force_name, force_dict in molecule_forces.items():
                print(f"\n{force_name}:")
                for (atom_indices, parameter) in force_dict.items():
                    atomstr = ''
                    for idx in atom_indices:
                        atomstr += '%5s' % idx
                    print("atoms: %s  parameter_id: %s  smirks %s" % ([oe_mols[0].GetAtom(oechem.OEHasAtomIdx(i)).GetName()
                                                                                     for i in atom_indices], parameter.id, parameter.smirks))


                    # This is not catching _all_ the atoms that hit a certain parameter.
                    # I think these need to be initialized in the outer loop.
                    # Each parameter is getting a list of length 1.

                    if parameter.id not in smiles_by_smirks[force_name]:
                        smiles_by_smirks[force_name][parameter.id] = {}
                    if "atom_indices" not in smiles_by_smirks[force_name]:
                        smiles_by_smirks[force_name][parameter.id]["atom_indices"] = []
                    if "atom_names" not in smiles_by_smirks[force_name]:
                        smiles_by_smirks[force_name][parameter.id]["atom_names"] = []

                    smiles_by_smirks[force_name][parameter.id]["atom_indices"].append(atom_indices)
                    smiles_by_smirks[force_name][parameter.id]["atom_names"].append([oe_mols[0].GetAtom(oechem.OEHasAtomIdx(i)).GetName()
                                                                                     for i in atom_indices])
                    smiles_by_smirks[force_name][parameter.id]["smirks"] = parameter.smirks


    return smiles_by_smirks

def mol2_to_smiles(file_path):
    """Loads a receptor from a mol2 file.

    Parameters
    ----------
    file_path: str
        The file path to the mol2 file.

    Returns
    -------
    str
        The smiles descriptor of the loaded receptor molecule
    """

    receptor_molecule = Molecule.from_file(file_path, 'MOL2')
    return receptor_molecule.to_smiles()


def _get_installed_benchmarks():
    _installed_benchmarks = {}

    for entry_point in pkg_resources.iter_entry_points(group="taproom.benchmarks"):
        _installed_benchmarks[entry_point.name] = entry_point.load()
    return _installed_benchmarks


# https://gist.github.com/douglasmiranda/5127251
# https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-python-dictionaries-and-lists
def _find_key(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in _find_key(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in _find_key(key, d):
                    yield result


if __name__ == "__main__":
    installed_benchmarks = _get_installed_benchmarks()
    yaml_list = list(_find_key("yaml", installed_benchmarks))
    molecule_paths = []
    # for file in yaml_list:
    #     with open(file, "r") as f:
    #         yaml_data = yaml.safe_load(f)
    #
    #     molecule_paths.append(file.parent.joinpath(yaml_data["structure"]))
    #


    molecule_paths = ["/Users/dslochower/Documents/projects/host-guest-benchmarks/taproom/systems/bcd/bcd.mol2"]



    smiles_list = []
    for molecule in molecule_paths:
        smiles_list.append(mol2_to_smiles(str(molecule)))

    smiles_by_smirks = find_smirks_parameters(smiles_list, molecule_paths)
    print(json.dumps(smiles_by_smirks, indent=2))