"""
This contains extra helper constructs that built off the base constructs defined in the core module.
"""

from construct.core import *


@singleton
def CBytes():
    """
    Extracts bytes until first null byte is encountered. (Consumed)

    Use this instead of CString() if you can't guarantee it won't fail to decode.
    """
    return NullTerminated(GreedyBytes)


@singleton
def SkipNull():
    r"""
    Skips over until it hits the first non-zero byte.

    >>> Struct('num' / Int32ul, SkipNull, 'entry' / String(3)).parse(b'\x01\x00\x00\x00\x00\x00\x00\x00hi!')
    Container(num=1, entry=u'hi!')
    """
    return Const(b'\x00')[:]
