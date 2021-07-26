# Taproom

A repository of host-guest systems available for benchmarking force fields used in the 
[OpenFF-Evaluator](https://github.com/openforcefield/openff-evaluator) program.

![US Patent 664824](tap.png)

## Host-guest systems
Taproom includes the following host-guest systems with YAML files containing information necessary to perform 
free energy calculation with the attach-pull-release (APR) method.

* `alpha-cyclodextrin` (acd):
    * Data set from [Rekharsky et al.](https://pubs.acs.org/doi/abs/10.1021/jp962715n)
* `beta-cyclodextrin` (bcd):
    * Data set from [Rekharsky et al.](https://pubs.acs.org/doi/abs/10.1021/jp962715n)
* `cucurbit[7]uril` (cb7):
    * SAMPL4 data set
* `octa-acid` (oah):
    * SAMPL(4,5,6) data set
* `tetra-endo-methyl octa-acid` (oam):
    * SAMPL(5,6) data set

## Installation

This module is designed to be lightweight and have minimal dependencies. 
As such, the simplest way to use these benchmarks is to clone this repository and run `python setup.py develop`.
After installation, `taproom.benchmarks` is exposed as an entry point, and available to other Python modules.
The dictionary `host_guest_systems` contains YAML-formatted "instructions" that can be used to simulate the host-guest systems.
The dictionary `host_guest_measurements` contains YAML-formatted experimental data, curated from public literature.

The following snippet can be used to expose the installed benchmarks.

```python
import pkg_resources

def _get_installed_benchmarks():
    _installed_benchmarks = {}

    for entry_point in pkg_resources.iter_entry_points(group="taproom.benchmarks"):
        _installed_benchmarks[entry_point.name] = entry_point.load()
    return _installed_benchmarks
```

## Schema

For information on the YAML formatting, see [`Schema.md`](docs/Schema.md).

## License

MIT. See [License](LICENSE) for more information.

## Copyright

Copyright (c) 2019, Open Force Field Consortium


## Contributors

- David R. Slochower
- Simon Boothroyd
- Katy Kellett
- Jeff Setiadi
