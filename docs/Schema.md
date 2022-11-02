# Specifications for YAML files
Below are the specification for the `host`, `guest` and `measurement` YAML files. The variables `net_charge`, `force_constant`, and `target` require pint unit (see one of the guest.yaml file for an example).

## YAML host file schema

- name (`str`):
- structure (`dict`):
  - mol2 (`str`)
  - sdf(`str`)
- monomer (`str`, optional)
- resname (`str`):
- net_charge (`int`, `unit.Quantity`):
- aliases (`dict`, optional):
- restraints (`dict`):
    - static (`list`)
      - atoms (`str`)
      - force_constant (`float`, `unit.Quantity`)
    - conformational (`list`)
      - atoms (`str`)
      - force_constant (`float`, `unit.Quantity`)
      - target (`float`, `unit.Quantity`)
- calculation (`dict`)
    - windows (`dict`)
        - attach (`int`)
        - pull (`int`)
        - release (`int`)
    - lambda (`dict`)
        - attach (`list` of `float`)
        - release (`list` of `float`)
    - target (`dict`)
        - pull (`float`, `unit.Quantity`)
    - system (`dict`)
        - waters (`int`)
        - model (`str`)
        
## YAML guest file schema
- name (`str`):
- structure (`dict`):
  - mol2 (`str`)
  - sdf (`str`)
- complex (`str`):
- net_charge (`float`, `unit.Quantity`)
- data_set (`dict`, optional):
    - SAMPL (`int`):
    - guest_id (`str`)
- aliases (`dict`, optional):
- restraints (`list`):
    - guest (`list`)
      - atoms (`str`)
      - attach/pull (`dict`)
        - force_constant (`float`, `unit.Quantity`)
        - target (`float`, `unit.Quantity`)
    - wall_restraint (`list`)
      - atoms (`str`)
      - force_constant (`float`, `unit.Quantity`)
      - target (`float`, `unit.Quantity`)
- symmetry_correction (`dict`):
    - restraints (`dict`)
      - atoms (`str`)
      - force_constant (`float`, `pint_unit`)
      - target (`float`, `pint_unit`)
    - microstates (`int`)

## YAML measurements file schema
- state (`dict`):
    - temperature (`unit.Quantity`):
    - pressure (`unit.Quantity`):
    - pH (`Quantity`):
- substance (`dict`):
    - name (`str`):
    - SMILES (`str`):
    - buffer (`list`):
- measurement (`dict`):
    - technique (`str`):
    - delta_G (`unit.Quantity`):
    - delta_G_uncertainty (`unit.Quantity`):
    - delta_H (`unit.Quantity`, optional):
    - delta_H_uncertainty (`unit.Quantity`, optional):
    - stoichiometry (`str`, optional):
    - comment (`str`, optional):
- provenance (`dict`):
    - comment (`str`, optional):
    - doi (`str`, optional):
- unusual (`bool`, optional)

## Version history
* 0.3 - Add more H-G complexes, includes SDF files, and update metadata schema.
* 0.2 - Fix bugs and adjusted the coordinates of some guest molecules.
* 0.1 - This version of taproom was used in benchmarking Open Force Field (OpenFF) Parsley Force Field (v1.0.0).