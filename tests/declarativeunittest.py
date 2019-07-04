import os, math, random, collections, itertools, io, hashlib, binascii

import pytest

from construct import *
from construct.lib import *

ontravis = "TRAVIS" in os.environ
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


def commonhex(format, hexdata):
    commonbytes(format, binascii.unhexlify(hexdata))


def commondumpdeprecated(format, filename):
    filename = "tests/deprecated_gallery/blobs/" + filename
    if ontravis:
        filename = "../" + filename
    with open(filename, 'rb') as f:
        data = f.read()
    commonbytes(format, data)


def commondump(format, filename):
    filename = "tests/gallery/blobs/" + filename
    if ontravis:
        filename = "../" + filename
    with open(filename, 'rb') as f:
        data = f.read()
    commonbytes(format, data)


def commonbytes(format, data):
    obj = format.parse(data)
    data2 = format.build(obj)
