# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "89b02ac3d586bcba37aaa8684d1a69eb",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "2f477f3706f438280c39da3c3e6d468f",
    "command": "129234a5e166be2afc6b19fd2fbdebe8",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "af6f2e358d55b4baef2e4667609e2ff4",
    "defines": "8bbd6d00c6b7cc3bce6834c682951c47",
    "display": "05d0d93528cc6851b05a3f044b2945be",
    "encoder": "c0e7a509aed0f691f5a03aa241392485",
    "engines": "4bfd2a3190f64c5f446489ccaed474da",
    "fetcher": "2076f8bc6165275ac59bdc128cdc50e8",
    "loggers": "fea0b2243d8c853db59721babf4ac76d",
    "looping": "24f16cfbed9e05553fc8374d3f270ba5",
    "message": "d183205ff7f71f6403dec4b69b3dac42",
    "methods": "b24a809698acdc68e66365ee7169ec9b",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "cb87960578112ff634510ded115ccd5b",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "dbf05305d4c5fa716d046ad9f9bd609a",
    "pooling": "f7910c9d310e515e732a5a71ba87fd7b",
    "repeats": "696afca4ff11d415d415133b5a149bad",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "33db993b1f1caa067aae298e672d6cfa",
    "runtime": "133167a80848ccabe0534fe8cf86145c",
    "sources": "c3532ecab9e1a64db3c673dd53cb0e62",
    "threads": "60f69a0890f109ee0367f5f6493ffd8a",
    "typings": "61ff8bb73412c04efca1c7b7e0a2a2c1",
    "utility": "c42a26e972e7a1ae1b5072bfbc2e89a0",
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
