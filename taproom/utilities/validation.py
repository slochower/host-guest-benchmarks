from pydantic import BaseModel
from typing import List
from paprika.setup import _get_installed_benchmarks
from paprika.restraints.read_yaml import read_yaml


class TaproomHost(BaseModel):
    name: str = "host"
    structure: str = f"{name}.mol2"
    resname: str = name.upper()
    net_charge: int = 0
    aliases: List[dict] = []
    restraints: Dict = []



installed_benchmarks = _get_installed_benchmarks()
yaml_data = read_yaml(
    installed_benchmarks["host_guest_systems"]["test_host"]["yaml"][0]
)

tmp = TaproomHost(
    name = yaml_data["name"],
    structure = yaml_data["structure"],
    resname = yaml_data["resname"],
    net_charge = yaml_data["net_charge"],
    aliases = yaml_data["aliases"],

)

print(tmp.name)
print(isinstance(tmp.name, str))