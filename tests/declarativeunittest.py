# TODO: Replace this with a conftest.py

import pytest

xfail = pytest.mark.xfail
skip = pytest.mark.skip
skipif = pytest.mark.skipif

import os, math, random, collections, itertools, io, hashlib, binascii

from construct import *
from construct.lib import *


ident = lambda x: x


def common(format, data_sample, obj_sample, size_sample=SizeofError, **kw):
    obj = format.parse(data_sample, **kw)
    assert obj == obj_sample
    data = format.build(obj_sample, **kw)
    assert data == data_sample
    # following are implied by above (re-parse and re-build)
    # assert format.parse(format.build(obj)) == obj
    # assert format.build(format.parse(data)) == data
    if isinstance(size_sample, int):
        size = format.sizeof(**kw)
        assert size == size_sample
    else:
        with pytest.raises(size_sample):
            format.sizeof(**kw)

    # attemps to compile, ignores if compilation fails
    # following was added to test compiling functionality
    # and implies: format.parse(data) == cformat.parse(data)
    # and implies: format.build(obj) == cformat.build(obj)
    try:
        cformat = format.compile()
    except Exception:
        pass
    else:
        obj = cformat.parse(data_sample, **kw)
        assert obj == obj_sample
        data = cformat.build(obj_sample, **kw)
        assert data == data_sample

def commonhex(format, hexdata):
    commonbytes(format, binascii.unhexlify(hexdata))

def commondumpdeprecated(format, filename):
    filename = os.path.join(os.path.dirname(__file__), "deprecated_gallery/blobs/" + filename)
    with open(filename,'rb') as f:
        data = f.read()
    commonbytes(format, data)

def commondump(format, filename):
    filename = os.path.join(os.path.dirname(__file__), "gallery/blobs/" + filename)
    with open(filename,'rb') as f:
        data = f.read()
    commonbytes(format, data)

def commonbytes(format, data):
    obj = format.parse(data)
    data2 = format.build(obj)
