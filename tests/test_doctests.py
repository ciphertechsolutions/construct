
import doctest
import sys

import pytest

import construct
from construct import this


# TODO: Also test examples in documentation.
@pytest.mark.skipif(sys.version_info[0] != 3, reason="Doctests designed for Python 3")
def test_doctests():
    modules = [
        construct.core,
        construct.helpers,
    ]
    for module in modules:
        results = doctest.testmod(module)
        assert not results.failed
