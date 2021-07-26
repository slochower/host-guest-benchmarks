"""
Tests whether `taproom` can find hosts.
"""
import yaml
import logging

from simtk.openmm.app import PDBFile
from openff.toolkit.topology import Molecule, Topology
from taproom.entry_points import find_host_guest_pairs

logger = logging.getLogger(__name__)


def test_bcd_yaml():
    """ Test that we can find two host YAML instructions for β-cyclodextrin. """
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()
    assert len(host_guest_systems["bcd"]["yaml"]) == 2
    assert host_guest_systems["bcd"]["yaml"]["s"].name == "host-s.yaml"
    assert host_guest_systems["bcd"]["yaml"]["p"].name == "host-p.yaml"


def test_acd_bam_measurements():
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()
    assert host_guest_measurements["acd"]["bam"]["yaml"].name == "measurement.yaml"


# Test if systems can be configured with OpenFF-Toolkit
def test_acd_systems():
    host = "cb7"
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()

    host_yaml_file = host_guest_systems[host]['yaml']
    orientations = len(host_yaml_file)

    with open(host_yaml_file['p'], "r") as f:
        host_yaml = yaml.safe_load(f)

    host_molecule = Molecule.from_file(host_yaml['structure'])

    for guest in host_guest_systems[host]:
        if guest in ["yaml", "path"]:
            continue
"O=C(C(O1)=O)O[Pt]21[NH2][C@@H]3CCCC[C@H]3[NH2]2"
        yaml_file = host_guest_systems[host][guest]['yaml']
        with open(yaml_file, "r") as f:
            guest_yaml = yaml.safe_load(f)

        guest_molecule = Molecule.from_file(guest_yaml['structure'])

        pdbfile = PDBFile(guest_yaml['structure']['complex'].replace('.pdb', '-p.pdb'))

        topology = Topology.from_openmm(pdbfile.topology, unique_molecules=[host_molecule, guest_molecule])

        assert topology is not None
