# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "eb77c8edddc947366e426712ebddbfbc",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "a95264453bbfa417e4404e45ba0ea6d0",
    "command": "9f3a3e01f7ff3a15b475221b7cc95fa3",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "bf4ff83294fd9da7096ef496fd192254",
    "defines": "b8e15ccad79099579b802d1bd7108540",
    "display": "84b5d1c78342555524eca2045e9d64ac",
    "encoder": "a3812b8a3463e33bc8fc1db9ae7aac53",
    "fetcher": "0332bf3cd0c7dfae06bb3c63cc283f5e",
    "handler": "4a25a67e8b516fa25f3b4b1d07e54992",
    "loggers": "9de82546991fe7f0c5a10ae42d4c0ade",
    "looping": "c63da1fe1c26388e684da267f0f66315",
    "message": "44dafdecbb71a8e1b9aa4442819a9a45",
    "methods": "5b2f62558948a85d8bcd3e2c7799b5ac",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "a347c135442ad3f2451a8f129b660310",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "3108cd760aea8365e1b1b2dc08ea6bc9",
    "pooling": "3aef2f8677df380f8aa7d2b1bb715d0c",
    "repeats": "47f08d61ed6059c9595d80caa0d69fe8",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "32f3d085ad5a8c7ec07a346b874a8a08",
    "sources": "81c781b5929fce5591842088b09c65ab",
    "tasking": "fa176b061fd795639ed220d477ae2456",
    "typings": "5175dc470cfe316babae70f8ec78c1e0",
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
