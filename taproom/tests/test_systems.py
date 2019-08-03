"""
Tests whether `taproom` can find hosts.
"""

import logging
from taproom.entry_points import find_host_guest_pairs

logger = logging.getLogger(__name__)

# Systems

def test_cb6():
    """ Test that we can find one host YAML for CB6. """
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()
    assert len(host_guest_systems["cb6"]["yaml"]) == 1
    assert host_guest_systems["cb6"]["yaml"][0].name == "host.yaml"

def test_bcd():
    """ Test that we can find two host YAML instructions for β-cyclodextrin. """
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()
    assert len(host_guest_systems["bcd"]["yaml"]) == 2
    assert host_guest_systems["bcd"]["yaml"][0].name == "host-s.yaml"
    assert host_guest_systems["bcd"]["yaml"][1].name == "host-p.yaml"

def test_cb6_but():
    """ Test that we can find one configuration for CB6:BUT. """
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()
    assert host_guest_systems["cb6"]["yaml"][0].name == "host.yaml"
    assert host_guest_systems["cb6"]["but"]["yaml"].name == "guest.yaml"

# Test `measurements`
def test_acd_bam_measurements():
    host_guest_systems, host_guest_measurements = find_host_guest_pairs()
    assert host_guest_measurements["acd"]["bam"]["yaml"].name == "measurement.yaml"

if __name__ == "__main__":
    test_acd_bam_measurements()
