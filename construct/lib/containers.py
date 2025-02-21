from construct.lib.py3compat import *
import re
import sys


globalPrintFullStrings = False
globalPrintFalseFlags = False
globalPrintPrivateEntries = False


def setGlobalPrintFullStrings(enabled=False):
    r"""
    When enabled, Container __str__ produces full content of bytes and unicode strings, otherwise and by default, it produces truncated output (16 bytes and 32 characters).

    :param enabled: bool
    """
    global globalPrintFullStrings
    globalPrintFullStrings = enabled


def setGlobalPrintFalseFlags(enabled=False):
    r"""
    When enabled, Container __str__ that was produced by FlagsEnum parsing prints all values, otherwise and by default, it prints only the values that are True.

    :param enabled: bool
    """
    global globalPrintFalseFlags
    globalPrintFalseFlags = enabled


def setGlobalPrintPrivateEntries(enabled=False):
    r"""
    When enabled, Container __str__ shows keys like _ _index _etc, otherwise and by default, it hides those keys. __repr__ never shows private entries.

    :param enabled: bool
    """
    global globalPrintPrivateEntries
    globalPrintPrivateEntries = enabled


def recursion_lock(retval="<recursion detected>", lock_name="__recursion_lock__"):
    """Used internally."""
    def decorator(func):
        def wrapper(self, *args, **kw):
            if getattr(self, lock_name, False):
                return retval
            setattr(self, lock_name, True)
            try:
                return func(self, *args, **kw)
            finally:
                delattr(self, lock_name)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def value_to_string(value):
    if value.__class__.__name__ == "EnumInteger":
        return "(enum) (unknown) %s" % (value, )

    if value.__class__.__name__ == "EnumIntegerString":
        return "(enum) %s %s" % (value, value.intvalue, )

    if value.__class__.__name__ in ["HexDisplayedBytes", "HexDumpDisplayedBytes"]:
        return str(value)

    if isinstance(value, bytes):
        printingcap = 16
        if len(value) <= printingcap or globalPrintFullStrings:
            return "%s (total %d)" % (repr(value), len(value))
        return "%s... (truncated, total %d)" % (repr(value[:printingcap]), len(value))

    if isinstance(value, str):
        printingcap = 32
        if len(value) <= printingcap or globalPrintFullStrings:
            return "%s (total %d)" % (repr(value), len(value))
        return "%s... (truncated, total %d)" % (repr(value[:printingcap]), len(value))

    return str(value)


class Container(dict):
    # NOTE: be careful when working with these objects. Any method can be shadowed, so instead of doing `self.items()` you should do `dict.items(self)`. Operation that use methods implicitly (such as `x in self` or `self[k]`) will work as usual.
    r"""
    Generic ordered dictionary that allows both key and attribute access, and preserves key order by insertion. Adding keys is preferred using \*\*entrieskw. Equality does NOT check item order. Also provides regex searching.

    Example::

        >>> Container()
        >>> Container([("name", "anonymous"), ("age", 21)])
        >>> Container(name="anonymous", age=21)
        >>> Container(dict2)
        >>> Container(container2)

    ::

        >>> print(repr(obj))
        Container(text='utf8 decoded string...', value=123)
        >>> print(obj)
        Container
            text = u'utf8 decoded string...' (total 22)
            value = 123
    """
    __slots__ = ('__dict__', '__recursion_lock__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def copy(self, /):
        return self.__class__(self)

    def __copy__(self, /):
        return self.__class__.copy(self)

    # this is required because otherwise copy.deepcopy() will
    # copy self and self.__dict__ separately for some reason
    def __deepcopy__(self, _, /):
        return self.__class__.copy(self)

    def __dir__(self, /):
        """For auto completion of attributes based on container values."""
        return list(self.__class__.keys(self)) + list(self.__class__.__dict__) + dir(super(Container, self))

    def __eq__(self, other, /):
        if self is other:
            return True
        if not isinstance(other, dict):
            return False
        def isequal(v1, v2):
            if v1.__class__.__name__ == "ndarray" or v2.__class__.__name__ == "ndarray":
                import numpy
                return numpy.array_equal(v1, v2)
            return v1 == v2
        for k, v in self.__class__.items(self):
            if isinstance(k, str) and k.startswith("_"):
                continue
            if k not in other or not isequal(v, other[k]):
                return False
        for k, v in other.__class__.items(other):
            if isinstance(k, str) and k.startswith("_"):
                continue
            if k not in self or not isequal(v, self[k]):
                return False
        return True

    def __ne__(self, other, /):
        return not self == other

    @recursion_lock()
    def __repr__(self, /):
        parts = []
        for k, v in self.__class__.items(self):
            if isinstance(k, str) and k.startswith("_"):
                continue
            parts.append(f'{k}={v!r}')
        return "Container(%s)" % ", ".join(parts)

    @recursion_lock()
    def __str__(self, /):
        indentation = "\n    "
        text = ["Container: "]
        isflags = getattr(self, "_flagsenum", False)
        for k, v in self.__class__.items(self):
            if isinstance(k, str) and k.startswith("_") and not globalPrintPrivateEntries:
                continue
            if isflags and not v and not globalPrintFalseFlags:
                continue
            text.extend([indentation, str(k), " = ", indentation.join(value_to_string(v).split("\n"))])
        return "".join(text)

    def _search(self, compiled_pattern, search_all, /):
        items = []
        for key, value in self.__class__.items(self):
            try:
                if isinstance(value, (Container, ListContainer)):
                    ret = value.__class__._search(value, compiled_pattern, search_all)
                    if ret is not None:
                        if search_all:
                            items.extend(ret)
                        else:
                            return ret
                elif compiled_pattern.match(key):
                    if search_all:
                        items.append(value)
                    else:
                        return value
            except Exception:
                pass
        if search_all:
            return items
        else:
            return None

    def search(self, pattern):
        """
        Searches a container (non-recursively) using regex.
        """
        compiled_pattern = re.compile(pattern)
        return self.__class__._search(self, compiled_pattern, False)

    def search_all(self, pattern):
        """
        Searches a container (recursively) using regex.
        """
        compiled_pattern = re.compile(pattern)
        return self.__class__._search(self, compiled_pattern, True)

    def __getstate__(self, /):
        """
        Used by pickle to serialize an instance to a dict.
        """
        return dict(self)

    def __setstate__(self, state, /):
        """
        Used by pickle to de-serialize from a dict.
        """
        self.__class__.clear(self)
        self.__class__.update(self, state)


class ListContainer(list):
    r"""
    Generic container like list. Provides pretty-printing. Also provides regex searching.

    Example::

        >>> ListContainer()
        >>> ListContainer([1, 2, 3])

    ::

        >>> obj
        ListContainer([1, 2, 3])
        >>> print(repr(obj))
        ListContainer([1, 2, 3])
        >>> print(obj)
        ListContainer
            1
            2
            3
    """

    @recursion_lock()
    def __repr__(self, /):
        return "ListContainer(%s)" % (list.__repr__(self),)

    @recursion_lock()
    def __str__(self, /):
        indentation = "\n    "
        text = ["ListContainer: "]
        for k in self:
            text.append(indentation)
            lines = value_to_string(k).split("\n")
            text.append(indentation.join(lines))
        return "".join(text)

    def _search(self, compiled_pattern, search_all, /):
        items = []
        for item in self:
            try:
                ret = item.__class__._search(item, compiled_pattern, search_all)
            except Exception:
                continue
            if ret is not None:
                if search_all:
                    items.extend(ret)
                else:
                    return ret
        if search_all:
            return items
        else:
            return None

    def search(self, pattern):
        """
        Searches a container (non-recursively) using regex.
        """
        compiled_pattern = re.compile(pattern)
        return self._search(compiled_pattern, False)

    def search_all(self, pattern):
        """
        Searches a container (recursively) using regex.
        """
        compiled_pattern = re.compile(pattern)
        return self._search(compiled_pattern, True)


class Context(Container):
    """Special type of Container used to store contextual information during processing."""

    def __init__(self, _parsing=False, _building=False, _sizing=False, _io=None, _index=0, _subcons=None, **kwargs):
        super(Context, self).__init__(
            _=None,                   # Parent context.
            _root=None,               # Root context.
            _params=self,             # Global parameters.
            # TODO: Perhaps have a "state" attribute instead to avoid contradictions due to multiple flags being true.
            _parsing=_parsing,        # Processing parsing()?
            _building=_building,      # Processing building()?
            _sizing=_sizing,          # Processing sizeof()?
            _io=_io,                  # Processing stream.
            _index=_index,            # Current index (for Array)
            _subcons=_subcons or [],  # Current subcons
        )
        # Recursively build internal dictionaries as child contexts.
        for key, value in kwargs.items():
            if isinstance(value, dict) and value is not self and not isinstance(value, Context):
                value = self.create_child(**value)
            self[key] = value

    def create_child(self, _io=None, _subcons=None, **kwargs):
        """Factory method for initializing a child Context."""
        # Don't allow children to change the processing status or index
        kwargs.pop('_parsing', None)
        kwargs.pop('_building', None)
        kwargs.pop('_sizing', None)
        kwargs.pop('_index', None)

        context = Context(
            _parsing=self._parsing,
            _building=self._building,
            _sizing=self._sizing,
            _io=_io,
            _subcons=_subcons,
            _index=self._index,
            **kwargs,
        )
        context._ = self
        context._params = self._params
        # First child is root, since the very first parent context holds the user defined external parameters.
        context._root = self._root or context
        return context

    def get_child(self, name, default=None):
        """Retrieves child Context or returns default if it doesn't exist."""
        child_context = self.get(name, None)
        if child_context and isinstance(child_context, Context):
            return child_context
        else:
            return default
