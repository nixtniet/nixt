# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "efcbec09b3cc48a779a83709dfad1a31",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "67f93bade968660cd3b47dfc32057774",
    "command": "129234a5e166be2afc6b19fd2fbdebe8",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "6e261ecbd6e9ae42ce133a13b3a2b81d",
    "defines": "1e9607b3c93eb439dd5b394d4e0f1019",
    "display": "05d0d93528cc6851b05a3f044b2945be",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "engines": "4bfd2a3190f64c5f446489ccaed474da",
    "fetcher": "a98c4c3d790e9dc2b7531074038e2b6d",
    "loggers": "dd73bcbf4004f5a33d15156742b235e8",
    "looping": "24f16cfbed9e05553fc8374d3f270ba5",
    "message": "83d30c322575665e9508080d2d5de135",
    "methods": "b24a809698acdc68e66365ee7169ec9b",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "b5f7dec775b8c9a6009efd31738bf622",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "dbf05305d4c5fa716d046ad9f9bd609a",
    "pooling": "9a001965a4e17a82c12bed1b3661fa9a",
    "repeats": "f5c89a2e2e44b88ebeb3b240fa62d6b3",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "4a6127e3831ce7b53d47d1563661eed7",
    "runtime": "133167a80848ccabe0534fe8cf86145c",
    "sources": "c9ee3a48be447f97db87e00b291d61c0",
    "threads": "c1f3c6188a7fc2d961ce83db50c704d5",
    "typings": "1a7ae589e7e9f3e0a320e8353d76178b",
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
