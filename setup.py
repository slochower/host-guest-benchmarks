"""
Taproom
A library of host-guest systems to benchmark Open Force Field Consortium force fields.
This module provides entry points for pAPRika.
"""

from setuptools import setup, find_packages

import versioneer

short_description = __doc__.split("\n")

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except IOError:
    long_description = "\n".join(short_description[2:]),


setup(
    name="taproom",
    author="David R. Slochower",
    author_email="slochower@gmail.com",
    description=short_description[0],
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT',
    entry_points={
        "taproom.benchmarks": [
            "host_guest_systems = taproom.entry_points:host_guest_systems",
            "host_guest_measurements = taproom.entry_points:host_guest_measurements"
        ]
    },
    packages=find_packages(),
    include_package_data=True,
)
