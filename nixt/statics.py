# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "e0f7ea918f07e8fb42cc56ff0abc9215",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "a95264453bbfa417e4404e45ba0ea6d0",
    "command": "9f3a3e01f7ff3a15b475221b7cc95fa3",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "48205062a1378b54def4d2e7c295066b",
    "defines": "b8e15ccad79099579b802d1bd7108540",
    "display": "50a5e7bc8d6e48caaffb5dd92b8fe802",
    "encoder": "a3812b8a3463e33bc8fc1db9ae7aac53",
    "fetcher": "3de0ac17ca510e27a9e0dcc5cf81419c",
    "handler": "4a25a67e8b516fa25f3b4b1d07e54992",
    "loggers": "5acc2e2d437ac995149b663fcefc7817",
    "looping": "62bdd619111332c70628473c7462f8dd",
    "message": "07e8febe6e1e5e2170a518d9826879c2",
    "methods": "4bb771a2dc9b1893907f02c2aa53617e",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "8510f983ae958e78d366de3dc4dc21a0",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "1a7df57b4ec32976a64771db75190a63",
    "pooling": "70e2300c8743cafd980b2ca8c7335e2a",
    "repeats": "a57e40cc76eb2fccb918b1a1fda8a82d",
    "require": "a472ffdc7c82a0772bb331fa06da0130",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "sources": "5dc6584098d67d3fca63b089469a02cb",
    "tasking": "1297fd2406c28e90566912ac9bba2fcd",
    "typings": "23faf506bb59632d9a55b6947a3ddaf3",
    "utility": "a3e4314d950086b29135a36d411984a0",
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
