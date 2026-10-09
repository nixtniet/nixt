# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "e7d8e35a9dcd2952ff32fc6786c7467f",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "a95264453bbfa417e4404e45ba0ea6d0",
    "command": "9f3a3e01f7ff3a15b475221b7cc95fa3",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "848ab4b6f4eafdfcda31cba7311d62fa",
    "defines": "b8e15ccad79099579b802d1bd7108540",
    "display": "50a5e7bc8d6e48caaffb5dd92b8fe802",
    "encoder": "a3812b8a3463e33bc8fc1db9ae7aac53",
    "fetcher": "5dc6fd7d6b0410adbee0b43b216bf2bd",
    "handler": "4a25a67e8b516fa25f3b4b1d07e54992",
    "loggers": "27c867484e3cca8cff53584f1a514eb9",
    "looping": "c63da1fe1c26388e684da267f0f66315",
    "message": "07e8febe6e1e5e2170a518d9826879c2",
    "methods": "4bb771a2dc9b1893907f02c2aa53617e",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "1098af502dcde8586901fef49761f4b0",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "05e98937fa8629f7420dcbcb84e69e39",
    "pooling": "3aef2f8677df380f8aa7d2b1bb715d0c",
    "repeats": "71fb58b59d46577ae59dbcd570ce4028",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "sources": "b62e6c4520d84458618ab52f1b2985e5",
    "tasking": "1ebffb8594f0f424f4ff83ecbc2c8a72",
    "typings": "23faf506bb59632d9a55b6947a3ddaf3",
    "utility": "8431e19f7c45a7353348f155545ee490",
    "watcher": "24434817f9ef07676ba93a77458c1949"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
