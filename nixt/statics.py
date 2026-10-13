# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "e0f7ea918f07e8fb42cc56ff0abc9215",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "fa4850755baafcb4997f982da4ae73b2",
    "command": "2ceacce55c25c8ef053cb4873b651c1e",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "f3b198d0c14513a5f963400e111d70a8",
    "defines": "b8e15ccad79099579b802d1bd7108540",
    "display": "50a5e7bc8d6e48caaffb5dd92b8fe802",
    "encoder": "a3812b8a3463e33bc8fc1db9ae7aac53",
    "fetcher": "3de0ac17ca510e27a9e0dcc5cf81419c",
    "handler": "4a25a67e8b516fa25f3b4b1d07e54992",
    "loggers": "5acc2e2d437ac995149b663fcefc7817",
    "looping": "62bdd619111332c70628473c7462f8dd",
    "message": "07e8febe6e1e5e2170a518d9826879c2",
    "methods": "a463da77995cc65a82221f11e7d61948",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "8510f983ae958e78d366de3dc4dc21a0",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "9b4e14c867649a51eb51408d4ce65275",
    "pooling": "70e2300c8743cafd980b2ca8c7335e2a",
    "repeats": "a57e40cc76eb2fccb918b1a1fda8a82d",
    "require": "a472ffdc7c82a0772bb331fa06da0130",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "sources": "5dc6584098d67d3fca63b089469a02cb",
    "tasking": "6c67908256e52b88a8d866790b64db8d",
    "typings": "5175dc470cfe316babae70f8ec78c1e0",
    "utility": "c44d27b0b08ad077693bf4e31609df4d",
    "watcher": "a4a871d1f4ad3435b53dafff9aed1d2b"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
