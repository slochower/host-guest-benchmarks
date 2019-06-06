"""
This module contains the function that generates the entry point used by pAPRika to run benchmark calculations.
"""

from pathlib import Path
import yaml
import pkg_resources
import logging

logger = logging.getLogger(__name__)

def find_hosts(directory, subdirectory):
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

    hosts = {}
    p = Path(directory).joinpath(subdirectory)
    for file in p.resolve().glob("*/*.yaml"):
        
        hosts[file.parent.stem] = file.resolve()
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

    guests = {}
    for file in Path(host).parents[0].glob("*/*.yaml"):
        guests[file.parent.stem] = file.resolve()
        logger.debug(f"Found guest: {file.resolve()}")
    return guests


def find_host_guest_pairs():

    host_guest_systems = {}
    host_guest_measurements = {}

    installed_module_location = Path(pkg_resources.resource_filename("taproom", "entry_points.py")).parents[0]
    hosts = find_hosts(installed_module_location, subdirectory="systems")
    for host, host_path in hosts.items():
        host_guest_systems[host] = {}
        host_guest_systems[host]["yaml"] = host_path
        guests = find_guests(host_path)
        for guest, guest_path in guests.items():
            host_guest_systems[host][guest] = guest_path

    hosts = find_hosts(installed_module_location, subdirectory="measurements")
    for host, host_path in hosts.items():
        host_guest_measurements[host] = {}
        host_guest_measurements[host]["yaml"] = host_path
        guests = find_guests(host_path)
        for guest, guest_path in guests.items():
            host_guest_measurements[host][guest] = guest_path

    return host_guest_systems, host_guest_measurements

host_guest_systems, host_guest_measurements = find_host_guest_pairs()