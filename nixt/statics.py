# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "a392b93865904b9085e6b5bce13fb639",
    "brokers": "e6d97de854b6220319fd731a17a4d12f",
    "buffers": "03707592f939b6df3de4bf0cc6e58e62",
    "clients": "bb0d56f37316fe77a70ecf44b81c0e23",
    "command": "49a4201f3f06c82e455e342aa7fbd0a0",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "defines": "ee1d525fa88792d8c9a4ce5ef88625b8",
    "display": "f0c41f61a7a8c03c175fc8ced906effc",
    "encoder": "6de8b10e3ebe0c231b4fea1b9141e055",
    "engines": "4a56d81de1376e5ad363405ac5a485df",
    "fetcher": "8ee28797c0286f7f274ede9824994c43",
    "loggers": "a247909a266b7fe54f1092704f1a267b",
    "looping": "40a250f106c8e7daf218ea8b9d603262",
    "message": "ab69a9b66eea9296433317a5eb33a206",
    "methods": "e371c3c752324299dbe0b604cf6a811a",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "f0114b8d6c73545c7608f8f80db1e1d8",
    "parsers": "16fab1c7e5866f831f3baea69305de04",
    "persist": "b8a51a9105d0523083895af09cb5bc53",
    "pooling": "bc52696b2408b20178118120327b9c1f",
    "repeats": "cfdb4d001f1b23305019f5c441ef96d9",
    "require": "d52360d1f0867865d4ca104cf834bcaf",
    "runners": "3a5effd018b5938507ed1e7e831aba23",
    "runtime": "d6a4d8d969006954145d56896f8a1c34",
    "sources": "918b6e33540e12c29919a81edeebef6a",
    "threads": "abeb4368f00052221e57446becc46bf2",
    "timings": "7fd6bd7509c3baebd32e4cc5d51666f3",
    "utility": "1a2328bcae6ffa3c6591cb12b0229857",
    "watcher": "4ca3f35fe5e808665b127ebef43634df"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
