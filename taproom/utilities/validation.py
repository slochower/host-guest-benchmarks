from pydantic import BaseModel, validator
from typing import Dict, List, Optional
from paprika.setup import _get_installed_benchmarks
from paprika.restraints.read_yaml import read_yaml
from pint import UnitRegistry
from pint.quantity import _Quantity
from pathlib import Path

ureg = UnitRegistry()

def check_atoms_are_string(atoms):
    if isinstance(atoms, str):
        return
    else:
        raise ValueError(f"Restraint atom definition not detected as `str`: {atoms}")


def check_force_constant_is_float(force_constant):
    if isinstance(force_constant, float):
        return
    else:
        raise ValueError(f"Restraint force constant not detected as `float`: {force_constant}")


def check_restraint_target_is_float(restraint_target):
    if isinstance(restraint_target, float):
        return
    else:
        raise ValueError(f"Restraint target value not detected as `float`: {restraint_target}")

def check_restraint_by_phase(restraint, phase):
    if "force_constant" not in restraint[phase].keys():
        raise ValueError(f"Restraints missing atom force constant: {restraint}")
    check_force_constant_is_float(restraint[phase]["force_constant"])
    check_restraint_target_is_float(restraint[phase]["target"])

class TaproomHost(BaseModel):
    name: str
    path: Path
    structure: str
    net_charge: float
    resname: str
    aliases: Optional[List[Dict]]
    restraints: List[Dict]
    attach_windows: int
    pull_windows: int
    release_windows: int
    lambda_attach: List[float]
    lambda_release: List[float]
    pull_value: float
    waters: int
    water_model: str

    class Config:
        arbitrary_types_allowed = True

    @validator("structure")
    def structure_exists(cls, value, values):
        if not Path.exists(values["path"].parent.joinpath(value)):
            raise ValueError(f"Structure file appears not to exist: {values['path'].parent.joinpath(value)}")
        return value

    @validator("restraints")
    def restraints_have_atoms_and_values(cls, value):
        if not value["atoms"]:
            raise ValueError(f"Restraints missing atom definition: {value}")
        if not value["force_constant"]:
            raise ValueError(f"Restraints missing atom force constant: {value}")
        if not isinstance(value["atoms"], str):
            raise ValueError(f"Restraint atom definition not detected as `str`: {value}")
        if not isinstance(value["force_constant"], float):
            raise ValueError(f"Restraint force constant definition not detected as `float`: {value}")
        return value


class TaproomGuest(BaseModel):
    name: str
    path: Path
    structure: str
    complex: str
    net_charge: float
    aliases: Optional[List[Dict]]
    restraints: List[Dict]
    microstates: int

    class Config:
        arbitrary_types_allowed = True

    @validator("structure")
    def structure_exists(cls, value, values):
        if not Path.exists(values["path"].parent.joinpath(value)):
            raise ValueError(f"Structure file appears not to exist: {values['path'].parent.joinpath(value)}")
        return value

    @validator("complex")
    def at_least_one_complex_exists(cls, value, values):
        complex_prefix = Path(value).stem
        p = list(values["path"].parent.glob(f"{complex_prefix}*.pdb"))
        if len(p) < 1:
            raise ValueError(f"Did not find at least one complex file: {values['path'].parent.joinpath(f'{complex_prefix}*.pdb')}")
        return value

    @validator("restraints")
    def restraints_have_atoms_and_values(cls, value):
        if not value["atoms"]:
            raise ValueError(f"Restraints missing atom definition: {value}")

        keys = value.keys()

        if "attach" in keys:
            check_restraint_by_phase(value, "attach")
        if "pull" in keys:
            check_restraint_by_phase(value, "pull")
        if "release" in keys:
            check_restraint_by_phase(value, "release")

        if "force_constant" in keys():
            check_force_constant_is_float(value["foce_constant"])
        if "target" in keys():
            check_restraint_target_is_float(value["target"])

        return value


class TaproomMeasurement(BaseModel):
    temperature: _Quantity
    pressure: _Quantity
    pH: float = 6.90
    name: str = "guest"
    SMILES: str = "C"
    buffer: List[Dict]
    technique: str = "ITC"
    delta_G: _Quantity
    delta_G_uncertainty: _Quantity
    delta_H: _Quantity
    delta_H_uncertainty: _Quantity
    stoichiometry: str = "1:1"
    comment: str = ""
    doi: str = ""
    unusual: bool = False

    class Config:
        arbitrary_types_allowed = True

    @validator("temperature")
    def temperature_is_positive(cls, value):
        if value.magnitude < 0:
            raise ValueError(f"Temperature must be positive: {value}")
        if not value.check('[temperature]'):
            raise ValueError(f"Temperature in correct units: {value}")
        return value

    @validator("delta_G", "delta_G_uncertainty", "delta_H", "delta_H_uncertainty")
    def measurement_units(cls, value):
        if not value.check('[length] ** 2 * [mass] / [substance] / [time] ** 2'):
            raise ValueError(f"Experimental value is not in correct units: {value}")
        return value


installed_benchmarks = _get_installed_benchmarks()
yaml_data = read_yaml(
    installed_benchmarks["host_guest_measurements"]["acd"]["bam"]["yaml"]
)

tmp = TaproomMeasurement(
    temperature=ureg(yaml_data["state"]["temperature"]),
    pressure=ureg(yaml_data["state"]["pressure"]),
    pH=yaml_data["state"]["pH"],
    name=yaml_data["substance"]["name"],
    SMILES=yaml_data["substance"]["SMILES"],
    buffer=yaml_data["substance"]["buffer"],
    technique=yaml_data["measurement"]["technique"],
    delta_G=ureg(yaml_data["measurement"]["delta_G"]),
    delta_G_uncertainty=ureg(yaml_data["measurement"]["delta_G_uncertainty"]),
    delta_H=ureg(yaml_data["measurement"]["delta_H"]),
    delta_H_uncertainty=ureg(yaml_data["measurement"]["delta_H_uncertainty"]),
    comment=yaml_data["measurement"]["comment"],
    doi=yaml_data["provenance"]["doi"],
    unusual=yaml_data["unusual"]
)

yaml_data = read_yaml(
    installed_benchmarks["host_guest_systems"]["acd"]["yaml"]["p"]
)

all_restraints = []
for restraint in yaml_data["restraints"]["static"]:
    all_restraints.append(restraint)
for restraint in yaml_data["restraints"]["conformational"]:
    all_restraints.append(restraint)

tmp = TaproomHost(
    name=yaml_data["name"],
    path=installed_benchmarks["host_guest_systems"]["acd"]["yaml"]["p"],
    structure=yaml_data["structure"],
    net_charge=yaml_data["net_charge"],
    resname=yaml_data["resname"],
    aliases=yaml_data["aliases"],
    restraints=all_restraints,
    attach_windows=yaml_data["calculation"]["windows"]["attach"],
    pull_windows=yaml_data["calculation"]["windows"]["pull"],
    release_windows=yaml_data["calculation"]["windows"]["release"],
    lambda_attach=yaml_data["calculation"]["lambda"]["attach"],
    lambda_release=yaml_data["calculation"]["lambda"]["release"],
    pull_value=yaml_data["calculation"]["target"]["pull"],
    waters=yaml_data["calculation"]["system"]["waters"],
    water_model=yaml_data["calculation"]["system"]["model"]
)

yaml_data = read_yaml(
    installed_benchmarks["host_guest_systems"]["acd"]["bam"]["yaml"]
)

all_restraints = []
restraint_types = yaml_data["restraints"].keys()

for restraint_type in restraint_types:
    for restraint in yaml_data["restraints"][restraint_type]:
        all_restraints.append(restraint)

tmp = TaproomGuest(
    name=yaml_data["name"],
    path=installed_benchmarks["host_guest_systems"]["acd"]["bam"]["yaml"],
    structure=yaml_data["structure"],
    complex=yaml_data["complex"],
    net_charge=yaml_data["net_charge"],
    aliases=yaml_data["aliases"],
    restraints=all_restraints,
    microstates=yaml_data["symmetry_correction"]["microstates"]
)


