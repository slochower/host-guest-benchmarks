# Specifications for YAML files
Below are the specification for the `host`, `guest` and `measurement` YAML files.  

## YAML host file schema

- name (`str`):
- structure (`str`):
- resname (`str`):
- net_charge (`int`):
- aliases (`dict`, optional):
- restraints (`list`):
    - restraint_group (`str`) (e.g. static... )
    

- calculation (`list`)
    - windows (`list`)
        - attach (`int`)
        - pull (`int`)
        - release (`int`)
    - lambda (`list`)
        - attach (`list` of `float`)
        - release (`list` of `float`)
    - target (`list`)
        - pull (`float`)
    - system (`list`)
        - waters (`int`)
        - model (`str`)
        
## YAML guest file schema
- name (`str`):
- structure (`str`):
- complex (`str`):
- data_set (`dict`, optional):
    - SAMPL (`int`):
    - guest_id (`str`)   
- net_charge (`int`):
- aliases (`dict`, optional):
- restraints (`list`):
    - restraint_group (`str`) (e.g. static... )
- symmetry_correction (`list`):
    - restraints (`dict`)
    - microstates (`int)

## YAML measurements file schema
- state (`dict`):
    - temperature (`Quantity`):
    - pressure (`Quantity`):
    - pH (`Quantity`):
- substance (`dict`):
    - name (`str`):
    - SMILES (`str`):
    - buffer (`list`):
- measurement (`dict`):
    - technique (`str`):
    - delta_G (`Quantity`):
    - delta_G_uncertainty (`Quantity`):
    - delta_H (`Quantity`, optional):
    - delta_H_uncertainty (`Quantity`, optional):
    - stoichiometry (`str`, optional):
    - comment (`str`, optional):
- provenance (`dict`):
    - comment (`str`, optional):
    - doi (`str`, optional):
- unusual (`bool`, optional)

## Version history
* 0.2 - Fix bugs and adjusted the coordinates of some guest molecules.
* 0.1 - This version of taproom was used in benchmarking Open Force Field (OpenFF) Parsley Force Field (v1.0.0).