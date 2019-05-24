"""
This module contains the function that generates the entry point used by pAPRika to run benchmark calculations.
"""

from pathlib import Path
import pkg_resources
import logging

logger = logging.getLogger(__name__)

def find_hosts(directory):
    """
    Return the list of hosts that provide a YAML recipe.

    Parameters
    ----------
    directory : Path

    Returns
    -------
    hosts : List[Path]
        The list of directory paths containing YAML recipes.
    """

    hosts = []
    p = Path(directory).joinpath("systems")
    logger.debug(f"Looking for hosts in {p.resolve()}...")
    for file in p.resolve().glob("*/*.yaml"):
        hosts.append(file.resolve())
        logger.debug(f"Found host: {file.resolve()}")
    return hosts


def find_guests(host):
    """
    Return the list of guests that provide a YAML recipe, for a given host.

    Parameters
    ----------
    directory : Path

    Returns
    -------
    guests : List[Path]
        The list of directory paths containing YAML recipes.
    """

    guests = []
    for file in Path(host).parents[0].glob("*/*.yaml"):
        guests.append(file.resolve())
        logger.debug(f"Found guest: {file.resolve()}")
    return guests



host_guest_pairs = {}

installed_module_location = Path(pkg_resources.resource_filename("taproom", "entry_points.py")).parents[0]
hosts = find_hosts(installed_module_location)
for host in hosts:
    guests = find_guests(host)
    host_guest_pairs[host] = guests
