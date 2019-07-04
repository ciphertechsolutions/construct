#!/usr/bin/env python
from setuptools import setup
from construct.version import version_string


extra_require = [
    "enum34",
    "numpy",
    "arrow",
    "ruamel.yaml"
]


setup(
    name = "construct",
    version = version_string,
    packages = [
        'construct',
        'construct.lib',
    ],
    license = "MIT",
    description = "A powerful declarative symmetric parser/builder for binary data",
    long_description = open("README.rst").read(),
    platforms = ["POSIX", "Windows"],
    url = "http://construct.readthedocs.org",
    author = "Arkadiusz Bulski, Tomer Filiba, Corbin Simpson",
    author_email = "arek.bulski@gmail.com, tomerfiliba@gmail.com, MostAwesomeDude@gmail.com",
    install_requires = [],
    extras_require = {
        "extras": extra_require
    },
    test_require = extra_require + [
        "pytest",
        "pytest-benchmark",
    ],
    keywords = [
        "construct",
        "kaitai",
        "declarative",
        "data structure",
        "struct",
        "binary",
        "symmetric",
        "parser",
        "builder",
        "parsing",
        "building",
        "pack",
        "unpack",
        "packer",
        "unpacker",
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
