# pyproject-metadata

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pypa/pyproject-metadata/main.svg)](https://results.pre-commit.ci/latest/github/pypa/pyproject-metadata/main)
[![checks](https://github.com/pypa/pyproject-metadata/actions/workflows/checks.yml/badge.svg)](https://github.com/FFY00/python-pyproject-metadata/actions/workflows/checks.yml)
[![tests](https://github.com/pypa/pyproject-metadata/actions/workflows/tests.yml/badge.svg)](https://github.com/pypa/pyproject-metadata/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/pypa/pyproject-metadata/branch/main/graph/badge.svg?token=9chBjS1lch)](https://codecov.io/gh/pypa/pyproject-metadata)
[![Documentation Status](https://readthedocs.org/projects/pyproject-metadata/badge/?version=latest)](https://pep621.readthedocs.io/en/latest/?badge=latest)


> Dataclass for PEP 621 metadata with support for [core metadata] generation

This project does not implement the parsing of `pyproject.toml`
containing PEP 621 metadata.

Instead, given a Python data structure representing PEP 621 metadata (already
parsed), it will validate this input and generate a PEP 643-compliant metadata
file (e.g. `PKG-INFO`).


## Usage

After [installing `pyproject-metadata`](https://pypi.org/project/pyproject-metadata/),
you can use it as a library in your scripts and programs:

```python
from pyproject_metadata import StandardMetadata

parsed_pyproject = { ... }  # you can use parsers like `tomli` to obtain this dict
metadata = StandardMetadata.from_pyproject(parsed_pyproject, allow_extra_keys = False)
print(metadata.entrypoints)  # same fields as defined in PEP 621

pkg_info = metadata.as_rfc822()
print(str(pkg_info)))  # core metadata
```

## SPDX licenses (METADATA 2.4+)

If `project.license` is a string or `project.license-files` is present, then
METADATA 2.4+ will be used. A user is expected to validate and normalize
`metadata.license` with an SPDX validation tool, such as the one being added to
`packaging`. Add something like this:

```python
if isinstance(metadata.license, str):
    metadata.license = packaging.licenses.normalize_license_expression(metadata.license)
```

A backend is also expected to copy entries from `project.licence_files`, which
are paths relative to the project directory, into the `dist-info/licenses`
folder, preserving the original source structure.


[core metadata]: https://packaging.python.org/specifications/core-metadata/


## Dynamic Metadata (METADATA 2.2+)

Pyproject-metadata supports dynamic metadata. To use it, specify your METADATA fields in `dynamic_metadata`. If you want to convert `pyproject.toml` field names to METADATA field(s), use `pyproject_metadata.pyproject_to_metadata("field-name")`, which will return a frozenset of metadata names that are touched by that field.

## Adding extra fields

You can add extra fields to the Message returned by `to_rfc822()`, as long as they are valid metadata entries.

## Collecting multiple errors

You can use the `all_errors` argument to `from_pyproject` to show all errors in
the metadata parse at once, instead of raising an exception on the first one.
The exception type will be `pyproject_metadata.errors.ExceptionGroup` (which is
just `ExceptionGroup` on Python 3.11+).

## Validating extra fields

By default, a warning (`pyproject_metadata.errors.ExtraKeyWarning`) will be
issued for extra fields at the top level, in build-system, and in the project
table. If you want to make these errors, pass `allow_extra_keys=False` in
`from_pyproject`. Passing `True` instead avoid the check entirely. If you
want to only validate the `project` table, you can pass
`{"project": pyproject.get("project", None)}` instead of the full `pyproject.toml`.

## Validating classifiers

If you want to validate classifiers, then install the `trove_classifiers` library (the canonical source for classifiers), and run:

```python
import trove_classifiers

metadata_classifieres = {c for c in metadata.classifiers if not c.startswith("Private ::")}
invalid_classifiers = set(metadata.classifiers) - trove_classifiers.classifiers

# Also the deprecated dict if you want it
dep_names = set(metadata.classifiers) & set(trove_classifiers.deprecated_classifiers)
deprecated_classifiers = {k: trove_classifiers.deprecated_classifiers[k] for k in dep_names}
```

If you are writing a build backend, you should not validate classifiers with a `Private ::` prefix; these are only restricted for upload to PyPI (such as `Private :: Do Not Upload`).

Since classifiers are a moving target, it is probably best for build backends (which may be shipped by third party distributors like Debian or Fedora) to either ignore or have optional classifier validation.
