# Taproom

A repository of host-guest systems available for benchmarking force fields.

## Installation

This module is designed to be lightweight and have minimal dependencies. 
As such, the simplest way to use these benchmarks is to clone this repository and run `python setup.py develop`.
After installation, `taproom.benchmarks` is exposed as an entry point, and available to other Python modules.
The dictionary `host_guest_systems` contains YAML-formatted "instructions" that can be used to simulate the host-guest systems.
The dictionary `host_guest_measurements` contains YAML-formatted experimental data, curated from public literature.

The following snippet can be used to expose the installed benchmarks.

```python
def _get_installed_benchmarks():
    _installed_benchmarks = {}

    for entry_point in pkg_resources.iter_entry_points(group="taproom.benchmarks"):
        _installed_benchmarks[entry_point.name] = entry_point.load()
    return _installed_benchmarks
```

## Coverage

If the `openforcefield` toolkit is installed, running `coverage.py` will expose the parameters exercised by the installed benchmarks.

## Schema

For information on the YAML formatting, see [`Schema.md`](taproom/Schema.md).

## License

MIT. See [License](LICENSE) for more information.

## Copyright

Copyright (c) 2019, Open Force Field Consortium


## Contributors

- David R. Slochower
- Simon Boothroyd
- Katy Kellett