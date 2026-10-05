# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "946a1b52fa8203d72137ec15fb68aea7",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "01edcdd383e97d3669d09e341a7d4197",
    "command": "129234a5e166be2afc6b19fd2fbdebe8",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "6e261ecbd6e9ae42ce133a13b3a2b81d",
    "defines": "dbe7ff78a2e889dff262f0b785e1711c",
    "display": "05d0d93528cc6851b05a3f044b2945be",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "engines": "48486d1a4afd316a25999ae610adcb2e",
    "fetcher": "a98c4c3d790e9dc2b7531074038e2b6d",
    "loggers": "dd73bcbf4004f5a33d15156742b235e8",
    "looping": "6f8666579aec275d965035864833f797",
    "message": "8aed09bc218f089f756e42cccfcc36c0",
    "methods": "b24a809698acdc68e66365ee7169ec9b",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "b5f7dec775b8c9a6009efd31738bf622",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "dbf05305d4c5fa716d046ad9f9bd609a",
    "pooling": "8afb7795f3c50630db795cd1432b6e23",
    "repeats": "4c3627f380217e44f000c4498991521a",
    "require": "64863daa33090e4956eef461fd06280c",
    "runtime": "133167a80848ccabe0534fe8cf86145c",
    "sources": "c9ee3a48be447f97db87e00b291d61c0",
    "tasking": "981d6abfc1f6c8772a64661db9bd26cc",
    "threads": "0b028e674a379554bb05bb2c40e953c2",
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
