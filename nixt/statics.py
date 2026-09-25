# This file is placed in the Public Domain.


"tables"


from typing import Dict


CORE: Dict[str, str] = {
    "booting": "8690598166249f44ca9b132ddd7fe271",
    "brokers": "53a3b03458a5b6d88dd43591e00391ce",
    "buffers": "aa7c4742570fd7838602158d69a68b83",
    "clients": "0b7a52d0c0faf4299a4b02d877399166",
    "command": "ea36a9f87804ab830599d895a85166d4",
    "configs": "b03f330521d09d5b47114619c58bcafd",
    "defines": "66421075f718dd5bdd0dc5f2cdcf13c1",
    "display": "74425169ea2165f65f4e06a082ca0a14",
    "encoder": "67ba8b876ead765d906510dbd41fe62c",
    "engines": "c2960c54d18912e1906d9c8956467f39",
    "fetcher": "3ab78d1b884f561da221b4e463a2ab1d",
    "loggers": "2746b6b3768d2c099be3e2c9db2d6e2d",
    "looping": "7e7aeca78f3e192a25e8dce33b7544fa",
    "message": "040f16c95aef8fda8833de7b8a07b050",
    "methods": "ccc09b3f9308ecc24d6bc8644965caf3",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "6a1c0f3d4b3a4338826f347edb25bb9b",
    "parsers": "9b6b0be79a35bbe328b948f5c1f0285f",
    "persist": "4302bcce63f0909aecaa636cb765498c",
    "pooling": "1cf5e79228c44ff8b73c406c2080a687",
    "repeats": "78e43e4280e64f0ee24f2fcc51f80446",
    "require": "7660b1f98a32d4479d7120331f1b2dd3",
    "runners": "3952b86074abe27be3c34b4d1770e1ea",
    "runtime": "9de33036b70599ae10f93de70b73ede4",
    "sources": "bf5be27cab1a738a9d66653ad6623460",
    "threads": "49cb0127de6d2b043714a19c9401c4f0",
    "timings": "ff50ed60fd7c8c74281ec1ce3ef665a6",
    "utility": "64ae1ef703827578cd2e9a4550bc6826",
    "watcher": "9de56fc467ebb20f3fb83cd02fd81537"
}


MODULES: Dict[str,str] = {}


NAMES: Dict[str, str] = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
