# Specifications

## YAML host file schema

- name (`str`):
- structure (`str`):
- net_charge (`int`):
- restraints (`list`):
    - restraint_group (`str`)
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


## YAML measurements file schema

## Units

Unless otherwise specified... 

- 

We plan to add unit parsing.


## Version history

