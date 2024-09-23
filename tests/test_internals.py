import sys

import pytest

import pyproject_metadata
import pyproject_metadata._constants
import pyproject_metadata._pyproject
import pyproject_metadata.errors


def test_all() -> None:
    assert 'typing' not in dir(pyproject_metadata)
    assert 'annotations' not in dir(pyproject_metadata._constants)
    assert 'annotations' not in dir(pyproject_metadata.errors)
    assert 'annotations' not in dir(pyproject_metadata._pyproject)


def test_project_table_all() -> None:
    if sys.version_info < (3, 11):
        pytest.importorskip('typing_extensions')
    import pyproject_metadata.project_table

    assert 'annotations' not in dir(pyproject_metadata.project_table)
