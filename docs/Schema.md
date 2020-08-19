# Specifications for YAML files

asdfasd...

## YAML host file schema

- name (`str`):
- structure (`str`):
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


## YAML measurements file schema


## Version history