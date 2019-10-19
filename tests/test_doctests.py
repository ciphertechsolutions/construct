
import doctest

import pytest

import construct


# TODO: Also test examples in documentation.
@pytest.mark.parametrize("module", [
    construct.core,
    construct.helpers,
])
def test_doctests(module):
    results = doctest.testmod(module)
    assert not results.failed
