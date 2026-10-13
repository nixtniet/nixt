# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "eb77c8edddc947366e426712ebddbfbc",
    "brokers": "b8c55c1a8f48d15e44224e8121847ec2",
    "buffers": "a95264453bbfa417e4404e45ba0ea6d0",
    "command": "9f3a3e01f7ff3a15b475221b7cc95fa3",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "f12cd3e1a616b5cbc66aabccdaf6ec15",
    "defines": "b8e15ccad79099579b802d1bd7108540",
    "display": "50a5e7bc8d6e48caaffb5dd92b8fe802",
    "encoder": "a3812b8a3463e33bc8fc1db9ae7aac53",
    "fetcher": "168b9449a504aacffc3827637ae45681",
    "handler": "4a25a67e8b516fa25f3b4b1d07e54992",
    "loggers": "9de82546991fe7f0c5a10ae42d4c0ade",
    "looping": "c63da1fe1c26388e684da267f0f66315",
    "message": "07e8febe6e1e5e2170a518d9826879c2",
    "methods": "ac9459f60510a4c58e237c18e009f83c",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "a347c135442ad3f2451a8f129b660310",
    "parsers": "9d17a6c7999bd6f92ee137a206b34bce",
    "persist": "12a7367de108c7afd5f87e8f185ebe11",
    "pooling": "3aef2f8677df380f8aa7d2b1bb715d0c",
    "repeats": "47f08d61ed6059c9595d80caa0d69fe8",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "32f3d085ad5a8c7ec07a346b874a8a08",
    "sources": "81c781b5929fce5591842088b09c65ab",
    "tasking": "41b138a79e032d9229767432163e0c66",
    "typings": "0cbe1d31392c8de34dbf53628bdb0e74",
    "utility": "0d7d6069e8841758f24489a109a5915c",
    "watcher": "ef289da72834d9de33c9b4dd10c642ab"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
