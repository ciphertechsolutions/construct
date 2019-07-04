import pytest

from tests.declarativeunittest import *
from construct.lib.binary import *


@pytest.mark.parametrize("args,data", [
    ((19, 5), b"\x01\x00\x00\x01\x01"),
    ((19, 8), b"\x00\x00\x00\x01\x00\x00\x01\x01"),
    ((-13, 5, True), b"\x01\x00\x00\x01\x01"),
    ((-13, 8, True), b"\x01\x01\x01\x01\x00\x00\x01\x01"),
])
def test_integer2bits(args, data):
    assert integer2bits(*args) == data


@pytest.mark.parametrize("args,exception", [
    ((0, 0, False), ValueError),
    ((0, 0, True), ValueError),
    ((0, -1), ValueError),
    ((-1, 8, False), ValueError),
    ((-2**64, 8, True), ValueError),
    ((2**64, 8, True), ValueError),
    ((-2**64, 8, False), ValueError),
    ((2**64, 8, False), ValueError),
])
def test_integer2bits_errors(args, exception):
    with pytest.raises(exception):
        integer2bits(*args)


@pytest.mark.parametrize("args, data", [
    ((0, 4), b"\x00\x00\x00\x00"),
    ((1, 4), b"\x00\x00\x00\x01"),
    ((19, 4), b'\x00\x00\x00\x13'),
    ((255, 1), b"\xff"),
    ((255, 4), b"\x00\x00\x00\xff"),
    ((-1, 4, True), b"\xff\xff\xff\xff"),
    ((-255, 4, True), b"\xff\xff\xff\x01"),
])
def test_integer2bytes(args, data):
    assert integer2bytes(*args) == data


@pytest.mark.parametrize("args,exception", [
    ((0, 0, False), ValueError),
    ((0, 0, True), ValueError),
    ((0, -1), ValueError),
    ((-1, 8, False), ValueError),
    ((-2**64, 4, True), ValueError),
    ((2**64, 4, True), ValueError),
    ((-2**64, 4, False), ValueError),
    ((2**64, 4, False), ValueError),
])
def test_integer2bytes_errors(args, exception):
    with pytest.raises(exception):
        integer2bytes(*args)


@pytest.mark.parametrize("args,value", [
    ((b"\x01\x00\x00\x01\x01", False), 19),
    ((b"\x01\x00\x00\x01\x01", True), -13),
])
def test_bits2integer(args, value):
    assert bits2integer(*args) == value


@pytest.mark.parametrize("args,exception", [
    ((b"", False), ValueError),
    ((b"", True), ValueError),
])
def test_bits2integer_errors(args, exception):
    with pytest.raises(exception):
        bits2integer(*args)


@pytest.mark.parametrize("i", [-300, -255, -100, -1, 0, 1, 100, 255, 300])
def test_cross_integers(i):
    assert bits2integer(integer2bits(i,64,signed=(i<0)),signed=(i<0)) == i
    assert bytes2integer(integer2bytes(i,8,signed=(i<0)),signed=(i<0)) == i
    assert bits2bytes(integer2bits(i,64,signed=(i<0))) == integer2bytes(i,8,signed=(i<0))
    assert bytes2bits(integer2bytes(i,8,signed=(i<0))) == integer2bits(i,64,signed=(i<0))


@pytest.mark.parametrize("bytes,bits", [
    (b"", b""),
    (b"ab", b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00"),
])
def test_bytes2bits(bytes, bits):
    assert bytes2bits(bytes) == bits


@pytest.mark.parametrize("bits,bytes", [
    (b"", b""),
    (b"\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00", b"ab"),
])
def test_bits2bytes(bits, bytes):
    assert bits2bytes(bits) == bytes


@pytest.mark.parametrize("args,exception", [
    ((b"\x00",), ValueError),
    ((b"\x00\x00\x00\x00\x00\x00\x00",), ValueError),
])
def test_bits2bytes_errors(args, exception):
    with pytest.raises(exception):
        bits2bytes(*args)


@pytest.mark.parametrize("data,swapped", [
    (b"", b""),
    (b"abcd", b"dcba"),
])
def test_swapbytes(data, swapped):
    assert swapbytes(data) == swapped


@pytest.mark.parametrize("data,swapped", [
    (b"", b""),
    (b"0000000011111111", b"1111111100000000"),
])
def test_swapbytesinbits(data, swapped):
    assert swapbytesinbits(data, swapped)


@pytest.mark.parametrize("data,exception", [
    (b"1", ValueError),
])
def test_swapbytesinbites_errors(data, exception):
    with pytest.raises(exception):
        swapbytesinbits(data)


@pytest.mark.parametrize("data,swapped", [
    (b"", b""),
    (b"\xf0", b"\x0f"),
    (b"\xf0\x00", b"\x0f\x00"),
])
def test_swapbitsinbytes(data, swapped):
    assert swapbitsinbytes(data) == swapped
