"""
Vesper
A library of host-guest systems to benchmark Open Force Field Consortium force fields.
This module provides entry points for pAPRika.
"""

from setuptools import setup

setup(
    name="vesper",
    entry_points={
        "benchmarks": [
            "host_guest_pairs = entry_points:host_guest_pairs"
        ],
    }
)