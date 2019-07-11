import pkg_resources
import yaml
import json
import logging

logger = logging.getLogger(__name__)

try:
    from openforcefield.topology import Molecule, Topology
    from openforcefield.typing.engines import smirnoff
except ImportError as e:
    raise ImportError(f"{e}: If the `openforcefield` toolkit is installed, this will check the coverage of SMIRNOFF99Frosst "
          f"provided by `taproom`.")

# https://github.com/openforcefield/nistdataselection/blob/a111537902db4fff249e0602ccd124d6832333e0/nistdataselection/nistdataselection.py
def find_smirks_parameters(smiles_list, molecule_paths, term="vdW"):
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
    term: str
        The force field term (must be one of `vdW`, `Bonds`, `Angles`, `ProperTorsions`, `ImproperTorsions`,
        `Electrostatics`)

    Returns
    -------
    dict of str and list of str
        A dictionary with keys of SMIRKS patterns, and
        values of lists of SMILES patterns which would utilize
        those patterns, and the parameter ID in the force field.
    """
    allowed_terms = ["vdW", "Bonds", "Angles", "ProperTorsions", "ImproperTorsions", "Electrostatics"]
    if term not in allowed_terms:
        raise Exception(f"{term}: not a known force field term ({[allowed_term for allowed_term in allowed_terms]})")

    force_field = smirnoff.ForceField('smirnoff99Frosst-1.0.9.offxml')
    handler = force_field.get_parameter_handler(term)

    smiles_by_smirks = {}

    # Initialize the array with all possible smirks pattern
    # to make it easier to identify which are missing.
    for parameter in handler.parameters:

        if parameter.smirks in smiles_by_smirks:
            continue

        smiles_by_smirks[parameter.smirks] = {}
        smiles_by_smirks[parameter.smirks]["id"] = parameter.id
        smiles_by_smirks[parameter.smirks]["smiles"] = []
        smiles_by_smirks[parameter.smirks]["molecules"] = []

    # Populate the dictionary using the open force field toolkit.
    for index, smiles in enumerate(smiles_list):

        molecule = Molecule.from_smiles(smiles, allow_undefined_stereo=True)
        topology = Topology.from_molecules([molecule])

        assigned_parameters = force_field.label_molecules(topology)[0]
        parameters = assigned_parameters[term]

        for parameter in parameters.values():

            smiles_by_smirks[parameter.smirks]["smiles"].append(smiles)
            smiles_by_smirks[parameter.smirks]["molecules"].append(str(molecule_paths[index]))

    # Find terms exercised by the SMILES.
    terms_used = []
    for key, value in smiles_by_smirks.items():
        for sub_key, sub_value in value.items():
            if sub_key == "smiles" and sub_value != []:
                terms_used.append(value["id"])

    return smiles_by_smirks, terms_used

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
    for file in yaml_list:
        with open(file, "r") as f:
            yaml_data = yaml.safe_load(f)

        molecule_paths.append(file.parent.joinpath(yaml_data["structure"]))

    smiles_list = []
    for molecule in molecule_paths:
        smiles_list.append(mol2_to_smiles(str(molecule)))

    for term in ["vdW", "Bonds", "Angles", "ProperTorsions", "ImproperTorsions"]:

        smiles_by_smirks, terms_used = find_smirks_parameters(smiles_list, molecule_paths, term=term)
        logging.debug(json.dumps(smiles_by_smirks, indent=2))
        print(f"{term:<20} {terms_used}")