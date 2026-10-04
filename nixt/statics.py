# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "44b63ee0c5f70c738dbbb466cc333ad0",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "67f93bade968660cd3b47dfc32057774",
    "command": "129234a5e166be2afc6b19fd2fbdebe8",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "af6f2e358d55b4baef2e4667609e2ff4",
    "defines": "8bbd6d00c6b7cc3bce6834c682951c47",
    "display": "05d0d93528cc6851b05a3f044b2945be",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "engines": "4bfd2a3190f64c5f446489ccaed474da",
    "fetcher": "a98c4c3d790e9dc2b7531074038e2b6d",
    "loggers": "c4f92d6989345017f987bfdc32f6dfac",
    "looping": "24f16cfbed9e05553fc8374d3f270ba5",
    "message": "741f131afdc8ab2ef09cbeca3bd1a776",
    "methods": "b24a809698acdc68e66365ee7169ec9b",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "b5f7dec775b8c9a6009efd31738bf622",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "dbf05305d4c5fa716d046ad9f9bd609a",
    "pooling": "f7910c9d310e515e732a5a71ba87fd7b",
    "repeats": "f5c89a2e2e44b88ebeb3b240fa62d6b3",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "33db993b1f1caa067aae298e672d6cfa",
    "runtime": "133167a80848ccabe0534fe8cf86145c",
    "sources": "c9ee3a48be447f97db87e00b291d61c0",
    "threads": "ec89e3ab5da53d54baa010375faeabd4",
    "typings": "e23cb14ec29e23a5f4500372c7d86816",
    "utility": "2d4291520524811c0c64c91f0c6f9623",
    "watcher": "3b73894d7503d282d057d789640e4c13"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
