"""
This module contains the function that generates the entry point used by pAPRika to run benchmark calculations.
"""

from pathlib import Path


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
    for file in Path(directory).joinpath("systems").glob("*/*.yaml"):
        hosts.append(file)
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
        guests.append(file)
    return guests


host_guest_pairs = {}

hosts = find_hosts(".")
for host in hosts:
    guests = find_guests(host)
    host_guest_pairs[host] = guests
