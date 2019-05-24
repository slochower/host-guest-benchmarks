"""
Taproom
A library of host-guest systems to benchmark Open Force Field Consortium force fields.
This module provides entry points for pAPRika.
"""

from setuptools import setup

setup(
    name="taproom",
    entry_points={
        "taproom.benchmarks": [
            "host_guest_pairs = taproom.entry_points:host_guest_pairs"
        ],
    }
)